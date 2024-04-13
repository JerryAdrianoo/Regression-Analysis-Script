import pandas as pd
import os
import sys
    
def main(file):
    i = 0
    while i < 2:
        if os.path.exists(file) and file != "" and file.lower().endswith('.csv'):
            print("Arquivo encontrado com sucesso!")
            break
        else:
            print(f"Arquivo '{file}' não encontrado ou não é um arquivo CSV válido.\n")
            file = input("Digite novamente o nome do arquivo CSV:\n ")
            i += 1
    if i == 2:
        sys.tracebacklimit = 0
        raise Exception("\n\nArquivo não encontrado. Encerrando script.")
    return file

def InsertFiles(before_file, after_file):
    try:
        
        df_before = pd.read_csv(before_file).fillna('')
        df_after = pd.read_csv(after_file).fillna('')
        columns_before = df_before.columns.tolist()
        columns_after = df_after.columns.tolist()
        merged = pd.merge(df_before, df_after, on='Reverse Call Tree', how='outer', indicator=True, suffixes=('_Before', '_After'))
        missing_before = merged[merged['_merge'] == 'left_only']
        missing_after = merged[merged['_merge'] == 'right_only']
        before_sorted = missing_before.sort_values(by=columns_before[0])
        after_sorted = missing_after.sort_values(by=columns_after[0])
        
        return before_sorted, after_sorted
    except Exception as e:
        raise e

def cleanData(before_file, after_file):
    try:
        df_before, df_after = InsertFiles(before_file, after_file)

        output_before_file = "New-Before.csv"
        output_after_file = "New-After.csv"

        print("Gerando arquivos CSV...")
        df_before.to_csv(output_before_file, index=False)
        df_after.to_csv(output_after_file, index=False)
        print(f"\nResultados salvos em '{output_before_file}' e '{output_after_file}'")

    except Exception as e:
        print(f"Erro ao limpar dados: {e}")


before_file = input("Digite o nome do primeiro arquivo CSV:\n ")
before_file = main(before_file)
after_file = input("\nDigite o nome do segundo arquivo CSV:\n ")
after_file = main(after_file)

cleanData(before_file, after_file)