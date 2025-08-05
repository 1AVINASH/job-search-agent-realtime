import pandas as pd

class JobsSpreadsheetParser:
    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        df = pd.read_csv(f"/output/raw/{self.file_name}")
        print(df)
        df.to_csv(f"/output/parsed/{self.file_name}")
