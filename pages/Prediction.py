
import streamlit as st
import pickle

st.title("Looking Forwards")

rf_pickle = open('random_forest_clf.pickle', 'rb')
map_pickle = open('uniques_mapping.pickle', 'rb')
rfc = pickle.load(rf_pickle)
unique_penguin_mapping = pickle.load(map_pickle)
st.write(rfc)
st.write(unique_penguin_mapping)

age = st.number_input('Customer Age', min_value=0, step=1)
dependents = st.number_input('Number of Dependents', min_value=0, step=1)
months_on_book = st.number_input('Months on Book', min_value=0, step=1)
relationship_count = st.number_input('Relationship Count', min_value=0, step=1)
months_inactive = st.number_input('Months Inactive', min_value=0, step=1)
contacts_count = st.number_input('Contact Count', min_value=0, step=1)
credit_limit = st.number_input('Credit Limit', min_value=0, step=100)
balance = st.number_input('Balance', min_value=0, step=100)
open_to_buy = st.number_input('Open to Buy', min_value=0, step=1000)
chng_q4_q1 = st.number_input('Amt Change Quarter', min_value=0)
trans_amt = st.number_input('Total Transaction Amount', min_value=0, step=100)
total_trans_ct = st.number_input('Total Transaction Count', min_value=0, step=1)
total_ct = st.number_input('Count Change', min_value=0, step=1)
utilisation = st.number_input('Utilisation Ratio', min_value=0, step=1)

new_prediction = rfc.predict([[age, dependents, months_on_book,
                               relationship_count, months_inactive,
                               contacts_count, credit_limit, balance,
                               open_to_buy, chng_q4_q1, trans_amt,
                               total_trans_ct, total_ct, utilisation]])

prediction_outcome = unique_penguin_mapping[new_prediction][0]

st.write(new_prediction)
