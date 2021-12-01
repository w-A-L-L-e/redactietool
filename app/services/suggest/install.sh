mkdir -p python_env; \
python3 -m venv python_env; \
. python_env/bin/activate; \
python3 -m pip install --upgrade pip; \
python3 -m pip install -r requirements.txt;

