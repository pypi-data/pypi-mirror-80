## GusPI
This open-source python package aims to provide statistical support in supply chain analytics and finance/accounting analytics. We welcome everyone to use this python package for personal or professional projects. Please let us know any feedback you have. We'd love to improve the package and add feature enhancements to benefit researchers.

Report any bugs by opening an issue here: https://github.com/ygeszvain/GusPI/issues

Quick start

```
$ python3 -m pip install -U GusPI
```

## Templates
### Templates for suPY

[SalesData.csv](https://github.com/ygeszvain/GusPI/blob/master/sampleFiles/SalesData.csv)

### Templates for fiPY

[income_statement.csv](https://github.com/ygeszvain/GusPI/blob/master/sampleFiles/income_statement.csv)

[income_statement_yr.csv](https://github.com/ygeszvain/GusPI/blob/master/sampleFiles/income_statement_yr.csv)

[income_statement_m.csv](https://github.com/ygeszvain/GusPI/blob/master/sampleFiles/income_statement_m.csv)

[balancesheet.csv](https://github.com/ygeszvain/GusPI/blob/master/sampleFiles/balancesheet.csv)

[balance_sheet_yr.csv](https://github.com/ygeszvain/GusPI/blob/master/sampleFiles/balance_sheet_yr.csv)

[cashflow.csv](https://github.com/ygeszvain/GusPI/blob/master/sampleFiles/cashflow.csv)

## Demo notebook

[demo](https://colab.research.google.com/drive/1qc1ZuvbgWPLCrSP3z-8Umj4FYJSiViq8?usp=sharing)

## GusPI.suPY

```
from GusPI import suPY
```

### metrics

This package provides several analytical formulas to support supply chain analytics.

Economic order quantity
EOQ(demand, mean, STD, C, Ce, Cs, Ct)

Perfect Order Measurement
POM(TotalOrders, ErrorOrders)

Fill Rate
FR(TotalItems, ShippedItems)

Inventory Days of Supply
IDS(InventoryOnHand,AvgDailyUsage)

Freight cost per unit
FCU(TotalFreightCost,NumberOfItems)

Inventory Turnover
IT(COGS,AvgInventory)

Days of Supply (DOS)
DOS(AvgInventory,MonthlyDemand)

Gross Margin Return on Investment (GMROI)
GMROI(GrossProfit, OpeningStock, ClosingStock)

Inventory Accuracy
IA(ItemCounts, TotalItemCounts)

Storage Utilization Rate
SUR(InventoryCube, TotalWarehouseCube)

Total Order Cycle Time
TOCT(TimeOrderReceivedbyCustomer, TimeOrderPlaced,TotalNumberofOrdersShipped)

Internal Order Cycle Time
IOCT(TimeOrderShipped, TimeOrderReceived, NumberofOrdersShipped)

Read sales data from csv file and calculate basic safety sock and reorder point.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#safety days: 5
#leadtime in days: 7

suPy.basicSafetyStock('SalesData.csv','ProductNumber',5,7)
```

Read sales data from csv file and calculate basic safety sock and reorder point for all products.

```
#Example

#sales data from a csv file: salesData.csv
#safety days: 5
#leadtime in days: 7

suPy.basicSafetyStockList('SalesData.csv',5,7)
```

Read sales data from csv file and calculate safety sock and reorder point.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#service rate: 0.95
#leadtime in days: 7

suPy.safetyStockwtServiceRate('SalesData.csv','ProductNumber',0.95,7)
```

Read sales data from csv file and calculate basic safety sock and reorder point for all products.

```
#Example

#sales data from a csv file: salesData.csv
#service rate: 0.95
#leadtime in days: 7

suPy.safetyStockwtServiceRateList('SalesData.csv',0.95,7)
```

Read sales data from csv file and calculate coefficient of variation of a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#CV is non-negative and higher CV indicates higher volatility

suPy.cvPerProduct('SalesData.csv','ProductNumber')
```

Read sales data from csv file and calculate 'Intercept', 'Slope', 'Mean Absolute Error', 'Mean Squared Error', 'Root Mean Squared Error' of a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber

suPy.linearRegressionPerProduct('SalesData.csv','ProductNumber')
```

Read sales data from csv file and calculate EOQ of a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#Setup cost: 2000
#Holding cost: 1000

suPy.eoqPerProduct('SalesData.csv','ProductNumber',2000,1000)
```

Read sales data from csv file and create a list of average quantity sold per year for products.

```
#Example

#sales data from a csv file: salesData.csv

suPy.avgQtySoldList('SalesData.csv')
```

Read sales data from csv file and calculate the seasonality index of a product for a given year.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#year: 2018

suPy.seasonalityIndexPerProduct('SalesData.csv','ProductNumber',2018)
```

### graphs

Read sales data from csv file and print out a line plot of a product quantity sold.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber

#print the line plot
suPy.line plotQtyByMonth('salesData.csv','ProductNumber')
```

Read sales data from csv file and print out a line plot of a product's total cost sold.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber

#print the line plot
suPy.line plotTotalCostByMonth('salesData.csv','ProductNumber')
```

Read sales data from csv file and print out a line plot of a product's total sales.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber

#print the line plot
suPy.line plotTotalSalesByMonth('salesData.csv','ProductNumber')
```

Read sales data from csv file and print out a line plot of a product's average cost.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber

#print the line plot
suPy.line plotAverageCostByMonth('salesData.csv','ProductNumber')
```

Read sales data from csv file and print out a line plot of a product's average sales.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber

#print the line plot
suPy.line plotAverageSalesPriceByMonth('salesData.csv','ProductNumber')
```

Read sales data from csv file and print out sales forecast for a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#length in month for the prediction: 12

#print the metrics and line plot
suPy.forecastQtyMonthlySales('SalesData.csv','ProductNumber',12)
```

Read sales data from csv file and print out pricing forecast for a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#length in month for the prediction: 12

#print the metrics and line plot
suPy.forecastMonthlyPrice('SalesData.csv','ProductNumber',12)
```

Read sales data from csv file and print out cost forecast for a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: ProductNumber
#length in month for the prediction: 12

#print the metrics and line plot
suPy.forecastMonthlyCost('SalesData.csv','ProductNumber',12)
```

## GusPI.finPy

```
from GusPI import finPy
```

Get public financial data with simfin - annual income statements.

```
#Example

#country: us

#get annual income statements and return a dataframe
finPy.get_annual_finData_income(country)
```

Get public financial data with simfin - annual balancesheet.

```
#Example

#country: us

#get annual balancesheet and return a dataframe
finPy.get_annual_finData_balance(country)
```

Get public financial data with simfin - annual cashflow statements.

```
#Example

#country: us

#get annual cashflow statements and return a dataframe
finPy.get_annual_finData_cashflow(country)
```

Get public financial data with simfin - annual cashflow statements.

```
#Example

#category: income, balancesheet, or cashflow
#symbol: 'MSFT', 'AAPL'...
#country: us

#get annual cashflow statements and return a dataframe
finPy.getannual_finData_by_symbol(category,symbol,country)
```

Read financial statements from csv files and provide a line chart for analysis.

```
#Example

#dataframe for statements
#category from the dataframe such as revenue

#print line plots
finPy.lineplot(dataframe, '3 year BalanceSheet Graph')
```

Read financial statements from csv files and provide multiple line charts for analysis.

```
#Example

#dataframe for statements

#print multiple line plots
finPy.multiLineplot(dataframe, '3 year BalanceSheet Graph')
```

Read financial statements from csv files and provide financial metrics for analysis.

```
#Example

#dataframe from a csv file: balance_sheet_yr.csv
#dataframe from a csv file: income_statement_3yr.csv

#print financial metrics
finPy.calculateMetrics(df_balancesheet,df_income)
```

Get financial statements for a list of company symbols and provide financial metrics for analysis.

```
#Example

#symbols = ['AAPL', 'MSFT', 'FIS']
#mass = calculate_ratio_mass(symbols)

#get financial matrics for multiple companies
finPy.calculate_ratio_mass(symbols)
```

Read financial statements from csv files and provide horizontal analysis for the last two periods.

```
#Example

#dataframe from a csv file: balance_sheet_yr.csv

#print financial metrics
finPy.horizontalAnalysisLastTwo(dataframe)
```

## GusPI.statsPy

```
#Example

#perform Benford's Law anamoly detection
#dataframe from a csv file: GLACCT_sample.csv

df = pd.read_csv("GLACCT_sample.csv")
# (dataframe,colname to perform detection,target_colname,target_value)
value_arr = statsPy.init_benfordlaw(df, 'TotalAmount', 'GLACCT', '11111')
result = statsPy.process_benfordlaw(value_arr, alpha=0.3)
statsPy.plot_benfordlaw(result)
```

## GusPI.scraper

The scrape package provides an easy way to scrape Yelp business info and Yelp reviews for a specific business.

```
from GusPI import scraper
```

YelpBizInfo
The function collects business info and save it into a csv file.

```
#Example

#declare a list: https://www.yelp.com/biz/`artisan-ramen-milwaukee`
CUISINES = ['artisan-ramen-milwaukee','red-light-ramen-milwaukee-5']

#scrape the business info
scraper.YelpBizInfo(CUISINES)
```

YelpReview
The function collects reviews for respective business and save them into separate files by business names.
```
#Example

#declare a list: https://www.yelp.com/biz/`artisan-ramen-milwaukee`
CUISINES = ['artisan-ramen-milwaukee','red-light-ramen-milwaukee-5']

#scrape the business info
scraper.YelpReview(CUISINES)
```
