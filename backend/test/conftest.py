import pytest
from pathlib import Path

@pytest.fixture
def data_path() -> Path:
    "Returns the path to the SH1.119 Excel file"
    return (Path(__file__).parent / "SH1.119.xlsx").resolve()
