import pandas as pd
import os

# replace with your folder's path
folder_path = './resultados_csv/'

all_files = os.listdir(folder_path)

# Filter out non-CSV files
csv_files = [f for f in all_files if f.endswith('.csv')]

# Create a list to hold the dataframes
df_list = []

for csv in csv_files:
    file_path = os.path.join(folder_path, csv)
    try:
        # Try reading the file using default UTF-8 encoding
        df = pd.read_csv(file_path)
        df[['matricula_docente', 'matricula']] = df[['matricula_docente', 'matricula']].astype('Int64')
        df['total_faltas'] = df['total_faltas'].apply(lambda x: int(x))
        df_list.append(df)
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, try reading the file using UTF-16 encoding with tab separator
            df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
            df_list.append(df)
        except Exception as e:
            print(f"Could not read file {csv} because of error: {e}")
    except Exception as e:
        print(f"Could not read file {csv} because of error: {e}")

# Concatenate all data into one DataFrame
big_df = pd.concat(df_list, ignore_index=True)
big_df[['matricula_docente', 'matricula']] = big_df[['matricula_docente', 'matricula']].astype(object)
big_df = big_df.replace(-1, "-1.0")

# Save the final result to a new CSV file
big_df.to_csv(os.path.join(folder_path, 'combined_file.csv'), index=False)