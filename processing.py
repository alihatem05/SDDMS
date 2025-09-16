from settings import CONFIGS, logging
from pathlib import Path
import csv
import shutil
import re

def fail_move(file):
    destination = CONFIGS.OUTPUT / CONFIGS.ACTIONS["failure"]
    shutil.move(file, destination)
    logging.info(f"{file.name} moved to FAILURE folder: {destination.name}")

def success_move(file):
    destination = CONFIGS.OUTPUT / CONFIGS.ACTIONS["success"]
    shutil.move(file, destination)
    logging.info(f"{file.name} moved to SUCCESS folder: {destination.name}")

def fileIteration():
    logging.info("********** FILES PROCESSING INITIALIZED **********")
    input_dir = CONFIGS.INPUT
    for file in input_dir.iterdir():
        if file.suffix not in CONFIGS.ALLOWED_EXTENSIONS:
            logging.warning(f"{file.name} is not among the allowed file extensions.")
            fail_move(file)
            continue
        else:
            logging.info(f"{file.name} is queued for processing.")
            p = Processor(file)
            if p.process_file():
                success_move(file)
                logging.info(f"{file.name} is clean, moved to success directory.")
            else: 
                logging.info(f"{file.name} is NOT clean, moved to failure directory.")
                fail_move(file)


class Processor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.structure = CONFIGS.STRUCTURE
        self.constraints = CONFIGS.CONSTRAINTS
        logging.debug(f"Processor created for {self.filepath.name} with structure/constraints loaded.")

    def process_headers(self, headers):
        logging.debug(f"Checking headers for {self.filepath.name}. Found: {headers}")
        expected = list(self.structure.keys())
        if headers != expected:
            logging.warning(f"Header mismatch in {self.filepath.name}. Expected: {expected}, Found: {headers}")
        return headers == expected

    def process_file(self):
        logging.info(f"Processing started for {self.filepath.name}")
        with open(self.filepath, "r", newline="") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            if not self.process_headers(headers):
                return False
            logging.info(f"{self.filepath.name} has correct headers.")
            for row_num, row in enumerate(reader):
                logging.debug(f"Processing row #{row_num + 1}: {row}")
                result = self.process_row(row)
                if not result:
                    return False
        logging.info(f"Processing finished for {self.filepath.name}")
        return True

    def process_row(self, row):
        logging.debug(f"Row validation started: {row}")
        for header, col in row.items():
            col_rules = self.structure[f"{header}"]
            col_type = col_rules["type"]
            logging.debug(f"Validating column '{header}' with value '{col}' and rules {col_rules}")

            nullable = col_rules["nullable"]
            if not col:
                if not nullable:
                    logging.warning(f"Column '{header}' is empty but not nullable.")
                    return False
                logging.debug(f"Column '{header}' is empty but nullable, skipping.")
                continue

            if col_type == "int" or col_type == "float":
                logging.debug(f"Column '{header}' expected numeric type: {col_type}")
                result = self.check_number(col, col_rules, col_type)
            else: 
                logging.debug(f"Column '{header}' expected string type")
                result = self.check_string(col, col_rules)

            if not result:
                logging.warning(f"Column '{header}' failed validation. Value: {col}")
                return False
        logging.debug(f"Row passed validation: {row}")
        return True
    
    def check_number(self, col, col_rules, col_type):
        int_min = col_rules["min"]
        int_max = col_rules["max"]
    
        try:
            value = int(col) if col_type == "int" else float(col)
            logging.debug(f"Parsed number {value} from column value '{col}'")
        except ValueError:
            logging.warning(f"Failed to parse number from '{col}' for expected type {col_type}")
            return False

        if not (int_min <= value <= int_max):
            logging.warning(f"Value {value} not in range [{int_min}, {int_max}]")
            return False

        if col_type == "int" and float(col) != int(col):
            logging.warning(f"Value '{col}' is not a pure int")
            return False

        logging.debug(f"Numeric value '{col}' validated successfully.")
        return True
    
    def check_string(self, col, col_rules):
        min_length = col_rules["min_length"]
        max_length = col_rules["max_length"]
        str_format = col_rules["format"]

        if len(col) < min_length or len(col) > max_length:
            logging.warning(f"String length {len(col)} out of bounds [{min_length}, {max_length}] for value '{col}'")
            return False       

        if re.fullmatch(str_format, col):
            logging.debug(f"String value '{col}' matched format successfully.")
            return True
        else:
            logging.warning(f"String value '{col}' did not match required format.")
            return False