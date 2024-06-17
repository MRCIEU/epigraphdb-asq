# Analysis
# Setting up

```
# working dir is {REPO_ROOT}/analysis

# create the conda env
conda env create -f environment.yml
# --------

# install local packages
# inside the conda env
# then go to {REPO_ROOT} and
# install local package `analysis`
python3 -m pip install -e analysis
# install local package `common_processing`
python3 -m pip install -e common_processing
# check local package installation by `pip list`
# --------
```
