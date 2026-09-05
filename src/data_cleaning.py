import pandas as pd
import logging
import os
from dotenv import load_dotenv
load_dotenv()
from utils.formats import TEXT_COLUMNS,DATE_COLUMNS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", mode='w'),
        logging.StreamHandler() # Para ver logs en consola simultáneamente
    ]
)
logger = logging.getLogger(__name__)


# Defining the path where the csv is located at
PROCESSED_CSV = os.getenv('PROCESSED_CSV')
TEXT_COLUMNS = TEXT_COLUMNS
DATE_COLUMNS = DATE_COLUMNS

class DataCleaning:

    ''' 
    The class is designed to handle the cleaning process of your data, particularly focusing on text and date columns.

    - Constructor (__init__):

    Takes the file path, list of text columns and a list of date columns as input.
    Stores these details in instance attributes: self.path, self.text_cols, self.date_cols and self.df.
    
    - Cleaning (clean_data): This method performs the cleaning operations:
    Reads the CSV file into a pandas DataFrame (self.df).
    Handles text column cleanup: Uses .astype(str).str.strip() for removing leading/trailing whitespace from each column of the text type.
    Handles date column conversion and returns the cleaned DataFrame.
    
      Usage: The if __name__ == "__main__": block demonstrates how to create an instance of the DataCleaning class and call the 
    clean_data method.
    '''

    def __init__(self,path:str,text_cols:list,date_cols:list) -> None:
        self.path = path
        self.text_cols = text_cols
        self.date_cols = date_cols
        self.df = None
    
    def clean_data(self) -> pd.DataFrame:

        logger.info(f"Initializing cleaning for file {self.path}")

    # Read the csv
        self.df = pd.read_csv(self.path)
        try:
    # string columns
            for col in self.text_cols:
                if col in self.df.columns:
                    self.df[col] = self.df[col].astype(str).str.strip()
    #  date columns
            for col in self.date_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_datetime(self.df[col],errors='coerce')
                    return self.df
        except Exception as e:
            logger.error(f"Could not clean data {e}")
    


if __name__ == "__main__":
    data = DataCleaning(PROCESSED_CSV,TEXT_COLUMNS,DATE_COLUMNS)
    final_df = data.clean_data()
    print(final_df.head(5))

