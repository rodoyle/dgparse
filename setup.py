from setuptools import setup, find_packages


setup(
    name='dgparse',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'click',
        'openpyxl>=2.4.0',
        'xlsxwriter',
        'marshmallow>=2.0.0b4',
    ],
    entry_points={
        'console_scripts': ['snapgene-json = dgparse.snapgene.main:main'],
    },
)
