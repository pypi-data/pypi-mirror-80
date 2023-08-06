from PyWatermark.constants import POSITION_CONSTANTS, SIZE_CONSTANTS
class WatermarkException(Exception):
    """Creating the WatermarkException class."""

    # * We'll use clear codes to segregate between different types of errors
    def __init__(self, errorcode, val = None):
        """__init__ function for error messages.

        Send back error messages.
            Args:
                errorcode(int) : Specifying the errorcodes for different errors
                val(any): Any argument regarding the error
        """
        if errorcode == 0:
            super().__init__("INVALID POSTION CODE - \"{}\", MUST BE ONE OF : ".format(val), POSITION_CONSTANTS)
        elif errorcode == 1:
            super().__init__("INVALID SIZE CODE - \"{}\", MUST BE ONE OF : ".format(val), SIZE_CONSTANTS.keys())
        elif errorcode == 2:
            super().__init__("This font - {} isn't available, if you want to use your custom font give it your own path".format(val))
        elif errorcode == 3:
            super().__init__("Looks like you're using a custom font, make sure the path is valid and of .ttf extension.\n Invalid path - {}.".format(val))
        elif errorcode == 4:
            super().__init__("This is not a valid image file - {}".format(val))