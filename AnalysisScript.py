import pandas as pd
import os

def main():
    os.system('clear')
    files = []

    for i in range(2):
        file = input(f"Enter the name of the CSV file {'before' if i == 0 else 'after'} the regression: ")

        while not (os.path.exists(file) and file != "" and file.lower().endswith('.csv')):
            print(f"\nFile '{file}' not found or is not a valid CSV file.\n")
            file = input("\nPlease enter a valid CSV file name:\n ")

        print("\n   File was successfully inserted!   \n")
        files.append(file)
    generateFiles(files[0], files[1])

def treatData(before_file, after_file):
    try:
        df_before = pd.read_csv(before_file).fillna('')
        df_after = pd.read_csv(after_file).fillna('')
        
        if df_before is None or df_after is None:
            raise print(Exception)
        
        columns_before = df_before.columns.tolist()
        columns_after = df_after.columns.tolist()
        
        merged = pd.merge(df_before, df_after, left_on=columns_before[0], right_on=columns_before[0], how='outer', indicator=True, suffixes=('_Before', '_After'))
        missing_before = merged[merged['_merge'] == 'left_only'].filter(regex='^(?!.*_After).*$')
        missing_after = merged[merged['_merge'] == 'right_only'].filter(regex='^(?!.*_Before).*$')
        
        before_sorted = missing_before.sort_values(by=columns_before[0]).drop('_merge', axis=1)
        after_sorted = missing_after.sort_values(by=columns_after[0]).drop('_merge', axis=1)
        
        before_sorted.columns = [col.replace('_Before', '') for col in df_before.columns]
        after_sorted.columns = [col.replace('_After', '') for col in df_after.columns]
        
        return before_sorted, after_sorted
    except Exception as e:
        print(f"Error while processing files: {e}")

def generateFiles(before_file, after_file):
    try:
        print("\n   Generating CSV files...   ")
        df_before, df_after = treatData(before_file, after_file)

        output_before_file = "New-Before.csv"
        output_after_file = "New-After.csv"

        i = 0
        while os.path.exists(output_before_file):
            i += 1
            output_before_file = f"New-Before{i}.csv"

        df_before.to_csv(output_before_file, index=False)

        i = 0
        while os.path.exists(output_after_file):
            i += 1
            output_after_file = f"New-After{i}.csv"

        df_after.to_csv(output_after_file, index=False)

        print(f"\nResults saved in '{output_before_file}' and '{output_after_file}'")

    except Exception as e:
        print(f"Error while generating files: {e}")

if __name__ == "__main__":
    main()