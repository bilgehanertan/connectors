import os
from pathlib import Path

import yaml
from pycti import OpenCTIConnectorHelper, get_config_variable

from .utils import SUPPORTED_COLLECTIONS


class ConfigConnector:

    def __init__(self):
        """
        Initialize the connector with necessary configurations
        """

        # Load configuration file
        self.load = self._load_config()
        self.helper = OpenCTIConnectorHelper(self.load)
        self._initialize_configurations()

    @staticmethod
    def _load_config() -> dict:
        """
        Load the configuration from the YAML file
        :return: Configuration dictionary
        """

        config_file_path = Path(__file__).parents[1].joinpath("config.yml")
        print(f"CONFIG FILE PATH = {config_file_path}")
        config = (
            yaml.load(open(config_file_path), Loader=yaml.FullLoader)
            if os.path.isfile(config_file_path)
            else {}
        )

        return config

    def _initialize_configurations(self) -> None:
        """
        Connector configuration variables
        :return: None
        """
        self.duration_period = get_config_variable(
            env_var="CONNECTOR_DURATION_PERIOD",
            yaml_path=["connector", "duration_period"],
            config=self.load,
            required=True,
            default="PT1H",
        )

        self.bambenek_username = get_config_variable(
            env_var="BAMBENEK_USERNAME",
            yaml_path=["bambenek", "username"],
            config=self.load,
            required=True,
        )

        self.bambenek_password = get_config_variable(
            env_var="BAMBENEK_PASSWORD",
            yaml_path=["bambenek", "password"],
            config=self.load,
            required=True,
        )

        bambenek_collections_string = get_config_variable(
            env_var="BAMBENEK_COLLECTIONS",
            yaml_path=["bambenek", "collections"],
            config=self.load,
            required=True,
            default="c2_dga,c2_dga_high_conf,c2_domain,c2_domain_highconf,c2_ip,c2_ip_highconf",
        )
        bambenek_collections_list = [
            x.strip() for x in bambenek_collections_string.split(",")
        ]

        # validate collection configured
        for collection in bambenek_collections_list:
            if collection not in SUPPORTED_COLLECTIONS:
                self.helper.log_error(f"Unsupported collection: {collection}")
                bambenek_collections_list.remove(collection)

        self.bambenek_collections = bambenek_collections_list
