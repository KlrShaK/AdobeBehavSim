import pandas as pd

# Path to your Excel file
file_path = 'behaviour_content_simulation_train.xlsx'
# Path where you want to save the modified file
new_file_path = 'behavSimChallSmall.xlsx'

# Load the Excel file
df = pd.read_excel(file_path)

# Check if the file has more than 1000 lines
if len(df) > 1000:
    # Keep only the first 1000 lines
    df = df.iloc[:1000]

# Save the modified DataFrame back to an Excel file
df.to_excel(new_file_path, index=False)
