import json
import logging
from pathlib import Path

with open("data.json", "r") as file:
    settings = json.load(file)

logging.basicConfig(
    level=logging.INFO,
    filename="log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class CONFIGS:
    PATH = Path(settings["base_dir"])
    INPUT, OUTPUT, SUBDIRS = PATH / settings["input_dir"], PATH / settings["output_dir"], settings["output_subdirs"]
    ALLOWED_EXTENSIONS = settings["allowed_extensions"]
    ACTIONS = settings["actions"]
    CONSTRAINTS = settings["constraints_catalog"]
    STRUCTURE = settings["csv_structure"]

    def __init__(self):
        return
    
