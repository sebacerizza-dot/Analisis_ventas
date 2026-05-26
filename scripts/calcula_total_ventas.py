import pandas as pd
import os
import sys

def calculate_total_sales(file_path, output_file_path):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Redirect stdout to the output file
    original_stdout = sys.stdout
    with open(output_file_path, 'w') as f:
        sys.stdout = f
        try:
            df = pd.read_csv(file_path)
            if 'precio_total' in df.columns:
                total_sales = df['precio_total'].sum()
                print(f'Total de ventas 2025: {total_sales:.2f}')
            else:
                print("Error: 'precio_total' column not found in the CSV file.")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sys.stdout = original_stdout # Reset stdout

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(script_dir, '..', 'datos', 'ventas_2025.csv')
    output_file = os.path.join(script_dir, '..', 'resultados', 'total_ventas_2025.txt')
    calculate_total_sales(csv_file_path, output_file)
