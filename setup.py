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
