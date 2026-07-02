import streamlit as st

st.header('2. User Name?')

name = st.text_input("Feature Name?")
st.write(f"Input Name{name}")

situation = st.text_area("Current Situation?")
st.write(f"Current Status:{situation}")

temp = st.number_input("Temp?",
                        min_value=-50,
                        max_value=100,
                        step=1)
st.write(f"Temp.:{temp}")

onprocess = st.date_input("Select the data for MC")
st.write(f"Data{onprocess}")

target = st.selectbox("Select the Target?",
                      ["X1","X2","X3","y"])
st.write(f"Selected Target:{target}")

feature = st.multiselect("Select the feature",
                         ["Wheather","Wind","Temp.","Hummy"])
st.write(f"Selected Feature:{feature}")

job = st.radio("Needed Job?",
               ["Classifiaction","Regression"])

agree = st.checkbox("Data Preprocessing")
if agree:
    st.write("Do DP")
    
degree = st.slider("Hummy?",
                   min_value=0,
                   max_value=100)
st.write(f"Selected Hummy.:{degree}")

button = st.button("Analyze!")
if button:
    st.write("Analyzing")
    
toggle_state = st.toggle("Data Proprecessing")
st.write(f"Data Status:{toggle_state}")

import numpy as np
import pandas as pd

df = pd.DataFrame(
     np.random.randn(5,3),
     columns=["A","B","C"]
)

st.write(df)
st.dataframe(df)

col1,col2 = st.columns(2)

with col1:
    st.write(df)
with col2:
    st.write(df)
    
st.line_chart(df)
st.bar_chart(df)



