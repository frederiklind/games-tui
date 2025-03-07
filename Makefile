
# Variables
APP_NAME = games-tui
SRC_DIR = src
DIST_DIR = dist
CONFIG_DIR = config
DATA_DIR = data
VERSION = 1.0.0
BIN_DIR = /usr/local/bin  
APP_DIR = $(HOME)/.local/share/$(APP_NAME) 

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	python3 -m pip install pyinstaller

build:
	mkdir -p $(DIST_DIR)
	pyinstaller --onefile --name $(APP_NAME) $(SRC_DIR)/games_tui/main.py
	mv $(DIST_DIR)/$(APP_NAME) $(APP_NAME) 
	mkdir -p $(DIST_DIR)/config
	mkdir -p $(DIST_DIR)/data
	cp -r $(CONFIG_DIR)/* $(DIST_DIR)/config/
	cp -r $(DATA_DIR)/* $(DIST_DIR)/data/

install_binary:
	mkdir -p $(APP_DIR)/config
	mkdir -p $(APP_DIR)/data
	cp -r $(CONFIG_DIR)/* $(APP_DIR)/config/
	cp -r $(DATA_DIR)/* $(APP_DIR)/data/
	sudo cp $(APP_NAME) $(BIN_DIR) 

package:
	tar -czf $(APP_NAME)-$(VERSION)-macOS.tar.gz $(APP_NAME) -C $(DIST_DIR) config data

clean:
	rm -rf $(DIST_DIR) build $(APP_NAME).spec $(APP_NAME)

all: install build package install_binary
