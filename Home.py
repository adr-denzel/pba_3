
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
overall_churn_rate = round(float(overall_attrition / overall_total) * 100, 2)

m1, m2, m3 = st.columns((1, 1, 1))

m1.metric(label='Overall Customer Population: ', value=f'{overall_total:,}')
m2.metric(label='Overall Customer Attrition: ', value=str(overall_churn_rate) + '%')
m3.metric(label='Value of Business Lost: ', value=f'${overall_lost_business:,}' + '.00')

m4, m5, m6 = st.columns((1, 1, 1))

m4.metric(label='Customer Population Lost: ', value=f'{overall_attrition:,}')
m5.metric(label='Customer Population Retained: ', value=f'{overall_retained:,}')
m6.metric(label='Value of Business Retained: ', value=f'${overall_retained_business:,}' + '.00')

m7, m8 = st.columns((1, 1))

# count chart
data_overall_count = {
    'Category': ['Overall Attrition', 'Overall Retained'],
    'Values': [overall_attrition, overall_retained],
}

df_overall_count = pd.DataFrame(data_overall_count)

# Set up Seaborn bar plot
sns.set(style='whitegrid')
bar_plot_1 = sns.barplot(x='Category', y='Values', data=df_overall_count, palette='pastel')

# Convert Seaborn bar plot to a pie chart
fig_1, ax_1 = plt.subplots()

# Pie chart settings
colors_1 = sns.color_palette('pastel')
explode_1 = (0.05, 0.05)
ax_1.pie(df_overall_count['Values'], explode=explode_1, labels=df_overall_count['Category'], colors=colors_1,
         autopct='%1.0f%%', startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
ax_1.axis('equal')
ax_1.set_title('Population Attrition Overall', y=-0.2)

# Display the pie chart in Streamlit
m7.pyplot(fig_1)

# value chart
data_overall_value = {
    'Category': ['Overall Attrition', 'Overall Retained'],
    'Values': [overall_lost_business, overall_retained_business],
}

df_overall_value = pd.DataFrame(data_overall_value)

# Set up Seaborn bar plot
sns.set(style='whitegrid')
bar_plot_2 = sns.barplot(x='Category', y='Values', data=df_overall_value, palette='pastel')

# Convert Seaborn bar plot to a pie chart
fig_2, ax_2 = plt.subplots()

# Pie chart settings
colors_2 = sns.color_palette('pastel')
explode_2 = (0.05, 0.05)
ax_2.pie(df_overall_value['Values'], explode=explode_2, labels=df_overall_value['Category'], colors=colors_2,
         autopct='%1.0f%%', startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
ax_2.axis('equal')
ax_2.set_title('Business Attrition Overall', y=-0.2)

# Display the pie chart in Streamlit
m8.pyplot(fig_2)

# now for the interactive chart
st.header('Slicing that Picture')
st.info('Select Categorical and/or Numerical features to filter by:')

# Add a widget to choose variables
data_vars_num = ['Customer_Age', 'Dependent_count', 'Months_on_book', 'Total_Relationship_Count',
                 'Months_Inactive_12_mon', 'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
                 'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
                 'Total_Ct_Chng_Q4_Q1']

data_vars_cat = ['Gender', 'Education_Level', 'Marital_Status', 'Income_Category', 'Card_Category']

cat_selected_features = st.multiselect("Select categorical features here:", options=data_vars_cat)

cat_filters = {}

for feature in cat_selected_features:
    unique_values = df[feature].unique()
    selected_values = st.multiselect(f'Select {feature} Values', options=unique_values, default=unique_values)
    cat_filters[feature] = selected_values

# adding a numerical slider
num_selected_features = st.multiselect("Select numerical features here:", options=data_vars_num)

num_filters = {}

for feature in num_selected_features:
    min_value, max_value = int(df[feature].min()), int(df[feature].max())
    selected_range = st.slider(f'Select a range for {feature}', min_value=min_value, max_value=max_value, value=(min_value, max_value))
    num_filters[feature] = selected_range

# filter dataframe
filtered_df = df.copy()

for feature, selected_values in cat_filters.items():
    filtered_df = filtered_df[filtered_df[feature].isin(selected_values)]

for feature, selected_range in num_filters.items():
    filtered_df = filtered_df[(filtered_df[feature] >= selected_range[0]) & (filtered_df[feature] <= selected_range[1])]


count_attrition = len(filtered_df[filtered_df['Attrition_Flag'] == 'Attrited Customer'])
count_retained = len(filtered_df[filtered_df['Attrition_Flag'] == 'Existing Customer'])
total_filter = count_retained + count_attrition

lost_business = filtered_df[filtered_df['Attrition_Flag'] == 'Attrited Customer']['Total_Revolving_Bal'].sum()
retained_business = filtered_df[filtered_df['Attrition_Flag'] == 'Existing Customer']['Total_Revolving_Bal'].sum()

if total_filter > 0:
    sliced_churn_rate = round(float(count_attrition / total_filter) * 100, 2) or 0
else:
    sliced_churn_rate = 0

m9, m10, m11 = st.columns((1, 1, 1))

m9.metric(label='Sliced Customer Population: ', value=f'{total_filter:,}')
m10.metric(label='Sliced Customer Attrition: ', value=str(sliced_churn_rate) + '%')
m11.metric(label='Business Lost within Slice: ', value=f'${lost_business:,}' + '.00')

m12, m13, m14 = st.columns((1, 1, 1))

m12.metric(label='Sliced Population Lost: ', value=f'{count_attrition:,}')
m13.metric(label='Sliced Population Retained: ', value=f'{count_retained:,}')
m14.metric(label='Business Retained within Slice: ', value=f'${retained_business:,}' + '.00')

# sliced charts
try:
    m15, m16 = st.columns((1, 1))

    # value chart
    data_slice_count = {
        'Category': ['Attrition within Slice', 'Retained within Slice'],
        'Values': [count_attrition, count_retained],
    }

    df_slice_count = pd.DataFrame(data_slice_count)

    # Set up Seaborn bar plot
    sns.set(style='whitegrid')
    bar_plot_3 = sns.barplot(x='Category', y='Values', data=df_slice_count, palette='pastel6')

    # Convert Seaborn bar plot to a pie chart
    fig_3, ax_3 = plt.subplots()

    # Pie chart settings
    colors_3 = sns.color_palette('pastel6')
    explode_3 = (0.05, 0.05)
    ax_3.pie(df_slice_count['Values'], explode=explode_3, labels=df_slice_count['Category'], colors=colors_3,
             autopct='%1.0f%%', startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax_3.axis('equal')
    ax_3.set_title('Population Attrition within Slice', y=-0.2)

    # Display the pie chart in Streamlit
    m15.pyplot(fig_3)

    # value chart
    data_slice_value = {
        'Category': ['Attrition within Slice', 'Retained within Slice'],
        'Values': [lost_business, retained_business],
    }

    df_slice_value = pd.DataFrame(data_slice_value)

    # Set up Seaborn bar plot
    sns.set(style='whitegrid')
    bar_plot_4 = sns.barplot(x='Category', y='Values', data=df_slice_value, palette='pastel6')

    # Convert Seaborn bar plot to a pie chart
    fig_4, ax_4 = plt.subplots()

    # Pie chart settings
    colors_4 = sns.color_palette('pastel6')
    explode_4 = (0.05, 0.05)
    ax_4.pie(df_slice_value['Values'], explode=explode_3, labels=df_slice_value['Category'], colors=colors_3,
             autopct='%1.0f%%', startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax_4.axis('equal')
    ax_4.set_title('Business Attrition within Slice', y=-0.2)

    # Display the pie chart in Streamlit
    m16.pyplot(fig_4)

    m17, m18 = st.columns((1, 1))

    # value chart
    other_attrition_count = overall_attrition - count_attrition

    data_slice_count_2 = {
        'Category': ['Slice Attrition', 'Other Attrition', 'Overall Retained'],
        'Values': [count_attrition, other_attrition_count, overall_retained],
    }

    df_slice_count_2 = pd.DataFrame(data_slice_count_2)

    # Set up Seaborn bar plot
    sns.set(style='whitegrid')
    bar_plot_5 = sns.barplot(x='Category', y='Values', data=df_slice_count_2, palette='flare')

    # Convert Seaborn bar plot to a pie chart
    fig_5, ax_5 = plt.subplots()

    # Pie chart settings
    colors_5 = sns.color_palette('flare')
    explode_5 = (0.05, 0.05, 0.05)
    ax_5.pie(df_slice_count_2['Values'], explode=explode_5, labels=df_slice_count_2['Category'], colors=colors_5,
             autopct='%1.0f%%', startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax_5.axis('equal')
    ax_5.set_title('Sliced Population Attrition within Overall', y=-0.2)

    # Display the pie chart in Streamlit
    m17.pyplot(fig_5)

    other_attrition_value = overall_lost_business - lost_business

    data_slice_count_2 = {
        'Category': ['Slice Attrition', 'Other Attrition', 'Overall Retained'],
        'Values': [lost_business, other_attrition_value, overall_retained_business],
    }

    df_slice_count_2 = pd.DataFrame(data_slice_count_2)

    # Set up Seaborn bar plot
    sns.set(style='whitegrid')
    bar_plot_6 = sns.barplot(x='Category', y='Values', data=df_slice_count_2, palette='flare')

    # Convert Seaborn bar plot to a pie chart
    fig_6, ax_6 = plt.subplots()

    # Pie chart settings
    colors_6 = sns.color_palette('flare')
    explode_6 = (0.05, 0.05, 0.05)
    ax_6.pie(df_slice_count_2['Values'], explode=explode_5, labels=df_slice_count_2['Category'], colors=colors_5,
             autopct='%1.0f%%', startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax_6.axis('equal')
    ax_6.set_title('Sliced Business Attrition within Overall', y=-0.2)

    # Display the pie chart in Streamlit
    m18.pyplot(fig_6)

except ValueError:
    custom_css = """
    <style>
        .red-info {
            background-color: #ffcccc;
            border: 1px solid red;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
        }
    </style>
    """

    # Create a red info box using st.markdown and custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown('<div class="red-info">Please ensure at least 1 value for every feature you\'ve chosen to filter by has been selected.</div>',
                unsafe_allow_html=True)
