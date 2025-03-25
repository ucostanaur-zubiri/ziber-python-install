#!/bin/bash
if test ! -d /home/$USER/workspace; then
    echo "/home/$USER/workspace/python carpeta sortzen..."
	mkdir /home/$USER/workspace
	mkdir /home/$USER/workspace/python
else 
    echo "/home/$USER/workspace/python carpeta existitzen da"
fi
echo "python3.12-venv instalatzen..."
apt install -y python3.12-venv
echo "python ingurunea sortzen /home/$USER/workspace/python/.env karpetan..."
python3 -m venv /home/$USER/workspace/python/.env
echo "Ingurune birtuala aktibatzen..."
source /home/$USER/workspace/python/.env/bin/activate
echo "Pip eguneratzen..."
python3 -m pip install --upgrade pip
python3 -m pip --version
echo "Liburutegiak instalatzen..."
pip install python-snap7
pip install keyboard
pip install progressbar
cd /home/$USER/workspace/python
git clone https://github.com/ucostanaur-zubiri/ziber-python-attacks.git
