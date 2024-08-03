import streamlit as st
import pandas as pd
from itertools import combinations
import copy


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


df = pd.read_csv(file_name, header=None)

# List of essential variables:

essential_variables = ["id", "salary", "gender", "ethnicity", "job function", "job family", "job group", "job level", "pay grade", "geo location", "pay differential"]
collecting_variables = []

# Checking for variables in file that match with essential variables:

# Get the entire list of variables from the data frame:
variable_names = df.iloc[0].tolist()

# Extract the variables from th list:
counter = 0
for column in variable_names:

    if column.lower() in essential_variables:

        collecting_variables.append(column.lower())

    elif "Text" in column:

        print(df.iloc[1, counter].lower())
        if df.iloc[1, counter].lower() in essential_variables:

            collecting_variables.append(df.iloc[1, counter].lower())

    counter = counter+1

if "pay grade" in collecting_variables:

    essential_variables.remove("job level")
        
elif "job level" in collecting_variables:

    essential_variables.remove("pay grade")

if "geo location" in collecting_variables:

    essential_variables.remove("pay differential")

elif "pay differential" in collecting_variables:

    essential_variables.remove("geo location")

if "job function" in collecting_variables:

    essential_variables.remove("job family")
    essential_variables.remove("job group")

elif "job family" in collecting_variables:

    essential_variables.remove("job function")
    essential_variables.remove("job group")

elif "job group" in collecting_variables:

    essential_variables.remove("job function")
    essential_variables.remove("job family")


print("variables in collecting list: ")
print(collecting_variables)
print("variables in essential list: ")
print(essential_variables)

if set(collecting_variables) != set(essential_variables):
    
    essential_variables_copy = copy.deepcopy(essential_variables)

    for variable in essential_variables:
    
        if variable in collecting_variables:

            essential_variables_copy.remove(variable)
          
        else:

            if variable == "job level":

                essential_variables_copy.remove("job level")
                essential_variables_copy.remove("pay grade")
                essential_variables_copy.append("job level or pay grade")
                    
            if variable == "geo location":

                essential_variables_copy.remove("geo location")
                essential_variables_copy.remove("pay differential")
                essential_variables_copy.append("geo location or pay differential")
    
            if variable == "job function":

                essential_variables_copy.remove("job function")
                essential_variables_copy.remove("job family")
                essential_variables_copy.remove("job group")
                essential_variables_copy.append("job function/family/group")

    missing_variables = ""
    for variable in essential_variables_copy:

        missing_variables += "- " + variable + "\n\n"

    st.info("This file doesn't contain the following required variables:\n\n" + missing_variables + "Please choose another CSV file.")

else:

    # File contains all necessary variables and can proceed with analysis: 

    print("Yippee!")

    '''
    # Prep information (Aggregate the data):

    # Generate all combinations of essential variables of length 2:
    variable_combinations = list(combinations(essential_variables, 2))

    # Convert to list of lists:
    variable_combinations = [list(combo) for combo in variable_combinations]

    print(variable_combinations)

    # Count the number of occurrences in each value for each essential variable:

    combination_counts_list = []

    for combos in variable_combinations:

        combination_counts = df.groupby(combos).size().reset_index(name='Count')
        combination_counts_list.append((combos, combination_counts))

        print("Count of each combination:")
        print(combination_counts)












    # MAY USE:

    # Read the CSV file into a DataFrame (loads the entire file as data, including the first and second rows)

    df_raw = pd.read_csv(file_name, header=None)

    # Step 2: Extract column names from the second row (index 1) and drop the first two rows
    variables = df_raw.iloc[1].tolist()  # Extract column names from the second row
    df_clean = df_raw[2:]  # Drop the first two rows

    # Set new column names to the DataFrame:
    df_clean.columns = variables

    # Reset index:
    df_clean.reset_index(drop=True, inplace=True)

    # Present it with a visual (create bar graph)
    '''

