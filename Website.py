import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Bank Churners Analysis", layout="wide")

st.title("Bank Churners Analysis")
st.sidebar.header("Navigation")
st.sidebar.markdown("Created by [Omar Zahran](https://www.linkedin.com/in/omarzahran22/)")

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    data = pd.read_csv(r"D:\Power Bi @ITI\Python Visualization\Project\BankChurners.csv")
    data = data.drop([
        "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
        "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2"
    ], axis=1)
    data.rename(columns={
        'CLIENTNUM': 'Client_Number',
        'Dependent_count': 'Dependents',
        'Months_Inactive_12_mon': 'Inactive_Months',
        'Contacts_Count_12_mon': 'Contacts_Counts'
    }, inplace=True)
    return data

data = load_data()

# ---------------- Sidebar Navigation ----------------
option = st.sidebar.radio("Go to:", ["Data Overview", "EDA & Visualization"])

# ---------------- DATA OVERVIEW ----------------
if option == "Data Overview":
    st.subheader(" Data Overview")
    st.write(data.head())
    st.write("Shape:", data.shape)
    st.write("Summary Statistics:")
    st.write(data.describe())

# ---------------- EDA & VISUALIZATION ----------------
elif option == "EDA & Visualization":
    st.subheader("Exploratory Data Analysis & Visualizations")

    # ---------------- Pie Chart - Gender ----------------
    st.write("### Distribution of Customers by Gender")
    fig = px.pie(data, names='Gender', title="Gender Distribution",
                 color='Gender', color_discrete_map={'F':'darkorange','M':'darkblue'})
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Bar Chart - Education Level ----------------
    st.write("### Number of Customers by Education Level")
    edu_counts = data['Education_Level'].value_counts().reset_index()
    edu_counts.columns = ['Education_Level','Count']
    fig = px.bar(edu_counts, x='Education_Level', y='Count',
                 labels={'Education_Level':'Education Level','Count':'Number of Customers'},
                 color='Count', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Bar Chart - Marital Status ----------------
    st.write("### Number of Customers by Marital Status")
    marital_counts = data['Marital_Status'].value_counts().reset_index()
    marital_counts.columns = ['Marital_Status','Count']
    fig = px.bar(marital_counts, x='Marital_Status', y='Count',
                 labels={'Marital_Status':'Marital Status','Count':'Number of Customers'},
                 color='Count', color_continuous_scale='Cividis')
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Bar Chart - Income Category ----------------
    st.write("### Number of Customers by Income Category")
    income_counts = data['Income_Category'].value_counts().reset_index()
    income_counts.columns = ['Income_Category','Count']
    fig = px.bar(income_counts, x='Income_Category', y='Count',
                 labels={'Income_Category':'Income Category','Count':'Number of Customers'},
                 color='Count', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Bar Chart - Card Category ----------------
    st.write("### Number of Customers by Card Category")
    card_counts = data['Card_Category'].value_counts().reset_index()
    card_counts.columns = ['Card_Category','Count']
    fig = px.bar(card_counts, x='Card_Category', y='Count',
                 labels={'Card_Category':'Card Category','Count':'Number of Customers'},
                 color='Count', color_continuous_scale='Greens')
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Histograms - Numeric Columns ----------------
    st.write("### Distribution of Numeric Columns")
    numeric_cols = ['Customer_Age', 'Credit_Limit', 'Total_Trans_Amt', 'Total_Trans_Ct']
    for col in numeric_cols:
        fig = px.histogram(data, x=col, nbins=30, title=f'Distribution of {col}', marginal="box",
                           color_discrete_sequence=['skyblue'])
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Pie Chart - Attrition ----------------
    st.write("### Customer Attrition Distribution")
    fig = px.pie(data, names='Attrition_Flag', color='Attrition_Flag', 
                 color_discrete_map={'Existing Customer':'darkgreen','Attrited Customer':'red'})
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Attrition by Gender ----------------
    st.write("### Attrition by Gender")
    fig = px.histogram(data, x='Gender', color='Attrition_Flag', barmode='group',
                       color_discrete_map={'Existing Customer':'darkgreen','Attrited Customer':'red'})
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Correlation Heatmap ----------------
    st.write("### Correlation Heatmap")
    corr = data[['Customer_Age', 'Credit_Limit', 'Total_Trans_Amt', 'Total_Trans_Ct',
                 'Avg_Open_To_Buy','Inactive_Months']].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Boxplots ----------------
    st.write("### Boxplots: Inactive Months, Avg Open To Buy, Avg Utilization Ratio by Attrition")
    numeric = ['Inactive_Months', 'Avg_Open_To_Buy', 'Avg_Utilization_Ratio']
    for col in numeric:
        fig = px.box(data, x='Attrition_Flag', y=col, color='Attrition_Flag',
                     color_discrete_map={'Existing Customer':'darkgreen','Attrited Customer':'red'})
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Boxplots - Age, Transaction Count, Spending ----------------
    st.write("### Customer Age, Transaction Count, and Spending by Attrition Status")
    cols = ['Customer_Age', 'Total_Trans_Ct', 'Total_Trans_Amt']
    for col in cols:
        fig = px.box(data, x='Attrition_Flag', y=col, color='Attrition_Flag',
                     color_discrete_map={'Existing Customer':'darkgreen','Attrited Customer':'red'})
        st.plotly_chart(fig, use_container_width=True)
