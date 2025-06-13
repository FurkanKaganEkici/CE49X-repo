import sys
from pathlib import Path
import logging
import pandas as pd

# --- Add 'src' directory to the system path ---
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

# --- Import modules from the src directory ---
from src.data_input import DataInput
from src.calculations import LCACalculator
from utils import (
    convert_units,
    save_results,
    load_impact_factors,
    validate_numeric_range,
    create_summary_report,
    get_supported_units,
    UnitConversionError
)

# --- Define input/output directories and file paths ---
DATA_DIR = BASE_DIR / "data-raw"
RESULTS_DIR = BASE_DIR / "results"
SAMPLE_DATA_PATH = DATA_DIR / "sample_data.csv"
IMPACT_FACTORS_PATH = DATA_DIR / "impact_factors.json"

# --- Configure logging format ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("🚀 Starting LCA Tool...")

    RESULTS_DIR.mkdir(exist_ok=True)

    try:
        # 1. LOAD DATA
        data_input = DataInput()
        raw_data = data_input.read_data(SAMPLE_DATA_PATH)
        logging.info(f"{len(raw_data)} records loaded.")

        # 2. CLEANING & NORMALIZATION
        numeric_columns = [
            'quantity_kg', 'energy_consumption_kwh', 'transport_distance_km',
            'waste_generated_kg', 'recycling_rate', 'landfill_rate',
            'incineration_rate', 'carbon_footprint_kg_co2e', 'water_usage_liters'
        ]

        for col in numeric_columns:
            raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce').fillna(0.0)

        rate_cols = ['recycling_rate', 'landfill_rate', 'incineration_rate']
        default_rates = [0.5, 0.3, 0.2]
        for i, col in enumerate(rate_cols):
            raw_data[col] = raw_data.apply(
                lambda row: default_rates[i] if row[rate_cols].sum() == 0
                else row[col] / row[rate_cols].sum(), axis=1
            )

        cleaned_data = raw_data
        logging.info("✅ Data cleaning and normalization completed.")

        # 3. UTILITY DEMOS
        supported_units = get_supported_units()
        logging.info(f"Supported units: {supported_units}")

        try:
            converted = convert_units(1500, 'kg', 'ton')
            logging.info(f"Unit Conversion: 1500 kg = {converted:.2f} ton")
        except UnitConversionError as e:
            logging.error(f"Unit conversion error: {e}")

        try:
            validate_numeric_range(0.85, 0, 1, name="Recycling Rate")
        except ValueError as e:
            logging.error(f"Range validation error: {e}")

        # 4. LCA CALCULATIONS
        impact_factors = load_impact_factors(IMPACT_FACTORS_PATH)
        calculator = LCACalculator(impact_factors_path=IMPACT_FACTORS_PATH)

        stage_impacts = calculator.calculate_impacts(cleaned_data)
        total_impacts = calculator.calculate_total_impacts(stage_impacts)
        normalized_impacts = calculator.normalize_impacts(total_impacts)
        comparison = calculator.compare_alternatives(total_impacts, ['P001', 'P002'])
        summary = calculator.get_impact_summary(stage_impacts)

        # 5. SAVE RESULTS
        save_results(stage_impacts, RESULTS_DIR / "stage_impacts.csv", format="csv")
        save_results(total_impacts, RESULTS_DIR / "total_impacts.json", format="json")
        save_results(normalized_impacts, RESULTS_DIR / "normalized_impacts.json", format="json")
        save_results(comparison, RESULTS_DIR / "comparison.csv", format="csv")
        save_results(pd.DataFrame([create_summary_report(cleaned_data, stage_impacts)]),
                     RESULTS_DIR / "summary_report.json", format="json")

        logging.info("✅ All computations completed. Results have been saved successfully.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
