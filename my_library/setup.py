# setup.py
from setuptools import setup, find_packages

setup(
    name='my_library',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'mysql-connector-python',
        'openai',
        'werkzeug'
    ],
    entry_points={
        'console_scripts': [
            'my-library-run = my_library.run:main',
        ],
    },
)
