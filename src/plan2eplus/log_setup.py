import os
import logging
import logging.config
from dotenv import find_dotenv, load_dotenv
from plan2eplus.constants import CONFIG_DIR, LOG_DIR


# find .env file in parent directory
env_file = find_dotenv()
load_dotenv()




def setup_logging(fname="tests"):
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.ini")
    config_path = CONFIG_DIR / config # "/".join([CONFIG_DIR, config])

    # timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{fname}.log"},
    )
