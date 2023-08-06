# RWTH Notebooks

This project consists of Jupyter Notebook definitions used by RWTH Aachen University. 

Have a look at the [documentation](https://jupyter.pages.rwth-aachen.de/rwth-nb/).

## Installation

- Create conda environment `conda env create -f environment.yml`
- Activate environment `conda activate rwthlab`
- Install Jupyterlab extensions with `jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib jupyterlab-rwth`
- Install `rwth_nb`:
    - with `pip install git+https://git.rwth-aachen.de/jupyter/rwth-nb.git` or
    - with `python ./setup.sh develop` (for developers)
