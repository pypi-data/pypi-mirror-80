from setuptools import setup, find_packages

setup(name = 'brebsML',
      version = "1.0.6",
      description = 'Toutes les librairies que nous utiliseront pour ce comité',
      install_requires=[
          "tensorflow",
          "keras",
          "lightgbm",
          "matplotlib",
          "pandas",
          "scikit-learn",
          "seaborn",
          "xgboost",
          "scipy",
          "sklearn-pandas"
      ],

      setup_requires=["wheel"] 




)



