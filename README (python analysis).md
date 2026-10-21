# Used-Car Price Prediction with Python and Streamlit

I started this project during my Postgraduate Diploma in Data Science and later extended it for my portfolio.

The aim was to estimate recorded car prices from vehicle details and compare how well different regression models performed. I explored and cleaned the data in Python, evaluated the selected model and added a Streamlit app that uses the saved model to produce an estimate.

The project combines data analysis, regression modelling and a simple prediction app. The portfolio version includes improvements made after the original coursework.

Related work: **[Power BI report and calculations](powerbi/POWER_BI_README.md)**.

## Project components

| Component | Purpose |
|---|---|
| Python notebook | Inspect and clean the data, explore patterns, prepare the inputs and compare models |
| Saved model | Keep the fitted preparation and model together so they can be used again |
| Streamlit app | Collect vehicle details and display an estimated price |

The target is `selling_price`. The dataset was supplied during my PGDip, but its original public source, currency and some units remain unconfirmed. All price results are therefore shown in **dataset currency units**.

## Main results

| Item | Result |
|---|---:|
| Original records | 15,411 |
| Records after cleaning | 15,244 |
| Records used for development | 12,163 |
| Records kept for testing | 3,081 |
| Selected model | Random Forest |
| Test MAE | 100,519 |
| Test RMSE | 221,824 |
| Test R² | 0.928 |
| Median absolute percentage error | 10.1% |
| Test predictions within 20% of recorded price | 80.0% |

MAE and RMSE describe prediction errors in dataset price units. **R² of 0.928 is not the same as 92.8% accuracy.**

## Questions explored

1. What does the vehicle dataset contain, and are there data-quality problems?
2. How do vehicle details relate to recorded prices?
3. Which of the tested models gives the lowest average prediction error?
4. Where does the selected model still make larger mistakes?

## Analysis and modelling approach

### 1. Data exploration

I checked the first and last rows, column names, data types, missing values, unique values and numerical ranges. I used histograms, box plots, category counts and a correlation matrix to explore the data.

These checks helped me understand what each field contained and identify possible problems before fitting a model.

### 2. Data cleaning

| Step | Why it was done |
|---|---|
| Removed the exported index column, `Unnamed: 0` | A row number should not be used to predict a car's price |
| Removed `car_name` | Brand and model are already available separately |
| Trimmed extra spaces from text | Avoid treating the same category as different values because of spacing |
| Changed `ISUZU` to `Isuzu` | Keep the brand spelling consistent |
| Checked numerical fields | Find values that cannot be read correctly |
| Marked invalid input values as missing | Avoid treating an invalid specification as a valid measurement |
| Changed two zero-seat values to missing | Zero was not accepted as a valid seating capacity |
| Removed 167 exact duplicate records | Avoid repeating identical records in the analysis |

This left **15,244 records**. Zero years and zero kilometres can be valid, so they were not automatically removed. No records were removed for invalid target prices in this dataset.

I also checked unusually large or small values. A box-plot outlier does not automatically mean the value is wrong. Positive extreme values were kept, although some, such as a very high recorded distance, still need checking against the original source.

### 3. Development and test split

The development data is used to fit models and compare settings. The test data is kept separate to check the selected model on records it was not fitted on.

Records with exactly the same input details are kept together during splitting. This reduces the chance of having the same input profile in both development and test data, even when their recorded prices differ.

The code uses `GroupShuffleSplit` for this. It produces an approximately 80/20 split, with a fixed random seed of 42 so the split can be repeated. This groups matching details; it does not prove that records describe different physical cars.

### 4. Input preparation

| Preparation | Purpose |
|---|---|
| Median imputation | Fill a missing numerical input with a middle value learned from the training data |
| Missing category label | Use `Unknown` when a category is missing |
| One-hot encoding | Turn text categories into columns the model can use without giving brands an artificial ranking |
| Standard scaling for Ridge | Put numerical inputs on a comparable scale for that model |
| Pipelines | Keep preparation and model fitting together, so the same steps can be reused |

The preparation is fitted inside the training folds during cross-validation. This means the test records are not used to calculate the imputation values or fit the other preparation steps.

The Decision Tree and Random Forest do not use standard scaling. Ridge also tries a log transformation of the target price; its predictions are converted back into ordinary price units before evaluation.

### 5. Model comparison

I compared a median-price baseline, Ridge, Decision Tree and Random Forest.

The baseline predicts the same development-set median price for every test car. It gives me a simple result to compare the other models against.

I used three-fold grouped cross-validation on the development data. This means fitting and checking the models on three different development-data divisions, while keeping matching input profiles together. Small sets of model settings were compared using `GridSearchCV`.

| Model | Average development cross-validation MAE |
|---|---:|
| Median-price baseline | 399,809 |
| Ridge | 115,728 |
| Decision Tree | 124,326 |
| Random Forest | 105,126 |

**Random Forest was selected because it had the lowest development cross-validation MAE among the settings tested.** The test scores were not used to choose the winner.

Ridge also compared using eight selected encoded inputs with using all encoded inputs. It performed better with all of them. The final Random Forest uses all 11 original input fields after preparation.

### 6. Evaluation and saved model

After selection, I compared the Random Forest's predictions with the recorded prices in the test data.

| Check | Purpose |
|---|---|
| MAE | The average size of the prediction mistakes, ignoring whether they are too high or too low |
| RMSE | Another error measure that gives larger mistakes more weight |
| R² | How the model's squared errors compare with using the evaluated records' average price as a reference |
| Percentage errors | How large a mistake is compared with that car's recorded price |
| Error checks by group | Whether some price or brand groups have larger mistakes |

The notebook also includes actual/predicted plots, a residual plot and a feature-shuffling check called permutation importance. That check helps explore which inputs the fitted model relies on; it does not prove that an input causes a price change.

The Random Forest's test MAE was about **75.1% lower than the median-price baseline's test MAE**. Individual errors were also checked because a single average can hide large mistakes.

I saved the fitted preprocessing and model together in `car_price_pipeline.joblib` for use by the app.

## Streamlit application

The app collects the vehicle's brand, model, age, recorded distance, fuel economy, engine size, power, seats, seller type, fuel type and transmission. Brand and model are linked in the menus, while the remaining details are supplied separately.

Input checks reject invalid values before prediction. The app then passes the details through the saved preprocessing and model and displays the estimated price. It also provides the model's evaluation results and notes about its limitations. Predictions are generated from the fitted model; the app does not retrain it.

Using the saved pipeline keeps the app's encoding and missing-value handling consistent with the modelling work. The app was deployed on Streamlit and tested with a vehicle-price prediction.

Selecting a brand and model does not identify a specific variant or automatically set its other specifications. An unrealistic combination of inputs can therefore produce an unreliable estimate.

## Findings

- Random Forest had the lowest development cross-validation MAE among the tested settings.
- Its test MAE was approximately 75.1% lower than the median-price baseline's test MAE.
- Around 80% of test predictions were within 20% of their recorded price, but some individual errors were much larger.
- Higher-priced vehicles had larger absolute errors on average. Percentage errors helped me compare mistakes across different price levels.

## Limitations

- The dataset's original source, licence, dates, currency and some units are still unconfirmed.
- Important details such as condition, location and service history are missing.
- Some brands and models have few examples, so their results need care.
- Unusually large values still need checking against the source.
- The model has not been tested on current South African vehicle data or on a later time period.
- Training error was lower than test error. Development cross-validation R² was about 0.845, compared with about 0.928 on the test set. Reporting both provides a fuller view of performance than the higher test score alone.
- The test set has already been inspected for errors. A fresh independent dataset would be needed to make a new final-performance claim after further model changes.
- Choosing a brand and model in the app does not automatically fill that exact vehicle's specifications. Unrealistic combinations may produce unreliable estimates.

These results describe an academic dataset and do not establish performance as a commercial car-valuation service.

## Main files

| File | Purpose |
|---|---|
| `car_price_project.ipynb` | The analysis, modelling steps and saved results |
| `app.py` | The Streamlit application |
| `car_price_pipeline.joblib` | The fitted preparation, model and supporting app information |
| `requirements.txt` | Python packages and versions used by the project |
| `car_price_dataset.csv` | Original coursework data used for analysis and training |
| `README.md` | This explanation of the notebook and app |
| `powerbi/POWER_BI_README.md` | Separate explanation of the Power BI report |

The dataset's redistribution terms remain unconfirmed, so the file list describes the project's working files rather than a promise that all data is publicly available.

## Tools and methods used

| Tool or method | Application in the project |
|---|---|
| pandas and NumPy | Data inspection, cleaning and calculations |
| Matplotlib | Distribution, relationship and prediction-error plots |
| scikit-learn | Preprocessing, grouped splitting, cross-validation, model fitting and evaluation |
| joblib | Saving and loading the fitted pipeline and app information |
| Streamlit | Browser interface for entering vehicle details and displaying estimates |

## About the work

**Cameron James Naidoo — PGDip in Data Science coursework extended for my portfolio.**

The project began with my coursework notebook and was later extended with a Streamlit app and the linked Power BI report.

## References

These explain the tools used; they are not sources for the dataset.

- [scikit-learn: grouped splitting](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html)
- [scikit-learn: avoiding data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)
