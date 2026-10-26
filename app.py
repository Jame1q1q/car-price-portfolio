"""Streamlit interface: python -m streamlit run app.py"""
import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st
NUMERIC = ['vehicle_age', 'km_driven', 'mileage', 'engine', 'max_power', 'seats']
CATEGORICAL = ['brand', 'model', 'seller_type', 'fuel_type', 'transmission_type']
FEATURES = NUMERIC + CATEGORICAL
TARGET = 'selling_price'
ROOT = Path(__file__).resolve().parent
SEED = 42


def validate_input(frame):
    """Reject malformed app inputs before calling the model."""
    if list(frame.columns) != FEATURES:
        raise ValueError('Input columns must match the documented feature contract.')
    frame = frame.copy()
    for col in NUMERIC:
        values = pd.to_numeric(frame[col], errors='coerce')
        frame[col] = values
        if (~np.isfinite(values)).any() or (values < 0).any():
            raise ValueError(f'{col} must be a finite, nonnegative number.')
        if col in ['mileage', 'engine', 'max_power', 'seats'] and values.le(0).any():
            raise ValueError(f'{col} must be greater than zero.')
        if col in ['vehicle_age', 'seats'] and values.mod(1).ne(0).any():
            raise ValueError(f'{col} must be a whole number.')
    for col in CATEGORICAL:
        frame[col] = frame[col].astype('string').str.strip().replace('', pd.NA)
    frame['brand'] = frame['brand'].replace({'ISUZU': 'Isuzu'})
    if frame[CATEGORICAL].isna().any().any():
        raise ValueError('Choose a value for each category.')
    return frame


st.set_page_config(page_title='Used Car Price Explorer', page_icon='🚗', layout='centered')
st.title('Used Car Price Explorer')
st.write('Explore how recorded vehicle details relate to prices in this academic dataset.')

# Fixed, locally trained artifact only. Never accept uploaded pickle/joblib files.
model_path = Path(os.environ.get('CAR_PRICE_MODEL', ROOT / 'car_price_pipeline.joblib'))

@st.cache_resource
def load_bundle(path, modified_time):
    return joblib.load(path)

if not model_path.exists():
    st.info('The model has not been trained yet. Open car_price_project.ipynb and run its cells in order through the saving section.')
    st.stop()

try:
    bundle = load_bundle(str(model_path), model_path.stat().st_mtime_ns)
    model, meta = bundle['pipeline'], bundle['metadata']
except Exception:
    st.error('The saved model could not be loaded. Retrain it using this project environment.')
    st.stop()

if meta['quick_software_test']:
    st.warning('Software-test model only — predictions and scores are not portfolio results.')
st.caption("Currency: Rupee ₹")

# Outside the form so the model choices refresh immediately when brand changes.
brands = sorted(b for b, models in meta['brand_models'].items() if models)
brand = st.selectbox('Brand', brands)
vehicle_model = st.selectbox('Model', meta['brand_models'][brand])
labels = {'vehicle_age': 'Vehicle age (years)', 'km_driven': 'Distance driven (km)',
          'mileage': 'Fuel economy (original dataset units)',
          'engine': 'Engine size (original dataset units)',
          'max_power': 'Maximum power (original dataset units)', 'seats': 'Seats'}

with st.form('vehicle_details'):
    left, right = st.columns(2)
    values = {'brand': brand, 'model': vehicle_model}
    for i, col in enumerate(NUMERIC):
        median = meta['numeric_ranges'][col]['median']
        container = left if i % 2 == 0 else right
        with container:
            if col in ['vehicle_age', 'km_driven', 'seats']:
                values[col] = st.number_input(labels[col], min_value=1 if col == 'seats' else 0,
                    value=max(1 if col == 'seats' else 0, int(round(median))), step=1)
            else:
                values[col] = st.number_input(labels[col], min_value=0.01, value=max(0.01, float(median)))
    for col, label in [('seller_type', 'Seller type'), ('fuel_type', 'Fuel type'),
                       ('transmission_type', 'Transmission')]:
        values[col] = st.selectbox(label, meta['categories'][col])
    submitted = st.form_submit_button('Estimate price', type='primary')

if submitted:
    try:
        frame = validate_input(pd.DataFrame([values], columns=FEATURES))
        outside = [c for c in NUMERIC if not meta['numeric_ranges'][c]['min'] <= values[c] <= meta['numeric_ranges'][c]['max']]
        if outside:
            st.warning('Outside the training range: ' + ', '.join(outside) + '. This estimate may be unreliable.')
        prediction = float(model.predict(frame)[0])
        if not np.isfinite(prediction) or prediction <= 0:
            st.error('The model produced an invalid price for these inputs. Try a realistic vehicle configuration.')
        else:
            st.metric('Estimated price', f'{prediction:,.0f}', help=meta['currency'])
            st.caption('A point estimate, not a guaranteed sale price or a confidence interval.')
    except ValueError as exc:
        st.error(str(exc))

with st.expander('Model performance and limitations'):
    metrics = meta['evaluation']['holdout']
    st.write(f"Selected model: {meta['evaluation']['selected_model']}")
    st.write(f"Holdout MAE: {metrics['MAE']:,.0f} · RMSE: {metrics['RMSE']:,.0f} · R²: {metrics['R2']:.3f}")
    st.caption('MAE and RMSE use the dataset price units. R² is not percentage accuracy.')
    if 'median_APE_pct' in metrics:
        st.write(f"Median percentage error: {metrics['median_APE_pct']:.1f}% · "
                 f"Within 10% of recorded price: {metrics['within_10pct']:.1f}% · "
                 f"Within 20%: {metrics['within_20pct']:.1f}%")
        st.caption('These are observed test-set results, not a guarantee for this vehicle. '
                   'About half of test estimates differed from the recorded price by more than 10%.')
    st.write('Selection used cross-validation on development data. Identical input rows were kept together. '
             'Rare cars and unusual combinations '
             'may have large errors.')
    st.write('Source: Vehicle-dataset-from-cardekho'])
