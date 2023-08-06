from fbprophet import Prophet
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def fit_predict_model(dataframe, interval_width=0.99, changepoint_range=0.8):
    m = Prophet(daily_seasonality=False, yearly_seasonality=False, weekly_seasonality=False,
                seasonality_mode='multiplicative',
                interval_width=interval_width,
                changepoint_range=changepoint_range)
    m = m.fit(dataframe)

    pred = m.predict(dataframe)
    pred['mark'] = dataframe['y'].reset_index(drop=True)
    return pred

def detect_anomalies(pred):
    predicted = pred[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'mark']].copy()

    predicted['anomaly'] = 0
    predicted.loc[predicted['mark'] > predicted['yhat_upper'], 'anomaly'] = 1
    predicted.loc[predicted['mark'] < predicted['yhat_lower'], 'anomaly'] = -1

    predicted['importance'] = 0
    predicted.loc[predicted['anomaly'] == 1, 'importance'] = \
        (predicted['mark'] - predicted['yhat_upper']) / forecast['mark']
    predicted.loc[predicted['anomaly'] == -1, 'importance'] = \
        (predicted['yhat_lower'] - predicted['mark']) / forecast['mark']

    return predicted
