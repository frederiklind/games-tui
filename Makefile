#
# 	╔═╗╔═╗──╔╗─────╔═╗╔╗
# 	║║╚╝║║──║║─────║╔╝║║
# 	║╔╗╔╗╠══╣║╔╦══╦╝╚╦╣║╔══╗
# 	║║║║║║╔╗║╚╝╣║═╬╗╔╬╣║║║═╣
# 	║║║║║║╔╗║╔╗╣║═╣║║║║╚╣║═╣
# 	╚╝╚╝╚╩╝╚╩╝╚╩══╝╚╝╚╩═╩══╝
# 		

VERSION=1.0.0
APP_NAME=games-tui
CURRENT_USER := $(shell whoami)
PYTHON ?= $(shell which python || which python3)
OS := $(shell uname)

ifeq ($(OS),Linux)
	APP_DIR=/usr/local/lib/$(APP_NAME)
	CONFIG_DIR=$(HOME)/.config/$(APP_NAME)
	DATA_DIR=$(HOME)/.local/share/$(APP_NAME)
	BIN_DIR=/usr/local/bin
	BIN_FILE=$(APP_DIR)/$(APP_NAME)
	VENV=.venv/bin

else ifeq ($(OS),Darwin)
	APP_DIR=/usr/local/lib/$(APP_NAME)
	CONFIG_DIR="/Users/$(CURRENT_USER)/Library/Application Support/$(APP_NAME)/config"
	DATA_DIR="/Users/$(CURRENT_USER)/Library/Application Support/$(APP_NAME)/data"
	BIN_DIR=/usr/local/bin
	BIN_FILE=$(APP_DIR)/$(APP_NAME)
	VENV=.venv/bin
endif

install:
	@echo -e "\n\033[1;34mInstalling $(APP_NAME) \033[1;36m$(VERSION)\033[0m\n"
	@echo -e "------------------------------------------------\n"

	@echo "===== Creating virtual environment. ====="
	$(PYTHON) -m venv .venv
	$(VENV)/pip install --upgrade pip
	$(VENV)/pip install -r requirements.txt
	$(VENV)/pip install pyinstaller
	
	@if [ "$(OS)" = "Windows" ]; then \
		echo "Installing windows curses..."; \
		$(VENV)/pip install windows-curses; \
	fi	

	@echo "Creating binary..."
	$(VENV)/pyinstaller --onefile --name $(APP_NAME) src/games_tui/main.py
	
	@if [ "$(OS)" = "Linux" ]; then \
		mkdir -p $(CONFIG_DIR); \
		cp -r config/* $(CONFIG_DIR); \
		mkdir -p $(DATA_DIR); \
		cp -r data/* $(DATA_DIR); \
		sudo mkdir $(APP_DIR); \
		sudo cp dist/$(APP_NAME) $(APP_DIR); \
		sudo ln -sf $(BIN_FILE) $(BIN_DIR)/$(APP_NAME); \
	elif [ "$(OS)" = "Darwin" ]; then \
		echo "Setting up macOS specific directories..."; \
		mkdir -p $(CONFIG_DIR); \
		cp -r config/* $(CONFIG_DIR); \
		mkdir -p $(DATA_DIR); \
		cp -r data/* $(DATA_DIR); \
		sudo mkdir -p $(APP_DIR); \
		sudo cp dist/$(APP_NAME) $(APP_DIR); \
		sudo mkdir -p $(BIN_DIR); \
		sudo ln -sf $(BIN_FILE) $(BIN_DIR)/$(APP_NAME); \
	fi

uninstall:
	@echo -e "\n\033[1;34mUninstalling $(APP_NAME)\033[0m\n"
	@echo -e "------------------------------------------------\n"
	@if [ "$(OS)" = "Linux" ]; then \
			if [ -d "$(CONFIG_DIR)" ]; then \
					rm -rf $(CONFIG_DIR); \
					echo "$(CONFIG_DIR) removed"; \
			else \
					echo "$(CONFIG_DIR) does not exist, skipping"; \
			fi; \
			if [ -d "$(DATA_DIR)" ]; then \
					rm -rf $(DATA_DIR); \
					echo "$(DATA_DIR) removed"; \
			else \
					echo -e "$(DATA_DIR) does not exist, skipping"; \
			fi; \
			if [ -f "$(BIN_DIR)/$(APP_NAME)" ]; then \
					sudo rm $(BIN_DIR)/$(APP_NAME); \
					echo -e "$(BIN_DIR)/$(APP_NAME) removed"; \
			else \
					echo -e "$(BIN_DIR)/$(APP_NAME) does not exist, skipping"; \
			fi; \
			if [ -d "$(APP_DIR)" ]; then \
					sudo rm -rf $(APP_DIR); \
					echo -e "$(APP_DIR) removed"; \
			else \
					echo -e "$(APP_DIR) does not exist, skipping"; \
			fi \
	elif [ "$(OS)" = "Darwin" ]; then \
		echo "stuff"; \
	fi

	@echo -e "\n\033[1;32m$(APP_NAME) has been uninstalled.\033[0m"

clean:
	rm -rf dist build .venv $(APP_NAME).spec
	@echo "Cleaned up build artifacts."

all: install clean

.PHONY: install uninstall clean all
