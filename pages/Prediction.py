
import pickle
import streamlit as st
from PIL import Image

model_file = 'random_forest_clf.pickle'

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

st.title("Let's Find a Churner")

image = Image.open(
    'images/investment-forecast-or-prediction-vision-to-see-investing-opportunity-future-profit-from-stock-and-crypto-trading-concept-flat-modern-illustration-vector.jpg')

st.image(image,
         caption='Source: https://static.vecteezy.com/system/resources/previews/014/563/665/original/investment-forecast-or-prediction-vision-to-see-investing-opportunity-future-profit-from-stock-and-crypto-trading-concept-flat-modern-illustration-vector.jpg',
         use_column_width=True)

st.sidebar.info('Select values and make a prediction:')

age = st.sidebar.slider('Age:', min_value=18, max_value=100, value=30)
gender = st.sidebar.selectbox('Gender:', ['Male', 'Female'])
dependent_count = st.sidebar.slider('Dependent Count:', min_value=0, max_value=5, value=0)
education_level = st.sidebar.selectbox('Education Level:',
                                       ['Uneducated', 'High School', 'College', 'Graduate', 'Post-Graduate',
                                        'Doctorate', 'Unknown'])

marital_status = st.sidebar.selectbox('Marital Status:', ['Single', 'Married', 'Divorced', 'Unknown'])
income_category = st.sidebar.selectbox('Income Category:',
                                       ['Less than $40K', '$40K - $60K', '$80K - $120K', '$60K - $80K', '$120K +',
                                        'Unknown'])

card_category = st.sidebar.selectbox('Credit Card Product:', ['Blue', 'Silver', 'Gold', 'Platinum'])
months_on_book = st.sidebar.slider('Months on Book:', min_value=12, max_value=60, value=12)
relationship_count = st.sidebar.slider('Relationship Count:', min_value=1, max_value=6, value=1)
months_inactive_12_mon = st.sidebar.slider('Months Inactive Over Past Year', min_value=0, max_value=6, value=2)
contact_count_12_mon = st.sidebar.slider('Contact Count Over Past Year', min_value=0, max_value=6, value=2)
credit_limit = st.sidebar.slider('Credit Limit:', min_value=1000, max_value=35000, value=1000, step=1000)
total_revolving_balance = st.sidebar.slider('Card Balance:', min_value=0, max_value=35000, value=1000, step=1000)
total_trans_amount = st.sidebar.slider('Total Transactions Value:', min_value=0, max_value=35000, value=5000, step=1000)
total_trans_count = st.sidebar.slider('Total Transactions Count:', min_value=0, max_value=150, value=50)
total_amt_change_q4_q1 = st.sidebar.slider('Total Transactions Value Change Change Q4 to Q1:', min_value=0,
                                           max_value=4, value=1)

total_ct_change_q4_q1 = st.sidebar.slider('Total Transactions Count Change Q4 to Q1:', min_value=0, max_value=4,
                                          value=1)

avg_utilisation_rate = total_revolving_balance / credit_limit
avg_open_to_buy = credit_limit - total_revolving_balance

output = 0.12
output_prob = 0.55
input_dict = {
    "Customer_Age": age,
    "Gender": gender,
    "Dependent_count": dependent_count,
    "Education_Level": education_level,
    "Marital_Status": marital_status,
    "Income_Category": income_category,
    "Card_Category": card_category,
    "Months_on_book": months_on_book,
    "Total_Relationship_Count": relationship_count,
    "Months_Inactive_12_mon": months_inactive_12_mon,
    "Contacts_Count_12_mon": contact_count_12_mon,
    "Credit_Limit": credit_limit,
    "Total_Revolving_Bal": total_revolving_balance,
    "Avg_Open_To_Buy": avg_open_to_buy,
    "Total_Amt_Chng_Q4_Q1": total_amt_change_q4_q1,
    "Total_Trans_Amt": total_trans_amount,
    "Total_Trans_Ct": total_trans_count,
    "Total_Ct_Chng_Q4_Q1": total_ct_change_q4_q1,
    "Avg_Utilization_Ratio": avg_utilisation_rate
}

if st.sidebar.button("Predict"):
    '''
    X = dv.transform([input_dict])
	y_pred = model.predict_proba(X)[0, 1]
	churn = y_pred >= 0.5
	output_prob = float(y_pred)
	output = bool(churn)
	'''

m1, m2, m3 = st.columns((1, 1, 1))
m1.write('')
m2.metric('Churn Prediction: ', value=str(output))
m3.metric('Probability of Prediction: ', value=str(round(float(output_prob * 100), 2)) + '%')
