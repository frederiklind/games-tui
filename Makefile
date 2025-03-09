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
CURRENT_USER := $(shell whoami)
PYTHON ?= $(shell which python || which python3)
OS := $(shell uname)

ifeq ($(OS), Linux)
	APP_DIR 		= /usr/local/lib/$(APP_NAME)
	CONFIG_DIR 	= $(HOME)/.config/$(APP_NAME)
	DATA_DIR 		= $(HOME)/.local/share/$(APP_NAME)
	BIN_DIR 		= /usr/local/bin
	BIN_FILE 		= $(APP_DIR)/$(APP_NAME)
	LINK_DIR 		= /usr/local/bin
	VENV 				= .venv/bin

else ifeq ($(OS), Darwin)
	APP_DIR 		= /usr/local/lib/$(APP_NAME)
	BIN_FILE 		= $(APP_DIR)/$(APP_NAME)
	LINK_DIR 		= /usr/local/bin
	VENV 				= .venv/bin
	CONFIG_DIR 	= "/Users/$(CURRENT_USER)/Library/Application Support/games-tui"

else ifeq ($(OS), Windows)
	APP_DIR 		= "C:/Program Files/$(APP_NAME)"
	BIN_FILE 		= $(APP_DIR)/$(APP_NAME).exe
	LINK_DIR 		= "C:/Program Files/$(APP_NAME)"
	VENV 				= .venv/Scripts
	CONFIG_DIR 	= "C:/Users/$(CURRENT_USER)/AppData/Roaming/games-tui"
endif

install:
	@echo "\n===== Creating virtual environment. =====\n"
	$(PYTHON) -m venv .venv
	$(VENV)/pip install --upgrade pip
	$(VENV)/pip install -r requirements.txt
	$(VENV)/pip install pyinstaller
	
	# install windows curses, if on Windows
	if [ $(OS) =  Windows ]; then 
		@echo "Installing windows curses..."
		$(VENV)/pip install windows-curses 
	fi

	@echo "Creating binary..."
	$(VENV)/pyinstaller --onefile --name $(APP_NAME) src/games_tui/main.py
	
ifeq ($(OS), "Linux")
	# app config
	sudo mkdir -p $(CONFIG_DIR)
	sudo cp -r config/* $(CONFIG_DIR)
	
	# app data
	sudo mkdir -p $(DATA_DIR)
	sudo cp -r data/* $(DATA_DIR)

	# bin
	sudo mkdir $(APP_DIR)
	sudo cp dist/$(APP_NAME) $(APP_DIR)
	sudo ln -sf $(BIN_FILE) $(BIN_DIR)/$(APP_NAME)

	@echo "Binary installed to: /usr/local/bin/$(APP_NAME)"
	@echo "Config installed to: $(HOME)/.config/$(APP_NAME)"
	@echo "Data installed to: $(HOME)/.local/share/$(APP_NAME)"
endif

clean:
	rm -rf $(DIST_DIR) build $(APP_NAME).spec
	@echo "Cleaned up build artifacts."







all: install build install_binary clean

