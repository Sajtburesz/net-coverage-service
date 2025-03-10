class BaseGeoCodingException(Exception):
    """Base class for GeoCodingExceptions so in a try except I could catch all of this type in 1 except"""

class GeoCodingPointNotFound(BaseGeoCodingException):
    """Custom exception for when absolutely no geocoding point found with address or gps"""
    pass

class GeoCodingMissingCityCodes(BaseGeoCodingException):
    """Custom exception for when a point is found but no insee and no postcode is returned"""