from pathlib import Path
import pandas as pd
import plotly.express as px
import numpy as np
import statsmodels.api as sm
from typing import Tuple

class Station:
    '''this class performs analysis on the provided data frame and stores the summary statistics and results. 
    Original dataframe is destructed in the process. Results are annual mean temperatures. 
    Summary statistics are r-squared, slope estimate and intercept'''
    def __init__(self, name:str, coords: tuple):
        self.name = name
        self.sufficient = False
        self._annual_T = pd.DataFrame()
        self._model = None
        self._coordinates = coords
        if len(coords) != 2:
            raise ValueError("coordinates must have two elements")

    def run(self, data: pd.DataFrame) -> bool:
        '''clean and analyse one climate station. 
        Returns true if analysis was successful. 
        "Successful" currently means enough data to do something useful, but not necessarily enough for statistically robust results'''
        self._annual_T = self._clean_data(data)
        if not self.sufficient: return False
        self._model = self._analyse()
        return True# if self._model['rsq'] > 0.6 else False  -> possibly too strict
    
    @property
    def temperatures(self):
        return self._annual_T if self.sufficient else None
    
    @property
    def statistics(self) -> dict:
        return self._model if self.sufficient else None
    
    @property
    def coordinates(self) -> tuple:
        return self._coordinates
    
    def plot (self):
        '''quick plot of results for validation, not beautiful but sufficient'''
        fig = px.scatter(x = self._annual_T['year'], y = self._annual_T['T'])
        fig.update_yaxes(range = (0, self._annual_T['T'].max()))
        fig.show()


    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """preprocessing of data. Creates annual mean for all years with >= 180 days.
        sets flag self.sufficient after processing
        input data is altered in the process, not to be reused!"""

        for col in ['TMAX', 'TMIN']:
            data[col] = data[col].replace([-9999, -999, -99, '', 'NAN'], np.nan).astype(float) /10.0
        data['DATE'] = pd.to_datetime(data['DATE'], format="%Y-%m-%d", errors='coerce')
        data.dropna(subset=['DATE', 'TMAX', 'TMIN'], inplace=True)
        data['year'] = data['DATE'].dt.year
        data['T'] = (data['TMAX'] + data['TMIN']) / 2.0
        
        annuals = (
            data.groupby('year')['T']
            .agg(count = 'count', mean = 'mean')
            .query('count >= 180')
            .reset_index()
            .rename(columns ={'mean': 'T'})
        )

        self.sufficient = len(annuals) >= 3
        return annuals

    
    def _analyse(self) ->dict :
        """performs a statistical analysis on the data. """ 
        X = sm.add_constant(self._annual_T['year'])
        y = self._annual_T["T"]
        model = sm.OLS(y, X).fit()
        results = {
            'intercept': model.params['const'],
            'slope': model.params['year'],
            'rsq': model.rsquared
        }
        del model
        return results