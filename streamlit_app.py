import streamlit as st
import pandas as pd
from itertools import combinations
import copy
import matplotlib.pyplot as plt
import numpy as np


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

    return pd.read_csv(file_name, header=None)


# Main code:

st.title("My new app")

# Check validity of file:

df = checkingFile()

# List of essential variables:

essential_variables = ["id", "salary", "gender", "ethnicity", "job function", "job family", "job group", "job level", "pay grade", "geo location", "pay differential"]
collecting_variables = []
official_variables_list = []

# Checking for variables in file that match with essential variables:

# Get the entire list of variables from the data frame:
variable_names = df.iloc[0].tolist()

# Extract the variables from th list:
salary_index = 0 # For converting Salary to categorical data
counter = 0
for column in variable_names:

    if column.lower() in essential_variables:

        if column.lower() == "salary":
            salary_index = counter

        collecting_variables.append(column.lower())
        official_variables_list.append(df.iloc[1, counter])

    elif "Text" in column:

        if df.iloc[1, counter].lower() in essential_variables:

            collecting_variables.append(df.iloc[1, counter].lower())
            official_variables_list.append(df.iloc[1, counter])

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

    st.header("Here is a summary of the individual relationships between your essential variables: ")

    # File contains all necessary variables and can proceed with analysis: 

    # Prep information (Aggregate the data):

    # Set column names to the second row:

    df.columns = df.iloc[1] 

    # Remove the first two rows (header and the data that became headers):
    df = df[2:]

    # Reset index to clean up any residual index issues:

    df.reset_index(drop=True, inplace=True)

     # For non-categorical, numeric data (Salary) sort into categories/ranges:

    # Convert the column at Salary index to numeric
    df.iloc[:, salary_index] = pd.to_numeric(df.iloc[:, salary_index], errors='coerce')

    # Define bin edges based on data statistics
    min_value = df.iloc[:, salary_index].min()
    max_value = df.iloc[:, salary_index].max()
    bin_edges = np.linspace(min_value, max_value, num=21)  # 20 bins

    # Automatically generate bins
    df["Salary_Binned"] = pd.cut(df.iloc[:, salary_index], bins=bin_edges)

    # Drop the original Salary column
    df = df.drop(df.columns[salary_index], axis=1)

    # Rename the binned column to 'Salary':
    df = df.rename(columns={'Salary_Binned': 'Salary'})

    # Generate all combinations of essential variables of length 2:

    variable_combinations = list(combinations(official_variables_list, 2))

    # Present it with a visual (create bar graph):

    for combo in variable_combinations:

        # Extract unique value combos from variable and variable:
        value_combinations = df[[combo[0], combo[1]]].drop_duplicates()

        # Convert DataFrame to a NumPy record array:
        record_array = value_combinations.to_records(index=False)

        # Create a list of tuples with unique value combos and their frequencies:
        value_combo_list = []

        # Count the number of occurrences in each value combo:
        for value_combo in record_array:

            # Define the values you want to match:
            value1 = value_combo[0]
            value2 = value_combo[1]
            
            # Filter rows where both conditions are met:

            filtered_df = df[(df[f"{combo[0]}"] == value1) & (df[f"{combo[1]}"] == value2)]

            # Count the number of such entries:
            count = filtered_df.shape[0]

            a_tuple = (str(value1) + " and " + str(value2), count)

            value_combo_list.append(a_tuple)

        # Plot the variable combo:

        # Create a new figure for each combination:
        fig, ax = plt.subplots(layout='constrained')

        # The label locations:
        x = np.arange(len(value_combo_list))
        width = 0.25  # the width of the bars
        multiplier = 0

        for attribute, combo_value in value_combo_list:

            offset = width * multiplier
            rects = ax.bar(x + offset, attribute, width, label=combo_value)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel("Frequencies")
        ax.set_title(f"Frequency of {combo[1]} within {combo[0]}")
        ax.set_xticks(x + width, combo[0])
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim(0, 250)

        plt.show()


