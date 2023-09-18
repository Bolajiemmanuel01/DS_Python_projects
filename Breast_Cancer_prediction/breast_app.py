import streamlit as st
import pandas as pd
import json
import requests
from PIL import Image
import joblib
from streamlit_lottie import st_lottie

image = Image.open(r"Images/breast_ribbon.jpg")


@st.cache_resource
def load_resources():
    model = joblib.load(r'Datasets and Models/classifier.pkl')
    scaler = joblib.load(r'Datasets and Models/scaler.pkl')
    return model, scaler


@st.cache_resource
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def scale_data(data, scaler):
    scaled_data = scaler.transform(data)
    return scaled_data


def predict_cancer(data, model):
    predictions = model.predict(data)
    return predictions


def display_results(predictions):
    if predictions == 'M':
        st.success("The tumor cell seems to be malignant and the patient needs to be treated as soon as possible.")
        st.warning(
            "Be cautious as this is just a predictive model and dosen't always reflect the ground scenario, although the model has high accuracy. Please consult a specialized doctor for futher evaluation.")
    else:
        st.success("The tumor cell seems to be benign and the patient dosen't require any cancer treatment")
        st.warning(
            "Be cautious as this is just a predictive model and dosen't always reflect the ground scenario, although the model has high accuracy. Please consult a specialized doctor for futher evaluation.")


def get_description(column):
    descriptions = {
        'radius_mean': 'Mean of distances from center to points on the perimeter',
        'texture_mean': 'Mean gray-scale value',
        'perimeter_mean': 'Perimeter of the tumor',
        'area_mean': 'Area of the tumor',
        'smoothness_mean': 'Local variation in radius lengths',
        'compactness_mean': 'Perimeter^2 / area - 1.0',
        'concavity_mean': 'Severity of concave portions of the contour',
        'concave points_mean': 'Number of concave portions of the contour',
        'symmetry_mean': 'Symmetry of the tumor',
        'fractal_dimension_mean': 'Fractal dimension of the tumor',
        'radius_se': 'Standard error of distances from center to points on the perimeter',
        'texture_se': 'Standard deviation of gray-scale values',
        'perimeter_se': 'Standard error of the tumor perimeter',
        'area_se': 'Standard error of the tumor area',
        'smoothness_se': 'Standard error of local variation in radius lengths',
        'compactness_se': 'Standard error of perimeter^2 / area - 1.0',
        'concavity_se': 'Standard error of severity of concave portions of the contour',
        'concave points_se': 'Standard error of number of concave portions of the contour',
        'symmetry_se': 'Standard error of symmetry of the tumor',
        'fractal_dimension_se': 'Standard error of fractal dimension of the tumor',
        'radius_worst': 'Worst (largest) value of distances from center to points on the perimeter',
        'texture_worst': 'Worst (largest) value of gray-scale values',
        'perimeter_worst': 'Worst (largest) value of the tumor perimeter',
        'area_worst': 'Worst (largest) value of the tumor area',
        'smoothness_worst': 'Worst (largest) value of local variation in radius lengths',
        'compactness_worst': 'Worst (largest) value of perimeter^2 / area - 1.0',
        'concavity_worst': 'Worst (largest) value of severity of concave portions of the contour',
        'concave points_worst': 'Worst (largest) value of number of concave portions of the contour',
        'symmetry_worst': 'Worst (largest) value of the tumor symmetry',
        'fractal_dimension_worst': 'Worst (largest) value of the fractal dimension of the tumor'
    }
    return descriptions.get(column, column)


def main():
    st.set_page_config(page_title="Breast Cancer Prediction App", page_icon=image, layout="wide")
    with st.container():
        page_tittle, lottie, buff = st.columns([65, 25, 5])
        with lottie:
            lottie_file = load_lottie("https://lottie.host/94453939-f758-4091-aaf7-518179fc83e1/4Qkd5J13IP.json")
            st_lottie(lottie_file, key='flag', height=200, width=200)
        with page_tittle:
            st.title('Breast Cancer Prediction')
    with st.container():
        user_input_checkbox = st.checkbox('Enter Your Own Values: ')
        st.markdown('#')

        x_test = pd.read_csv(r'Datasets and Models/X_test.csv')
        model, scaler = load_resources()

        if user_input_checkbox:

            input_data = pd.DataFrame(columns=x_test.columns)
    st.title('YES')


if __name__ == '__main__':
    main()
