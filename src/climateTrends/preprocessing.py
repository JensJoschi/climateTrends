from pathlib import Path
import pandas as pd
import random
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from climateTrends.station import Station

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
    
def remove_irrelevant(folder: Path) -> int:
    """remove files which do not have the required columns"""
    all_files = [f for f in folder.iterdir() if f.is_file()]
    removed = 0
    for file in all_files:
        if not is_relevant(file):
            file.unlink()
            removed += 1
    print (f'{removed} files removed. ') 
    return removed

def process_file(file: Path) -> Station | None:
    try:
        df = get_data(file)
        station = Station(file.stem)
        return station if station.run() else None
    except Exception:
        return None

def main():
    raw_folder = Path("data/raw/weather_data")
    if not raw_folder.exists():
        raise FileNotFoundError(f"Raw weather folder not found: {raw_folder}")
#remove_irrelevant() #89162
    all_files = [f for f in raw_folder.iterdir() if f.is_file()]
    print(f"{len(all_files)} stations.")

    threads = os.cpu_count() * 20

    analysed = []
    with ThreadPoolExecutor(max_workers= threads) as executor:
        futures = [executor.submit(process_file, f) for f in all_files]
        for future in as_completed(futures):
            result = future.result()
            if result:
                analysed.append(result)

    print (f"Done. {len(analysed)} Stations.")
    output_path = Path("data/processed/stations.pkl")
    print (output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(analysed, f)

if __name__ == "__main__":
    print ("start", flush = True)
    main()