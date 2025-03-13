import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Function to load and explore the dataset
def load_and_explore_data(file_path):
    """
    Loads wind data from a CSV file, converts timestamps, and checks basic dataset info.
    """
    abs_path = os.path.abspath(file_path)  # Convert relative path to absolute path
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")
    
    df = pd.read_csv(abs_path)  # Read the dataset
    df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp column to datetime
    print(f"Dataset Info for {file_path}:")
    print(df.info())
    print("\nSummary Statistics:")
    print(df.describe())
    return df

# Function to calculate wind speed using u10m and v10m components
def calculate_wind_speed(df):
    """
    Computes wind speed from u10m and v10m components.
    """
    df["wind_speed"] = np.sqrt(df["u10m"]**2 + df["v10m"]**2)
    return df

# Function to extract temporal features like month, season, and hour
def add_temporal_features(df):
    """
    Extracts month, season, and hour from timestamp.
    """
    df["month"] = df["timestamp"].dt.month  # Extract month
    df["hour"] = df["timestamp"].dt.hour  # Extract hour of the day
    
    # Define season mapping
    season_map = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    }
    df["season"] = df["month"].map(season_map)  # Map months to seasons
    return df

# Function to compute monthly wind speed averages
def compute_monthly_averages(df):
    """
    Computes monthly averages for wind speed.
    """
    return df.groupby("month")["wind_speed"].mean()

# Function to compute seasonal wind speed averages
def compute_seasonal_averages(df):
    """
    Computes seasonal averages for wind speed.
    """
    return df.groupby("season")["wind_speed"].mean()

# Function to identify the highest wind speed records
def identify_extreme_wind_speeds(df):
    """
    Finds the timestamps with the highest wind speeds.
    """
    max_speed = df["wind_speed"].max()
    return df[df["wind_speed"] == max_speed]

# Function to compute wind speed patterns for different hours of the day
def compute_diurnal_patterns(df):
    """
    Computes average wind speed per hour of the day.
    """
    return df.groupby("hour")["wind_speed"].mean()

# Function to visualize wind speed comparison between Berlin and Munich
def plot_wind_speed_comparison(berlin_avg, munich_avg, title, xlabel, ylabel):
    """
    Plots wind speed comparisons between Berlin and Munich.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(berlin_avg, marker='o', linestyle='-', label='Berlin')
    plt.plot(munich_avg, marker='s', linestyle='-', label='Munich')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

# Function to plot wind rose diagrams
def plot_wind_rose(df, title):
    """
    Creates a wind rose diagram showing wind direction and speed.
    """
    plt.figure(figsize=(6, 6))
    plt.scatter(df["u10m"], df["v10m"], alpha=0.5)
    plt.xlabel("U Component (m/s)")
    plt.ylabel("V Component (m/s)")
    plt.title(title)
    plt.grid()
    plt.show()

# Define dataset paths using relative paths
berlin_file_path = os.path.join(os.path.dirname(__file__), "../../datasets/berlin_era5_wind_20241231_20241231.csv")
munich_file_path = os.path.join(os.path.dirname(__file__), "../../datasets/munich_era5_wind_20241231_20241231.csv")

# Load datasets
berlin_data = load_and_explore_data(berlin_file_path)
munich_data = load_and_explore_data(munich_file_path)

# Compute wind speed for both cities
berlin_data = calculate_wind_speed(berlin_data)
munich_data = calculate_wind_speed(munich_data)

# Add temporal features to datasets
berlin_data = add_temporal_features(berlin_data)
munich_data = add_temporal_features(munich_data)

# Compute monthly and seasonal wind speed averages
berlin_monthly_avg = compute_monthly_averages(berlin_data)
munich_monthly_avg = compute_monthly_averages(munich_data)
berlin_seasonal_avg = compute_seasonal_averages(berlin_data)
munich_seasonal_avg = compute_seasonal_averages(munich_data)

# Identify extreme wind speeds
extreme_berlin = identify_extreme_wind_speeds(berlin_data)
extreme_munich = identify_extreme_wind_speeds(munich_data)
print("Extreme Wind Speeds - Berlin:")
print(extreme_berlin)
print("\nExtreme Wind Speeds - Munich:")
print(extreme_munich)

# Compute diurnal patterns for wind speed
berlin_diurnal_avg = compute_diurnal_patterns(berlin_data)
munich_diurnal_avg = compute_diurnal_patterns(munich_data)

# Plot wind speed comparisons
plot_wind_speed_comparison(berlin_monthly_avg, munich_monthly_avg, "Monthly Wind Speed Comparison", "Month", "Wind Speed (m/s)")
plot_wind_speed_comparison(berlin_seasonal_avg, munich_seasonal_avg, "Seasonal Wind Speed Comparison", "Season", "Wind Speed (m/s)")
plot_wind_speed_comparison(berlin_diurnal_avg, munich_diurnal_avg, "Diurnal Wind Speed Pattern", "Hour of Day", "Wind Speed (m/s)")

# Plot wind rose diagrams for both cities
plot_wind_rose(berlin_data, "Berlin Wind Rose")
plot_wind_rose(munich_data, "Munich Wind Rose")



#Skyrim is a modal that forecast wind speed, temperature trends, particpation levels and atmospheric pressure,
#it forecasts those things by forecast.py document and common.py script save the forecast results. I think this 
#this data science project is quite clean work even in coding you can see minimal row is prefered to make it more clear.