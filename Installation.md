# Technical Portfolio Analysis
# Install guide
conda activate base  
conda create -n pyvizenv python=3.7 -y  
conda activate pyvizenv  
conda install -c conda-forge ta-lib  
conda install -c conda-forge holoviews  
conda install -c conda-forge python-dotenv -y  
conda install -c anaconda nb_conda -y  
conda install -c conda-forge nodejs=12 -y  
conda install -c pyviz holoviz -y  
conda install -c plotly plotly -y  
conda install -c conda-forge jupyterlab=2.2 -y  
conda install -c anaconda numpy==1.19 -y  
conda install -c conda-forge matplotlib==3.0.3 -y  
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build  
jupyter labextension install jupyterlab-plotly --no-build  
jupyter labextension install plotlywidget --no-build  
jupyter labextension install @pyviz/jupyterlab_pyviz --no-build  
jupyter lab build  
