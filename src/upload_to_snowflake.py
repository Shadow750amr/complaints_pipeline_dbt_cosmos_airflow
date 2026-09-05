import os
import logging
from utils.snowflake_connector import SnowflakeConnector


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class UploadToSnowflake(SnowflakeConnector):
    ''' This class is used to load data into snowflake using an s3 bucket as source (external stage).
        ingest_from_stage: This uploads the csv to the stage.
        create_table: This creates a destination schema based on the table schema from the s3 bucket.
        '''

    def create_table(self,table_name: str, stage_name: str) -> str:
        cursor = self._get_connection().cursor()
        try:
            self.logger.info("Creando tabla base")
            create_query = f"""
            CREATE OR REPLACE TABLE {table_name}
            USING TEMPLATE (
                SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
                FROM TABLE(
                    INFER_SCHEMA(
                        LOCATION => '@{stage_name}',
                        FILE_FORMAT => 'CSV'
                    )
                )
            )
            """
            cursor.execute(create_query)
        except Exception as e:
            self.logger.error(f"An error ocurred creating the table {e}.")
                    
        finally:
            cursor.close()

    def ingest_from_stage(self, table_name: str, stage_name: str) -> str:
        
        cursor = self._get_connection().cursor()
        try:
            self.logger.info(f"Uploading data into {table_name}...")
            copy_query =f"""
            COPY INTO {table_name}
            FROM @{stage_name}
            FILE_FORMAT = (
            FORMAT_NAME = 'CSV')
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
            """ 
            cursor.execute(copy_query)
        finally:
            cursor.close()
            self.logger.info("Process finished.")

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    uploader = UploadToSnowflake(
        user=os.getenv('SNOWFLAKE_USER'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

    
    uploader.create_table(os.getenv('SNOWFLAKE_TABLE_NAME'),os.getenv('SNOWFLAKE_STAGE_NAME'))
    
    
    uploader.ingest_from_stage(os.getenv('SNOWFLAKE_TABLE_NAME'),os.getenv('SNOWFLAKE_STAGE_NAME'))

   
    uploader.close()

