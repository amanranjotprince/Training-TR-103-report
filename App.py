import numpy as np
import pandas as pd
import  pickle as pkl
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import base64

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
    
    # Convert to Indian Rupees (1 USD = 83 INR)
    predicted_cost_inr = predicted_cost[0] * 1
    display_string = f'Insurance cost: ₹ {round(predicted_cost_inr, 2)}'
    
    st.markdown(display_string)
    
    # Personal Data Table
    st.subheader("Your Personal Data")
    personal_data = {
        'Parameter': ['Age', 'Gender', 'BMI', 'Children', 'Smoker', 'Region'],
        'Value': [age, 'Female' if gender == 0 else 'Male', bmi, childern, 
                 'No' if smoker == 0 else 'Yes', 
                 ['SouthEast', 'SouthWest', 'NorthWest', 'NorthEast'][region]]
    }
    personal_df = pd.DataFrame(personal_data)
    st.dataframe(personal_df, use_container_width=True)
    
    # Personal Data Analysis
    st.subheader("Your Data Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Your Age Position")
        fig, ax = plt.subplots(figsize=(6, 4))
        categories = ['Young (<30)', 'Adult (30-50)', 'Senior (>50)']
        values = [1 if age < 30 else 0, 1 if 30 <= age <= 50 else 0, 1 if age > 50 else 0]
        colors = ['lightblue' if age < 30 else 'lightgray',
                 'lightblue' if 30 <= age <= 50 else 'lightgray',
                 'lightblue' if age > 50 else 'lightgray']
        ax.bar(categories, values, color=colors)
        ax.set_ylabel('Your Category')
        ax.set_ylim(0, 1.2)
        st.pyplot(fig)
        
    with col2:
        st.write("BMI Category")
        fig, ax = plt.subplots(figsize=(6, 4))
        bmi_categories = ['Underweight (<18.5)', 'Normal (18.5-25)', 'Overweight (25-30)', 'Obese (>30)']
        bmi_values = [1 if bmi < 18.5 else 0, 1 if 18.5 <= bmi <= 25 else 0,
                     1 if 25 < bmi <= 30 else 0, 1 if bmi > 30 else 0]
        bmi_colors = ['lightblue' if bmi < 18.5 else 'lightgray',
                     'lightblue' if 18.5 <= bmi <= 25 else 'lightgray',
                     'lightblue' if 25 < bmi <= 30 else 'lightgray',
                     'lightblue' if bmi > 30 else 'lightgray']
        ax.bar(bmi_categories, bmi_values, color=bmi_colors)
        ax.set_ylabel('Your BMI Category')
        ax.set_ylim(0, 1.2)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    
    # Additional Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("Risk Factor Analysis")
        fig, ax = plt.subplots(figsize=(6, 4))
        risk_factors = ['Smoking', 'High BMI', 'Age > 50']
        risk_values = [smoker, 1 if bmi > 30 else 0, 1 if age > 50 else 0]
        risk_colors = ['red' if smoker == 1 else 'lightgreen',
                      'red' if bmi > 30 else 'lightgreen',
                      'red' if age > 50 else 'lightgreen']
        ax.bar(risk_factors, risk_values, color=risk_colors)
        ax.set_ylabel('Risk Present')
        ax.set_ylim(0, 1.2)
        st.pyplot(fig)
        
    with col4:
        st.write("Cost Comparison")
        fig, ax = plt.subplots(figsize=(6, 4))
        cost_labels = ['Your Cost', 'Average Cost']
        cost_values = [predicted_cost[0], 13270.42]  # Average from dataset
        cost_colors = ['blue', 'orange']
        ax.bar(cost_labels, cost_values, color=cost_colors)
        ax.set_ylabel('Insurance Cost ($)')
        st.pyplot(fig)
    
    # PDF Generation
    st.subheader("Your PDF Report")
    
    def create_pdf_report():
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Convert to INR
        predicted_cost_inr = predicted_cost[0] * 1
        
        # Title
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, height - 50, "Insurance Cost Prediction Report")
        
        # User Input Section
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, height - 90, "Personal Information:")
        
        p.setFont("Helvetica", 12)
        p.drawString(120, height - 110, f"Age: {age} years")
        p.drawString(120, height - 130, f"Gender: {'Female' if gender == 0 else 'Male'}")
        p.drawString(120, height - 150, f"BMI: {bmi}")
        p.drawString(120, height - 170, f"Number of Children: {childern}")
        p.drawString(120, height - 190, f"Smoking Status: {'No' if smoker == 0 else 'Yes'}")
        p.drawString(120, height - 210, f"Region: {['SouthEast', 'SouthWest', 'NorthWest', 'NorthEast'][region]}")
        
        # Prediction Result Section
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, height - 250, "Prediction Result:")
        
        p.setFont("Helvetica-Bold", 16)
        p.setFillColorRGB(0.2, 0.4, 0.8)
        p.drawString(120, height - 280, f"Insurance Cost: Rs. {round(predicted_cost_inr, 2)}")
        
        # Reset color
        p.setFillColorRGB(0, 0, 0)
        
        # Risk Assessment
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, height - 340, "Risk Assessment:")
        
        p.setFont("Helvetica", 12)
        risk_factors = []
        if smoker == 1:
            risk_factors.append("Smoker")
        if bmi > 30:
            risk_factors.append("High BMI")
        if age > 50:
            risk_factors.append("Age over 50")
        
        if risk_factors:
            p.drawString(120, height - 360, f"Risk Factors: {', '.join(risk_factors)}")
        else:
            p.drawString(120, height - 360, "No significant risk factors identified")
        
        # Footer
        p.setFont("Helvetica", 10)
        p.drawString(100, 50, "Generated by Medical Insurance Cost Prediction System")
        
        p.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    # PDF Download Button
    pdf_data = create_pdf_report()
    st.download_button(
        label="Download PDF Report",
        data=pdf_data,
        file_name="insurance_analysis_report.pdf",
        mime="application/pdf"
    )


#streamlit run app.py
