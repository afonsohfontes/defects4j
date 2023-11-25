import pandas as pd

# Load the data
df = pd.read_csv('/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/unified_dataset.csv')

# Remove empty columns
df = df.dropna(axis=1, how='all')

# Remove the branch bitstring timeline column
if 'BranchCoverageBitStringTimeline' in df.columns:
    df = df.drop(columns=['BranchCoverageBitStringTimeline'])
# Remove the branch bitstring timeline column
if 'BranchBitstringTimeline' in df.columns:
    df = df.drop(columns=['BranchBitstringTimeline'])

# Save the filtered data to a new CSV file
df.to_csv('/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/rq1-2-filtered_dataset.csv', index=False)