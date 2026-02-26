import streamlit as st
import pandas as pd

#buttons
st.title("Buttons")

left, right = st.columns(2)
if left.button("Reset",width="stretch"):
    left.markdown("You clicked 'RESET' button")
    
if right.button("Submit",width="stretch"):
    right.markdown("You clicked 'SUBMIT' button")
    
st.divider()

#download button
st.title("Download Button")
st.markdown("## Download .csv") 
#downloading dataframe as .csv
@st.cache_data
def get_data():
    df = pd.DataFrame({
        "Team":["WI","RSA","IND","ZIM"],
        "Played":[1,1,1,1],
        "Won":[1,1,0,0],
        "Lost":[0,0,1,1],
        "NR":[0,0,0,0],
        "Pts":[2,2,0,0],
        "NRR":[5.350,3.800,-3.800,-5.350]
    })
    return df

@st.cache_data
def download_csv(df):
    return df.to_csv(index=False).encode("utf-8")

df = get_data()
csv = download_csv(df)

st.table(df)

st.download_button(
    label = "Download CSV",
    data = csv,
    file_name = "data.csv",
    mime="text/csv",
    icon = ":material/download:"
)

st.divider()

#download string input as .txt
st.markdown("## Download .txt")

text = st.text_area("Enter your text here")

if text:
    st.download_button(
        label = "Download Text",
        data = text,
        file_name = "text.txt",
        mime = "text/plain",
        icon = ":material/download:"
    )
else:
    st.info("Please enter some text to download")