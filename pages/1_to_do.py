### tut (inc free deployment) https://www.youtube.com/watch?v=D0D4Pa22iG0
# streamlit run main.py

import streamlit as st

### STYLE
# set in config.toml

### CONTENT

# my_list = [1, 2, 3, 4, 5]
# st.write(my_list)
st.title("To do list:")

my_list = ["Random Worldcat resources button (needs Search API to replace num gen approach)"]
st.markdown("* " + "\n* ".join(map(str, my_list)))

st.title("Stewing:")

my_list = ["https://vimeo.com/nwfilmarchive",
           "https://mmuspecialcollections.calmhosting.net/default.aspx"]
st.markdown("* " + "\n* ".join(map(str, my_list)))

st.title("Future ideas:")

my_list = ["None here right now :)"]
st.markdown("* " + "\n* ".join(map(str, my_list)))

st.title("Metrics Example")
st.subheader("Testing it out")

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Temperature", value="70 °F", delta="1.2 °F")
col2.metric(label="Wind", value="9 mph", delta="-8%") 
col3.metric(label="Humidity", value="86%", delta="4%")
col4.metric(label="Coffee :coffee:", delta="4%", value="86%")

for item in my_list:
    st.markdown(f"""
    <p>{item}</p>
    """, unsafe_allow_html=True)