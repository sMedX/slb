"""
Module for loading web application configuration
"""
from typing import Dict

import yaml

from pathlib import Path

__all__ = ('load_config',)


def load_config(config_file: str = None) -> Dict:
    """
    Load config from 'config.yaml' file with update from config_file

    :param config_file: optional config file to update configuration
    from default 'config.yaml'
    :return: application configuration with dict interface
    """
    default_file = Path(__file__).parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    config_from_file = {}
    if config_file:
        config_from_file = yaml.safe_load(config_file)

    config.update(**config_from_file)
    return config
