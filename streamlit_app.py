import streamlit as st
import pandas as pd

# Note: For running streamlit app through VSCode: streamlit run streamlit_app.py

# Helper methods:

def checkingFile(): 

    # Create a file uploader widget to upload file:

    file_name = st.file_uploader("Please input a csv file", type="csv")

    if file_name is not None:

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

    return file_name






# Main code:

st.title("My new app")

# Check validity of file:

file_name = checkingFile()

# Read the CSV file into a DataFrame (CSV is in format of Pay Equity Instruction and Data Template)

df = pd.read_csv(file_name)

# List of essential variables:

essential_variables = ["ID", "Salary", "Gender", "Ethnicity", "Job Function/Family/Group", "Job Level", "Pay Grade", "Geo Location", "Pay Differential"]
collecting_variables = []

# Chrcking for variables in file that match with essential variables:

for column in df.columns:
    
    if column in essential_variables:

        collecting_variables.append(column)

if "Pay Grade" in collecting_variables:

    essential_variables.remove("Job Level")
        
if "Job Level" in collecting_variables:

    essential_variables.remove("Pay Grade")

if "Geo Location" in collecting_variables:

    essential_variables.remove("Pay Differential")

if "Pay Differential" in collecting_variables:

    essential_variables.remove("Geo Location")

essential_set = set(essential_variables)
collecting_set = set(collecting_variables)

if essential_set != collecting_set:

    st.info("This file doesn't contain the minimum variables.")

print("Works!")

# Display the DataFrame

# print(df)







# Prep information ()


# Present it with a visual (create bar graph)


