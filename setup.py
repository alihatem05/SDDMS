from settings import CONFIGS, logging
from pathlib import Path
import csv

def setup():
    logging.info("********** SETUP INITIALIZED **********")
    CONFIGS.PATH.mkdir(exist_ok=True)
    logging.debug("Base directory created.")
    CONFIGS.INPUT.mkdir(exist_ok=True)
    logging.debug("Input directory created.")
    CONFIGS.OUTPUT.mkdir(exist_ok=True)
    logging.debug("Output directory created.")
    for sd in CONFIGS.SUBDIRS:
        temp = CONFIGS.OUTPUT / sd
        temp.mkdir(exist_ok=True)
        logging.debug(f"{sd} directory created.")
    
    logging.info("Setup finished successfully.")
    # dummy part
    # dummy_setup()

def dummy_setup():
    if not Path("dummy.csv").exists():
        logging.warning("Dummy CSV file was not found, aborting dummy copying process.")
        return
    logging.debug("Dummy CSV file setup initializing.")
    with open("dummy.csv", "r", newline="") as dummy:
        rows = csv.reader(dummy)
        with open(CONFIGS.INPUT / "school.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
    logging.debug("Dummy CSV copied to input directory as school.csv.")