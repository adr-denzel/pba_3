import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv('BankChurners_processed.csv')

# an introduction to the dataset
st.title('Data Introduction')
st.write('The table below is a sample from the dataset moulded expressly for addressing this business problem:')

st.dataframe(df.head(5).T)

# paragraphs
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
st.header('Feature Exploration')

# Add a widget to choose variables
data_vars_num = ['Customer_Age', 'Dependent_count', 'Months_on_book', 'Total_Relationship_Count',
             'Months_Inactive_12_mon', 'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
             'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
             'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio']

# histograms
st.subheader('Histograms')
st.write('Beginning with our numeric features we can begin to explore their individual distributions with histograms.')

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
st.write('Scatter plots help us explore the interactions and relations between numeric variables in a 2-d setting.')
st.write('Labelling our points on the plot with their target feature categorizations could aid in uncovering useful patterns.')

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
st.write('With bar charts we get a sense of the count and proportions of our population our target categories occupy.')

category_column = st.selectbox("Select the categorical column for the bar chart", data_vars_cat)

sns.countplot(data=df, x=category_column, hue=color_column)

plt.xlabel(category_column)
plt.ylabel("Count")
plt.title(f"Bar Chart of {category_column} (Count of Instances per Target Category)")

st.pyplot(plt.gcf())
plt.clf()
