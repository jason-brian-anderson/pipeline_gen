#!/bin/bash

# Start a jupyter notebook in the background

# Check if jupyter is installed
#"jupyter", "notebook", "--ip=0.0.0.0", "--port=80", "--no-browser", "--allow-root", "--NotebookApp.token=''"
command -v jupyter >/dev/null 2>&1 || { echo >&2 "I require jupyter but it's not installed.  Aborting."; exit 1; }
# Start jupyter in the background
jupyter notebook --ip=0.0.0.0 --port=80 --no-browser --allow-root --NotebookApp.token='' #--symlink --sys-prefix captum.insights.attr_vis.widget

echo "Jupyter notebook started in the background."



