import pytest
from pathlib import Path
from src.climateTrends.station import Station
from src.climateTrends.services import load_stations, find_nearest

def test_load_data():
    p = Path("data/stations.pkl")
    analysed = load_stations(p)
    assert len(analysed) > 0
 #   analysed[4].plot()


def test_find_nearest():
    p = Path("data/stations.pkl")
    analysed = load_stations(p)
    s = find_nearest(analysed, 40, 7)
    assert(s.coordinates[0] < 41 and s.coordinates[0] > 40)
    assert(s.coordinates[1] < 9 and s.coordinates[1] > 8)
