import pandas as pd
import os
import sys

def find_top_selling_product(file_path, output_file_path):
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
            
            # Assuming 'producto' for product names and 'cantidad' for quantity sold
            if 'producto' in df.columns and 'cantidad' in df.columns:
                top_product_df = df.groupby('producto')['cantidad'].sum().reset_index()
                most_sold_product = top_product_df.loc[top_product_df['cantidad'].idxmax()]
                
                print(f"El producto más vendido en 2025 es '{most_sold_product['producto']}'.")
            else:
                print("Error: 'producto' or 'cantidad' column not found in the CSV file. Please ensure these columns exist.")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sys.stdout = original_stdout # Reset stdout

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(script_dir, '..', 'datos', 'ventas_2025.csv')
    output_file = os.path.join(script_dir, '..', 'resultados', 'top_ventas_2025.txt')
    find_top_selling_product(csv_file_path, output_file)
