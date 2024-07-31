import streamlit as st
import pandas as pd

 # For running streamlit app through VSCode: streamlit run streamlit_app.py

def mainMethod ():

    st.title("My new app")
    st.write(
        "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
    )

    # Call method to check for valid CSV file

    fileName = fileChecking()
        
    # Read the CSV file into a DataFrame (CSV is in format of Pay Equity Instruction and Data Template)

    df = pd.read_csv(fileName)

    # Display the DataFrame

    print(df)



    # Prep information ()


    # Present it with a visual (create bar graph)






def fileChecking():

    # Create a file uploader widget:
    
    fileName = st.file_uploader("Please input a csv file", type="csv")

    # Check if a file has been uploaded:

    if fileName is not None:

        return fileName
           
    else:

        fileChecking()
