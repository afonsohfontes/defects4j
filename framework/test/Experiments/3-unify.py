import pandas as pd
import ast  # For safely evaluating strings as Python literals
import matplotlib.pyplot as plt

def extract_bitstring_array(bitstring_timeline):
    """
    Extracts and cleans bitstrings from the 'BranchBitstringTimeline' column.
    """
    second_array_str = bitstring_timeline.split('array([')[-1].split('])')[0]
    bitstrings = [s.strip().replace('[', '').replace(']', '').replace(' ', '') for s in second_array_str.split(',')]
    cleaned_bitstrings = [''.join(filter(lambda x: x in '01', s)) for s in bitstrings]
    return cleaned_bitstrings

def pad_bitstrings(bitstrings):
    """
    Pads the bitstrings in the array to ensure equal length.
    """
    max_length = max(len(bitstring) for bitstring in bitstrings)
    return [bitstring.ljust(max_length, '0') for bitstring in bitstrings]

def plot_bitstrings(bitstrings):
    """
    Plots the bitstrings with different colors for 0s and 1s.
    """
    plt.figure(figsize=(12, 8))
    for i, bitstring in enumerate(bitstrings):
        for j, bit in enumerate(bitstring):
            color = 'blue' if bit == '1' else 'red'
            plt.plot(j, i, color=color, marker='o', markersize=4 if bit == '0' else 6)
    plt.xlabel('Entry in Array')
    plt.ylabel('Position in Array')
    plt.title('Bitstring Changes Over Time')
    plt.show()

def parsing_function(string_data):
    # Remove 'array', parentheses, and potentially problematic whitespace characters
    clean_data = string_data.replace('array', '').replace('(', '').replace(')', '')
    clean_data = clean_data.replace('\n', '').replace('\20', '').replace('\t', '').replace(' ', '')

    try:
        # Evaluate the cleaned string
        timeline = ast.literal_eval(clean_data)
        return timeline if len(timeline) == 2 else ([], [])
    except Exception as e:
        print(f"Error parsing string: {e}")
        return [], []



def apply_cumulative_coverage(bitstrings, final_coverage_bitstring):
    """Apply cumulative coverage logic to bitstrings based on the final coverage bitstring."""
    cumulative_bitstring = ['0'] * len(final_coverage_bitstring)
    for i, bitstring in enumerate(bitstrings):
        for j, bit in enumerate(bitstring):
            if bit == '1' or (cumulative_bitstring[j] == '1' and final_coverage_bitstring[j] == '1'):
                cumulative_bitstring[j] = '1'
        bitstrings[i] = ''.join(cumulative_bitstring)
    return bitstrings

def calculate_coverage(bitstring):
    """Calculate coverage as the number of '1's divided by the length of the bitstring."""
    if bitstring:
        return bitstring.count('1') / len(bitstring)
    return 0


def apply_cumulative_coverage(bitstrings, final_coverage_bitstring):
    """
    Apply cumulative coverage logic to bitstrings based on the final coverage bitstring.
    """
    cumulative_bitstring = list(final_coverage_bitstring)  # Start with the final coverage bitstring
    aggregated_bitstrings = []

    for bitstring in bitstrings:
        for index, bit in enumerate(bitstring):
            # Update the cumulative bitstring: once a bit is covered, it remains covered
            if bit == '1':
                cumulative_bitstring[index] = '1'
        # Append the current state of the cumulative bitstring to the list
        aggregated_bitstrings.append(''.join(cumulative_bitstring))

    return aggregated_bitstrings

# Example usage:
# final_coverage = '11001'  # This is the final coverage bitstring
# bitstring_timeline = ['00000', '01000', '11000', '10001']  # Sample timeline of bitstrings
# aggregated_timeline = apply_cumulative_coverage(bitstring_timeline, final_coverage)
# print(aggregated_timeline)  # Output: ['00000', '01000', '11000', '11001']

def apply_cumulative_coverage_to_row(row):
    """
    Applies cumulative coverage logic to a single row of the DataFrame.
    """
    # Extract the bitstrings and the final coverage bitstring from the row
    bitstrings = row['BranchBitstringTimeline']
    final_coverage_bitstring = row['BranchCoverageBitString']

    # Apply the cumulative coverage logic
    aggregated_bitstrings = apply_cumulative_coverage(bitstrings, final_coverage_bitstring)

    return aggregated_bitstrings


# Load the reference dataset and create a set of (Project, Bug) IDs
reference_df = pd.read_csv('final_filtered_reduced_dataset.csv')
reference_ids = set(zip(reference_df['Project'], reference_df['Bug']))

# Initialize an empty DataFrame to hold the unified data
unified_df = pd.DataFrame()

# Load each "1-" CSV file, filter and collect the data
csv_files = ['1-complement_data_wave_1.csv', '1-complement_data_wave_2.csv', '1-everyTrialReport.csv']
for file in csv_files:
    temp_df = pd.read_csv(file)
    temp_df['ID_tuple'] = list(zip(temp_df['Project'], temp_df['Bug']))
    temp_df = temp_df[temp_df['ID_tuple'].isin(reference_ids)]
    temp_df = temp_df.drop('ID_tuple', axis=1)
    unified_df = pd.concat([unified_df, temp_df], ignore_index=True)

# Remove entries where 'Generation_success' equals 0
unified_df = unified_df[unified_df['Generation_success'] != 0]

# Save the filtered unified DataFrame to a new CSV
#unified_df.to_csv('unified_dataset_filtered.csv', index=False)

data = unified_df

# Apply the functions
data['BranchBitstringTimeline'] = data['BranchBitstringTimeline'].apply(extract_bitstring_array)
data['BranchBitstringTimeline'] = data['BranchBitstringTimeline'].apply(pad_bitstrings)
data.drop(columns=['BranchCoverageTimeline'], inplace=True)
# Example of plotting the first entry
#plot_bitstrings(data['Padded_Bitstrings'].iloc[0])  # Remove this line if plotting is not needed

# Optionally, save the processed data
data.to_csv('unified_dataset_filtered.csv', index=False)

# Save the first 5 entries to a separate file
data.head(8).to_csv('first_8_entries.csv', index=False)

