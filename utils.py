import pickle
import json
from typing import Any, Dict

def save_as_pickle(obj: Any, filepath: str) -> None:
    with open(filepath, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_as_json(obj: Dict, filepath: str) -> None:
    with open(filepath, 'w') as fp:
        json.dump(obj, fp)

def load_pickle(filepath: str) -> Any:
    with open(filepath, 'rb') as handle:
        obj = pickle.load(handle)
    return obj

MODEL_FEATURES = [  # picked these numerical features randomly just to get going 
    'manufactured_year', 
    'mileage', 
    'engine_size', 
    'top_speed', 
    'engine_power', 
    'engine_torque', 
    'height', 
    'length', 
    'wheelbase', 
    'width', 
    'fuel_tank_capacity', 
    'boot_space_seats_up', 
    'urban', 
    'extra_urban', 
    'co2_emissions'
    ]