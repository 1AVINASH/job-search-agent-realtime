import os
import traceback
import json
import pytz
import re

from langchain_community.tools import TavilySearchResults
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langgraph.graph import END, StateGraph
from typing import TypedDict, List, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.tools.playwright import NavigateTool, ExtractTextTool
from langchain_community.tools import TavilySearchResults
import pandas as pd
from datetime import datetime
from services.job_search_agent.templates import Templates
from playwright.sync_api import sync_playwright
from langchain.output_parsers import PydanticOutputParser
from services.job_search_agent.dtos import JobDetails, JobList


class JobSearchAgent:
    def __init__(self):
        self._initialize_scraper()
        self._initialize_workflow()
        self.jobs_scraped = 0
    
    @property
    def max_jobs_to_scrape(self):
        return int(os.getenv("MAX_JOBS_TO_SCRAPE") or 25)
    
    @property
    def search_query(self):
        return os.getenv("JOB_SEARCH_QUERY") or "Software engineer jobs (contract) at recently funded startups"

    @property
    def llm(self):
        # Shared LLM
        return ChatOpenAI(
            # base_url="http://localhost:8002/v1",
            temperature=0,
            model="gpt-4o-mini",
        )
    
    @staticmethod
    def __clean_string(text):
        # The string is first encoded to bytes using 'latin1'
        # and then decoded using 'unicode_escape', which interprets the escape sequences.
        try:
            pattern = r"---(.*?)---"
            matched = re.findall(pattern, text, re.DOTALL)

            # return ast.literal_eval(escaped_text)
            return matched[0].strip("\n\n")
        except Exception as e:
            print(f"Escaped Text: {text}")
            raise e

    def _initialize_scraper(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

        self.navigator = NavigateTool(sync_browser=self.browser)
        self.text_extracter = ExtractTextTool(sync_browser=self.browser)

    # Define state structure
    class GraphState(TypedDict):
        urls: List[str]
        job_data: List[dict]
        current_url: Optional[str]
        current_html: Optional[str]
        current_text: Optional[str]
        current_info: Optional[dict]

    # --- NODES ---

    # 1. Search jobs and return URLs
    def search_jobs(self, state: GraphState) -> GraphState:
        search = TavilySearchResults()
        results = search.invoke({"query": self.search_query})
        urls = [r['url'] for r in results if 'url' in r]
        print(f"Total urls found: {len(urls)}")
        return {**state, "urls": urls}

    def visit_page(self, state: GraphState) -> GraphState:
        url = state["urls"][0]
        try:
            self.navigator.invoke({"url": url})
        except Exception as e:
            print(f"Ran into an error while visiting page {e}")
        
        print(f"Visiting page with url {url}. Remaining URLs: {len(state['urls'])}")
        state["urls"].pop(0)
        return {**state, "current_url": url}


    # 3. Extract job text
    def extract_job_text(self, state: GraphState) -> GraphState:
        text = ""
        try:
            text = self.text_extracter.invoke({})
        except Exception as e:
            print(f"Ran into an error while visiting page {e}")
        # print(text)
        return {**state, "current_text": text}


    def parse_job_info(self, state: GraphState) -> GraphState:
        parser = PydanticOutputParser(pydantic_object=JobList)
        # 4. Parse job into structured data

        parse_prompt = PromptTemplate.from_template(
            template=Templates.JOBS_PARSER,
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        try:
            parse_chain = LLMChain(llm=self.llm, prompt=parse_prompt)
            raw_output_text = parse_chain.run({"text": state["current_text"]})
            parsed_jobs_list = parser.parse(raw_output_text)
            parsed = parsed_jobs_list.model_dump_json()
        except Exception as e:
            print(f"Ran into an error while visiting page {e}")
            parsed = json.dumps({})
        return {**state, "current_info": parsed}

    # 5. Generate cover letter

    def generate_letter(self, state: GraphState) -> GraphState:
        try:
            cover_letter_template = PromptTemplate.from_template(
                template=Templates.REMOTE_MAIL
            )
            letter_chain = LLMChain(llm=self.llm, prompt=cover_letter_template)
            job = state["current_info"]
            current_infos = json.loads(state["current_info"]).get("jobs")

            if type(current_infos)!=list:
                return state
            for idx, ci in enumerate(current_infos):
                print(ci)
                letter = letter_chain.run(ci)
                cleaned_letter = self.__clean_string(letter)
                current_infos[idx] = {**current_infos[idx], "cover_letter": cleaned_letter}
                self.jobs_scraped+=1
            state["current_info"] = json.dumps({"jobs": current_infos}, ensure_ascii=False)
        except Exception as e:
            print(traceback.format_exc())
        return state

    # 6. Save result
    def save_result(self, state: GraphState) -> GraphState:
        all_jobs = state.get("job_data", [])
        try:
            job = {}
            job["current_info"] = state["current_info"]
            job["url"] = state["current_url"]
            all_jobs.append(job)
        except Exception as e:
            print(traceback.format_exc())
        return {**state, "job_data": all_jobs}

    # Conditional loop or end
    def has_more_urls(self, state: GraphState):
        if state["urls"] and self.jobs_scraped<2:
            return "visit"
        else:
            return END
        
    def _initialize_workflow(self):
            # Build the state machine
        self.workflow = StateGraph(self.GraphState)

        self.workflow.add_node("search", self.search_jobs)
        self.workflow.add_node("visit", self.visit_page)
        self.workflow.add_node("extract", self.extract_job_text)
        self.workflow.add_node("parse", self.parse_job_info)
        self.workflow.add_node("generate_letter", self.generate_letter)
        self.workflow.add_node("save", self.save_result)

        # Connect nodes
        self.workflow.set_entry_point("search")

        self.workflow.add_edge("search", "visit")
        self.workflow.add_edge("visit", "extract")
        self.workflow.add_edge("extract", "parse")
        self.workflow.add_edge("parse", "generate_letter")
        self.workflow.add_edge("generate_letter", "save")

        self.workflow.add_conditional_edges("save", self.has_more_urls, {
            "visit": "visit",
            END: END
        })

        # Compile
        self.app = self.workflow.compile()

    def run(self):
        final_jobs = []

        while self.jobs_scraped<self.max_jobs_to_scrape:
            state = {
                "urls": [],
                "job_data": []
            }

            final_state = self.app.invoke(state, {"recursion_limit": 100})
            final_jobs.extend(final_state.get("job_data") or [])

        # Save to CSV
        df = pd.DataFrame(final_jobs)
        current_datetime = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%b-%YT%H:%M:%S")
        file_location = f"/output/raw/remote_jobs-{current_datetime}.csv"
        df.to_csv(file_location, index=False)

        print("Saved jobs:", len(df))
        print("File saved at:", file_location)