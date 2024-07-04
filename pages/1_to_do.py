### tut (inc free deployment) https://www.youtube.com/watch?v=D0D4Pa22iG0
# streamlit run main.py

import streamlit as st

### STYLE
# Read the CSS file
with open("styles.css") as f:
    css = f.read()

# Inject CSS with st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

### CONTENT

# my_list = [1, 2, 3, 4, 5]
# st.write(my_list)
st.title("To do list:")

my_list = ["Random Worldcat resources button (need requirements doc and Search API to replace num gen approach)"]
st.markdown("* " + "\n* ".join(map(str, my_list)))

st.title("Stewing:")

my_list = ["https://vimeo.com/nwfilmarchive, https://mmuspecialcollections.calmhosting.net/default.aspx"]
st.markdown("* " + "\n* ".join(map(str, my_list)))

st.title("Future ideas:")

my_list = ["Resource usage visualising?"]
st.markdown("* " + "\n* ".join(map(str, my_list)))


st.title("Metrics Example")
st.subheader("Testing it out")

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Temperature", value="70 °F", delta="1.2 °F")
col2.metric(label="Wind", value="9 mph", delta="-8%") 
col3.metric(label="Humidity", value="86%", delta="4%")
col4.metric(label="Coffee :coffee:", delta="4%", value="86%")