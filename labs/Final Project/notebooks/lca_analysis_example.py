import sys
import os

# HER ŞEYİN ÇALIŞMASI İÇİN EN ÜSTE KOY
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# src klasörünü Python'a tanıt
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, "..", "src"))
if src_path not in sys.path:
    sys.path.append(src_path)

def main():
    from data_input import DataInput
    from calculations import LCACalculator
    from visualization import LCAVisualizer
    import pandas as pd
    import matplotlib.pyplot as plt

    # Data input
    data_input = DataInput()
    product_data = data_input.read_data('../data-raw/sample_data.csv')
    impact_factors = data_input.read_impact_factors('../data-raw/impact_factors.json')

    # Impact calculation
    calculator = LCACalculator(impact_factors_path='../data-raw/impact_factors.json')
    impacts = calculator.calculate_impacts(product_data)

    # Visualization
    visualizer = LCAVisualizer()
    fig = visualizer.plot_impact_breakdown(impacts, 'carbon_impact', 'material_type')
    plt.show()

if __name__ == "__main__":
    main()



# Load product data
product_data = data_input.read_data('../data-raw/sample_data.csv')
print("Product Data Shape:", product_data.shape)
product_data.head()