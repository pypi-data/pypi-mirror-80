"""
Setup configuration for the package.
"""
from setuptools import setup, find_packages

setup(name='usersconfig',
      version='0.1.7',
      packages=find_packages(),
      license='GPL3',
      # zip_safe=False,
      #install_requires=['click', 'click_log'],
      #include_package_data=True,
      package_data={'usersconfig': ['default_config.yml', 'TODO']},
      # metadata to display on PyPI
      author='Alen Šiljak',
      author_email='usersconfig@alensiljak.eu.org',
      description='Library for application configuration management',
      keywords='configuration library yaml',
      url='https://gitlab.com/alensiljak/usersconfig',
      project_urls={
          "Source Code": "https://gitlab.com/alensiljak/usersconfig.git"
      },
      # Scripts
    #   entry_points={
    #       "console_scripts": [
    #           "ib = ibcli.cli:cli"
    #       ]
    #   }
    install_requires=['pyxdg', 'pyyaml']

      )
