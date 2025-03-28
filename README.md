![Graphical Summary of README](docs/_static/header.jpg)
CADDKit
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/davidkastner/caddkit/workflows/CI/badge.svg)](https://github.com/davidkastner/caddkit/actions?query=workflow%3ACI)
[![Documentation Status](https://readthedocs.org/projects/caddkit/badge/?version=latest)](https://caddkit.readthedocs.io/en/latest/?badge=latest)

# CADDKit Package
## Table of Contents
1. **Overview**
2. **Tutorials**
    * quickCSA
3. **Installation**
    * Download the package from GitHub
    * Creating a python environment
    * Developer install of CADDKit
    * Supporting installations
4. **What is included?**
    * File structure
    * Command Line Interface
5. **Documentation**
    * Update the ReadTheDocs
    * GitHub refresher


## 1. Overview
CADDKit is a package for accelerating insights gained from structure function relationship (SFR) with an emphasis on QM, MD, and QM/MM workflows. 
The package contains useful tools for all stages of the computer-aided drug design workflow.
The functionality is built around the Amber-TeraChem interface.

## 2. Tutorials
To improve the usuability of the CADDKit package, this section will contain video-style tutorials.
You can also find additional information and README's in the tutorials folder.

### quickCSA

[![Video Tutorial](https://raw.githubusercontent.com/davidkastner/CADDKit/main/docs/_static/thumbnail.jpg)](https://www.youtube.com/watch?v=Zck8fznmTPA&t=27s&ab_channel=DavidW.Kastner)

## 3. Installation
Install the package by running the follow commands inside the downloaded repository. 
This will perform a developmental version install. 
It is good practice to do this inside of a virtual environment.

### Download the package from GitHub
```
git clone git@github.com:davidkastner/CADDKit.git
```

### Creating python environment
All the dependencies can be loaded together using the prebuilt environment.yml file.
Compatibility is automatically tested for python versions 3.8 and higher.
Installing all dependencies together has shown to produce more robust installations.

```
cd CADDKit
conda env create -f environment.yml
conda activate caddkit
source activate caddkit  #Alternatively used on some clusters
```

### Developer install of CADDKit
```
cd caddkit
python -m pip install -e .
```

### Supporting installations
To have complete access to all CADDKit functionality, you should also install following dependencies. 
This should be done inside you caddkit virtual environment. 
CADDKit contains automated workflows for modelling in missing loops using Modeller.

```
conda install -c salilab modeller
```

## 4. What's included?
CADDKit is built as both a library and a collection of pre-built scripts.
The scripts aim to accelerate data processesing and automation of calculations.
If a script is not already included for procedure, many of the functions may be useful in building a procedure.

### File structure

```
.
|── cli.py      # Command-line interface entry point
├── docs        # Readthedocs documentation site
├── caddkit      # Directory containing CADDKit modules
│   ├── md      # Processes for setting MD optimizations prior to QM/MM
│   └── qm      # Processes for running and anlayzing QM cluster model jobs 
└── ...
```

### Command Line Interface
The contents of the library are designed to be navigated through the commandline interface.
Add the following line to your bash.rc

```
alias caddkit='python /the/path/to/CADDKit/cli.py'
```


## 5. Documentation
Accurate documentation will always be a high priority for the project.
You can find documentation at the project's [ReadtheDocs](https://caddkit.readthedocs.io/).

### Update the ReadTheDocs

```
make clean
make html
```

### GitHub refresher
#### Push new changes

```
git status
git pull
git add -A
git commit -m "Change a specific functionality"
git push -u origin main
```

#### Making a pull request
```
git checkout main
git pull

# Before you begin making changes, create a new branch
git checkout -b new-feature-branch
git add -A
git commit -m "Detailed commit message describing the changes"
git push -u origin new-feature-branch

# Visit github.com to add description, submit, merge the pull request

# Once finished on github.com, return to local
git checkout main
git pull

# Delete the remote branch
git branch -d new-feature-branch
```

#### Handle merge conflict

```
git stash push --include-untracked
git stash drop
git pull
```

#### Copyright
&copy; 2025,  David W. Kastner

