def point_from_coord(coords):
    """
    Return the point type from the coordinates names

    This function should not be used if the data are correctly opened
    with open_nemo function that sets an attribute with the point type

    Parameters
    ----------
    coords : list of strings
        Contain the name of the coordinates (e.g. ['x_c', 'y_c', 'time']
    """
    raise (NotImplementedError)


class Point:
    """
    Point types

    TODO
    """

    def __init__(self, point_type):
        """
        point_type : 'T', 'U', 'V', 'F', 'W', 'UW', 'VW', 'FW'
        """
        if point_type not in ["T", "U", "V", "F", "W", "UW", "VW", "FW"]:
            raise (
                ValueError(
                    "*point_type* must be in ['T', 'U', 'V', 'F', 'W', 'UW', 'VW', 'FW'] \n   We got point_type={}".format(
                        point_type
                    )
                )
            )
        self.point_type = point_type
        self.get_x()
        self.get_y()
        self.get_z()

    def get_x(self):
        if self.point_type in ["T", "V", "W", "VW"]:
            # Center of the cell
            self.x = "x_c"
        elif self.point_type in ["U", "F", "UW", "FW"]:
            # Face of the cell
            self.x = "x_f"

    def get_y(self):
        if self.point_type in ["T", "U", "W", "UW"]:
            # Center of the cell
            self.y = "y_c"
        elif self.point_type in ["V", "F", "VW", "FW"]:
            self.y = "y_f"

    def get_z(self):
        if self.point_type in ["T", "U", "V", "F"]:
            self.z = "z_c"
        elif self.point_type in ["W", "UW", "VW", "FW"]:
            self.z = "z_f"
