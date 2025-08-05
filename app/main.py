import os

from dotenv import load_dotenv
load_dotenv()

from services.job_search_agent.agent import JobSearchAgent
from services.spreadsheet_parser.parser import JobsSpreadsheetParser

def main():
    if os.getenv("MODE")=="SCRAPE":
        job_search_agent = JobSearchAgent()
        job_search_agent.run()
    elif os.getenv("MODE")=="PARSE":
        parser = JobsSpreadsheetParser(file_name=os.getenv("FILENAME"))
        parser.parse()
    else:
        return "Mode not allowed"

if __name__=="__main__":
    main()