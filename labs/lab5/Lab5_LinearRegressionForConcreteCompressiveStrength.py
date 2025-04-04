
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def load_data(file_path):
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")
    
    df = pd.read_excel(abs_path)
    print("Dataset Info:")
    print(df.info())
    print("\nSummary Statistics:")
    print(df.describe())
    return df


def split_data(df):
    X = df.drop("Concrete compressive strength(MPa, megapascals) ", axis=1)
    y = df["Concrete compressive strength(MPa, megapascals) "]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\nModel Performance:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R² Score: {r2:.2f}")
    return y_pred


def plot_results(y_test, y_pred):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.xlabel("Actual Strength")
    plt.ylabel("Predicted Strength")
    plt.title("Actual vs. Predicted Concrete Strength")
    plt.grid(True)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.tight_layout()
    plt.show()


def plot_residuals(y_test, y_pred):
    residuals = y_test - y_pred
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, residuals, alpha=0.6)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel("Predicted Strength")
    plt.ylabel("Residuals (Actual - Predicted)")
    plt.title("Residual Plot")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    concrete_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "Concrete_Data.xlsx")
    df = load_data(concrete_file_path)
    X_train, X_test, y_train, y_test = split_data(df)
    model = train_model(X_train, y_train)
    y_pred = evaluate_model(model, X_test, y_test)
    plot_results(y_test, y_pred)
    plot_residuals(y_test, y_pred)


if __name__ == "__main__":
    main()
