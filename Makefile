#
# 	╔═╗╔═╗──╔╗─────╔═╗╔╗
# 	║║╚╝║║──║║─────║╔╝║║
# 	║╔╗╔╗╠══╣║╔╦══╦╝╚╦╣║╔══╗
# 	║║║║║║╔╗║╚╝╣║═╬╗╔╬╣║║║═╣
# 	║║║║║║╔╗║╔╗╣║═╣║║║║╚╣║═╣
# 	╚╝╚╝╚╩╝╚╩╝╚╩══╝╚╝╚╩═╩══╝
# 		


VERSION = 1.0.0
APP_NAME = games-tui
SRC_DIR = src
DIST_DIR = dist
APP_CONFIG = config
DATA_DIR = data
VENV = .venv
CURRENT_USER := $(shell whoami)

PYTHON ?= $(shell which python3 || which python3)

# os detect
OS := $(shell uname)

ifeq ($(OS), Linux)
	APP_DIR = /usr/local/$(APP_NAME)
	BIN_DIR = /usr/local/bin
	BIN_FILE = $(APP_DIR)/$(APP_NAME)
	COPY = cp -r
	RM = rm -rf
	INSTALL = sudo install -m 0755
	VENV_ACTIVATE = . $(VENV)/bin/activate
	LINK_DIR = /usr/local/bin
	CONFIG_DIR = $(HOME)/.config/games-tui
else ifeq ($(OS), Darwin)
	APP_DIR = /usr/local/lib/$(APP_NAME)
	BIN_FILE = $(APP_DIR)/$(APP_NAME)
	LINK_DIR = /usr/local/bin
	COPY = cp -r
	RM = rm -rf
	INSTALL = sudo install -m 0755
	VENV_ACTIVATE = . $(VENV)/bin/activate
	LINK_DIR = /usr/local/bin
	CONFIG_DIR = /Users/$(CURRENT_USER)/Library/Application\ Support/games-tui
else ifeq ($(OS), Windows)
	APP_DIR = "C:/Program Files/$(APP_NAME)"
	BIN_FILE = $(APP_DIR)/$(APP_NAME).exe
	COPY = xcopy /E /I /Y
	RM = rmdir /S /Q
	INSTALL = copy
	VENV_ACTIVATE = .\$(VENV)\Scripts\activate
	LINK_DIR = "C:/Program Files/$(APP_NAME)"
	CONFIG_DIR = "C:/Users/$(CURRENT_USER)/AppData/Roaming/games-tui"
endif

install:
	@echo "Creating virtual environment."
	$(PYTHON) -m venv $(VENV)
	$(VENV_ACTIVATE)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install pyinstaller

build:
	mkdir -p $(DIST_DIR)
	pyinstaller --onefile --name $(APP_NAME) $(SRC_DIR)/games_tui/main.py
	mv dist/$(APP_NAME) $(APP_NAME)
	@echo "Binary created at: $(PWD)/$(APP_NAME)"

install_binary:
ifeq ($(OS), Windows)
	# For Windows
	mkdir $(APP_DIR)/config
	mkdir $(APP_DIR)/data
	$(INSTALL) $(APP_NAME) $(BIN_FILE)
	xcopy /E /I /Y $(APP_CONFIG) $(APP_DIR)/config
	xcopy /E /I /Y $(DATA_DIR) $(APP_DIR)/data
	@echo "Binary installed to: $(BIN_FILE)"
	@echo "Config installed to: $(APP_DIR)/config"
	@echo "Data installed to: $(APP_DIR)/data"
else ifeq ($(OS), Darwin)
	# For macOS
	sudo mkdir -p $(CONFIG_DIR)
	sudo cp -r $(APP_CONFIG)/* $(CONFIG_DIR)/

	# Create directories and install the binary
	sudo mkdir -p $(APP_DIR)/config
	sudo mkdir -p $(APP_DIR)/data
	$(INSTALL) -m 0755 $(APP_NAME) $(BIN_FILE)
	sudo $(COPY) $(APP_CONFIG)/* $(APP_DIR)/config/
	sudo $(COPY) $(DATA_DIR)/* $(APP_DIR)/data/
	sudo ln -sf $(BIN_FILE) $(LINK_DIR)/$(APP_NAME)

	@echo "Binary installed to: $(BIN_FILE)"
	@echo "Symlink created at: $(LINK_DIR)/$(APP_NAME)"
	@echo "Config installed to: $(APP_DIR)/config"
	@echo "Data installed to: $(APP_DIR)/data"
	@echo "Config copied to: $(CONFIG_DIR)"
else
	# For Linux
	# Ensure the config and data directories are copied to the correct locations
	mkdir -p $(CONFIG_DIR)
	$(COPY) $(APP_CONFIG)/* $(CONFIG_DIR)/

	mkdir -p $(CONFIG_DIR)/data
	$(COPY) $(DATA_DIR)/* $(CONFIG_DIR)/data/

	# Create directories and install the binary
	sudo mkdir -p $(APP_DIR)/config
	sudo mkdir -p $(APP_DIR)/data
	$(INSTALL) -m 0755 $(APP_NAME) $(BIN_FILE)
	sudo $(COPY) $(APP_CONFIG)/* $(APP_DIR)/config/
	sudo $(COPY) $(DATA_DIR)/* $(APP_DIR)/data/
	sudo ln -sf $(BIN_FILE) $(LINK_DIR)/$(APP_NAME)

	@echo "Binary installed to: $(BIN_FILE)"
	@echo "Symlink created at: $(LINK_DIR)/$(APP_NAME)"
	@echo "Config installed to: $(APP_DIR)/config"
	@echo "Data installed to: $(APP_DIR)/data"
	@echo "Config copied to: $(CONFIG_DIR)"
endif

clean:
	rm -rf $(DIST_DIR) build $(APP_NAME).spec $(APP_NAME) $(VENV)
	@echo "Cleaned up build artifacts."

all: install build install_binary clean

.PHONY: install build install_binary clean all
