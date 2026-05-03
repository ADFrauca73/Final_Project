import os
raw_data_path = 'data/original_raw.csv'
vizzes_dir = 'vizzes'

# Create vizzes directory if it doesn't exist
if not os.path.exists(vizzes_dir):
    os.makedirs(vizzes_dir)

# Load the dataset
import pandas as pd
df = pd.read_csv(raw_data_path)
# create a json mapping each column to its unique values
column_unique_values = {col: df[col].unique().tolist() for col in df.columns}
import json
with open(os.path.join(vizzes_dir, 'column_unique_values.json'), 'w') as f:
    json.dump(column_unique_values, f, indent=4)

# drop the names
df = df.drop(columns=['Traveler Name'])

# save the cleaned dataset
cleaned_data_path = 'data/cleaned_data.csv'