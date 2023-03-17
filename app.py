import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)

df=pd.read_excel(
    io='supermarkt_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000,
)

st.dataframe(df)

#sidebar
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer :",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gemder:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection=df.query(
    "City == @city & Customer_type==@customer_type & Gender==@gender"
)


#mainpage

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


total_sales=int(df_selection["Total"].sum())
average_rating=round(df_selection["Rating"].mean(),1)
star_rating=":star:"*int(round(average_rating,0))

avg_sale=round(df_selection["Total"].mean(),2)

leftc,midc,rightc=st.columns(3)

with leftc:
    st.subheader("Total Sales :")
    st.subheader(f"US $ {total_sales:,}")

with midc:
    st.subheader("Average rating")
    st.subheader(f"{average_rating} {star_rating}")

with rightc:
    st.subheader("Average Sales per Transaction")
    st.subheader(f"US $ {avg_sale}")

st.markdown("---")



#sales chart

sales_by_product_line=(
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")

)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#66FFFF"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales)