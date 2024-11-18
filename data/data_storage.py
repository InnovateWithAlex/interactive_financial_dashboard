# data/data_storage.py

import json
import os

# File paths
INCOME_DATA_FILE = 'data/income_data.json'
EXPENSES_DATA_FILE = 'data/expenses_data.json'

def load_income_data():
    if os.path.exists(INCOME_DATA_FILE):
        with open(INCOME_DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

def save_income_data(data):
    with open(INCOME_DATA_FILE, 'w') as f:
        json.dump(data, f)

def load_expenses_data():
    if os.path.exists(EXPENSES_DATA_FILE):
        with open(EXPENSES_DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

def save_expenses_data(data):
    with open(EXPENSES_DATA_FILE, 'w') as f:
        json.dump(data, f)
