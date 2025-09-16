import logging
from settings import CONFIGS
from setup import setup
import processing

def main():
    logging.info("===== Starting SDDMS Project =====")
    
    try:
        setup()
        logging.info("Setup completed successfully.")

        processing.fileIteration()

    except Exception as e:
        logging.error(f"Critical failure in main: {e}")
    finally:
        logging.info("===== Project run finished =====")


if __name__ == "__main__":
    main()
