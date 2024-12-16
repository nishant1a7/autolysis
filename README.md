# Automated Data Analysis Script

This project automates basic data analysis tasks, including:
- Generating summary statistics.
- Visualizing distributions and correlations.
- Creating an analysis report in Markdown format.

## Prerequisites
- Python 3.8 or higher.
- Install the required libraries with `pip install -r requirements.txt`.

## Usage
1. Set the environment variable for your OpenAI API key:
   ```bash
   export AIPROXY_TOKEN=<your_openai_api_key>
   ```
2. Run the script with your dataset:
   ```bash
   python autolysis.py <dataset.csv>
   ```

3. Check the output directory for:
   - Data visualizations.
   - A `README.md` with the generated insights.
