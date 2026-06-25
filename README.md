# DataLens

**DataLens** is a reusable Jupyter Notebook for performing exploratory data analysis (EDA) on CSV datasets.

The notebook provides a structured workflow for inspecting a new dataset, computing descriptive statistics, identifying potential data quality issues, and generating a standard set of visualisations.

It is intended for data scientists, researchers, students, and anyone who wants a quick overview of tabular data before further analysis or machine learning.

---

## Features

The notebook automatically performs the following analyses:

- Load a CSV file into a Pandas DataFrame
- Display dataset dimensions
- Preview the dataset
- Inspect column data types
- Compute descriptive statistics
- Detect missing values
- Detect duplicate rows
- Separate numeric and categorical variables
- Compute a correlation matrix
- Generate histograms
- Generate boxplots
- Generate a scatter matrix
- Generate count plots for categorical variables
- Produce a summary report

Each analysis step is accompanied by detailed explanations describing:

- why the analysis is performed,
- how the statistics are computed,
- and how the resulting plots should be interpreted.

---

## Repository Structure

```
.
├── DataLens_EDA.ipynb     # Main notebook
├── sample_data.csv               # Example dataset
├── README.md
└── LICENSE
```

---

## Requirements

Python 3.10 or newer is recommended.

Install the required packages:

```bash
pip install pandas numpy matplotlib seaborn notebook
```

or

```bash
pip install -r requirements.txt
```

---

## Usage

1. Clone the repository.

```bash
git clone https://github.com/<username>/DataLens.git
```

2. Start Jupyter Notebook.

```bash
jupyter notebook
```

3. Open

```
DataLens_EDA.ipynb
```

4. Set the input file near the beginning of the notebook:

```python
DATA_FILE = "data.csv"
```

5. Run all cells.

The notebook will automatically generate statistics and visualisations for the selected dataset.

---

## Input Data

Any CSV file readable by Pandas can be analysed.

Example:

```python
DATA_FILE = "employees.csv"
```

or

```python
DATA_FILE = "datasets/sales.csv"
```

---

## Generated Analysis

The notebook produces:

- Dataset overview
- Descriptive statistics
- Missing-value report
- Duplicate-row report
- Numeric vs categorical feature identification
- Correlation heatmap
- Histograms
- Boxplots
- Scatter matrix
- Count plots
- Dataset summary

---

## Example Dataset

An example `data.csv` is included to demonstrate the notebook's functionality.

The sample dataset contains:

- Employee ID
- Department
- Age
- Years of experience
- Salary
- Performance score
- Remote working status
- Gender

---

## Intended Use

DataLens is designed as a first-pass exploratory analysis tool before:

- statistical analysis
- feature engineering
- machine learning
- predictive modelling
- dashboard development
- reporting

---

## Future Enhancements

Possible future additions include:

- Automatic outlier detection
- PCA visualisation
- Feature importance estimation
- Statistical hypothesis testing
- Time-series analysis
- Interactive Plotly charts
- Automatic HTML profiling reports
- Export of figures and reports
- Machine learning readiness checks

---

## License

This project is licensed under the Apache License 2.0.

---

## Citation

If you use DataLens in research or teaching, please cite the repository.

A `CITATION.cff` file is recommended for GitHub repositories.

---

## Contributing

Contributions are welcome.

Suggestions, bug reports, and pull requests are appreciated.

---

## Author

Created as a reusable exploratory data analysis notebook for rapid inspection of CSV datasets.
