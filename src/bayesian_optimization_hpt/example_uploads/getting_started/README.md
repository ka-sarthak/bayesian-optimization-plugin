# 🚀 Bayesian optimization of Hydrogen Plasma Treatment
Welcome! This tutorial will guide you through using Bayesian optimization of HPT
process parameters.

## 📁 What's inside?
You will find an `analysis` entry of type `BayesianOptimizationHPT` which has a linked
Jupyter notebook. The notebook contains the necessary code conducting Bayesian
optimization and also interact with the `analysis` entry. The notebook uses NOMAD API
to retrieve `analysis` entry, create new entries for the measurements, and overwrite
`analysis` entry with new data.

## 🛠️ How to get started
1. Open the `analysis` entry and go to the DATA tab.
2. Click on the right arrow next to `notebook` quantity. Launch JupyterHub to open the
notebook.
3. Follow the steps in the notebook and run the cells.

You will end up creating entries for the available measurement data, train a surrogate
model, and generate proposals for next measurements. All while adding important metadata
related to the analysis in the `analysis` entry.
