# Life Cycle Assessment (LCA) Tool – Final Project

Author: Furkan Kağan Ekici
Course: CE49X   
Institution: Bogazici University  
Language: Python 3.8+  

---

## Overview

This project presents a modular Python-based Life Cycle Assessment (LCA) tool for evaluating the environmental impact of products and materials. It allows users to assess the sustainability of items by calculating carbon emissions, energy usage, water consumption, and waste generation throughout various stages of the product life cycle. The tool supports data import, computation, visualization, and reporting.

---

## Key Functionalities

- Supports data input from `.csv` and `.json` files.
- Performs life cycle impact calculations using stage- and material-specific conversion factors.
- Normalizes impact data for comparison across products.
- Generates summary statistics and structured outputs in both tabular and JSON format.
- Provides multiple visualization options such as pie charts, bar graphs, radar plots, and heatmaps.

---

## Project Structure

```plaintext
.
├── data-raw/
│   ├── sample_data.csv           # Input data for life cycle inventory
│   └── impact_factors.json       # Environmental impact factors
│
├── notebooks/
│   └── lca_analysis_example.ipynb # Demonstration notebook for interactive analysis
│
├── results/
│   ├── stage_impacts.csv          # Impact data per product and stage
│   ├── total_impacts.json         # Aggregated product-level impacts
│   ├── normalized_impacts.json    # Normalized values for comparison
│   ├── comparison.csv             # Comparison between selected product IDs
│   ├── summary_report.json        # Metadata and descriptive summary
│   └── plots/
│       ├── carbon_impact.png            # Pie chart: carbon by material
│       ├── life_cycle_impact.png        # Bar chart: life cycle impacts
│       ├── product_comparison.png       # Radar chart: product comparison
│       ├── end_of_life_breakdown.png    # Stacked bar chart: EoL breakdown
│       └── impact_correlation.png       # Heatmap of impact correlations
│
├── src/
│   ├── __init__.py               # Package initializer for src module
│   ├── data_input.py             # Data loading, validation, cleaning functions
│   ├── calculations.py           # Main class for LCA impact computations
│   ├── utils.py                  # Helper functions for unit conversion, saving, etc.
│   └── visualization.py          # Functions to generate plots
│
├── tests/
│   ├── test_data_input.py        # Unit tests for data reading/validation
│   ├── test_calculations.py      # Unit tests for LCA calculations
│   └── test_visualization.py     # Unit tests for plots
│
├── main.py                       # Primary script to run the full LCA analysis
├── requirements.txt              # Dependency list
└── README.md                     # General description file
```

---

## Input Data Format

### Sample Data File (`.csv`, `.xlsx`, `.json`)

The input file should contain life cycle information for products with the following columns:

- `product_id`: Unique product identifier
- `product_name`: Human-readable name
- `life_cycle_stage`: Lifecycle stage (e.g., manufacturing, transportation)
- `material_type`: Material used (e.g., steel, plastic)
- `quantity_kg`: Mass of the material (kg)
- `energy_consumption_kwh`: Energy used (kWh)
- `transport_distance_km`: Distance transported (km)
- `transport_mode`: Transportation method
- `waste_generated_kg`: Waste output (kg)
- `recycling_rate`, `landfill_rate`, `incineration_rate`: Disposal method ratios (0–1)
- `carbon_footprint_kg_co2e`: Direct CO₂ emissions
- `water_usage_liters`: Water usage per stage

### Impact Factors File (`.json`)

Defines how each material contributes to environmental impacts in each life cycle stage.

Structure:
```json
{
  "material_name": {
    "life_cycle_stage": {
      "impact_type": value
    }
  }
}
```

Example:
```json
{
  "steel": {
    "manufacturing": {
      "carbon_impact": 1.8,
      "energy_impact": 20,
      "water_impact": 250
    },
    "disposal": {
      "carbon_impact": 0.1,
      "energy_impact": 0.5,
      "water_impact": 10
    }
  },
  "plastic": {
    "manufacturing": {
      "carbon_impact": 2.5,
      "energy_impact": 70,
      "water_impact": 180
    }
  }
}
```

---

## Output Description

After running `main.py`, the following files will be created under `results/`:

- `stage_impacts.csv`: Per-stage impact values per product
- `total_impacts.json`: Product-level aggregate impacts
- `normalized_impacts.json`: Normalized values between 0–1
- `comparison.csv`: Impact comparison between selected products
- `summary_report.json`: Report with basic statistics and metadata
- Plots (`.png` files) under `results/plots/`:
  - `carbon_impact.png`
  - `life_cycle_impact.png`
  - `product_comparison.png`
  - `end_of_life_breakdown.png`
  - `impact_correlation.png`

---

## Module & API Reference

### 1. Package Initialization (`src/__init__.py`)

Exports important classes and functions to simplify import statements:

- Classes: `DataInput`, `LCACalculator`, `LCAVisualizer`
- Functions: `convert_units`, `save_results`, `create_summary_report`
- Exceptions: `UnitConversionError`, `DataValidationError`, `VisualizationError`

### 2. Data Input Module (`src/data_input.py`)

Handles all data-related operations:
```python
class DataInput:
    def read_data(file_path)
    def validate_data(data)
    def clean_data(data)
    def read_impact_factors(file_path)
```

### 3. Calculations Module (`src/calculations.py`)

Contains logic for LCA computation:
```python
class LCACalculator:
    def __init__(impact_factors_path)
    def calculate_impacts(data, use_impact_factors=True)
    def calculate_total_impacts(impacts)
    def normalize_impacts(impacts)
    def compare_alternatives(impacts, product_ids)
    def get_impact_summary(impacts)
```

### 4. Visualization Module (`src/visualization.py`)

Generates visual representations:
```python
class LCAVisualizer:
    def plot_impact_breakdown(...)
    def plot_life_cycle_impacts(...)
    def plot_product_comparison(...)
    def plot_end_of_life_breakdown(...)
    def plot_impact_correlation(...)
    def close_all_figures()
```

### 5. Utilities Module (`src/utils.py`)

Helper functions across modules:
```python
def convert_units(value, from_unit, to_unit)
def save_results(data, file_path, format)
def load_impact_factors(file_path)
def validate_numeric_range(value, min, max)
def create_summary_report(data, impacts)
def get_supported_units()
```

### 6. Main Script (`main.py`)

Coordinates the entire LCA workflow:
- Loads and preprocesses data
- Executes all impact calculations
- Exports results in standard formats
- Logs all steps for traceability

---

## Error Handling

| Exception               | Cause                                                      |
|-------------------------|------------------------------------------------------------|
| `FileNotFoundError`     | Missing input files (CSV, JSON)                            |
| `UnitConversionError`   | Invalid or unsupported unit conversion                     |
| `ValueError`            | Invalid numeric ranges (e.g., recycling rate > 1.0)        |
| `DataValidationError`   | Missing or incorrect columns in input data                 |

All exceptions are captured and logged via the built-in Python `logging` module.

---

## Conclusion

This LCA tool provides a robust, modular, and reusable framework for performing life cycle assessments on products. It supports transparent calculations, rich data visualization, and structured reporting. With both automated scripting and interactive notebook support, it is suitable for both academic and industrial use cases.