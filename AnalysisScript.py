import pandas as pd
import os

def main():
    try:
        os.system('clear')

        files = []

        for i in range(2):
            file = input(f"\n\033[96mEnter the name of the CSV file \033[1m{'before' if i == 0 else 'after'}\033[0m \033[96mthe regression: \033[0m")

            if not (os.path.exists(file) and file != "" and file.lower().endswith('.csv')):
                print(f"\n\n\033[91mFile '{file}' not found or is not a valid CSV file.\n\033[0m")

                file = input("\n\033[96mPlease enter a valid CSV file name: \033[0m\n")
            else:
                print("\033[92m\n\n   File was successfully inserted!   \n\033[0m")
                files.append(file)

        generateFiles(files[0], files[1])
    except KeyboardInterrupt as e:
        print(f"\n\n\033[91m   Error while reading files {e}   \n\033[0m")

def treatData(before_file, after_file):
    try:
        df_before = pd.read_csv(before_file).fillna('')
        df_after = pd.read_csv(after_file).fillna('')

        if df_before is None or df_after is None:
            raise print(f"\n\n\033[91m{Exception}\033[0m")

        columns_before = df_before.columns.tolist()
        columns_after = df_after.columns.tolist()

        merged = pd.merge(df_before, df_after, left_on=columns_before[0], right_on=columns_after[0], how='outer', indicator=True, suffixes=('_Bifor', '_Afta'))

        missing_before = merged[merged['_merge'] == 'left_only'].filter(regex='^(?!.*_Bifor).*$')
        missing_after = merged[merged['_merge'] == 'right_only'].filter(regex='^(?!.*_Afta).*$')

        before_sorted = missing_before.sort_values(by=columns_before[0]).drop('_merge', axis=1)
        after_sorted = missing_after.sort_values(by=columns_after[0]).drop('_merge', axis=1)

        before_sorted.columns = [col.replace('_Bifor', '') for col in df_before.columns]
        after_sorted.columns = [col.replace('_Afta', '') for col in df_after.columns]

        return before_sorted, after_sorted

    except KeyboardInterrupt as e:
        print(f"\033[91mError while processing files: {e}\033[0m")

def extraLines(before_file, after_file):
    try:
        df_before = pd.read_csv(before_file).fillna('')
        df_after = pd.read_csv(after_file).fillna('')

        columns_before = df_before.columns.tolist()
        columns_after = df_after.columns.tolist()

        if 'Time (ms)' in columns_before and 'Time (ms)' in columns_after:
            df_before = df_before.drop(columns=['Time (ms)'])
            df_after = df_after.drop(columns=['Time (ms)'])

        merged = pd.merge(df_before, df_after, how='right', indicator=True)

        lines_merged = merged[merged['_merge'] == 'right_only'].drop('_merge', axis=1)

        b_sorted = df_before.sort_values(by=df_before.columns[0])
        a_sorted = lines_merged.sort_values(by=lines_merged.columns[0])

        lines_after = a_sorted[~a_sorted.isin(b_sorted)].dropna()

        return lines_after

    except KeyboardInterrupt as e:
        print(f"\033[91mError while analyzing and saving extra lines: {e}\033[0m")


def generateFiles(before_file, after_file):
    try:
        print("\033[96m\n   Generating CSV files...   \n\n\033[0m")

        df_before, df_after = treatData(before_file, after_file)
        df_extraLines = extraLines(before_file, after_file)

        output_before_file = "New-Before.csv"
        output_after_file = "New-After.csv"
        output_extra_file = "Extra-Lines-After.csv"

        file_names = [output_before_file, output_after_file, output_extra_file]
        data_frames = [df_before, df_after, df_extraLines]

        for file_name, df in zip(file_names, data_frames):
            i = 0
            base_name, extension = os.path.splitext(file_name)
            new_file_name = file_name

            while os.path.exists(new_file_name):
                i += 1
                new_file_name = f"{base_name} ({i}){extension}"

            df.to_csv(new_file_name, index=False)

            print(f"\033[92mResults saved in '{new_file_name}'\033[0m")

    except KeyboardInterrupt as e:
        print(f"\033[91mError while generating files: {e}\033[0m")


if __name__ == "__main__":
    main()