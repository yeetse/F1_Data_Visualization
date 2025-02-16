import matplotlib.pyplot as plt
import fastf1
from fastf1 import plotting
import sys

fastf1.plotting.setup_mpl(misc_mpl_mods=True, color_scheme="fastf1")


def analyze_2_drivers(driver1, driver2, year, race_identifier, session_type):
    """
    Creates a telemetry sheet comparing two drivers
    :param driver1: the first driver's number in the form of a int
    :param driver2: the second driver's number in the form of a int
    :param year: the year of the race
    :param race_identifier: The country the race was held in
    :param session_type: the session which you want to get the data from (FP1/2/3, Q, or R), with FP1/2/3
        being Free Practice 1/2/3, Qualifying, or Race, respectively
    :return: a telemetry sheet that shows the overlap of data of both drivers
    """
    session = fastf1.get_session(year, race_identifier, session_type)
    session.load(laps=False, telemetry=False, weather=False)

    # checks to see if the driver participated in the session
    if (str(driver1) not in session.drivers or str(driver2) not in session.drivers):
        print("Driver not valid")
        sys.exit()  # stops the running of the rest of the code if a driver was not in the session

    # loads the rest of session data if both drivers were in the session
    session.load(laps=True, telemetry=True, weather=True)

    driver1_name = session.get_driver(str(driver1))["LastName"]
    driver2_name = session.get_driver(str(driver2))["LastName"]


    # driver1_num = str(session.get_driver(driver1)["DriverNumber"])
    # Grabbing driver 1's fastest lap in the given session (FP1/2/3, Q, or R)
    driver1_fastest = session.laps.pick_drivers(driver1).pick_fastest()
    driver1_car_data = driver1_fastest.get_car_data()  # Grabbing the car data from that fastest lap
    driver1_fastest_lap_time = str(driver1_fastest["LapTime"]).split()[2].split("00:0")[1][:-3]  # Grabbing the
    # actual lap time

    # Grabbing driver 2's fastest lap in the given session (FP1/2/3, Q, or R)
    driver2_fastest = session.laps.pick_drivers(driver2).pick_fastest()
    driver2_car_data = driver2_fastest.get_car_data()
    driver2_fastest_lap_time = str(driver2_fastest["LapTime"]).split()[2].split("00:0")[1][:-3]  # Grabbing the

    # Setting time and speed variable
    t1 = driver1_car_data["Time"]
    speed1 = driver1_car_data["Speed"]
    rpm1 = driver1_car_data["RPM"]
    gear1 = driver1_car_data["nGear"]
    throttle1 = driver1_car_data["Throttle"]
    brake1 = driver1_car_data["Brake"]

    t2 = driver2_car_data["Time"]
    speed2 = driver2_car_data["Speed"]
    rpm2 = driver2_car_data["RPM"]
    gear2 = driver2_car_data["nGear"]
    throttle2 = driver2_car_data["Throttle"]
    brake2 = driver2_car_data["Brake"]

    # Setting up plot
    fig, ax = plt.subplots(5, 1, gridspec_kw={"height_ratios": [4, 2, 1, 1, 1]})
    ax[0].plot(t1, speed1, label=driver1)
    ax[0].plot(t2, speed2, label=driver2)
    ax[0].set_ylabel("Speed")

    ax[1].plot(t1, rpm1, label=driver1)
    ax[1].plot(t2, rpm2, label=driver2)
    ax[1].set_ylabel("RPM")

    ax[2].plot(t1, gear1, label=driver1)
    ax[2].plot(t2, gear2, label=driver2)
    ax[2].set_ylabel("Gear")

    ax[3].plot(t1, throttle1, label=driver1)
    ax[3].plot(t2, throttle2, label=driver2)
    ax[3].set_ylabel("Throttle %")

    ax[4].plot(t1, brake1, label=driver1)
    ax[4].plot(t2, brake2, label=driver2)
    ax[4].set_xlabel("Time")
    ax[4].set_ylabel("Brake (Y/N)")

    fig.suptitle("FL of " + driver1_name + " versus " + driver2_name + " (" + str(year) +
                 " " + race_identifier + " Grand Prix " + session_type + ")", fontsize=16, y=.97)
    ax[0].set_title(driver1_name + ": " + driver1_fastest_lap_time + "; " + driver2_name + ": " +
                    driver2_fastest_lap_time, fontsize=12)

    ax[0].legend(loc="lower right", fontsize="x-small")
    plt.subplots_adjust(hspace=0.5)

    plt.show()
