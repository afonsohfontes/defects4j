import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast

# Load your dataset
file_path = 'unified_dataset_filtered.csv'
data = pd.read_csv(file_path)

# Function to clean and align bitstrings
def clean_and_align_bitstrings(timeline, coverage_bitstring):
    clean_timeline = ["".join(filter(lambda x: x in ['0', '1'], bs)) for bs in timeline]
    length = len(str(coverage_bitstring))
    aligned_timeline = [bs.ljust(length, '0')[:length] for bs in clean_timeline]
    return aligned_timeline

# Function to apply adjusted cumulative coverage logic
def adjusted_cumulative_coverage(timeline):
    cumulative_timeline = []
    cumulative_bits = '0' * len(timeline[0])

    for bitstring in timeline:
        new_bits = ''
        for index, bit in enumerate(bitstring):
            new_bit = '1' if bit == '1' or cumulative_bits[index] == '1' else '0'
            new_bits += new_bit
        cumulative_bits = new_bits
        cumulative_timeline.append(new_bits)

    return cumulative_timeline

# Function to plot timeline as dots
def plot_timeline_as_dots(timeline, title="Dot Plot of Cumulative Coverage Timeline"):
    plt.figure(figsize=(12, 6))

    for y, bitstring in enumerate(timeline):
        for x, bit in enumerate(bitstring):
            color = 'blue' if bit == '1' else 'red'
            plt.plot(x, y, 'o', color=color)

    plt.title(title)
    plt.xlabel('Bit Position')
    plt.ylabel('Timeline Entry')
    plt.grid(True)
    plt.show()

# Preprocess the BranchBitstringTimeline column
data['BranchBitstringTimeline'] = data['BranchBitstringTimeline'].apply(ast.literal_eval)
data['AlignedTimeline'] = data.apply(lambda row: clean_and_align_bitstrings(row['BranchBitstringTimeline'], row['BranchCoverageBitString']), axis=1)

# Apply the adjusted cumulative coverage logic
data['CumulativeCoverageTimeline'] = data['AlignedTimeline'].apply(adjusted_cumulative_coverage)

# ...

# Function to calculate coverage for each bitstring
def calculate_coverage(bitstring):
    bit_sum = sum(int(bit) for bit in bitstring)
    return bit_sum / len(bitstring) if len(bitstring) > 0 else 0

# Apply the function to create BranchCoverageTimelineV2
data['BranchCoverageTimelineV2'] = data['CumulativeCoverageTimeline'].apply(lambda timeline: [calculate_coverage(bs) for bs in timeline])

# Now you can save the DataFrame with the new column
output_file_path = 'processed_dataset_with_coverage_v2.csv'  # Update the file path as needed
data.to_csv(output_file_path, index=False)


#for index in range(len(data)):
#    plot_timeline_as_dots(data.loc[index, 'CumulativeCoverageTimeline'], title=f"Dot Plot of Entry {index}")

data.drop(columns=['BranchBitstringTimeline'], inplace=True)
data.drop(columns=['CumulativeCoverageTimeline'], inplace=True)
data.drop(columns=['AlignedTimeline'], inplace=True)


# Function to plot coverage evolution over time
def plot_coverage_evolution(coverage_timeline, title="Coverage Evolution Over Time"):
    plt.figure(figsize=(12, 6))
    plt.plot(coverage_timeline, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel('Timeline Entry')
    plt.ylabel('Coverage Proportion')
    plt.grid(True)
    plt.show()

# Iterate and plot coverage evolution for each entry
#for index, row in data.iterrows():
#    plot_coverage_evolution(row['BranchCoverageTimelineV2'], title=f"Coverage Evolution for Entry {index}")


output_file_path = '4-processed_dataset-parcial.csv'  # Replace with your desired output file path
data.to_csv(output_file_path, index=False)

