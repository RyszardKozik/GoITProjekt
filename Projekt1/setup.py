from setuptools import setup, find_packages

setup(
    name='GoITProjekt',
    version='1.0',
    description='Osobisty asystent do zarządzania kontaktami i notatkami.',
    url='https://github.com/PartickPinace/GoITProjekt.git',
    author='Projekt Python grupa 3',
    author_email='komorowskimateusz96@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'python-Levenshtein',
    ],
)