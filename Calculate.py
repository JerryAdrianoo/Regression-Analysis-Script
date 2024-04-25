import statistics
import csv
import os

def calculate_statistics(values):
    numbers = [float(num) for num in values]
    mean = sum(numbers) / len(numbers)
    median = statistics.median(numbers)
    std_dev = statistics.stdev(numbers)
    return mean, median, std_dev

def main():
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
            filename = f"{base_filename[:-4]} ({count}).csv"
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

if __name__ == "__main__":
    main()
