# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "SiaSearch"
copyright = "2020, Merantix Automotive"
author = "Merantix Automotive"

# The full version, including alpha/beta/rc tags
release = "0.0.1b"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "sphinx_rtd_theme"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "../../../frontend/public/favicon.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "../../../frontend/public/favicon.ico"

# The master toctree document.
master_doc = "index"

autodoc_mock_imports = ["pandas", "matplotlib", "scikit-image", "requests", "ipython", "IPython.display", "skimage"]

try:
    import IPython
except ImportError:
    IPython = sys.modules["IPython"] = mock.Mock()

try:
    import IPython.display
except ImportError:
    IPython.display = sys.modules["IPython.display"] = mock.Mock()
