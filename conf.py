import configparser
import os

def get_conf(sect):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if sect in config:
        return config[sect]

