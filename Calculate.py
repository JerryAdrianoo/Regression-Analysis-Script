import csv
import statistics
import os

def process_csv_files(csv_files):
    all_data = []

    # Iterar sobre cada arquivo CSV
    for csv_file in csv_files:
        try:
            # Abrir o arquivo CSV e ler os dados
            with open(csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                data = list(reader)

                # Adicionar os dados do arquivo à lista geral
                all_data.extend(data)

        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found. Skipping.")
        except Exception as e:
            print(f"Error processing file '{csv_file}': {e}. Skipping.")

    # Se houver dados válidos coletados
    if all_data:
        # Extrair os valores dos campos de interesse (exemplo: 'Mean', 'Median', 'StdDev')
        values = [float(row['Value']) for row in all_data]

        # Calcular estatísticas a partir dos valores coletados
        if values:
            final_mean = statistics.mean(values)
            final_median = statistics.median(values)
            final_std_dev = statistics.stdev(values) if len(values) > 1 else 0

            # Escrever os resultados em um novo arquivo CSV
            output_filename = 'combined_statistics_results.csv'
            with open(output_filename, 'w', newline='') as csvfile:
                fieldnames = ['Statistic', 'Value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Statistic': 'Final Mean', 'Value': final_mean})
                writer.writerow({'Statistic': 'Final Median', 'Value': final_median})
                writer.writerow({'Statistic': 'Final Standard Deviation', 'Value': final_std_dev})

            print(f"Combined statistics results saved to '{output_filename}'.")
        else:
            print("No valid data found to process.")
    else:
        print("No valid data found to process.")

def main():
    print("Choose an option:")
    print("1. Calculate statistics from input values")
    print("2. Process CSV files to calculate statistics")

    option = input("Enter your choice (1 or 2): ")

    if option == '1':
        user_input = input("Enter values separated by spaces: ")
        values_str = user_input.split()

        try:
            mean, median, std_dev = calculate_statistics(values_str)
            print(f"Mean: {mean}")
            print(f"Median: {median}")
            print(f"Standard Deviation: {std_dev}")

            base_filename = 'results.csv'
            filename = base_filename
            count = 1
            while os.path.exists(filename):
                filename = f"{base_filename[:-4]}({count}).csv"
                count += 1

            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Type', 'Value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Type': 'Mean', 'Value': mean})
                writer.writerow({'Type': 'Median', 'Value': median})
                writer.writerow({'Type': 'Standard Deviation', 'Value': std_dev})
            
            print(f"Results saved to '{filename}'.")

        except ValueError:
            print("Error: Invalid input values.")

    elif option == '2':
        # Solicitar ao usuário os nomes dos arquivos CSV separados por vírgula
        input_csv_files = input("Enter CSV file names separated by spaces: ")
        csv_files = [filename.strip() for filename in input_csv_files.split()]

        # Chamar a função para processar os arquivos CSV
        process_csv_files(csv_files)

    else:
        print("Invalid option. Please choose either 1 or 2.")

if __name__ == "__main__":
    main()
