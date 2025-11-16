import numpy as np
import pandas as pd
import  pickle as pkl
import streamlit as st

model = pkl.load(open('MIPML.pkl','rb'))

st.header("Medical Insurance Cost Predication")

gender = st.selectbox('Choose the gender',['Female','Male'])
age = st.slider('Enter Age:',5,80)
region = st.selectbox("Choose Region",['SouthEast','SouthWest','NorthWest','NorthEast'])
bmi = st.slider('Enter BMI',5,100)
childern = st.slider('Choose no of childern',0,5)
smoker = st.selectbox("Are you a smoker ?",['No','Yes'])

if gender == 'Female':
    gender = 0
else:
    gender = 1


if smoker == 'No':
    smoker = 0
else:
    smoker = 1


if region == 'SouthEast':
    region = 0
if region == 'SouthWest':
    region = 1
if region == 'NorthWest':
    region = 2
else:
    region = 3


input_data=(age,gender,bmi,childern,smoker,region)
input_data= np.asarray(input_data)
input_data = input_data.reshape(1,-1)

if st.button('Predict'):
    predicted_cost = model.predict(input_data)
    display_string = 'Insurance cost will be ' + str(round(predicted_cost[0], 2)) + ' USD Dollars'
    
    st.markdown(display_string)


#streamlit run app.py