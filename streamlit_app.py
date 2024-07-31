import streamlit as st
import pandas as pd

# Note: For running streamlit app through VSCode: streamlit run streamlit_app.py

# Helper methods:

def checkingFile(): 

    # Create a file uploader widget to upload file:

    fileName = st.file_uploader("Please input a csv file", type="csv")

    if fileName is not None:

        # Check for valid CSV file:

        try:

            pass

        except pd.errors.EmptyDataError:
                        
            st.error("The file is empty. Please try again.")
       
        except pd.errors.ParserError:
                    
            st.error("There was an error parsing the file. Please ensure the file is a valid CSV.")
                    
        except Exception as e:
                    
            # Displaying error message in the Streamlit app: 

            st.error(f"An error occurred: {e}")
            
    else:

        st.info("Please upload a CSV file to proceed.")

    return fileName






# Main code:

st.title("My new app")

# Check validity of file:

fileName = checkingFile()

# Read the CSV file into a DataFrame (CSV is in format of Pay Equity Instruction and Data Template)

df = pd.read_csv(fileName)

# Display the DataFrame

print(df)







# Prep information ()


# Present it with a visual (create bar graph)


