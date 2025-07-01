# ========================
# collector/config.py
# ========================
import yaml
import os

def load_config(path="config.yaml"):
    full_path = os.path.join(os.path.dirname(__file__), "..", path)
    full_path = os.path.abspath(full_path)
    with open(full_path, 'r') as f:
        return yaml.safe_load(f)
