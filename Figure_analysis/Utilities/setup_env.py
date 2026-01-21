"""
setup_env.py
Shared environment for PRIME / figure analysis notebooks.

Usage:
    import setup_env as env
    # or
    from setup_env import *
"""

# ------------------------------------------------------------------------
# Standard library
# ------------------------------------------------------------------------
from __future__ import annotations
import os
import json
import math
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List

# ------------------------------------------------------------------------
# GLOBAL CONFIG
# ------------------------------------------------------------------------

# Path to your main nerd database
NERD_SQLITE = '../../../Core_nerd_analysis/nerd.sqlite'


# ------------------------------------------------------------------------
# Core numerical / data libraries
# ------------------------------------------------------------------------
import numpy as np
import pandas as pd

# ------------------------------------------------------------------------
# Plotting libraries
# ------------------------------------------------------------------------
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import seaborn as sns

# Optional interactive plotting (used in SFig16)
try:
    import plotly.express as px
except ImportError:
    px = None  # Used in only a few notebooks

# ------------------------------------------------------------------------
# Stats / modeling libraries
# ------------------------------------------------------------------------
import statsmodels.api as sm
import statsmodels.formula.api as smf

from scipy import constants, stats
import scipy.constants as sc
from scipy.constants import R, calorie
from scipy.integrate import solve_ivp

# ------------------------------------------------------------------------
# lmfit
# ------------------------------------------------------------------------
import lmfit
from lmfit.model import Model, save_modelresult, load_modelresult
from lmfit.models import LinearModel, ExponentialModel
from lmfit import minimize, Parameters, create_params, report_fit

# ------------------------------------------------------------------------
# Machine learning (sklearn)
# ------------------------------------------------------------------------
try:
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import (
        roc_curve,
        auc,
        precision_recall_curve,
        precision_recall_fscore_support,
    )
    from scipy.stats import wilcoxon
except ImportError:
    DecisionTreeClassifier = None
    roc_curve = auc = precision_recall_curve = precision_recall_fscore_support = None
    wilcoxon = None

# ------------------------------------------------------------------------
# ODE / numba / numbalsoda (SFig1)
# ------------------------------------------------------------------------
try:
    from numba import cfunc, njit
    from numbalsoda import lsoda, lsoda_sig
except ImportError:
    cfunc = njit = lsoda = lsoda_sig = None

# ------------------------------------------------------------------------
# NUPACK (construct design notebooks)
# ------------------------------------------------------------------------
try:
    from nupack import *  # noqa: F401,F403
    NUPACK_AVAILABLE = True
except ImportError:
    NUPACK_AVAILABLE = False

# ------------------------------------------------------------------------
# Global plotting configuration
# ------------------------------------------------------------------------

mpl.rcParams.update(
    {
        "font.size": 8,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica"],
        "pdf.fonttype": 42,  # avoid Type 3 fonts in PDFs
        "ps.fonttype": 42,
    }
)


# ------------------------------------------------------------------------
# Public API (for `from setup_env import *`)
# ------------------------------------------------------------------------
__all__ = [
    # global config
    "NERD_SQLITE",
    # stdlib
    "os",
    "json",
    "math",
    "sqlite3",
    "Path",
    "Any",
    "Dict",
    "Optional",
    "Tuple",
    "List",
    # core libs
    "np",
    "pd",
    # plotting
    "mpl",
    "plt",
    "sns",
    "FuncFormatter",
    "Line2D",
    "cm",
    "mcolors",
    "LinearSegmentedColormap",
    "inset_axes",
    "px",
    # stats / modeling
    "sm",
    "smf",
    "constants",
    "stats",
    "sc",
    "R",
    "calorie",
    "solve_ivp",
    # lmfit
    "lmfit",
    "Model",
    "save_modelresult",
    "load_modelresult",
    "LinearModel",
    "ExponentialModel",
    "minimize",
    "Parameters",
    "create_params",
    "report_fit",
    # sklearn / stats extras
    "DecisionTreeClassifier",
    "roc_curve",
    "auc",
    "precision_recall_curve",
    "precision_recall_fscore_support",
    "wilcoxon",
    # numba / numbalsoda
    "cfunc",
    "njit",
    "lsoda",
    "lsoda_sig",
    # nupack flag
    "NUPACK_AVAILABLE",
]