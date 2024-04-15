import pandas as pd
import os

def main():
    os.system('clear')

    files = []

    for i in range(2):
        file = input(f"\nEnter the name of the CSV file {'before' if i == 0 else 'after'} the regression: ")

        while not (os.path.exists(file) and file != "" and file.lower().endswith('.csv')):
            print(f"\nFile '{file}' not found or is not a valid CSV file.\n")

            file = input("\nPlease enter a valid CSV file name: ")

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

        missing_before = merged[merged['_merge'] == 'left_only'].filter(regex='^(?!.*_Before).*$')
        missing_after = merged[merged['_merge'] == 'right_only'].filter(regex='^(?!.*_After).*$')

        before_sorted = missing_before.sort_values(by=columns_before[0]).drop('_merge', axis=1)
        after_sorted = missing_after.sort_values(by=columns_after[0]).drop('_merge', axis=1)

        before_sorted.columns = [col.replace('_Before', '') for col in df_before.columns]
        after_sorted.columns = [col.replace('_After', '') for col in df_after.columns]

        return before_sorted, after_sorted

    except Exception as e:
        print(f"Error while processing files: {e}")

def extraLines(before_file, after_file):
    try:
        df_before = pd.read_csv(before_file).fillna('')
        df_after = pd.read_csv(after_file).fillna('')
        
        columns_before = df_before.columns.tolist()
        columns_after = df_after.columns.tolist()
        
        if 'Time (ms)' in columns_before and 'Time (ms)' in columns_after:
            df_before_new = df_before.drop(columns=['Time (ms)'])
            df_after_new = df_after.drop(columns=['Time (ms)'])
        
            merged = pd.merge(df_before_new, df_after_new, how='right', indicator=True)

            lines_merged = merged[merged['_merge'] == 'right_only'].drop('_merge', axis=1)

            b_sorted = df_before_new.sort_values(by=df_before_new.columns[0])
            a_sorted = lines_merged.sort_values(by=lines_merged.columns[0])

            lines_after = a_sorted[~a_sorted.isin(b_sorted)].dropna()
        else:
            merged = pd.merge(df_before, df_after, how='right', indicator=True)

            lines_merged = merged[merged['_merge'] == 'right_only'].drop('_merge', axis=1)

            b_sorted = df_before.sort_values(by=df_before.columns[0])
            a_sorted = lines_merged.sort_values(by=lines_merged.columns[0])

            lines_after = a_sorted[~a_sorted.isin(b_sorted)].dropna()

        return lines_after

    except Exception as e:
        print(f"Error while analyzing and saving extra lines: {e}")


def generateFiles(before_file, after_file):
    try:
        print("\n   Generating CSV files...   \n")

        df_before, df_after = treatData(before_file, after_file)
        df_extraLines = extraLines(before_file, after_file)

        output_before_file = "New-Before.csv"
        output_after_file = "New-After.csv"
        output_extra_file = "Extra-Lines-After.csv"

        file_names = [output_before_file, output_after_file, output_extra_file]
        data_frames = [df_before, df_after, df_extraLines]

        for file_name, df in zip(file_names, data_frames):
            i = 0
            while os.path.exists(file_name):
                i += 1
                file_name = f"{file_name.split('.')[0]} ({i}).csv"

            df.to_csv(file_name, index=False)
            print(f"Results saved in '{file_name}'")

    except Exception as e:
        print(f"Error while generating files: {e}")


if __name__ == "__main__":
    main()