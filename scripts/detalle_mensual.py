import pandas as pd
import os
import sys

def calculate_monthly_billing(file_path, output_file_path):
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
            
            # Ensure 'fecha' and 'precio_total' columns exist
            if 'fecha' in df.columns and 'precio_total' in df.columns:
                df['fecha'] = pd.to_datetime(df['fecha'])
                df['mes'] = df['fecha'].dt.month_name(locale='es_ES') # For Spanish month names
                
                monthly_billing = df.groupby('mes')['precio_total'].sum().reset_index()
                
                # Define a custom order for months
                month_order = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                               'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                monthly_billing['mes'] = pd.Categorical(monthly_billing['mes'], categories=month_order, ordered=True)
                monthly_billing = monthly_billing.sort_values('mes')
                
                print("Facturación mensual para 2025:")
                for index, row in monthly_billing.iterrows():
                    print(f"  {row['mes']}: {row['precio_total']:.2f}")
            else:
                print("Error: 'fecha' or 'precio_total' column not found in the CSV file. Please ensure these columns exist.")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sys.stdout = original_stdout # Reset stdout

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(script_dir, '..', 'datos', 'ventas_2025.csv')
    output_file = os.path.join(script_dir, '..', 'resultados', 'detalle_mensual_2025.txt')
    calculate_monthly_billing(csv_file_path, output_file)
