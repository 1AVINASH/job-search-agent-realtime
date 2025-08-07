import os

from dotenv import load_dotenv
load_dotenv()

from services.job_search_agent.agent import JobSearchAgent
from services.job_search_linkedin_agent.agent import JobSearchLinkedAgent
from services.spreadsheet_parser.parser import JobsSpreadsheetParser

def main():
    if os.getenv("MODE")=="SCRAPE":
        job_search_agent = JobSearchAgent()
        job_search_agent.run()
    elif os.getenv("MODE")=="LINKEDIN_SCRAPE":
        job_search_agent = JobSearchLinkedAgent()
        job_search_agent.run()
    elif os.getenv("MODE")=="PARSE":
        parser = JobsSpreadsheetParser()
        parser.parse()
    else:
        return "Mode not allowed"

if __name__=="__main__":
    main()