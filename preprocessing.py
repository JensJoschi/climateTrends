from pathlib import Path
import pandas as pd
import random
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from station import Station

def get_data( p: Path) -> pd.DataFrame:
    """reads data from one climate station. Returns a panda table with date and temperature"""
    if not p.exists():
        raise FileNotFoundError(f"CSV file not found: {p}")
    try:
        data = pd.read_csv(p, usecols=["TMIN", "TMAX", "DATE"])
        if len(data) < 180:
            raise ValueError ("too little data")
    except ValueError as e:
        raise ValueError(f"Error reading CSV: {e}")
    return data    

def is_relevant(p:Path) -> bool:
    '''checks if absolutely neccessary data is contained (quick check only)'''
        data = pd.read_csv(p, nrows = 0) #header only
        required_cols = {"TMIN", "TMAX", "DATE"}
        return required_cols.issubset(data.columns)
    
def remove_irrelevant():      
    """remove files which do not have the required columns"""
    folder = Path("weather_data")
    all_files = [f for f in folder.iterdir() if f.is_file()]
    i = 0
    for file in all_files:
        if not is_relevant(file):
            file.unlink()
            i += 1
    print (f'{i} files removed. ') 

def process_file(file: Path):
    try:
        df = get_data(file)
        station = Station(file.stem)
        return station if station.run() else None
    except Exception:
        return None

if __name__ == "__main__":
    threads = os.cpu_count() * 20

    #remove_irrelevant() #89162

    folder = Path("weather_data")
    all_files = [f for f in folder.iterdir() if f.is_file()]
    print(f"{len(all_files)} stations.")

    analysed = []
    with ThreadPoolExecutor(max_workers= threads) as executor:
        futures = [executor.submit(process_file, f) for f in all_files]
        for future in as_completed(futures):
            result = future.result()
            if result:
                analysed.append(result)

    print (f"Done. {len(analysed)} Stations.")
    with open('stations.pkl', 'wb') as f:
        pickle.dump(analysed, f)