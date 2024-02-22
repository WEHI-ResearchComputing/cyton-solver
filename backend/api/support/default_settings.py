"""
Last Edit: 11-Feb-2024

Function for Endpoint: Default Settings
"""
from core.settings import DEFAULT_PARS, DEFAULT_BOUNDS, DEFAULT_VARY

def get_default_settings():
    """
    Retrieve the default settings for parameter, bounds and vary.

    Returns:
    - dict: A dictionary containing the default settings.
    """
    default_settings = {
        'parameters': DEFAULT_PARS,
        'bounds': DEFAULT_BOUNDS,
        'vary': DEFAULT_VARY
    }
    return default_settings