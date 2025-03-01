from setuptools import setup, find_packages

setup(
    name='rubiks-tui',
    version='0.1',
    packages=find_packages(where='rubiks_tui'),
    package_dir={'': 'rubiks_tui'},
    entry_points={
        'console_scripts': [
            'rubiks-tui = rubiks_tui.main:main',
            'rubiks-tui-setup = rubiks_tui.install:install'
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
