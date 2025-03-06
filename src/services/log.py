import logging


def setup_logging(log_file="application.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),  # Log em arquivo
            logging.StreamHandler(),  # Log no console
        ],
    )
