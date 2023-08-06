import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.2.8'
PACKAGE_NAME = 'train_test_plot_def'
AUTHOR = 'Dr Debdarsan Niyogi'
AUTHOR_EMAIL = 'debdarsan.niyogi@gmail.com'
URL = 'https://github.com/debdarsan/train_test_plot_def'

LICENSE = 'MIT License'
DESCRIPTION = 'Python package to train, test, evaluate and plot confusion matrices, feature importance for classification problem using default settings of classifiers'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'matplotlib',
      'seaborn',
      'sklearn',
      'xgboost'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )