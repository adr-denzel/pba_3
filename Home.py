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
st.image(image,
         caption='Source: https://cdn.technologyadvice.com/wp-content/uploads/2020/03/6-Ways-CRM-Stop-Customer-Churn.png',
         use_column_width=True)

st.header('Overall Picture')

overall_attrition = len(df[df['Attrition_Flag'] == 'Attrited Customer'])
overall_retained = len(df[df['Attrition_Flag'] == 'Existing Customer'])
overall_total = overall_attrition + overall_retained

overall_lost_business = df[df['Attrition_Flag'] == 'Attrited Customer']['Total_Revolving_Bal'].sum()
overall_retained_business = df[df['Attrition_Flag'] == 'Existing Customer']['Total_Revolving_Bal'].sum()

m1, m2, m3 = st.columns((1, 1, 1))

overall_churn_rate = round(float(overall_attrition / overall_total) * 100, 2)

m1.metric(label='Full Customer Population: ', value=f'{overall_total:,}')
m2.metric(label='Churn Rate within Population: ', value=str(overall_churn_rate) + '%')
m3.metric(label='Value of Lost Business: ', value=f'${overall_lost_business:,}' + '.00')

m4, m5, m6 = st.columns((1, 1, 1))

m4.metric(label='Churned Customer Population: ', value=f'{overall_attrition:,}')
m5.metric(label='Retained Customer Population: ', value=f'{overall_retained:,}')
m6.metric(label='Value of Retained Business: ', value=f'${overall_retained_business:,}' + '.00')

st.header('Slicing that Picture')
st.info('Select features to filter by:')

# Add a widget to choose variables
data_vars_num = ['Customer_Age', 'Dependent_count', 'Months_on_book', 'Total_Relationship_Count',
                 'Months_Inactive_12_mon', 'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
                 'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
                 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio']

data_vars_cat = ['Gender', 'Education_Level', 'Marital_Status', 'Income_Category', 'Card_Category']

selected_features = st.multiselect("Select a feature or more:", options=data_vars_cat)

filters = {}

for feature in selected_features:
    unique_values = df[feature].unique()
    selected_values = st.multiselect(f'Select {feature} Values', options=unique_values, default=unique_values)
    filters[feature] = selected_values

filtered_df = df.copy()

for feature, selected_values in filters.items():
    filtered_df = filtered_df[filtered_df[feature].isin(selected_values)]

count_attrition = len(filtered_df[df['Attrition_Flag'] == 'Attrited Customer'])
count_retained = len(filtered_df[df['Attrition_Flag'] == 'Existing Customer'])
total_filter = count_retained + count_attrition

lost_business = filtered_df[df['Attrition_Flag'] == 'Attrited Customer']['Total_Revolving_Bal'].sum()
retained_business = filtered_df[df['Attrition_Flag'] == 'Existing Customer']['Total_Revolving_Bal'].sum()

if total_filter > 0:
    sliced_churn_rate = round(float(count_attrition / total_filter) * 100, 2) or 0
else:
    sliced_churn_rate = 0

m7, m8, m9 = st.columns((1, 1, 1))

m7.metric(label='Sliced Customer Population: ', value=f'{total_filter:,}')
m8.metric(label='Population Churn Rate: ', value=str(sliced_churn_rate) + '%')
m9.metric(label='Value of Lost Business: ', value=f'${lost_business:,}' + '.00')

# pie charts of the population churn rate as well as the value of the balance lost on that population, to the balance retained
m10, m11 = st.columns((1, 1))

# population chart

data_2 = {
    'Category': ['Attrited', 'Retained'],
    'Values': [count_attrition, count_retained],
}

df_pie_2 = pd.DataFrame(data_2)

# Set up Seaborn bar plot
sns.set(style='whitegrid')
bar_plot_2 = sns.barplot(x='Category', y='Values', data=df_pie_2, palette='pastel')

# Convert Seaborn bar plot to a pie chart
fig_2, ax = plt.subplots()

# Pie chart settings
colors = sns.color_palette('pastel')
explode = (0.05, 0.05)
ax.pie(df_pie_2['Values'], explode=explode, labels=df_pie_2['Category'], colors=colors, autopct='%1.1f%%', startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Display the pie chart in Streamlit
m10.pyplot(fig_2)

# value chart

data = {
    'Category': ['Attrited', 'Retained'],
    'Values': [lost_business, retained_business],
}

df_pie = pd.DataFrame(data)

# Set up Seaborn bar plot
sns.set(style='whitegrid')
bar_plot = sns.barplot(x='Category', y='Values', data=df_pie, palette='pastel')

# Convert Seaborn bar plot to a pie chart
fig, ax = plt.subplots()

# Pie chart settings
colors = sns.color_palette('pastel')
explode = (0.05, 0.05)
ax.pie(df_pie['Values'], explode=explode, labels=df_pie['Category'], colors=colors, autopct='%1.1f%%', startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Display the pie chart in Streamlit
m11.pyplot(fig)
