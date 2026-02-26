import streamlit as st
import pandas as pd

#tabel
st.title("Table")

st.markdown("## **Super 8 Group 1**")
df1 = pd.DataFrame({
    "Team":["WI","RSA","IND","ZIM"],
    "Played":[1,1,1,1],
    "Won":[1,1,0,0],
    "Lost":[0,0,1,1],
    "NR":[0,0,0,0],
    "Pts":[2,2,0,0],
    "NRR":[5.350,3.800,-3.800,-5.350]
})
st.table(df1)

st.markdown("## **Super 8 Group 2**")
df2 = pd.DataFrame({
    "Team":["ENG","NZ","PAK","SL"],
    "Played":[2,1,2,1],
    "Won":[2,0,0,0],
    "Lost":[0,0,1,1],
    "NR":[0,1,1,0],
    "Pts":[4,1,1,0],
    "NRR":[1.491,0.000,-0.461,-2.550]
})
st.table(df2)

st.divider()