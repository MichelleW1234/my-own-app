import streamlit as st
import pandas as pd

# Note: For running streamlit app through VSCode: streamlit run streamlit_app.py

# Helper methods:

def rerunFile():

    st.rerun




# Main code:

st.title("My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)


# Create a file uploader widget and checking for valid file:

try:

    fileName = st.file_uploader("Please input a csv file", type="csv")

except pd.errors.EmptyDataError:
                
    st.error("The file is empty. Please try again.")

    # Rerun the app to clear error message

    rerunFile()

            
except pd.errors.ParserError:
            
    st.error("There was an error parsing the file. Please ensure the file is a valid CSV.")

    # Rerun the app to clear error message

    rerunFile()
            
except Exception as e:
            
     # Displaying error message in the Streamlit app: 

    st.error(f"An error occurred: {e}")

    # Rerun the app to clear error message

    rerunFile()
           
        
# Read the CSV file into a DataFrame (CSV is in format of Pay Equity Instruction and Data Template)

df = pd.read_csv(fileName)

# Display the DataFrame

print(df)



# Prep information ()


# Present it with a visual (create bar graph)



