import json
import logging


def setup_logging(config_file='config.json'):
    """
    Set up logging from a JSON configuration file.
    """
    with open(config_file, 'r') as file:
        config = json.load(file)
    log_file = config.get('log_file', 'app.log')
    log_level = config.get('log_level', 'DEBUG').upper()

    logging.basicConfig(filename=log_file, level=getattr(logging, log_level),
                        format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
