# users-config

A simple configuration manager for user-specific app configuration files.
Written in Python.

## Purpose

The idea behind the project is to have a common component which can be reused in multiple applications to store configuration. Sounds simple but, for whatever reason, I could not find an appropriate solution and it was more cost-effective in terms of time to package my code into a separate Python package.

## Features

The library offers the following:

- store the configuration in a standardized, user- and application- specific configuration file, using xdg_config_home variable
- use Yaml for easy manual modifications
- expose the functionality to other Python programs and scripts

