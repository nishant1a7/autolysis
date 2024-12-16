import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import openai

plt.switch_backend('Agg')

if "AIPROXY_TOKEN" not in os.environ:
    print("Error: AIPROXY_TOKEN environment variable not set.")
    sys.exit(1)

token = os.environ["AIPROXY_TOKEN"]
openai.api_key = token

def analyze_csv(filename):
    try:
        data = pd.read_csv(filename)
        report = {
            "summary_stats": data.describe(include='all').to_dict(),
            "missing_values": data.isnull().sum().to_dict(),
            "column_types": data.dtypes.apply(str).to_dict()
        }
        if not data.select_dtypes(include=[np.number]).empty:
            report["correlations"] = data.corr().to_dict()
        report["example_values"] = data.head(3).to_dict()
        return data, report
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)

def visualize_data(data, output_dir):
    try:
        charts = []
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            plt.figure()
            sns.histplot(data[col].dropna(), kde=True)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            chart_path = os.path.join(output_dir, f"{col}_distribution.png")
            plt.savefig(chart_path)
            charts.append(chart_path)
        if not data.select_dtypes(include=[np.number]).empty:
            plt.figure(figsize=(10, 8))
            sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Correlation Heatmap")
            heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
            plt.savefig(heatmap_path)
            charts.append(heatmap_path)
        return charts
    except Exception as e:
        print(f"Error creating visualizations: {e}")
        sys.exit(1)

def generate_story(data_summary, charts):
    try:
        prompt = f"""
        You are an AI data analyst. Here's the summary of a dataset:

        - Summary statistics: {data_summary["summary_stats"]}
        - Missing values: {data_summary["missing_values"]}
        - Column types: {data_summary["column_types"]}
        - Correlations: {data_summary.get("correlations", "None")}
        - Example values: {data_summary["example_values"]}

        Write a narrative explaining:
        1. The dataset in simple terms.
        2. Key findings from the analysis.
        3. Insights from visualizations.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error generating story: {e}")
        sys.exit(1)

def save_markdown(output_dir, story, charts):
    try:
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write("# Automated Data Analysis\n\n")
            f.write(story + "\n\n")
            for chart in charts:
                chart_name = os.path.basename(chart)
                f.write(f"![{chart_name}]({chart_name})\n\n")
        print(f"Markdown file saved at {readme_path}")
    except Exception as e:
        print(f"Error saving Markdown: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = os.path.splitext(input_file)[0]
    os.makedirs(output_dir, exist_ok=True)
    data, report = analyze_csv(input_file)
    charts = visualize_data(data, output_dir)
    story = generate_story(report, charts)
    save_markdown(output_dir, story, charts)

if __name__ == "__main__":
    main()
