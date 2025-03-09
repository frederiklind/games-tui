from setuptools import setup, find_packages

setup(
    name='games-tui',
    version='0.1',
    packages=find_packages(where='games_tui'),
    package_dir={'': 'games_tui'},
    entry_points={
        'console_scripts': [
            'games-tui = games_tui.main:main',
            'games-tui-setup = games_tui.install:install'
        ],
    },
    install_requires=[],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7'
)
	# MACOS

	# else ifeq ($(OS), Darwin)
	# 	sudo mkdir -p $(CONFIG_DIR)
	# 	sudo cp -r $(CONFIG_DIR)/* $(CONFIG_DIR)/
	# 	sudo mkdir -p $(APP_DIR)/config
	# 	sudo mkdir -p $(APP_DIR)/data
	# 	$(INSTALL) -m 0755 $(APP_NAME) $(BIN_FILE)
	# 	sudo $(COPY) $(CONFIG_DIR)/* $(APP_DIR)/config/
	# 	sudo $(COPY) $(DATA_DIR)/* $(APP_DIR)/data/
	# 	sudo ln -sf $(BIN_FILE) $(LINK_DIR)/$(APP_NAME)
	#
	# # WINDOWS
	#
	# else ifeq ($(OS), Windows)
	# 	mkdir $(APP_DIR)\config
	# 	mkdir $(APP_DIR)\data
	# 	$(INSTALL) $(APP_NAME) $(BIN_FILE)
	# 	xcopy /E /I /Y .\config $(APP_DIR)\config
	# 	xcopy /E /I /Y .\data $(APP_DIR)\data
