
import pickle
import pandas as pd
import streamlit as st
from PIL import Image

model_file = 'rfc_model.pickle'

with open(model_file, 'rb') as rfc:
    model = pickle.load(rfc)

st.title("Find a Churner")

image = Image.open(
    'images/investment-forecast-or-prediction-vision-to-see-investing-opportunity-future-profit-from-stock-and-crypto-trading-concept-flat-modern-illustration-vector.jpg')

st.image(image,
         caption='Source: https://static.vecteezy.com/system/resources/previews/014/563/665/original/investment-forecast-or-prediction-vision-to-see-investing-opportunity-future-profit-from-stock-and-crypto-trading-concept-flat-modern-illustration-vector.jpg',
         use_column_width=True)

st.sidebar.info('Select inputs ***here***:')

# customer age: integer
age = st.sidebar.slider('Age:', min_value=18, max_value=100, value=30)

# customer sex: binary
gender = st.sidebar.selectbox('Gender:', ['Male', 'Female'])

female = 0
male = 0

if gender == 'Male':
    male = 1
else:
    female = 1

# dependent count: integer
dependent_count = st.sidebar.slider('Dependent Count:', min_value=0, max_value=5, value=0)

# education level: ordinal encoding
education_level = st.sidebar.selectbox('Education Level:',
                                       ['Uneducated', 'High School', 'College', 'Graduate', 'Post-Graduate',
                                        'Doctorate', 'Unknown'])

if education_level == 'Doctorate':
    edu_code = 0
elif education_level == 'Post-Graduate':
    edu_code = 1
elif education_level == 'Graduate' or 'Unknown':
    edu_code = 2
elif education_level == 'College':
    edu_code = 3
elif education_level == 'High School':
    edu_code = 4
else:
    edu_code = 5

marital_status = st.sidebar.selectbox('Marital Status:', ['Single', 'Married', 'Divorced', 'Unknown'])

single = 0
married = 0
divorced = 0

if marital_status == 'Single':
    single = 1
elif marital_status == 'Married' or 'Unknown':
    married = 1
else:
    divorced = 1

income_category = st.sidebar.selectbox('Income Category:',
                                       ['Less than $40K', '$40K - $60K', '$80K - $120K', '$60K - $80K', '$120K +',
                                        'Unknown'])

if income_category == '$120K +':
    income_code = 0
elif income_category == '$80K - $120K':
    income_code = 1
elif income_category == '$60K - $80K':
    income_code = 2
elif income_category == '$40K - $60K':
    income_code = 3
else:
    income_code = 4

card_category = st.sidebar.selectbox('Credit Card Product:', ['Blue', 'Silver', 'Gold', 'Platinum'])

blue = 0
silver = 0
gold = 0
platinum = 0

if card_category == 'Blue':
    blue = 1
elif card_category == 'Silver':
    silver = 1
elif card_category == 'Gold':
    gold = 1
else:
    platinum = 1

months_on_book = st.sidebar.slider('Months on Book:', min_value=12, max_value=60, value=12)

relationship_count = st.sidebar.slider('Relationship Count:', min_value=0, max_value=6, value=1)

months_inactive_12_mon = st.sidebar.slider('Months Inactive Over Past Year', min_value=0, max_value=6, value=2)

contact_count_12_mon = st.sidebar.slider('Contact Count Over Past Year', min_value=0, max_value=6, value=2)

credit_limit = st.sidebar.slider('Credit Limit:', min_value=1000, max_value=35000, value=1000, step=1000)

total_revolving_balance = st.sidebar.slider('Card Balance:', min_value=0, max_value=35000, value=1000, step=1000)

total_trans_amount = st.sidebar.slider('Total Transactions Value:', min_value=0, max_value=35000, value=5000, step=1000)

total_trans_count = st.sidebar.slider('Total Transactions Count:', min_value=0, max_value=150, value=50)

total_amt_change_q4_q1 = st.sidebar.slider('Total Transactions Value Change Change Q4 to Q1:', min_value=0.00,
                                           max_value=4.00, value=1.00, step=0.05)

total_ct_change_q4_q1 = st.sidebar.slider('Total Transactions Count Change Q4 to Q1:', min_value=0.00, max_value=4.00,
                                          value=1.00, step=0.05)

input_dict = {
    "Customer_Age": [age],
    "Dependent_count": [dependent_count],
    "Education_Level": [edu_code],
    "Income_Category": [income_code],
    "Months_on_book": [months_on_book],
    "Total_Relationship_Count": [relationship_count],
    "Months_Inactive_12_mon": [months_inactive_12_mon],
    "Contacts_Count_12_mon": [contact_count_12_mon],
    "Credit_Limit": [credit_limit],
    "Total_Revolving_Bal": [total_revolving_balance],
    "Total_Amt_Chng_Q4_Q1": [total_amt_change_q4_q1],
    "Total_Trans_Amt": [total_trans_amount],
    "Total_Trans_Ct": [total_trans_count],
    "Total_Ct_Chng_Q4_Q1": [total_ct_change_q4_q1],
    "F": [female],
    "M": [male],
    "Divorced": [divorced],
    "Married": [married],
    "Single": [single],
    "Blue": [blue],
    "Gold": [gold],
    "Platinum": [platinum],
    "Silver": [silver],
}

X = pd.DataFrame(input_dict)

st.info('Select your inputs and press ***Predict*** to make a classification:')


def predict_with_threshold(classifier, x, threshold=0.78):
    y_proba = classifier.predict_proba(x)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)
    return y_pred


if st.sidebar.button("Predict"):

    # Make predictions with the specific threshold
    y_prediction = predict_with_threshold(model, X)
    y_probability = model.predict_proba(X)[:, 1]

    if y_prediction == 1:
        st.metric('Prediction: ', value='Customer Retained')
    else:
        st.metric('Prediction: ', value='Customer Lost')
