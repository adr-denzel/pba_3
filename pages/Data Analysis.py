import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv('BankChurners_processed.csv')

# an introduction to the dataset
st.title('Data Introduction')
st.write('The table below is a sample from the dataset moulded expressly for addressing this business problem:')

st.dataframe(df.head(5).T)

st.write('With a mixture of both numeric and categorical data, a thorough exploration of the data is needed to '
         'effectively assess its relative potential within possible modeling paradigms.')

st.write('By beginning with visualisations of our data, we can start to assess how workable, complete, '
         'or even potentially inappropriate features may or may not be for particular modeling solutions.')

st.write('We also begin to understand the ***shape*** of our data. This can lead to discovering trends or patterns '
         'that would not be as readily apparent if the data is simply examined as a structured table.')

st.header('Feature Summary')
st.write('* Categorical target feature: ***Attrition_Flag***. This is a **binary classification** problem.')
st.write('* 14 Numeric features: ***Customer_Age***, ***Dependent_count***, ***Months_on_book***, ***Total_Relationship_Count***, '
         '***Months_Inactive_12_mon***, ***Contacts_Count_12_mon***, ***Credit_Limit***, ***Total_Revolving_Bal***, ***Avg_Open_To_Buy*** '
         '***Total_Amt_Chng_Q4_Q1***, ***Total_Trans_Amt***, ***Total_Trans_Ct***, ***Total_Ct_Chng_Q4_Q1***, ***Avg_Utilization_Ratio***')
st.write('* 5 Categorical features: ***Gender***, ***Education_Level***, ***Marital_Status***, ***Income_Category***, ***Card_Category***')

# exploratory analysis with histograms for numeric data
st.header('Numeric Feature Exploration')

# Add a widget to choose variables
data_vars = ['Customer_Age', 'Dependent_count', 'Months_on_book', 'Total_Relationship_Count',
                     'Months_Inactive_12_mon', 'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
                     'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
                     'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio']

# histograms
st.subheader('Histograms')
st.write('Beginning with our numeric features we can begin to explore their individual distributions with histograms.')

x_var_hist = st.selectbox('Select a variable', options=data_vars)

hist_fig = px.histogram(df, x=x_var_hist)

for trace in hist_fig.data:
    trace.marker.line.width = 1
    trace.marker.line.color = 'black'

st.plotly_chart(hist_fig)

# correlation matrix
st.subheader('Correlation Matrix')
st.write('With a correlation matrix we can explore the interactions and relations between numeric variables in an '
         'condensed and information rich form.')

corr_mat = df[data_vars].corr()

fig, ax = plt.subplots(figsize=(15, 12))
sns.heatmap(corr_mat, ax=ax, annot=True, cmap='coolwarm')

ax.set_title('Correlation Matrix')

st.pyplot(fig)
