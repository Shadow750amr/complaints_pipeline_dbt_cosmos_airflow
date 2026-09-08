from airflow.decorators import dag,task
from airflow.sdk import Asset
from src.data_extraction import Extraction
from src.upload_to_s3 import upload_file
from src.upload_to_snowflake import UploadToSnowflake
from utils.utils import URL,FILE_PATH
import datetime
import os

# "Self-contained daily ETL pipeline built with the TaskFlow API and Asset approach for reusability and asset orchestration. 
#  Orchestrates three sequential steps: local download, persistence to S3, and automated loading into Snowflake using a staging scheme.

snowflake_complaints_asset = Asset(
    uri="snowflake://{account}.snowflakecomputing.com/{database}/{schema}/{table}".format(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA'),
        table=os.getenv('SNOWFLAKE_TABLE_NAME', 'COMPLAINTS')
    )
)

@dag(start_date=datetime.datetime(2026, 9, 6),schedule='@daily',catchup=False)
def complaints_pipeline():
    @task(task_id="ejecutar_descarga")
    def descarga_archivo():
        descargar_archivo = Extraction(url=URL,filename=FILE_PATH)
        path_archivo = descargar_archivo.connect_and_save()
        return path_archivo

    @task(task_id="cargar_s3")
    def mandar_archivo_s3(path_archivo):
        return upload_file(
            file_name=path_archivo,
            bucket = os.getenv('BUCKET_NAME'),
            aws_conn_id='aws_default'
        )
    
    @task(task_id="cargar_snowflake",outlets=[snowflake_complaints_asset])
    def ingest_to_snowflake():
        uploader = UploadToSnowflake(
            user=os.getenv('SNOWFLAKE_USER'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA'))
        uploader.create_table(os.getenv('SNOWFLAKE_TABLE_NAME'),os.getenv('SNOWFLAKE_STAGE_NAME'))
        uploader.ingest_from_stage(os.getenv('SNOWFLAKE_TABLE_NAME'),os.getenv('SNOWFLAKE_STAGE_NAME'))
        return uploader.close()

        
    
    t1 = descarga_archivo()
    t2 = mandar_archivo_s3(t1)
    t3 = ingest_to_snowflake()

    t1 >> t2 >> t3

complaints_pipeline()

        