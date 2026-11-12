import os

# Download FibrilGen source code
os.system('git clone https://github.com/ChaoYuYang0/FibrilGen-v1 fibrilgen_local')

# These packages can be installed through conda
os.system('conda install -y conda-forge::jupyterlab')
os.system('conda install -y python=3.12.12')
os.system('conda install -y -c conda-forge pymol-open-source=3.1.0')

# These packages can be installed through pip
os.system('pip install -r requirements.txt')
