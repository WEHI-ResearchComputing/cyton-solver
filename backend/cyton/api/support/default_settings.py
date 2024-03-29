"""
Last Edit: 11-Feb-2024

Function for Endpoint: Default Settings
"""
from cyton.core.settings import DEFAULT_PARS, DEFAULT_BOUNDS, DEFAULT_VARY
from cyton.core.models import ExperimentSettings

def get_default_settings() -> ExperimentSettings:
    """
    Retrieve the default settings for parameter, bounds and vary.

    Returns:
    - dict: A dictionary containing the default settings.
    """
    return ExperimentSettings(
        parameters=DEFAULT_PARS,
        bounds=DEFAULT_BOUNDS,
        vary=DEFAULT_VARY
    )
