# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'radiantkit'
copyright = '2024, BiCroLab'
author = 'BiCroLab'

import radiantkit as rk
version=rk.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# https://github.com/readthedocs/sphinx_rtd_theme
# pip install sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"

html_static_path = ['_static']


# -- Options for PDF output -----------------------------------------------------

# This backend supports unicode characters
latex_engine = "xelatex"
