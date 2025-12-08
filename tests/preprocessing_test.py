import pytest
from src.climateTrends.preprocessing import get_data, process_file
from src.climateTrends.station import Station
from pathlib import Path
import pandas as pd
import tempfile
import os

def test_getData():
    """Test the get_data function using a real GHCN file"""
    test_file_path = Path("raw_ghcn/ACW00011604.csv") #first file as example. Insufficient number of years, but doesnt matter for this test.
    
    data, coordinates = get_data(test_file_path)
    
    assert isinstance(data, pd.DataFrame)
    assert isinstance(coordinates, tuple)
    assert len(coordinates) == 2 #latitude/longitude pair
    
    assert coordinates[0] == 17.11667
    assert coordinates[1] == -61.78333

    # Test that required columns exist
    required_columns = {"TMIN", "TMAX", "DATE"}
    assert required_columns.issubset(data.columns), f"Data must contain columns: {required_columns}"

    assert len(data) >= 180
    assert data["TMIN"][0] ==  217
    assert data["TMAX"][0] == 289
    assert data["DATE"][0] == "1949-01-01"

def test_getData_file_not_found():
    """Test get_data function with non-existent file"""
    no_path = Path("raw_ghcn/nonexistent_file.csv")
    
    with pytest.raises(FileNotFoundError):
        get_data(no_path)

def test_getData_insufficient_data():
    """Test get_data function with file containing insufficient data (< 180 rows)"""
    # Create a temporary CSV file with insufficient data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_file.write('STATION,DATE,LATITUDE,LONGITUDE,ELEVATION,NAME,TMIN,TMAX\n')
        for i in range(50): 
            temp_file.write(f'TEST001,2020-01-{i+1:02d},45.0,-75.0,100,TEST STATION,200,300\n')
        temp_path = temp_file.name
    
    try:
        temp_file_path = Path(temp_path)
        with pytest.raises(ValueError):
            get_data(temp_file_path)
    finally:
        os.unlink(temp_path)

def test_process_file():
    """Test the process_file function using a real GHCN file"""
    test_file_path = Path("raw_ghcn/ZI000067991.csv") #last file in folder, should have sufficient data
    result = process_file(test_file_path)
    assert result
    insuff = Path ("raw_ghcn/ACW00011647.csv")
    result = process_file(insuff)
    assert result == None

def test_process_file_invalid():
    """Test process_file function with non-existent file"""
    non_existent_path = Path("raw_ghcn/nonexistent_file.csv")
    
    # Should return None for invalid files (exception handling in process_file)
    result = process_file(non_existent_path)
    assert result is None, "process_file should return None for non-existent files"
    