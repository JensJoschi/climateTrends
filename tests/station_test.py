import pytest
from src.climateTrends.station import Station
import pandas as pd
import numpy as np
import random 

def test_station_all_good():
    testStat = Station ("test", (14,21.2))
    dates = pd.date_range("1983-01-01", "1988-12-31", freq="D")
    days = np.arange(len(dates))
    testData = pd.DataFrame({
        "DATE": dates,
        "TMIN": 200 + days, #should be sinusoid with period 360 days + annual trend, but just using linear increase for simplicity 
        "TMAX": 250 + days  
    })
    ok = testStat.run(testData)
    assert(ok)
    assert(len(testStat.temperatures) == 6)
    assert(testStat.statistics["slope"] >36.5) 
    assert(testStat.statistics["slope"] < 37.0)
    assert(testStat.statistics["rsq"] == pytest.approx(1.0))
    y = testStat.temperatures[testStat.temperatures['year'] == 1983]
    assert(np.mean(y['T']) == 40.7) #mean of 200+364/2 and 250+364/2; cut decimal according to GHCN file format

def test_station_insufficient_data():
    testStat = Station ("test", (14,21.2))
    dates = pd.date_range("1983-01-01", "1984-06-10", freq="D")
    days = np.arange(len(dates))
    testData = pd.DataFrame({
        "DATE": dates,
        "TMIN": 200 + days,
        "TMAX": 250 + days  
    })
    enough = testStat.run(testData)
    assert(not enough)

def test_station_badRsq():
    testStat = Station ("test", (14,21.2))
    dates = pd.date_range("1983-01-01", "1998-12-31", freq="D")
    r = [random.randint(0,100) for i in range(len(dates))]
    testData = pd.DataFrame({
        "DATE": dates,
        "TMIN": r,
        "TMAX": r
    })
    ok = testStat.run(testData)
    assert(not ok)
    assert(testStat.statistics["rsq"] < 0.1) # close to 0, usually
# slope should be ~ 0 and mean T approx 5 but testing this is inherently flaky due to randint()

def test_station_coordinates():
    testStat = Station("test", (14, 21.2))
    assert(testStat.coordinates == (14,21.2))
    t2 = Station("test", [12, 121.042])
    assert(t2.coordinates == [12, 121.042])
    with pytest.raises(ValueError):
        Station("test", (14,))
    
    with pytest.raises(ValueError):
        Station("test", (14, 21.2, 30))