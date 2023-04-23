
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Load the CSV data
df = pd.read_csv('BankChurners_processed.csv')

# an introduction to the dataset
st.title('Feel the Churn')

image = Image.open('images/6-Ways-CRM-Stop-Customer-Churn.png')
st.image(image, caption='Source: https://cdn.technologyadvice.com/wp-content/uploads/2020/03/6-Ways-CRM-Stop-Customer-Churn.png', use_column_width=True)

st.sidebar.info('Select features to filter by to investigate what drives customer churn:')

m1, m2, m3, m4, m5 = st.columns((1, 1, 1, 1, 1))



m1.write('')
m2.metric(label='Total Number of Customers', value=int(to['Value']), delta=str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
m3.metric(label='Current Handover Average', value=str(int(ch['Value']))+" Mins", delta = str(int(ch['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
m4.metric(label='Time Lost today (Above 15 mins)', value=str(int(hl['Value']))+" Hours", delta = str(int(hl['Previous']))+' Compared to yesterday')
m1.write('')

st.header('Understanding a Churner')

# Add a widget to choose variables
data_vars_num = ['Customer_Age', 'Dependent_count', 'Months_on_book', 'Total_Relationship_Count',
             'Months_Inactive_12_mon', 'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
             'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
             'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio']

# histograms
st.subheader('Histograms')

x_var_hist = st.selectbox('Select a variable', options=data_vars_num)
bins_hist = st.slider("Number of bins", min_value=5, max_value=50, value=5)

sns.histplot(data=df, x=x_var_hist, bins=bins_hist, color='green')
plt.xlabel(x_var_hist)
plt.ylabel("Frequency")
plt.title(f"Histogram of {x_var_hist}")

st.pyplot(plt.gcf())
plt.clf()

# scatter plots
st.subheader('Scatter Plots')

x_scatter = st.selectbox("Select the x-axis column", data_vars_num, index=0)
y_scatter = st.selectbox("Select the y-axis column", data_vars_num, index=1)

color_column = 'Attrition_Flag'

sns.scatterplot(data=df, x=x_scatter, y=y_scatter, hue=color_column)

plt.xlabel(x_scatter)
plt.ylabel(y_scatter)
plt.title(f"Scatter plot of {x_scatter} vs {y_scatter}")

st.pyplot(plt.gcf())
plt.clf()

# categorical data exploration
data_vars_cat = ['Gender', 'Education_Level', 'Marital_Status', 'Income_Category', 'Card_Category']

# bar charts
st.subheader('Bar Charts')

category_column = st.selectbox("Select the categorical column for the bar chart", data_vars_cat)

sns.countplot(data=df, x=category_column, hue=color_column)

plt.xlabel(category_column)
plt.ylabel("Count")
plt.title(f"Bar Chart of {category_column} (Count of Instances per Target Category)")

st.pyplot(plt.gcf())
plt.clf()

st.subheader('Now we may progress to the modeling phase.')
