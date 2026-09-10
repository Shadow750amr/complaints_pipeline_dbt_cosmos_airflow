import pytest
from src.data_extraction import Extraction

def file_validation():
    with pytest.raises(ValueError):
        file_validation(Extraction)
    