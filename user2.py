import streamlit as st 

st.sidebar.header("MC system")
page = st.sidebar.radio("Select Pape?",
                        ["Home","DataUpload","Predict"])
st.write(f"Home Page:{page}")


upload = st.file_uploader("Upload the File",
                          type=['csv','txt'])
if upload:
    st.write("Name of file",upload.name)

download = st.download_button(
    label="Sample Data",
    data ="hellow world",
    file_name="sample.txt"
)