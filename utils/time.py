def julian_date(year, month, day, hour, minute, second):
    """
    get Julian Date from gregorian calendar

    :param year int
    :param month int
    :param day int
    :param hour int
    :param minute int
    :param second float
    :return: julian date (float)
    """
    m_term = -int((-month + 14) / 12)
    a_term = int((1461 * (year + 4800 + m_term)) / 4)
    b_term = int((367 * (month - 2 - 12 * m_term)) / 12)
    c_term = int((3 * int((year + 4900 + m_term) / 100)) / 4)
    j = a_term + b_term - c_term + day
    j -= 32075
    # offset to start of day
    j -= 0.5

    # Apply the time
    jd = j + (hour + (minute + (second / 60.0)) / 60.0) / 24.0

    return jd


# ---------------------------------------- #
# Auxiliary function: Modified Julian Date #
# ---------------------------------------- #
def modified_julian_date(year, month, day, hour, minute, second):
    """
    get modified julian date (MJD):
        The MJD therefore gives the number of days since midnight on November 17, 1858.
        This date corresponds to 2400000.5 days after day 0 of the Julian calendar

    :param year: int
    :param month: int
    :param day: int
    :param hour: int
    :param minute: int
    :param second: float
    :return: Modified julian date (float)
    """
    return julian_date(year, month, day, hour, minute, second) - 2400000.5


def modified_julian_date2000(year, month, day, hour, minute, second):
    """
    get modified julian date since the 1st January of Year 2000 at 0h 0m 0s Terrestrial Time.
    see https://www.isdc.unige.ch/integral/download/osa/doc/11.0/osa_um_intro/node32.html

    :param year: int
    :param month: int
    :param day: int
    :param hour: int
    :param minute: int
    :param second: float
    :return: mjd2000 (float)
    """
    return modified_julian_date(
        year, month, day, hour, minute, second) - 51544.0
