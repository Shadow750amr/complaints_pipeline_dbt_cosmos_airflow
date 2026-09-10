import pytest
from src.data_extraction import Extraction

def test_file_validation():
    with pytest.raises(ValueError):
        test_file_validation(Extraction)
    