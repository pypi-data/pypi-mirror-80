import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import plotly.graph_objects as go
import json
import simfin as sf
from simfin.names import *


def prep_dataframe(file):
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    statement = pd.read_csv(file)
    statement.iloc[:, 0] = statement.iloc[:, 0].str.replace(' ', '_')
    statement.iloc[:, 0] = statement.iloc[:, 0].str.replace(',', '')
    statement.iloc[:, 0] = statement.iloc[:, 0].str.replace('&', '')
    statement.iloc[:, 0] = statement.iloc[:, 0].str.lower()
    statement = statement.set_index(statement.columns[0])
    statement = statement.abs()
    return statement


def prep_json(file):
    statement = prep_dataframe(file)
    statement_json = statement.to_json(orient="index")
    parsed = json.loads(statement_json)
    statement_json = json.dumps(parsed)
    return statement_json


# period = annual, quarterly
# country= us
def prepare_finData(country):
    sf.set_api_key('free')
    sf.set_data_dir('~/simfin_data/')
    sf.load_companies(market=country)
    sf.load_industries()


def get_annual_finData_income(country):
    prepare_finData(country)
    df_income = sf.load_income(variant='annual', market=country)
    df_income.columns = df_income.columns.str.replace(' ', '_')
    return df_income


def get_annual_finData_balance(country):
    prepare_finData(country)
    df_balance = sf.load_balance(variant='annual', market=country)
    df_balance.columns = df_balance.columns.str.replace(' ', '_')
    return df_balance


def get_annual_finData_cashflow(country):
    prepare_finData(country)
    df_cashflow = sf.load_cashflow(variant='annual', market=country)
    df_cashflow.columns = df_cashflow.columns.str.replace(' ', '_')
    return df_cashflow


def get_annual_finData_by_symbol(category, symbol, country):
    try:
        if category == "income":
            df = get_annual_finData_income(country)
        if category == "balancesheet":
            df = get_annual_finData_balance(country)
        if category == "cashflow":
            df = get_annual_finData_cashflow(country)
        df.columns = df.columns.str.lower()
        df = df.loc[symbol].transpose()
        df = df.rename(index={'fiscal_year': 'breakdown'})
        df.columns = df.loc['breakdown']
        df = df.drop(['simfinid', 'currency', 'breakdown', 'fiscal_period', 'publish_date', 'restated_date'])
        return df
    except UnboundLocalError:
        print('Not a valid category')
    except KeyError:
        print('Not a valid symbol')


def printStatement(file):
    statement = prep_dataframe(file)
    print(statement)


def lineplot(dataframe, category):
    plotData = dataframe.T
    plotData = plotData.reset_index()
    # plotData.columns[0]= pd.to_datetime(plotData.columns[0])
    plotData = plotData.sort_values(plotData.columns[0])
    plotData = plotData[[plotData.columns[0], category]]
    plotData[category] = plotData[category].astype(float)

    plt.figure(figsize=(20, 9))
    sns.lineplot(data=plotData, x=plotData.columns[0], y=category)


def multiLineplot(dataframe, title):
    plotData = dataframe.T
    plotData = plotData.reset_index()
    if len(str(plotData.iat[0, 0])) > 4:
        plotData['index'] = pd.to_datetime(plotData['index'])
    plotData = plotData.sort_values(plotData.columns[0])

    columnsList = list(plotData.columns.values)
    graphRowCount = math.ceil(len(plotData.columns) / 3)
    fig = plt.figure(figsize=(30, 45))
    fig.suptitle(title, fontsize=30)

    for x in range(1, len(columnsList)):
        plotNumber = 'ax' + str(x)
        colname = plotData.columns[x]

        plotNumber = fig.add_subplot(graphRowCount, 3, x)
        plotNumber.set_title(colname)
        plotNumber.plot(plotData.iloc[:, 1],
                        plotData[colname])
        plt.xticks(rotation=45)

    plt.show()


def calculateMetrics(balanceSheet, incomeStatement):
    frames = [balanceSheet, incomeStatement]
    Ratio = pd.DataFrame()
    dataframeForRatio = pd.concat(frames)
    dataframeForRatio = dataframeForRatio.T
    dataframeForRatio['average_inventory'] = dataframeForRatio['inventories'].mean()
    dataframeForRatio['average_accounts_receivable'] = dataframeForRatio['accounts_&_notes_receivable'].mean()

    # Liquidity Ratios
    # Ratio['quick_ratio'] = (dataframeForRatio['Cash,_Cash_Equivalents_&_Short_Term_Investments']+dataframeForRatio['Accounts_&_Notes_Receivable']+dataframeForRatio['short_term_investments'])/dataframeForRatio['Total_Current_Liabilities']
    Ratio['acid-test_ratio'] = dataframeForRatio['total_current_assets'] / dataframeForRatio[
        'total_current_liabilities']
    Ratio['cash_ratio'] = (dataframeForRatio['total_current_assets'] - dataframeForRatio['inventories']) / \
                          dataframeForRatio['total_current_liabilities']

    # Leverage Financial Ratios
    Ratio['debt_to_equity_ratio'] = dataframeForRatio['total_liabilities'] / dataframeForRatio['total_equity']
    Ratio['interest_coverage_ratio'] = dataframeForRatio['gross_profit'] / dataframeForRatio['interest_expense,_net']
    Ratio['current_ratio'] = dataframeForRatio['total_current_assets'] / dataframeForRatio['total_current_liabilities']
    # Ratio['debt_service_coverage_ratio'] = dataframeForRatio['gross_profit']/dataframeForRatio['']

    # Efficiency Ratios
    Ratio['asset_to_sales_ratio'] = dataframeForRatio['total_assets'] / dataframeForRatio['revenue']
    Ratio['asset_turnover_ratio'] = dataframeForRatio['revenue'] / dataframeForRatio['total_assets']
    Ratio['inventory_turnover_ratio'] = dataframeForRatio['cost_of_revenue'] / dataframeForRatio['average_inventory']
    Ratio['days_sales_in_inventory_ratio'] = 365 / Ratio['inventory_turnover_ratio']
    Ratio['receivables_turnover_ratio'] = dataframeForRatio['revenue'] / dataframeForRatio[
        'average_accounts_receivable']
    Ratio['average_collection_period'] = 365 / Ratio['receivables_turnover_ratio']
    Ratio['interest_coverage_ratio'] = dataframeForRatio['pretax_income_(loss),_adj.'] / dataframeForRatio[
        'interest_expense,_net']

    # Profitability Ratios
    Ratio['gross_margin_ratio'] = dataframeForRatio['gross_profit'] / dataframeForRatio['revenue']
    Ratio['operating_margin_ratio'] = dataframeForRatio['net_income'] / dataframeForRatio['revenue']
    Ratio['return_on_assets_ratio'] = dataframeForRatio['net_income'] / dataframeForRatio['revenue']
    Ratio['return_on_equity_ratio'] = dataframeForRatio['net_income'] / (
            dataframeForRatio['revenue'] - dataframeForRatio['total_liabilities'])
    Ratio['net_working_capital'] = dataframeForRatio['total_current_assets'] - dataframeForRatio['total_liabilities']
    Ratio['operating_margin'] = dataframeForRatio['operating_income_(loss)'] / dataframeForRatio['revenue']
    Ratio['retention_ratio'] = dataframeForRatio['retained_earnings'] / dataframeForRatio['revenue']

    Ratio = Ratio.T
    Ratio = Ratio.round(4)
    return Ratio


def bulletChart(file, item):
    statement = prep_dataframe(file)

    data = statement.T
    data = data.reset_index()
    data = data.sort_values(by='index', ascending=False)
    avg_item = 'avg_' + item
    data[avg_item] = data[item].mean()
    data = data.round(2)
    data = data.iloc[0]

    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        gauge={'shape': "bullet"},
        value=data[item],
        delta={'reference': data[avg_item]},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': item}))
    fig.update_layout(height=250)

    fig.show()


def horizontalAnalysisLastTwo(dataframe):
    statement = dataframe
    statement = statement.reindex(sorted(statement.columns), axis=1)
    statement_lastPeriods = statement[statement.columns[-2:]]
    statement_lastPeriods_lastColName = statement[statement_lastPeriods.columns[-1:]].columns.values[0]
    statement_lastPeriods_secondLastColName = statement[statement_lastPeriods.columns[-2:-1]].columns.values[0]
    statement_lastPeriods['Amount(Increased/Decreased)'] = statement_lastPeriods[statement_lastPeriods_lastColName] - \
                                                           statement_lastPeriods[
                                                               statement_lastPeriods_secondLastColName]
    statement_lastPeriods['Percentage(Increased/Decreased)'] = (statement_lastPeriods[
                                                                    statement_lastPeriods_lastColName] /
                                                                statement_lastPeriods[
                                                                    statement_lastPeriods_secondLastColName]) - 1
    statement_lastPeriods = statement_lastPeriods.dropna()
    statement_lastPeriods['Percentage(Increased/Decreased)'] = pd.Series(
        ["{0:.2f}%".format(val * 100) for val in statement_lastPeriods['Percentage(Increased/Decreased)']],
        index=statement_lastPeriods.index)
    statement_lastPeriods.to_csv('horizontalAnalysisLastTwo.csv')
    print("Horizontal Analysis with Last two Periods", statement_lastPeriods, sep='\n')


def _process_symbol(symbol: str):
    df_income = get_annual_finData_by_symbol('income', symbol, 'us')
    df_balancesheet = get_annual_finData_by_symbol('balancesheet', symbol, 'us')

    ret = calculateMetrics(df_balancesheet, df_income)
    ret = ret.T
    ret = ret.reset_index()
    ret = ret.rename(columns={'breakdown': 'fiscal_year'})
    ret.insert(0, 'Ticker', symbol)
    ret = ret.set_index(['Ticker', 'fiscal_year'])
    return ret


def calculate_ratio_mass(symbols):
    concate = pd.DataFrame()
    for symbol in symbols:
        ratio = _process_symbol(symbol)
        concate = pd.concat([concate, ratio])
    return concate
