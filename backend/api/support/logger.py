"""
Logger

Creates a logger object that can be used to log messages to the console.
"""
import logging

def initialize_logger():

    log = logging.getLogger("app.py")
    log.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_handler.setFormatter(logging.Formatter('%(levelname)s:     %(asctime)s - %(message)s'))
    log.addHandler(c_handler) 
    
    return log