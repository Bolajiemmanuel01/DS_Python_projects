import streamlit as st
import pandas as pd

dataset = pd.read_csv("./data/Public_School_Characteristics_2020-21.csv")

st.dataframe(dataset)
