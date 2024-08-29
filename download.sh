echo "Creating virtual environment"
python3 -m venv venv
echo "Virtual environment created"
source venv/bin/activate
echo "Installing all libraries"
pip install -r requirements.txt
echo "All libraries installed"
