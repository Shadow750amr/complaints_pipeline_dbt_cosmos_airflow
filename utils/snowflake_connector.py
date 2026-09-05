import snowflake.connector                                #  Standard import to handle snowflake connections
from snowflake.connector import SnowflakeConnection       # this was imported to define the connection return which is indeed a SnowflakeConnection
import os
import logging
from typing import Optional,Dict
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class SnowflakeConnector:

    ''' This class is used to create a connection between snowflake and an external resource.
        _get_connection: Lazy initialization to define a connection to snowflake
        close: This close the connection to snowflake making sure there is no active connection (really important to switch off the wh)  '''

    def __init__(self, user: str, account: str, warehouse: str, 
                 database: str, schema: str, password: Optional[str] = None) -> None:
        
        self.conn_params = {
            "user": user,
            "password": password or os.getenv('SNOWFLAKE_PASSWORD'),
            "account": account,
            "warehouse": warehouse,
            "database": database,
            "schema": schema
        }
        self.conn = None
        self.logger = logging.getLogger(__name__) # Definiciòn del logger

    def _get_connection(self) -> SnowflakeConnection:          #Lazy initialization
        self.logger.info("Conection initialized.")
        if self.conn is None:
            self.conn = snowflake.connector.connect(**self.conn_params)         # ** to return the list of arguments listed above with no mistakes
        return self.conn
    
  
    def _close(self):
        if self.conn:
            self.conn.close()







