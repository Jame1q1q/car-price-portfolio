# Used-Car Data and Model Results in Power BI

I added this report to my PGDip car-price project to explore the vehicle data and present the model's results in Power BI. It compares recorded prices across vehicle groups and shows where the selected model makes larger mistakes.

The data comes from the Python project: cleaned vehicle records and saved test predictions.

Related work: **[Python analysis and Streamlit app](../README.md)**. The sections below explain the report pages, data fields and calculations.

## What the report uses

| Item | Detail |
|---|---|
| Data source for the report | `Car_PowerBI_Data.csv`, prepared from the Python project |
| Main table | `Vehicles` |
| Cleaned records | 15,244 |
| Test records with predictions | 3,081 |
| Development records without exported predictions | 12,163 |
| Model supplying the predictions | Random Forest selected in the Python project |

Power BI reads the saved predictions rather than training the model. Only Test records have exported predictions, so the performance page uses those records.

The dataset was supplied during my PGDip. Its public source, currency and some units remain unconfirmed; recorded prices are shown in **dataset currency units**.

## Overall report results

| Measure | Result with slicers cleared |
|---|---:|
| Vehicle records | 15,244 |
| Median recorded price | 559,000 |
| Test records | 3,081 |
| Test MAE | 100,519 |
| Test RMSE | 221,824 |
| Test R² | 0.928 |
| Predictions within 20% | 80.0% |
| Median absolute percentage error | 10.1% |

These figures match the saved Python test results and the imported report data. Filtered selections may show different results. R² is not percentage accuracy.

## Report pages and visual choices

The report covers **both the dataset and the model's performance**. Only the Model Reliability page evaluates predictions.

### Page 1: Vehicle Overview

| Visual | Purpose |
|---|---|
| Brand, Model, Fuel Type and Transmission slicers | Filter the records used by the page's summaries and comparisons |
| Vehicle records card | Show how many records are included in the selection |
| Median recorded price card | Show the middle recorded price |
| Median age card | Show the middle vehicle age |
| Median distance card | Show the middle recorded distance |
| Top 10 brand chart | Show the most represented brands in the selected data |
| Brand/model and transmission matrix | Compare record counts and median prices, with a hierarchy from brand to model |

The matrix works like a pivot-style table. These counts describe the dataset, not real-world market share or confirmed sales.

### Page 2: Price Comparisons

| Visual | Purpose |
|---|---|
| Four slicers | Narrow the comparison to the selected vehicles |
| Record count and median price cards | Give context to the selection |
| Median price by age band | Compare recorded prices across age groups |
| Median price by distance band | Compare recorded prices across distance groups |
| Age and fuel matrix | Compare two groupings together, with prices and supporting record counts |

The matrix shading highlights differences in median price. A darker cell does not mean better model performance. These are comparisons between different vehicles, not a measurement of the same car losing value over time.

### Page 3: Model Reliability

| Visual | Purpose |
|---|---|
| Four slicers | Look at test results for a selected group |
| Test record count | Show how many predictions support the results |
| MAE, RMSE and R² cards | Summarise the model's performance |
| Within 20% card | Show the percentage of test predictions inside this chosen tolerance |
| Median absolute percentage error card | Show the middle percentage error |
| Sample note | Flag selections with few or no test records |
| Actual/predicted scatter plot | Look at individual predictions and their mistakes |
| MAE by price group | Compare absolute errors across actual-price ranges |
| Error table | Inspect the individual records with the largest errors |

The page is filtered to **Test** records. Changing a slicer recalculates the summaries from saved predictions; it does not retrain the model.

### Page 4: Brand Detail

| Visual | Purpose |
|---|---|
| Brand title | Show the brand selected through drill-through |
| Record count, median price and median age cards | Summarise that brand's records |
| Model table | Compare model counts, shares, median prices and distances |
| Model-price chart | Compare median prices for the ten most represented models |
| Back button | Return to the previous page |

Brand drill-through passes the selected brand into this detail page. It shows that brand across the cleaned dataset. I kept the destination focused on the brand rather than carrying over the previous page's fuel, transmission or Test-only filters.

Page navigation connects the main views, while reset bookmarks restore each main page's default selection. The three main pages have separate filter selections.

## Data structure and calculations

The report uses one table called `Vehicles`. All its fields describe the same record-level dataset, so this version does not need relationships between separate tables.

| Term | Meaning in this project |
|---|---|
| Imported column | A field brought in from the prepared CSV, such as brand or price |
| Power Query custom column | A field created before loading the data, such as an age band |
| DAX calculated column | A calculation for each row, such as that row's prediction error |
| DAX measure | A summary that changes with filters, such as average test error |

For example, a car record's absolute error stays the same when a filter changes. The average error can change because a different group of records is being averaged.

I used **DAX calculated columns** to calculate errors for individual records and **DAX measures** to summarise the selected records. The formulas below document those calculations and their purposes.

<details>
<summary><strong>Column guide: what each field is for</strong></summary>

### The 12 original fields kept for analysis

| Field | Meaning and use |
|---|---|
| `brand` | Brand; a model input and report grouping |
| `model` | Model name; a model input and within-brand comparison |
| `vehicle_age` | Age in years; a model input and age grouping |
| `km_driven` | Distance in kilometres; a model input and distance grouping |
| `seller_type` | Seller category; a model input |
| `fuel_type` | Fuel category; a model input and report filter |
| `transmission_type` | Transmission category; a model input and report filter |
| `mileage` | Fuel economy, not distance driven; its original unit still needs confirmation |
| `engine` | Engine-size specification; its original unit still needs confirmation |
| `max_power` | Power specification; its original unit still needs confirmation |
| `seats` | Number of seats; a model input |
| `selling_price` | Recorded price; the value the model tries to predict |

The first 11 fields are the model inputs. `selling_price` is the target, so it is not given to the model as an input when making a prediction.

### Three fields added to the reporting export

| Field | Why it is included |
|---|---|
| `Record_ID` | A unique key for each exported record, used to keep scatter points and table rows separate |
| `Split` | Shows whether the record belongs to Development or Test |
| `predicted_price` | Holds the selected model's predictions for the test records |

There are intentionally **no exported predictions for the 12,163 development records**. A blank prediction does not mean zero or a correct prediction. It means that record is not part of the report's test evaluation.

`Record_ID` identifies a dataset row, not a verified unique physical car. These three reporting fields are not model inputs.

### Five Power Query fields

| Field | Why it is included |
|---|---|
| `Age Band — Text` | Put ages into readable groups |
| `Age Sort — Whole Number` | Put those age groups in the correct order |
| `Distance Band — Text` | Put distances into readable groups |
| `Distance Sort — Whole Number` | Put those distance groups in the correct order |
| `Price Band — Text` | Compare errors for lower- and higher-priced records |

The two sort fields use codes 1–4, with 5 for Unknown. The helpers are stored as single-digit text codes in the current file, despite the type hints in their names. Their values preserve the intended band order.

### Four DAX error columns

| Field | Why it is included |
|---|---|
| `Prediction Error` | Show whether a prediction is too high or too low, and by how much |
| `Absolute Error` | Show the size of the mistake without its sign |
| `Squared Error` | Support the RMSE and R² calculations |
| `Absolute Percentage Error` | Express the mistake relative to the actual price |

This gives the report **24 columns**. The reporting bands and error columns are not fed back into model training.

</details>

## Power Query: grouping the records

Power Query reads the prepared `Car_PowerBI_Data.csv`, promotes the header row, converts fields to suitable types and adds the groups below. The earlier duplicate removal and main cleaning were done in Python.

I used `en-US` locale conversions for several decimal fields so decimal points were read correctly. The saved query also removes `.0` text from age, distance and seats before converting them to whole numbers. This step was specific to the supplied export; it is not a general numeric-cleaning rule.

<details>
<summary><strong>The five custom-column formulas and why I used them</strong></summary>

I created the following custom columns in Power Query using M expressions. They group individual values into readable categories and provide sort codes for the charts and matrices.

### Age Band — Text

```powerquery
if [vehicle_age] = null then "Unknown"
else if [vehicle_age] <= 3 then "0–3 years"
else if [vehicle_age] <= 7 then "4–7 years"
else if [vehicle_age] <= 12 then "8–12 years"
else "13+ years"
```

This groups ages into 0–3, 4–7, 8–12 and 13+ years. It makes the price comparison easier to read. An age of 6 goes into 4–7 years.

### Age Sort — Whole Number

```powerquery
if [vehicle_age] = null then 5
else if [vehicle_age] <= 3 then 1
else if [vehicle_age] <= 7 then 2
else if [vehicle_age] <= 12 then 3
else 4
```

This gives each age group an order code. It stops the text labels being shown in an unwanted alphabetical order. Unknown goes last.

### Distance Band — Text

```powerquery
if [km_driven] = null then "Unknown"
else if [km_driven] < 50000 then "Under 50,000 km"
else if [km_driven] < 100000 then "50,000–99,999 km"
else if [km_driven] < 150000 then "100,000–149,999 km"
else "150,000+ km"
```

This groups distances into four ranges. For example, 75,000 km goes into 50,000–99,999 km. Exactly 100,000 km goes into the next range.

### Distance Sort — Whole Number

```powerquery
if [km_driven] = null then 5
else if [km_driven] < 50000 then 1
else if [km_driven] < 100000 then 2
else if [km_driven] < 150000 then 3
else 4
```

This puts the distance bands in order from lowest to highest. It is used for sorting, not as an extra model input.

### Price Band — Text

```powerquery
if [selling_price] <= 380000 then "1. Lower recorded prices"
else if [selling_price] <= 555000 then "2. Lower-middle prices"
else if [selling_price] <= 825000 then "3. Upper-middle prices"
else "4. Higher recorded prices"
```

This groups actual prices for checking model errors. The cutoffs came from the development data: its lower quarter, middle and upper-quarter prices were 380,000, 555,000 and 825,000. The bands stay fixed when report filters change. They are not model inputs, because the price is what we are trying to predict.

</details>

## DAX calculated columns: work out each record's error

<details>
<summary><strong>The four formulas, explained with a simple example</strong></summary>

I created four DAX calculated columns to compare each Test record's predicted price with its actual recorded price. These row-level errors support the summary measures and error-investigation table.

### Prediction Error

```dax
Prediction Error =
IF(
    Vehicles[Split] = "Test"
        && NOT ISBLANK(Vehicles[predicted_price]),
    Vehicles[predicted_price] - Vehicles[selling_price],
    BLANK()
)
```

I subtract the actual price from the predicted price. A positive answer means the model predicted too high; a negative answer means it predicted too low. The calculation only runs for Test rows that have a prediction. Other rows stay blank. In the formula, `&&` means both conditions must be true.

### Absolute Error

```dax
Absolute Error =
IF(
    ISBLANK(Vehicles[Prediction Error]),
    BLANK(),
    ABS(Vehicles[Prediction Error])
)
```

`ABS` removes the plus or minus sign. A mistake of +50,000 and a mistake of −50,000 both become 50,000. This lets me measure the size of errors without high and low predictions cancelling each other out. Blank errors remain blank.

### Squared Error

```dax
Squared Error =
IF(
    ISBLANK(Vehicles[Prediction Error]),
    BLANK(),
    Vehicles[Prediction Error] ^ 2
)
```

This multiplies the error by itself. For example, an error of 50,000 gives a squared error of 2,500,000,000. It is used in RMSE and R², not shown as an ordinary price amount.

### Absolute Percentage Error

```dax
Absolute Percentage Error =
IF(
    ISBLANK(Vehicles[Prediction Error]),
    BLANK(),
    DIVIDE(Vehicles[Absolute Error], Vehicles[selling_price])
)
```

This divides the absolute error by the actual price. An error of 50,000 on an actual price of 500,000 gives 0.10, displayed as 10.0%. The stored fraction is displayed using percentage formatting. `DIVIDE` also handles division by zero safely; the actual prices in this dataset are positive.

**Illustrative example of the error calculations:**

| Actual price | Predicted price | Prediction error | Absolute error | Absolute percentage error |
|---|---|---|---|---|
| 500,000 | 550,000 | +50,000 | 50,000 | 10.0% |
| 500,000 | 450,000 | −50,000 | 50,000 | 10.0% |

</details>

## DAX measures: summarise the selected records

<details>
<summary><strong>All 15 measures, with their formulas and purposes</strong></summary>

The 15 measures cover record counts, price summaries, prediction errors and report text. They respond to the current selection, such as a brand or price band.

### 1. Vehicle Records

```dax
Vehicle Records =
COUNTROWS(Vehicles)
```

I used this measure in the summary cards and comparison tables to show how many records support each result. With no filters it returns **15,244**.

### 2. Median Price

```dax
Median Price =
MEDIAN(Vehicles[selling_price])
```

This returns the middle recorded price. I use it because a few very expensive cars can pull the average upwards. With no filters it is **559,000**. A matrix total calculates the median for all records in that total; it does not add up the group medians.

### 3. Average Price

```dax
Average Price =
AVERAGE(Vehicles[selling_price])
```

I included the average in a tooltip alongside the median. Comparing the two helps show the effect of unusually expensive records on the average price.

### 4. Median Age

```dax
Median Age =
MEDIAN(Vehicles[vehicle_age])
```

The median-age card describes the selected vehicles in years, with one decimal place. It gives context to their recorded prices.

### 5. Median Distance

```dax
Median Distance =
MEDIAN(Vehicles[km_driven])
```

The median-distance card summarises recorded usage in kilometres. I used the median to reduce the effect of extreme distance values on the summary.

### 6. Share of Selected Records

```dax
Share of Selected Records =
DIVIDE(
    [Vehicle Records],
    CALCULATE(
        [Vehicle Records],
        ALLSELECTED(Vehicles[brand], Vehicles[model])
    )
)
```

This shows how much of the selected total belongs to each row in the Brand Detail model table. If a brand has 100 records and a model has 25, the model has a 25% share. `CALCULATE` changes which filters apply to the denominator. `ALLSELECTED` removes the current brand/model row grouping while keeping outside selections, so the denominator represents the selected total. `DIVIDE` performs the division safely. This is a share of dataset records, not market share.

### 7. Test Records

```dax
Test Records =
CALCULATE(
    COUNT(Vehicles[predicted_price]),
    Vehicles[Split] = "Test"
)
```

This shows the number of test predictions behind the performance results: **3,081** with slicers cleared. `CALCULATE` applies the Test condition while keeping other filters, such as brand. Blank development predictions are excluded.

### 8. Test MAE

```dax
Test MAE =
CALCULATE(
    AVERAGE(Vehicles[Absolute Error]),
    Vehicles[Split] = "Test"
)
```

MAE shows the average size of the test prediction errors: about **100,519 dataset price units** overall. I used it as an easily interpretable error summary and in the price-group comparison. Individual errors can be much smaller or larger.

### 9. Test RMSE

```dax
Test RMSE =
VAR MeanSquaredError =
    CALCULATE(
        AVERAGE(Vehicles[Squared Error]),
        Vehicles[Split] = "Test"
    )
RETURN
    IF(ISBLANK(MeanSquaredError), BLANK(), SQRT(MeanSquaredError))
```

This first averages the squared errors, then uses `SQRT` to take the square root. This puts the answer back into price units. `VAR` gives the intermediate result a name, and `RETURN` gives the final answer. The overall result is about **221,824**. RMSE is more affected by large mistakes than MAE.

### 10. Test R2

```dax
Test R2 =
VAR TestRows =
    FILTER(
        Vehicles,
        Vehicles[Split] = "Test"
            && NOT ISBLANK(Vehicles[predicted_price])
    )
VAR MeanActual = AVERAGEX(TestRows, Vehicles[selling_price])
VAR SSE = SUMX(TestRows, Vehicles[Squared Error])
VAR SST =
    SUMX(TestRows, (Vehicles[selling_price] - MeanActual) ^ 2)
RETURN
    IF(COUNTROWS(TestRows) < 2 || SST = 0, BLANK(), 1 - DIVIDE(SSE, SST))
```

This calculates R² for the selected Test records. `SSE` adds up the model’s squared errors. `SST` adds up how far the actual prices are from their own average, squared. The last step is `1 − SSE/SST`. `AVERAGEX` and `SUMX` work through the selected rows to calculate those values. The result is blank if there are fewer than two rows or no variation in actual prices. The overall result is **0.928** when displayed to three decimals. R² can be negative; it is a measure of fit rather than percentage accuracy.

### 11. Within 20 Percent

```dax
Within 20 Percent =
VAR Eligible =
    FILTER(
        Vehicles,
        Vehicles[Split] = "Test"
            && NOT ISBLANK(Vehicles[predicted_price])
    )
VAR WithinTolerance =
    FILTER(Eligible, Vehicles[Absolute Percentage Error] <= 0.20)
RETURN
    DIVIDE(COUNTROWS(WithinTolerance), COUNTROWS(Eligible))
```

This counts how many eligible Test predictions have an absolute percentage error of 20% or less, then divides by the eligible Test count. For an actual price of 500,000, predictions from 400,000 to 600,000 fall within this range. The overall result is **80.0%**. This is a chosen reporting threshold, not a promise that a new prediction will meet it. Percentage formatting displays the resulting fraction as a percentage.

### 12. Median Test Percentage Error

```dax
Median Test Percentage Error =
CALCULATE(
    MEDIAN(Vehicles[Absolute Percentage Error]),
    Vehicles[Split] = "Test"
)
```

I used the median absolute percentage error to summarise a typical relative error without giving the largest percentage errors as much influence as a mean would. It is displayed as **Median absolute % error**, with an overall result of **10.1%**.

### 13. Mean Prediction Bias

```dax
Mean Prediction Bias =
CALCULATE(
    AVERAGE(Vehicles[Prediction Error]),
    Vehicles[Split] = "Test"
)
```

This averages the signed errors. A positive result means prices are too high on average; a negative result means they are too low on average. The overall result is about **−4,368** price units. High and low errors can cancel, so this is an extra check rather than a replacement for MAE. The measure is available in the model but is not one of the six main performance cards.

### 14. Test Sample Note

```dax
Test Sample Note =
SWITCH(
    TRUE(),
    ISBLANK([Test Records]) || [Test Records] = 0, "No test records in this selection",
    [Test Records] < 30, "Small test group: interpret cautiously",
    "Test results describe this selection; they are not a guarantee for a new car"
)
```

This changes a text message according to the number of Test records selected. `SWITCH(TRUE(), ...)` checks each condition in order and returns the first matching message. It warns when there are fewer than 30 records. Thirty is only a simple warning rule; it is not proof that larger groups are reliable.

### 15. Brand Detail Title

```dax
Brand Detail Title =
"Brand detail: " & SELECTEDVALUE(Vehicles[brand], "Select a brand")
```

This puts the selected brand into the title. `SELECTEDVALUE` returns the brand when exactly one is selected; otherwise it returns “Select a brand”. `&` joins the two pieces of text. For example, the title can show **Brand detail: Hyundai**.

</details>

## Scatter plot: actual versus predicted price

The scatter plot shows individual Test predictions, with actual recorded price on the X-axis and predicted price on the Y-axis. It helps identify large mistakes and patterns of overprediction or underprediction that the summary cards alone would not show.

`Record_ID` defines one point per record. The price axes and numerical error tooltips use Average, which returns that record's value because each ID identifies one row. This prevents unrelated records being combined into a single point.

For example, a point at X = 2 million and Y = 3 million represents an overprediction of 1 million. Exact predictions satisfy `predicted = actual`. The notebook includes this equality line; the current Power BI scatter does not draw it. Axis abbreviations such as M indicate millions, not currency.

Records can overlap at the same coordinates, so the Test Records card provides the evaluated sample size. The plot is interpreted alongside the MAE-by-price-group chart and individual error table.

## Findings

- Maruti, Hyundai and Honda have the most records in this dataset.
- Random Forest performed best by development cross-validation MAE among the tested settings.
- About 80% of the Test predictions were within 20% of the recorded price.
- The highest-price group had larger average errors in price units. However, its median percentage error was lower than the lowest-price group's, showing why both types of error are useful.

| Actual-price group | Test records | Average absolute error | Median absolute percentage error |
|---|---:|---:|---:|
| Up to 380,000 | 746 | 44,368 | 13.34% |
| Above 380,000 to 555,000 | 776 | 56,832 | 9.42% |
| Above 555,000 to 825,000 | 823 | 72,070 | 9.01% |
| Above 825,000 | 736 | 235,306 | 9.51% |

These findings describe the full saved data or Test selection. Filtering the report can change the results. The notebook's price-group table uses **mean** percentage error, while this table uses **median** percentage error, matching the Power BI measure.

## Report files

| File | Purpose |
|---|---|
| `POWER_BI_README.md` | This explanation of the report and its calculations |
| `Car_PowerBI_Data.csv` | Cleaned records, split labels and saved Test predictions used for refresh |
| `Car_Price_Analysis_Repaired.pbix` | The saved Power BI report, including imported data, calculations and visuals |

The report stores the imported dataset and calculated fields in the PBIX. Its refresh query reads `Car_PowerBI_Data.csv` from a local file location. The prepared export includes Development/Test labels and predictions only for Test rows; the underlying Python workflow is documented in the linked project README.

The original dataset's redistribution terms remain unconfirmed. The PBIX includes imported data as well as the visuals.

## Limitations

- The source, licence, currency, dates and some measurement units are unconfirmed.
- Dataset counts are not market share or confirmed sales.
- Age-group comparisons describe different vehicles; they do not track the same car's depreciation over time.
- A result based on a small group is weaker evidence than one supported by many records.
- Error measures describe the supplied Test predictions, not a promise about a new vehicle.
- The report does not establish current South African car values.
- The two sort-helper columns are stored as text despite their names; their single-digit codes preserve the intended order in the current report.

## Skills applied

- Loading and preparing a CSV in Power Query.
- Creating useful grouping and sorting columns.
- Understanding the difference between calculated columns and measures.
- Writing DAX for summaries and prediction-error checks.
- Building pivot-style matrices, cards, charts and slicers.
- Adding drill-through, navigation and reset actions.
- Explaining what a visual shows and what it cannot prove.

## About the work

**Cameron James Naidoo — Power BI extension of my PGDip car-price project.**

This report forms the Power BI part of my car-price portfolio project. The Python analysis and Streamlit app are documented separately in the linked README.

## References

These explain Power BI features and functions; they are not sources for the vehicle dataset.

- [Microsoft: columns and measures](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-calculations-options)
- [Microsoft: ALLSELECTED](https://learn.microsoft.com/en-us/dax/allselected-function-dax)
- [Microsoft: scatter charts](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-scatter)
- [Microsoft: drill-through](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough)
