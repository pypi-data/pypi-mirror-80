
class damagefunctions:
    def pistrika_US_2010_block_group(water_depth_m, velocity_ms):
        """Damage fraction [0-1] from water depth (m) and flow velocity (m/s) using Pistrika and Jonkman (2010) results for block group
        Parameters
        ----------
        water_depth_m : float, (default : None)
            Water depth in meters
        velocity_ms : float, (default : None)
            Flow velocity in m/s
        Returns
        -------
        Damage ratio between 0 and 1.
        References
        ----------
        * (Pristrika and Jonkman (2010))[https://link.springer.com/article/10.1007/s11069-009-9476-y]
        """
        return 0.422+0.075*water_depth_m*velocity_ms**0.682

    def pistrika_US_2010_block(water_depth_m, velocity_ms):
        """Damage fraction [0-1] from water depth (m) and flow velocity (m/s) using Pistrika and Jonkman (2010) results for block
        Parameters
        ----------
        water_depth_m : float, (default : None)
            Water depth in meters
        velocity_ms : float, (default : None)
            Flow velocity in m/s
        Returns
        -------
        Damage ratio between 0 and 1.
        References
        ----------
        * (Pristrika and Jonkman (2010))[https://link.springer.com/article/10.1007/s11069-009-9476-y]
        """
        return 0.457+0.063*water_depth_m*velocity_ms**0.654