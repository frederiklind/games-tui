APP_NAME = games-tui
SRC_DIR = src
DIST_DIR = dist
CONFIG_DIR = config
DATA_DIR = data
VERSION = 1.0.0
BIN_DIR = /usr/local/bin  
APP_DIR = $(HOME)/Library/Application Support/$(APP_NAME)

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	python3 -m pip install pyinstaller

build:
	mkdir -p $(DIST_DIR)
	pyinstaller --onefile --name $(APP_NAME) --debug all $(SRC_DIR)/games_tui/main.py
	mv dist/$(APP_NAME) $(APP_NAME)  
	mkdir -p $(DIST_DIR)/config
	mkdir -p $(DIST_DIR)/data
	cp -r $(CONFIG_DIR)/* $(DIST_DIR)/config/
	cp -r $(DATA_DIR)/* $(DIST_DIR)/data/
	@echo "Binary created at: $(PWD)/$(APP_NAME)"
	@echo "Config copied to: $(PWD)/config"
	@echo "Data copied to: $(PWD)/data"

install_binary:
	mkdir -p $(HOME)/.local/bin/
	mkdir -p $(APP_DIR)/config
	mkdir -p $(APP_DIR)/data
	cp -r $(CONFIG_DIR)/* $(APP_DIR)/config/
	cp -r $(DATA_DIR)/* $(APP_DIR)/data/
	install -m 0755 $(APP_NAME) $(HOME)/.local/bin/
	@echo "Binary installed to: $(HOME)/.local/bin/$(APP_NAME)"
	@echo "Config installed to: $(APP_DIR)/config"
	@echo "Data installed to: $(APP_DIR)/data"

clean:
	rm -rf $(DIST_DIR) build $(APP_NAME).spec $(APP_NAME)
	@echo "Cleaned up build artifacts."

all: install build install_binary
