
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('BankChurners_processed.csv')

data_vars_num = ['Customer_Age', 'Dependent_count', 'Months_on_book', 'Total_Relationship_Count',
             'Months_Inactive_12_mon', 'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
             'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
             'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio']

# correlation matrix
st.subheader('Correlation Matrix')
st.write('With a correlation matrix we can condense the information within feature interactions and relations '
         'to identify features whose signals are highly synchronised.')
st.write('This helps in eliminating combinations of features to keep model biases balanced.')

corr_mat = df[data_vars_num].corr()

fig_corr, ax_corr = plt.subplots(figsize=(15, 12))
sns.heatmap(corr_mat, ax=ax_corr, annot=True, cmap='coolwarm')

ax_corr.set_title('Correlation Matrix')

# modeling



st.pyplot(fig_corr)

# evaluation

