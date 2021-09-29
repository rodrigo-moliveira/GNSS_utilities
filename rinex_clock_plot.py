import os
import numpy as np
from sklearn.linear_model import LinearRegression

import utils


# ------------------------------- #
#        User configuration       #
# ------------------------------- #
# configure data to read and plot
clock_paths = ("data/clocks/CLOCKBIAS_SV_OS_20160303.clk",
               "data/clocks/CLOCKBIAS_GS_OS_20160303.clk"
               )

# list of satellites to plot
satellite_list = ("E11",
                  "E12")
all_sats = False

# list of stations to plot
station_list = (
)
all_stations = False

remove_linear_trend = True


def read_clocks(container, clocks_paths):
    """

    Read each file and store clock data
    line format:
        AR/AS ID time_tag #values clock_bias [... optional]

    examples:
        AR EASa 2000  3 27  0  0  0.000000  1    1.197356518483E-01 -> AR for stations
        AS E11  2016  3  3  0  0  0.000000  1    1.197356518483E-01 -> AS for satellites


    :param container:
    :param clocks_paths:
    :return:
    """

    n = 0

    for fn in clocks_paths:
        print("Loading Clock File: " + os.path.basename(fn) + "...")
        try:
            clkFile = open(fn)
            n += 1
        except FileNotFoundError:
            print("WARNING: failed to open " + os.path.basename(fn))
            continue

        # iterate in clock file lines
        for line in clkFile:
            tokens = line.split()
            if tokens[0] == "AR" or tokens[0] == "AS":  # it is a valid measure

                # Get epoch in MJD2000
                year = int(tokens[2])
                month = int(tokens[3])
                day = int(tokens[4])
                hour = int(tokens[5])
                minute = int(tokens[6])
                sec = float(tokens[7])
                epoch = utils.modified_julian_date2000(year, month, day, hour, minute, sec)
                # store clk value

                value = float(tokens[9])

                # print(tokens[1], epoch, value)
                if tokens[0] == "AS":
                    container.addSatClock(tokens[1], epoch, value)

                elif tokens[0] == "AR":
                    container.addStationClock(tokens[1], epoch, value)
    if n == 0:
        print("ERROR: No clock data available, exiting...")
        exit()

    print("available satellites: " + str(list(container.SatClocksDict.keys())))
    print("available stations: " + str(list(container.StationClocksDict.keys())))


def plot_clocks(rinex_clocks, satellite_list, station_list, detrend=False):
    # plot satellites
    SatClocksDict = rinex_clocks.SatClocksDict

    for sat, time_series in SatClocksDict.items():

        if sat in satellite_list:
            # plot this sat
            print("plotting satellite " + sat + "...")

            # get time and clock data
            time = np.array(list(time_series.keys()))
            clocks = np.array(list(time_series.values()))

            # plot
            title = sat
            if detrend:
                utils.plots.new_plot(time, clocks, title, label="estimated")
                clocks_wo_trend, predicted = flatten_data(time, clocks)
                utils.plots.new_plot(time, predicted, title, new_figure=False, label="linear")

                title += " without linear trend"
                utils.plots.new_plot(time, clocks_wo_trend, title)
            else:
                utils.plots.new_plot(time, clocks, title, label="estimated")

    # plot stations
    StationClocksDict = rinex_clocks.StationClocksDict

    for station, time_series in StationClocksDict.items():

        if station in station_list:
            # plot this sat
            print("plotting station " + station + "...")

            # get time and clock data
            time = np.array(list(time_series.keys()))
            clocks = np.array(list(time_series.values()))

            # plot
            title = station
            if detrend:
                utils.plots.new_plot(time, clocks, title, label="estimated")
                clocks_wo_trend, predicted = flatten_data(time, clocks)
                utils.plots.new_plot(time, predicted, title, new_figure=False, label="linear")

                title += " without linear trend"
                utils.plots.new_plot(time, clocks_wo_trend, title)
            else:
                utils.plots.new_plot(time, clocks, title, label="estimated")


def flatten_data(x, y):
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    lr = LinearRegression().fit(x, y)
    slope = lr.coef_[0][0]
    y_int = lr.intercept_[0]
    flattened = []
    predicted = []
    for i in range(len(x)):
        expected_val = slope * x[i] + y_int
        flattened.append(y[i] - expected_val)
        predicted.append(expected_val)
    return flattened, predicted


def main():
    global satellite_list, station_list

    rinex_clocks = utils.RinexClockContainer()
    read_clocks(rinex_clocks, clock_paths)

    if all_sats:
        satellite_list = list(rinex_clocks.SatClocksDict.keys())
    if all_stations:
        station_list = list(rinex_clocks.StationClocksDict.keys())

    plot_clocks(rinex_clocks, satellite_list, station_list, remove_linear_trend)

    utils.plots.show()


if __name__ == "__main__":
    main()
