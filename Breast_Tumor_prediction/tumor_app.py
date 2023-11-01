import streamlit as st
import pandas as pd
import requests
from PIL import Image
import joblib
from streamlit_lottie import st_lottie

image = Image.open(r"Images/breast_ribbon.jpg")
side_bar = Image.open(r"Images/sidebar_image.jpeg")


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
            "Be cautious as this is just a predictive model and doesn't always reflect the ground scenario, "
            "although the model has high accuracy. Please consult a specialized doctor for further evaluation.")
    else:
        st.success("The tumor cell seems to be benign and the patient doesn't require any cancer treatment")
        st.warning(
            "Be cautious as this is just a predictive model and doesn't always reflect the ground scenario, "
            "although the model has high accuracy. Please consult a specialized doctor for further evaluation.")


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

            num_features = len(x_test.columns)
            num_columns = 3

            input_cols = st.columns(num_columns)

            input_values = []
            for i in range(0, num_features, num_columns):
                for j in range(num_columns):
                    if i + j < num_features:
                        column = x_test.columns[i + j]
                        description = get_description(column)
                        value = input_cols[j].text_input(
                            column.replace('_', ' - ').title().replace('Se', 'Standard Error').replace(
                                'Fractal - Dimension', 'Fractal Dimension'), help=description, value='', placeholder=0)
                        input_values.append(value)
            for i, vales in enumerate(input_values):
                if vales == '':
                    input_values.pop(i)
            st.markdown('#')
            buff1, button, buff2 = st.columns([5, 2, 5])
            with button:
                predict_button = st.button("Predict", key='predict', use_container_width=True)

            if predict_button:
                if len(input_values) == num_features:
                    input_data.loc[0] = input_values
                    scaled_data = scale_data(input_data, scaler)
                    predictions = predict_cancer(scaled_data, model)
                    display_results(predictions[0])
                else:
                    st.error("Please Enter Values For All Features.")
        else:
            st.write("Select Values From Test Data:")
            st.markdown("#")

            selected_data = pd.DataFrame(columns=x_test.columns)

            num_features = len(x_test.columns)
            num_columns = 3

            select_cols = st.columns(num_columns)

            selected_values = []
            for i in range(0, num_features, num_columns):
                for j in range(num_columns):
                    if i + j < num_features:
                        column = x_test.columns[i + j]
                        values = x_test[column].unique()
                        description = get_description(column)
                        value = select_cols[j].selectbox(
                            column.replace('_', ' - ').title().replace('Se', 'Standard Error').replace(
                                'Fractal - Dimension', 'Fractal Dimension'), values, help=description, index=0)
                        selected_values.append(value)
            st.markdown('#')
            buff1, button, buff2 = st.columns([5, 2, 5])
            with button:
                predict_button = st.button("Predict", key='predict', use_container_width=True)

            if predict_button:
                if len(selected_values) == num_features:
                    selected_data.loc[0] = selected_values
                    scaled_data = scale_data(selected_data, scaler)
                    predictions = predict_cancer(scaled_data, model)
                    display_results(predictions[0])

    with st.sidebar:

        st.image(side_bar, use_column_width=True)
        st.title("ABOUT")
        write_up = ("This is a Breast Cancer Prediction "
                    "App powered by an SVC model. The app takes various features of a breast tumor as input and "
                    "predicts "
                    "whether the tumor is benign or malignant.")
        st.markdown(f"<p style='text-align: justify;'>{write_up}</p>", unsafe_allow_html=True)
        st.markdown("- Accuracy: 97.36%")
        st.markdown("- False Negatives: 0.87%")

        st.title('Performance Metrics:')
        metrics_data = {
            'Tumor Type': ['Benign', 'Malignant'],
            'Precision': ['98%', '96%'],
            'Recall': ['97%', '98%'],
            'F1-Score': ['98%', '97%']
        }
        metrics = pd.DataFrame(metrics_data)
        st.dataframe(metrics, hide_index=True)


if __name__ == '__main__':
    main()
