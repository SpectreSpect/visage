import os
import logging


DEBUG = os.getenv("DEBUG", "False").lower() == "true"


def validate_dict(data: dict, required_key: str, context: str) -> dict:
    """
    Checks if a dictionary is not None and contains a required key.
    
    :param data: The dictionary to validate.
    :param required_key: The key that must be present.
    :param context: A message describing where this check is happening.
    :return: The original dictionary if valid, otherwise None.
    """
    if data is None:
        full_msg = f"{context}: Expected a dictionary but got None."
    elif required_key not in data:
        full_msg = f"{context}: Missing required key '{required_key}' in dictionary."
    else:
        return data  # Valid dictionary

    if DEBUG:
        raise KeyError(full_msg)

    logging.error(full_msg)
    return None