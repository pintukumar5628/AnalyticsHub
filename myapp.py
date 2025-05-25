# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Consoleflare Analytics Portal',
    page_icon='📊'
)
#title
st.title(':rainbow[AnalytixHub]')
st.subheader(':gray[Explore Data with ease.]', divider='rainbow')


file = st.file_uploader("Drop CSV, Excel, json, xml, parquet, avro, orc file", type=['CSV', 'xlsx', 'json', 'xml', 'parquet', 'avro', 'orc'])
if(file!=None):
    if(file.name.endswith('CSV')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info('File is successfully Uploaded',icon ='🚨')


    st.subheader(':rainbow[Basic information of the dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15,tab16,tab17,tab18,tab19 = st.tabs(['Dataset Summary','Top and Bottom Rows','Data Types','Column Names','Missing Values', 'Unique Values','Descriptive Statistics', 'Categorical Columns', 'Numerical Columns', 'Value Counts', 'Correlation Matrix', 'Data Distribution', 'Outlier Detection', 'Data Shape', 'Null Percentage', 'Duplicate Records', 'Constant Columns', 'Column-wise Summary', 'Combined Insights' ])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and  {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical summary of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))
    with tab3:
        st.subheader(':grey[Data types of column]')
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader('Column Names in Dataset')
        st.write(list(data.columns))
    with tab5:
        st.subheader('Missing Values')
        st.dataframe(data.isnull().sum())

    with tab6:
        st.subheader('Unique Values')
        st.dataframe(data.nunique())

    with tab7:
        st.subheader('Descriptive Statistics')
        st.dataframe(data.describe(include='all'))

    with tab8:
        st.subheader('Categorical Columns')
        cat_cols = data.select_dtypes(include='object').columns
        st.write(cat_cols)

    with tab9:
        st.subheader('Numerical Columns')
        num_cols = data.select_dtypes(include='number').columns
        st.write(num_cols)

    with tab10:
        st.subheader('Value Counts')
        column = st.selectbox("Select Column", data.columns)
        st.write(data[column].value_counts())

    with tab11:
        st.subheader('Correlation Matrix')
        st.dataframe(data.corr(numeric_only=True))
        fig, ax = plt.subplots()
        sns.heatmap(data.corr(numeric_only=True), annot=True, ax=ax)
        st.pyplot(fig)

    with tab12:
        st.subheader('Data Distribution')
        column = st.selectbox("Select numeric column", data.select_dtypes(include='number').columns, key='dist')
        fig, ax = plt.subplots()
        sns.histplot(data[column], kde=True, ax=ax)
        st.pyplot(fig)

    with tab13:
        st.subheader('Outlier Detection (Boxplot)')
        column = st.selectbox("Select numeric column", data.select_dtypes(include='number').columns, key='outlier')
        fig, ax = plt.subplots()
        sns.boxplot(x=data[column], ax=ax)
        st.pyplot(fig)

    with tab14:
        st.subheader('Data Shape')
        st.write(f"Rows: {data.shape[0]}")
        st.write(f"Columns: {data.shape[1]}")

    with tab15:
        st.subheader('Null Percentage')
        null_percent = data.isnull().mean() * 100
        st.dataframe(null_percent)

    with tab16:
        st.subheader('Duplicate Records')
        st.write(f"Total Duplicates: {data.duplicated().sum()}")

    with tab17:
        st.subheader('Constant Columns')
        const_cols = [col for col in data.columns if data[col].nunique() == 1]
        st.write(const_cols)

    with tab18:
        st.subheader('Column-wise Summary')
        for col in data.columns:
            st.write(f"**{col}**")
            st.write(data[col].describe())

    with tab19:
        st.subheader('Combined Insights')
        st.write(f"Dataset contains {data.shape[0]} rows and {data.shape[1]} columns.")
        st.write("Missing values:")
        st.dataframe(data.isnull().sum())
        st.write("Data types:")
        st.dataframe(data.dtypes)
        st.write("Top 5 rows:")
        st.dataframe(data.head())
        st.write("Correlation heatmap:")
        fig, ax = plt.subplots()
        sns.heatmap(data.corr(numeric_only=True), annot=True, ax=ax)
        st.pyplot(fig)


    st.subheader(':rainbow[Column Values To Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
          column  = st.selectbox('Choose Column name',options=list(data.columns))
        with col2:
            toprows = st.number_input('Top rows',min_value=1,step=1)
        
        count = st.button('Count')
        if(count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='gray')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Groupby : Simplify your data analysis]',divider='rainbow')
    st.write('The groupby lets you summarize data by specific categories and groups')
    with st.expander('Group By your columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your column to groupby',options = list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation',options=['sum','max','min','mean','median','count'])
        
        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col,operation)
            ).reset_index()

            st.dataframe(result)

            st.subheader(':gray[Data Visualization]',divider='gray')
            graphs = st.selectbox('Choose your graphs',options=['Line Chart',' Bar Chart','Scatter Plot','Pie Chart','Sunburst Chart','Heatmap',' Box Plot','Histogram','Treemap','Area Chart'])
            if(graphs=='Line Chart'):
                x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Color Information',options= [None] +list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif(graphs=='Bar Chart'):
                 x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                 y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                 color = st.selectbox('Color Information',options= [None] +list(result.columns))
                 facet_col = st.selectbox('Column Information',options=[None] +list(result.columns))
                 fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                 st.plotly_chart(fig)
            elif(graphs=='Scatter Plot'):
                x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Color Information',options= [None] +list(result.columns))
                size = st.selectbox('Size Column',options=[None] + list(result.columns))
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)
            elif(graphs=='Pie Chart'):
                values = st.selectbox('Choose Numerical Values',options=list(result.columns))
                names = st.selectbox('Choose labels',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)
            elif(graphs=='Sunburst Chart'):
                path = st.multiselect('Choose your Path',options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)

            elif graphs == 'Heatmap':
               fig, ax = plt.subplots()
               sns.heatmap(result.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
               st.pyplot(fig)

            elif graphs == 'Box Plot':
               x_axis = st.selectbox('Choose X axis', options=list(result.columns))
               y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
               fig = px.box(data_frame=result, x=x_axis, y=y_axis)
               st.plotly_chart(fig)

            elif graphs == 'Histogram':
               x_axis = st.selectbox('Choose X axis', options=list(result.columns))
               fig = px.histogram(data_frame=result, x=x_axis)
               st.plotly_chart(fig)

            elif graphs == 'Treemap':
               path = st.multiselect('Choose your Path', options=list(result.columns))
               fig = px.treemap(data_frame=result, path=path, values='newcol')
               st.plotly_chart(fig)

            elif graphs == 'Area Chart':
               x_axis = st.selectbox('Choose X axis', options=list(result.columns))
               y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
               fig = px.area(data_frame=result, x=x_axis, y=y_axis)
               st.plotly_chart(fig)

    


