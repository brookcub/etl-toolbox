# -*- coding: utf-8 -*-

# -- Path setup --------------------------------------------------------------

import os
import sys

import sphinx_bootstrap_theme

sys.path.insert(0, os.path.abspath(".."))

import etl_toolbox

# -- Project information -----------------------------------------------------

project = u'etl-toolbox 🧰'
copyright = '2020, Brooklyn Rose Ludlow'
author = 'Brooklyn Rose Ludlow'

release = etl_toolbox.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

language = 'en'

master_doc = "index"
source_suffix = ".rst"
pygments_style = "friendly"

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for sphinx extensions -------------------------------------------

# Looks for objects in external projects
intersphinx_mapping = {
    "pandas": (
        "https://pandas.pydata.org/pandas-docs/stable/",
        "https://pandas.pydata.org/pandas-docs/stable/objects.inv",
    ),
}

# -- Options for HTML output -------------------------------------------------

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_static_path = []

html_sidebars = {'**': ['localtoc.html']}

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

html_theme_options = {
    # Theme setting (from https://bootswatch.com/)
    'bootswatch_theme': "yeti",

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': False,

    # Include hidden toctree links (Default: true)
    'globaltoc_includehidden': "false",

    # Custom navbar links
    'navbar_links': [
        ("Overview", "index"),
        ("Modules & Functions", "modules"),
        # ("Link", "http://example.com", True),
    ],
}
