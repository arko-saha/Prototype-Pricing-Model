import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime
import warnings

class NaturalGasForecaster:
    """
    A class to forecast natural gas prices using the ARIMA model.
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.model_fit = None
        self.load_and_preprocess_data()
        self.train_model()

    def load_and_preprocess_data(self):
        """Loads data from CSV and handles date parsing."""
        self.df = pd.read_csv(self.data_path)
        self.df['Dates'] = pd.to_datetime(self.df['Dates'])
        self.df.set_index('Dates', inplace=True)
        self.df = self.df.sort_index()
        # Natural gas prices often have monthly seasonality. 
        # For simplicity in this prototype, we'll use ARIMA(1,1,1).
        # In a production environment, we'd use auto_arima or more complex SARIMA.

    def train_model(self):
        """Trains the ARIMA model on the historical data."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ARIMA(self.df['Prices'], order=(1, 1, 1))
            self.model_fit = model.fit()

    def predict(self, date):
        """
        Predicts the price for a given date.
        If the date is in the historical data, it returns the actual price.
        Otherwise, it uses the ARIMA model to forecast.
        """
        target_date = pd.to_datetime(date)
        
        if target_date in self.df.index:
            return self.df.loc[target_date, 'Prices']
        
        # Calculate number of steps from the last date in training data
        last_date = self.df.index[-1]
        
        # Simple heuristic: forecast month-by-month
        # For more precision, we'd calculate the exact steps.
        # But for this prototype, we'll estimate steps as months.
        diff = (target_date.year - last_date.year) * 12 + (target_date.month - last_date.month)
        
        if diff <= 0:
            # If it's in the past relative to the dataset but not found, 
            # return the nearest neighbor or interpolant (simplified)
            idx = self.df.index.get_indexer([target_date], method='nearest')[0]
            return self.df.iloc[idx]['Prices']

        # Forecast up to the target date
        forecast = self.model_fit.forecast(steps=diff)
        return forecast.iloc[-1]

    def get_historical_data(self):
        return self.df.reset_index()
