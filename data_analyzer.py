# Simple Data Analyzer
# Kriti Bhardwaj – beginner Python project

import pandas as pd

# Load a CSV file
file_path = input("Enter CSV file name (with .csv): ")

try:
    data = pd.read_csv(file_path)
    print("\n✅ File loaded successfully!\n")
except FileNotFoundError:
    print("❌ File not found. Please check the name and try again.")
    exit()

# Show first few rows
print("📋 Preview of data:")
print(data.head())

# Show numeric summary
print("\n📊 Numeric summary:")
print(data.describe())

# Show missing values
print("\n❗ Missing values per column:")
print(data.isnull().sum())
