import requests
import logging
from dotenv import load_dotenv
from utils.utils import URL,FILE_PATH
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", mode='w'),
        logging.StreamHandler() # Para ver logs en consola simultáneamente
    ]
)
logger = logging.getLogger(__name__)



class Extraction:
    '''
    This class manages archives downloads from an URL and its storage in a local repo.
    Atributes: url (str): resource path
               filename (str): the file's name (also cona be a desination path)
    Methods:   Executes customed download process (streamning) and save it.

    '''
    def __init__(self, url: str, filename: str) -> None:                    # Despite this is declarative I specically used an expected return
        self.url = url
        self.filename = filename
        logger.info("Clase Extraction instanciada correctamente.")
        return None

    def connect_and_save(self) ->str:
        try:
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()
                with open(self.filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):    # Notice the chunk size it is intentional so there is no RAM affectation
                        if chunk:
                            file.write(chunk)
            logger.info(f"Archivo {self.filename} generado con éxito.")
            return self.filename
        except Exception as e:
            logger.error(f"Error en la descarga: {e}")

if __name__ == "__main__":

    
    extractor = Extraction(URL, FILE_PATH)
    extractor.connect_and_save()

    