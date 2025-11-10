#!/usr/bin/env python3
"""
Enhanced Simple Data Analyzer (save summary + save plot)
Usage:
    python3 data_analyzer.py sample_data.csv
    python3 data_analyzer.py sample_data.csv --save summary.csv --plot sales,visitors --saveplot
"""

import argparse
from pathlib import Path
import sys

import pandas as pd

def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path)
    return df

def print_overview(df: pd.DataFrame):
    print("\n=== Data Overview ===")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print("\nColumns and dtypes:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())

def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.empty:
        print("\nNo numeric columns found.")
        return pd.DataFrame()
    summary = numeric_df.agg(['count', 'mean', 'median', 'std', 'min', 'max']).transpose()
    print("\n=== Numeric Summary ===")
    print(summary.round(4))
    return summary

def save_summary(summary: pd.DataFrame, path: Path):
    if summary.empty:
        print("No numeric columns to save.")
        return
    summary.to_csv(path)
    print(f"Summary saved to {path}")

def plot_and_maybe_save(df: pd.DataFrame, cols, save_plot: bool, plot_path: Path):
    import matplotlib.pyplot as plt
    numeric_df = df.select_dtypes(include=["number"])
    cols = [c.strip() for c in cols if c.strip()]
    for col in cols:
        if col not in numeric_df.columns:
            print(f"Skipping plot for '{col}': not a numeric column or not found.")
            continue
        plt.figure()
        numeric_df[col].dropna().hist(bins=20)
        plt.title(f"Histogram: {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        if save_plot:
            plt.savefig(f"{col}_hist.png")  # saves histogram for the column

    # bar chart of column means
    if not numeric_df.empty:
        plt.figure(figsize=(6,4))
        means = numeric_df.mean()
        means.plot(kind='bar')
        plt.title("Mean of numeric columns")
        plt.ylabel("Mean value")
        plt.tight_layout()
        if save_plot:
            plot_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(plot_path)
            print(f"Mean plot saved to {plot_path}")

    if not save_plot:
        print("\nDisplaying plots... (close plot windows to continue)")
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Enhanced Simple Data Analyzer")
    parser.add_argument("csvfile", help="Path to CSV file")
    parser.add_argument("--save", type=str, default="", help="Save numeric summary to CSV (path)")
    parser.add_argument("--plot", type=str, default="", help="Comma-separated numeric columns to plot (histograms)")
    parser.add_argument("--saveplot", action="store_true", help="Save plots to files instead of displaying")
    args = parser.parse_args()

    csv_path = Path(args.csvfile)
    try:
        df = load_data(csv_path)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    print_overview(df)
    summary = numeric_summary(df)

    if args.save:
        save_summary(summary, Path(args.save))

    if args.plot:
        cols = [c.strip() for c in args.plot.split(",") if c.strip()]
        plot_path = Path("plot_means.png")
        plot_and_maybe_save(df, cols, args.saveplot, plot_path)

if __name__ == "__main__":
    main()
