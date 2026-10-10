# Used Car Price Prediction

An academic regression project based on Cameron's PGDip coursework, revised with AI assistance. The notebook contains all analysis and training; app.py runs the Streamlit interface. The saved pipeline contains fitted preprocessing and the model. This is a historical dataset demonstration, not a current South African valuation service.

## Seven files only

| File | Purpose |
|---|---|
| car_price_project.ipynb | Complete notebook, explanations and saved real outputs |
| app.py | Standalone Streamlit application |
| car_price_pipeline.joblib | Trained pipeline, metadata and model-comparison results |
| car_price_dataset.csv | Original dataset for running the notebook locally |
| requirements.txt | Packages for the notebook and app |
| README.md | These instructions |
| .gitignore | Git exclusions for local data, environments and secrets |

## First: open the project
Extract the ZIP into Documents. In VS Code, use File > Open Folder and select the extracted car-price-graduate folder containing app.py. Keep it separate from your banking project and old coursework.

In **VS Code > Terminal > PowerShell**, run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The first command creates an isolated environment. The second installs the pinned packages into it. These commands avoid activation-policy changes. Python 3.12 was used for verification; Windows installation still needs checking on your computer.

## See the app
In the same **VS Code PowerShell terminal**, run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL it prints. Enter a realistic vehicle configuration and choose Estimate price. The trained pipeline is already included; you do not need to retrain first. Keep the terminal running; Ctrl+C stops the app.

## Read or rerun the notebook
Open car_price_project.ipynb in **VS Code's notebook editor**. Select the .venv interpreter as its kernel. Read the saved outputs first; no execution is needed just to view them. When you want to run it, start at the top and execute each cell in order. Run All performs full training and overwrites car_price_pipeline.joblib at the end. There is no training switch or large custom training function. Each model has its own visible section. Pipelines are retained to fit preprocessing within each fold and reuse it in the app. Training uses one worker and small grids; your computer may take several minutes.

Training results, cleaning, feature selection, error analysis and limitations are shown in the notebook. Source data remains unchanged. Restart the app after retraining. Load only trusted model artifacts and keep the pinned scikit-learn version.

## Results and limits
The verified random forest has holdout MAE 100,519; RMSE 221,824; R² 0.9283. Approximately 49.89% of predictions fall within 10% of recorded price and 80.01% within 20%. Currency is unconfirmed; these are dataset price units, not rand. R² is not percentage accuracy. The model was selected by development CV MAE, not holdout performance. Identical input profiles stay together across splits. The supplied pipeline is not refitted on the holdout.

Dataset source, licence, collection dates and fuel-economy/engine/power units still need confirmation. Extreme distances remain flagged. There is no condition, location or service-history information. This demonstrates a working regression workflow; it does not establish reliable commercial valuations. The separate formal report, slides and recording from your marking guide are not included.

## Start GitHub from scratch
**In your browser**, visit https://github.com/new. Create a new repository named car-price-portfolio. Choose Private initially while data attribution/licence is unconfirmed. Leave the optional README, .gitignore and licence unchecked: these files already exist locally. Do not delete your old repository.

In **VS Code > Terminal > PowerShell**, from this extracted project folder:

```powershell
git init
git branch -M main
git add .
git status --short
```

These create local history, name the branch and stage files. Check the listed files. The raw CSV, virtual environment and secrets are excluded. The notebook has example data in its outputs; use private visibility until sharing rights are confirmed. The saved pipeline is deliberately included because the app needs it.

```powershell
git commit -m "Add car price prediction notebook and Streamlit app"
git remote add origin https://github.com/YOUR-USERNAME/car-price-portfolio.git
git push -u origin main
```

Replace YOUR-USERNAME with your actual GitHub username, or use the exact new repository URL. Commit records your version locally; remote links it to GitHub; push uploads it. If Git requests author details, set your own user.name and user.email for this repository. Complete the sign-in prompt if needed. Do not upload the ZIP as the app source.

To host, visit https://share.streamlit.io in your browser. Create an app from the new repository, branch main, entrypoint app.py; select Python 3.12 in Advanced settings. Test the deployed app before sharing its URL. GitHub stores the files; Streamlit runs the application. No repository or hosted app has been created by this download.

## Coding style
The notebook uses direct pandas commands, named variables and short loops, with no custom function definitions or custom classes. It has more small cells so you can inspect each stage. A PGDip graduate should be able to explain the cleaning rules, grouped split, pipelines, model tuning and evaluation; you do not need to present this as production engineering.

## Verification
All 44 short code cells ran successfully from beginning to end, including model fitting. The selected model reproduced the reviewed version's 3,081 holdout predictions. The standalone Streamlit app produced a price and displayed its evaluation panel. Saved outputs are included. Windows installation and public hosting remain unverified.
