import pandas as pd
import numpy as np

def load_data(file_path): 
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:   
        print("Error: File not found.")
        return None

def clean_data(data):  
    if data is None:
        return None
    
    data.fillna(data.mean(), inplace=True)
    
    for column in data.select_dtypes(include=[np.number]).columns:
        mean_col = data[column].mean()
        std_col = data[column].std()
        data = data[(data[column] >= mean_col - 3 * std_col) & (data[column] <= mean_col + 3 * std_col)]
    
    return data

def compute_statistics(data):  
    numeric_columns = [col for col in data.select_dtypes(include=[np.number]).columns if col != 'sample_id']
    
    for column in numeric_columns:
        stats = {
            "Minimum": data[column].min(),
            "Maximum": data[column].max(),
            "Mean": data[column].mean(),
            "Median": data[column].median(),
            "Standard Deviation": data[column].std()
        }
        
        print(f"Statistics for {column}:")
        for key, value in stats.items():
            print(f"{key}: {value:.2f}")
        print("-")

if __name__ == "__main__":  
    file_path = r"C:\Users\furka\OneDrive\Masaüstü\lab\CE49X-repo\datasets\soil_test.csv"
    data = load_data(file_path)
    
    if data is not None:
        data = clean_data(data)
        compute_statistics(data)
