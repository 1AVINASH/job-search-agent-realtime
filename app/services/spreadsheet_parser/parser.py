import json
from typing import List, Any
import glob
import pandas as pd

class JobsSpreadsheetParser:
    def __init__(self): ...

    def _get_files_to_be_parsed(self):
        raw_files_folder = "/output/raw/"
        parsed_files_folder = "/output/parsed/"
        
        raw_files = glob.glob(f'{raw_files_folder}/*')
        parsed_files = glob.glob(f'{parsed_files_folder}/*')
        print(f"Raw files: {raw_files}")
        print(f"Parsed files: {parsed_files}")
        raw_files_cleaned = set(x.rsplit("/", maxsplit=1)[-1] for x in raw_files)
        parsed_files_cleaned = set(x.rsplit("/", maxsplit=1)[-1] for x in parsed_files)

        remaining_files = raw_files_cleaned - parsed_files_cleaned

        return remaining_files

    def _parse_single_file(self, df: pd.DataFrame):
        cols = ["Scraped From", "Company Name", "Company Website", "Job Title", "Job Link", "Contact Emails", "Company Summary", "Company Location", "Company Domain", "Job Summary", "Metadata", "Cover Letter"]
        rows = []
        for _, row in df.iterrows():
            scraped_from_url = row["url"]
            current_info = json.loads(row["current_info"])
            if type(current_info)!=dict:
                continue
            jobs: List[Any] = current_info["jobs"]
            for job in jobs:
                try:
                    row = [scraped_from_url, job["company_name"], job["company_website"], job["title"], job.get("job_link"), job["mails"], job["company_summary"], job["company_location"], job["company_domain"], job["summary"], job["metadata"], job.get("cover_letter")]
                    rows.append(row)
                except Exception as e:
                    print(f"Unable to read row. Error being {e}")

        df = pd.DataFrame(data=rows, columns=cols)

        return df

    def parse(self):
        files_to_parse = self._get_files_to_be_parsed()
        print(f"Files to parse: {files_to_parse}")
        for file in files_to_parse:
            df = pd.read_csv(f"/output/raw/{file}")
            # print(df)
            parsed_df = self._parse_single_file(df)
            parsed_df.to_csv(f"/output/parsed/{file}")
            print("Parsed Files")
