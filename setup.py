#!/usr/bin/env python3

import os
import sys
import shutil
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
        # case "Windows":
        #     appdata = os.environ.get("APPDATA", os.getcwd())
        #     return os.path.join(appdata, app_name)
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
        # case "Windows":
        case _:
            return os.path.join(os.getcwd())
                        

def main() -> None:
    """

    """
    print("Installing rubiks-tui:\n")

    app_name = "rubiks-tui"
    user_os = platform.system()
    print(f"Operating syste: {user_os}")
    
    config_dir = get_config_dir(user_os, app_name)
    data_dir = get_data_dir(user_os, app_name)
    
    # setup config directory
    if not os.path.exists(config_dir):
        config_dirs = [
            config_dir,
            os.path.join(config_dir, "ascii"),
            os.path.join(config_dir, "colorschemes")
        ]
        os.makedirs(config_dirs)
        for dir in config_dirs:
            os.makedirs(dir)
            print(f"> Created directory: {dir}")

        # copy ascii banners
        ascii_src = os.path.join(os.getcwd(), "conf", "ascii")
        for file in os.listdir(ascii_src):
            src_file = os.path.join(ascii_src, file)
            dest_file = os.path.join(config_dirs[1], file)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dest_file)
                print(f"> Copied {file} to {dest_file}")
        
        clrs_src = os.path.join(os.getcwd, "conf", "colorschemes")
        for file in os.listdir(clrs_src):
            src_file = os.path.join(clrs_src, file)
            dest_file = os.path.join(config_dirs[2], file)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dest_file)
                print(f"> Copied {file} to {dest_file}")

        conf_src = os.path.join(os.getcwd(), "conf", "config.toml")
        conf_dest = os.path.join(config_dir, "config.toml")
        shutil.copy2(conf_src, conf_dest)
        print("> Copied default configuration to config directory.")
    else:
        print(f"> Config directory already exist. Skipping this step")
    
    # setup data directory
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"> Created directory: {data_dir}")
    else:
        print("> Data directory already exist. Skipping this step")
    
    print("Installation finished!") 


if __name__ == "__main__":
    main()
