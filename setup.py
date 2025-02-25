#!/usr/bin/env python3

import os
import sys
import argparse
import platform


def get_config_dir(user_os: str, app_name: str) -> str:
    """
    Creates the directory path for the application's configuration,
    based on the operating system of the client device. 

    Args:
        user_os (str): Operating system of the client device.
        app_name (str): Name of the application.

    Returns:
        str: The full path to the config directory to be used by the application.
    """
    match user_os:
        case "Linux":
            home = os.environ.get("HOME", os.getcwd())
            return os.path.join(home, ".config", app_name)
        case "Darwin":
            home = os.environ.get("HOME", os.getcwd())
            return os.path.join(home, "Library", "Preferences", app_name)
        case "Windows":
            appdata = os.environ.get("APPDATA", os.getcwd())
            return os.path.join(appdata, app_name)
        case _:
            return os.path.join(os.getcwd())


def get_data_dir(user_os: str, app_name: str) -> str:
    """
    Creates the directory path for the application's data files,
    based on the operating system of the client device.

    Args:
        user_os (str): Operating system of the client device.
        app_name (str): Name of the application.

    Returns:
        str: The full path to the data directory to be used by the application.
    """
    match user_os:
        case "Linux":
            home = os.environ.get("HOME", os.getcwd())
            return os.path.join(home, ".local", "share", app_name)
        case "Darwin":
            home = os.environ.get("HOME", os.getcwd())
            return os.path.join(home, "Library", "Application Support")
        case "Windows":
            


def main():
    user_os = platform.system()

    




if __name__ == "__main__":
    main()
