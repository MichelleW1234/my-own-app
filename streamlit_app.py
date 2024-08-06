import streamlit as st
import pandas as pd
from itertools import combinations
import copy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from string import ascii_letters


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
essential_variables = ["salary", "gender", "ethnicity", "job function", "job family", "job group", "job level", "pay grade", "geo location", "pay differential"]

collecting_variables = []
official_variables_list = []

# Checking for variables in file that match with essential variables:

# Get the entire list of variables from the data frame:
variable_names = df.iloc[0].tolist()

# Extract the variables from th list:
salary_index = 0 # (For converting Salary to categorical data)
counter = 0
for column in variable_names:

    if column.lower() in essential_variables:

        # (For converting Salary to categorical data):
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
# File contains all necessary variables and can proceed with analysis: 

    st.header("Here is a summary of the individual relationships between your essential variables: ")

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

    # Plot each variable combination on a bar graph:
    for combo in variable_combinations:

        # Extract unique value combos from variable 1 and variable 2:
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

            a_tuple = (str(value1), str(value2), count)

            value_combo_list.append(a_tuple)


        # Extract unique values for Variable1 and Variable2:
        variable1_values = sorted(set(vc[0] for vc in value_combo_list))
        variable2_values = sorted(set(vc[1] for vc in value_combo_list))

        # Create a dictionary to map Variable1 values to their frequencies for each Variable2:
        frequency_dict = {var1: {var2: 0 for var2 in variable2_values} for var1 in variable1_values}

        # Fill the dictionary with frequencies:
        for var1, var2, freq in value_combo_list:
            frequency_dict[var1][var2] = freq

        # Prepare the plot:
        fig, ax = plt.subplots(figsize=(12, 8))

        # Set up bar width and positions:
        width = 0.2
        # Increase the space between groups:
        spacing = 0.5  
        x = np.arange(len(variable1_values)) * (width * len(variable2_values) + spacing)

        # Plot bars for each value in Variable2:
        for i, var2 in enumerate(variable2_values):
            heights = [frequency_dict[var1][var2] for var1 in variable1_values]
            ax.bar(x + i * width, heights, width, label=var2)

        # Add labels, title, and legend:
        ax.set_xticks(x + width * (len(variable2_values) - 1) / 2)
        ax.set_xticklabels(variable1_values, rotation=90)  # Rotate x-axis labels
        ax.set_ylabel(f"Frequencies of {combo[1]} within {combo[0]}")
        ax.set_xlabel(f"{combo[0]}")
        ax.set_title(f"{combo[1]} vs. {combo[0]}")
        ax.legend(title='Variable2', loc='upper left', bbox_to_anchor=(1, 1))  # Move legend outside the plot

        # Adjust layout:
        fig.subplots_adjust(top=0.85, bottom=0.15, left=0.15, right=0.95)
        plt.tight_layout(pad=2.0)

        # Display the plot in Streamlit:
        st.pyplot(fig)







'''    
    # Create a heatmap:

    sns.set_theme(style="white")

    # Generate a large random dataset
    rs = np.random.RandomState(33)
    d = pd.DataFrame(data=rs.normal(size=(100, 26)),
                    columns=list(ascii_letters[26:]))

    # Compute the correlation matrix
    corr = d.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

'''