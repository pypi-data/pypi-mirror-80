class Photo(object):
    """
    Array with associated photographic information.

    Attributes
    ----------
    exposure : float
        Exposure in seconds.

    Raises
    ------
    `Photo.colorspace`(c='rgb')
        Represent the photo in the given colorspace.
    `Photo.gamma(n=1.0)`
        Change the photo's gamma exposure.
    """
    
    def colorspace(self, c='rgb'):
        """Set the colorspace.
        """
        self.cs = c

    def gamma(self, n=1.0):
        """Set gamma correction.

        Parameters
        ----------
        n: float
            The gamma correction factor
        """
        self.gamma = n

