# LabScript
# Environmental Data Analysis and Visualization

This repository contains a Python script for analyzing and visualizing environmental data related to soil properties. The script loads data from a Google Sheet, processes it, and generates plots for various metrics like soil pH, organic carbon content, volumetric water content and more across different locations and depths.

## Features

- Import environmental data from a Google Sheet.
- Convert relevant columns to numerical values.
- Compute summary statistics for various soil properties.
- Visualize the data using line plots with error bars, for multiple locations and depths.
- Files for computing regression plot and korrelationmatrices.

## Requirements

- Python 3.x
- Required Python libraries:
  - `pandas`
  - `matplotlib`
  - `numpy`
  - 'statsmodels.api'
  - 'scipy'

Install the dependencies using `pip`:

```bash
pip install pandas matplotlib numpy scipy statsmodels
