import os
from scipy.stats import chisquare
from scipy.stats import ks_2samp
from scipy.stats import combine_pvalues
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fbprophet import Prophet


def init_df(df, colname, target, target_value):
    value_arr = df[colname].loc[df[target] == target_value].values
    return value_arr


# @misc{erdogant2020benfordslaw,
#   title={benfordslaw},
#   author={Erdogan Taskesen},
#   year={2019},
#   howpublished={\url{https://github.com/erdogant/benfordslaw}},
# }

# Benford's Law percentages
BENFORDLD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]


# process
def process_benfordlaw(value_arr, alpha=0.05, verbose=3):
    [counts_emp, percentage_emp, total_count, digit] = _count_first_digit(value_arr)
    counts_exp = _get_expected_counts(total_count)

    # get p-value
    [tstats1, Praw1] = chisquare(counts_emp, f_exp=counts_exp)
    [tstats2, Praw2] = ks_2samp(counts_emp, counts_exp)
    tstats, Praw = combine_pvalues([Praw1, Praw2], method='fisher')
    method = 'P_ensemble'

    if Praw <= alpha and verbose >= 3:
        print("[benfordslaw] >[%s] Anomaly detected! P=%g, Tstat=%g" % (method, Praw, tstats))
    elif verbose >= 3:
        print("[benfordslaw] >[%s] No anomaly detected. P=%g, Tstat=%g" % (method, Praw, tstats))

    result = {}
    result['p-value'] = Praw
    result['tstats'] = tstats
    result['alpha'] = alpha
    result['method'] = method
    result['percentage_emp'] = np.c_[digit, percentage_emp]
    return (result)


def _count_first_digit(data):
    data = data[data > 1]
    first_digits = list(map(lambda x: int(str(x)[0]), data))

    emperical_counts = np.zeros(9)
    digit = []
    for i in range(1, 10):
        emperical_counts[i - 1] = first_digits.count(i)
        digit.append(i)

    total_count = sum(emperical_counts)
    emperical_percentage = [(i / total_count) * 100 for i in emperical_counts]
    return (emperical_counts, emperical_percentage, total_count, digit)


def _get_expected_counts(total_count):
    result = []
    for p in BENFORDLD:
        result.append(round(p * total_count / 100))

    return (result)


# Plot
def plot_benfordlaw(result, title='', figsize=(15, 8)):
    fontsize = 16

    data_percentage = result['percentage_emp']
    x = data_percentage[:, 0]
    width = 0.3  # the width of the bars

    # Make figures
    fig, ax = plt.subplots(figsize=figsize)
    rects1 = ax.bar(x, data_percentage[:, 1], width=width, color='black', alpha=0.8, label='Emperical distribution')
    plt.plot(x, data_percentage[:, 1], color='black', linewidth=0.8)
    for rect in rects1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, '{:0.1f}'.format(height), ha='center', va='bottom',
                fontsize=13)

    # Plot expected benfords values
    ax.scatter(x, BENFORDLD, s=150, c='orange', zorder=3, label='Benfords distribution')

    if result['p-value'] <= result['alpha']:
        title = title + "\nAnomaly detected! P-value=%g, Tstat=%g" % (result['p-value'], result['tstats'])
    else:
        title = title + "\nNo anomaly detected. P-value=%g, Tstat=%g" % (result['p-value'], result['tstats'])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    fig.canvas.set_window_title('Percentage First Digits')
    ax.set_title(title, fontsize=fontsize)
    ax.set_ylabel('Frequency (%)', fontsize=fontsize)
    ax.set_xlabel('Digits', fontsize=fontsize)
    ax.set_xticks(x)
    ax.set_xticklabels(x, fontsize=fontsize)
    ax.grid(True)
    ax.legend()
    # Hide the right and top spines & add legend
    ax.legend(prop={'size': 15}, frameon=False)
    plt.show()

    return fig, ax


def _fit_predict_model(dataframe, interval_width=0.99, changepoint_range=0.8):
    m = Prophet(daily_seasonality=False, yearly_seasonality=False, weekly_seasonality=False,
                seasonality_mode='multiplicative',
                interval_width=interval_width,
                changepoint_range=changepoint_range)
    m = m.fit(dataframe)

    pred = m.predict(dataframe)
    pred['mark'] = dataframe['y'].reset_index(drop=True)
    return pred


def _detect_anomalies(pred):
    predicted = pred[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'mark']].copy()

    predicted['anomaly'] = 0
    predicted.loc[predicted['mark'] > predicted['yhat_upper'], 'anomaly'] = 1
    predicted.loc[predicted['mark'] < predicted['yhat_lower'], 'anomaly'] = -1

    predicted['importance'] = 0
    predicted.loc[predicted['anomaly'] == 1, 'importance'] = \
        (predicted['mark'] - predicted['yhat_upper']) / predicted['mark']
    predicted.loc[predicted['anomaly'] == -1, 'importance'] = \
        (predicted['yhat_lower'] - predicted['mark']) / predicted['mark']

    return predicted


def anomalies_detection(df, col_to_filter, filter_value, target_col):
    df = df.loc[df[col_to_filter] == filter_value]
    df = df[['date', target_col]]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.set_index('date').groupby(pd.Grouper(freq='D')).max()
    df = df.reset_index()
    df = df.dropna()
    df.columns = ['ds', 'y']
    pred = _fit_predict_model(df)
    pred = _detect_anomalies(pred)
    pred_ano = pred.loc[pred['anomaly'] == 1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pred['ds'], y=pred['mark'], name=target_col, mode='lines'))
    fig.add_trace(
        go.Scatter(x=pred_ano['ds'], y=pred_ano['mark'], mode='markers', name='Anomaly', marker=dict(color='red')))
    fig.update_layout(showlegend=True, title='Detected Anomalies')
    fig.show()
