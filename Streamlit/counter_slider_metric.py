import streamlit as st
import pandas as pd
import numpy as np

#counter
st.title("Counter")
if 'count' not in st.session_state:
    st.session_state.count = 0
    
def increment():
    st.session_state.count += 1

def decrement():
    st.session_state.count -= 1


col1, col2,col3 = st.columns(3)
with col1:
    st.button('Decrement', on_click=decrement)  #calling the increment func on 'click' action
with col2:
    st.write('Count : ',st.session_state.count)
with col3:
    st.button('Increment', on_click=increment)  #calling the decrement func on 'click' action
    
st.divider()

#slider
st.title("Slider")
if 'volume' not in st.session_state:
    st.session_state.volume = 50
    
#create a slider
st.slider(
    'Volume',
    min_value = 0,
    max_value = 100,
    key = 'volume'
)

st.write('Volume : ',st.session_state.volume)

st.divider()

#metric
st.title("Metric")

a,b,c = st.columns(3)
a.metric(label="Temperature", value="37 °C", delta="4 °C", border=True)
b.metric("Wind", "4 mph", "-2 mph", border=True)
c.metric("Humidity", "77%", "5%", border=True)

changes = np.random.standard_normal(25)
delta = round(changes[3],2)


st.metric("Line", 10, delta=delta, chart_data = changes, chart_type = "line", border=True)
st.metric("Area", 10, delta=delta, chart_data = changes, chart_type = "area", border=True)

st.divider()