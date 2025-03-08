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
CONFIG_DIR = config
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
	INSTALL = sudo install -m 0755
	VENV_ACTIVATE = . $(VENV)/bin/activate
	LINK_DIR = /usr/local/bin
else ifeq ($(OS), Darwin)
	APP_DIR = /usr/local/lib/$(APP_NAME)
	BIN_FILE = $(APP_DIR)/$(APP_NAME)
	LINK_DIR = /usr/local/bin
	INSTALL = sudo install -m 0755
	VENV_ACTIVATE = . $(VENV)/bin/activate
	LINK_DIR = /usr/local/bin
	# CONFIG_DIR = "/Users/$(CURRENT_USER)/Library/Application Support/games-tui"
else ifeq ($(OS), Windows)
	APP_DIR = "C:/Program Files/$(APP_NAME)"
	BIN_FILE = $(APP_DIR)/$(APP_NAME).exe
	COPY = xcopy /E /I /Y
	RM = rmdir /S /Q
	INSTALL = copy
	VENV_ACTIVATE = .\$(VENV)\Scripts\activate
	LINK_DIR = "C:/Program Files/$(APP_NAME)"
	# CONFIG_DIR = "C:/Users/$(CURRENT_USER)/AppData/Roaming/games-tui"
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
	mkdir $(APP_DIR)\config
	mkdir $(APP_DIR)\data
	$(INSTALL) $(APP_NAME) $(BIN_FILE)
	xcopy /E /I /Y $(CONFIG_DIR) $(APP_DIR)\config
	xcopy /E /I /Y $(DATA_DIR) $(APP_DIR)\data

else ifeq ($(OS), Darwin)
	sudo mkdir -p $(CONFIG_DIR)
	sudo cp -r $(CONFIG_DIR)/* $(CONFIG_DIR)/
	sudo mkdir -p $(APP_DIR)/config
	sudo mkdir -p $(APP_DIR)/data
	$(INSTALL) -m 0755 $(APP_NAME) $(BIN_FILE)
	sudo $(COPY) $(CONFIG_DIR)/* $(APP_DIR)/config/
	sudo $(COPY) $(DATA_DIR)/* $(APP_DIR)/data/
	sudo ln -sf $(BIN_FILE) $(LINK_DIR)/$(APP_NAME)

else
	sudo mkdir -p $(HOME)/.config/$(APP_NAME)
	sudo cp -r $(CONFIG_DIR)/* $(HOME)/.config/$(APP_NAME)

	sudo mkdir -p $(HOME)/.local/share/$(APP_NAME)
	sudo cp -r $(DATA)/* $(HOME)/.local/share/$(APP_NAME)

	$(INSTALL) -m 0755 $(APP_NAME) /usr/local/bin/$(APP_NAME)
	sudo ln -sf /usr/local/bin/$(APP_NAME) /usr/local/bin/$(APP_NAME)
endif

clean:
	rm -rf $(DIST_DIR) build $(APP_NAME).spec $(APP_NAME) $(VENV)
	@echo "Cleaned up build artifacts."

all: install build install_binary clean

