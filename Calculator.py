"""
This simple program asks the user to supply a distance between two points in space and an acceleration value, and uses
those to calculate how long the trip will take (assuming the ship wants to stop at the end of the trip and so will need
to slow down again) if the ship accelerates continuously for the first half of the trip and turns around to decelerate
for the second half.
"""

__author__ = 'AHAHAHAHAHAHAHAHA'

import math

def distance_traveled():
    """
    Asks user for distance to be traveled, which should be given in meters, kilometers, astronomical units, or miles.
    Separates distance number from unit label and ensures that both are valid. Identifies unit from label and converts
    distance number to meters for calculations in later steps.
    """
    user_distance = raw_input("How far is the ship going? Include unit label (m, km, au, or mi). ")
    distance = ""
    unit = ""
    for ch in user_distance:
        if ch in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            distance = distance + str(ch)
        elif ch == ".":
            distance = distance + "."
        elif ch == ",":
            distance = distance + "."
        else:
            unit = unit + str(ch)
    unit = unit.strip(" ")
    if distance[-1] == ".":
        distance = distance.strip(".")
    while True:
        try:
            float(distance)
        except ValueError:
            distance = raw_input("Invalid input. Please enter a positive number with no other non-decimal characters. ")
            continue
        else:
            break
    while float(distance) <= 0:
        distance = raw_input("Invalid input. Please enter a positive number. ")
        try:
            float(distance)
        except ValueError:
            distance = raw_input("Invalid input. Please enter a positive number with no other non-decimal characters. ")
            continue
        else:
            break
    distance = float(distance)
    expected_units_m = ["m", "meters"]
    expected_units_km = ["km", "kilometers"]
    expected_units_mi = ["mi", "miles"]
    expected_units_au = ["au", "ua", "astronomical units", "astronomical unit", "astronomic units", "astronomic unit"]
    while unit not in expected_units_m and unit not in expected_units_km and unit not in expected_units_au and unit \
            not in expected_units_mi:
        unit = raw_input("Unexpected unit type or label. Valid units are meters (m), kilometers (km), "
                         "astronomical units (au), or miles (mi). ")
    if unit in expected_units_m:
        distance = distance
    elif unit in expected_units_km:
        distance = distance * 1000
    elif unit in expected_units_au:
        distance = distance * 149597870700
    elif unit in expected_units_mi:
        distance = round((distance * 1609.344), 0)
    return distance


def acceleration():
    """
    Ask user for acceleration of ship in g. Assumes constant acceleration.
    """
    """
    This block allowed the user to choose whether to use m/s^2 or g as the unit of acceleration.
    valid_units = ["m", "M", "g", "G"]
    unit = raw_input("Would you like to enter burn acceleration in meters per second squared (press M) or in g-forces (press G)? ")
    while unit not in valid_units:
        unit = raw_input("Invalid input. Please press M for m/s^2 or G for g-forces. ")
    """
    acceleration = raw_input("What is the ship's acceleration in g? ")
    while True:
        try:
            float(acceleration)
        except ValueError:
            acceleration = raw_input("Invalid input. Please enter a positive number with no other non-decimal "
                                     "characters. ")
            continue
        else:
            break
    while float(acceleration) <= 0:
        acceleration = raw_input("Invalid input. Please enter a positive number. ")
        try:
            float(acceleration)
        except ValueError:
            acceleration = raw_input("Invalid input. Please enter a positive number with no other non-decimal "
                                     "characters. ")
            continue
        else:
            break
    # These two lines assisted the block above in converting to g if m/s^2 was chosen as the unit of acceleration.
    '''if unit in ["m", "M"]:
        acceleration = round(float(acceleration) / 9.8, 2)'''
    return float(acceleration)


distance_meters = distance_traveled()
burn = acceleration()
accel_mps2 = burn * 9.8


def calculate_travel_time_complex(distance_meters, accel_mps2):
    """
    Given distance of trip and acceleration, calculate travel time by procedurally incrementing speed and total distance
    traveled each second until the halfway point is reached, then double travel time to account for deceleration. This
    method was superseded by the simple method below, but was the initial means of calculation and served as a useful
    way to test the accuracy of the simple method's math. Returns travel time and highest speed reached during
    iterations.
    """
    time = 0
    distance_progress = 0
    speed = 0
    halfway_point = distance_meters / 2
    while distance_progress < halfway_point:
        time = time + 1
        speed = speed + accel_mps2
        distance_progress = distance_progress + speed
        """
        Output progress 
        print "{0} seconds | speed: {1} m/s | distance traveled: {2} m".format(time, speed, distance_progress)
        """
    time = time * 2
    return [time, speed]


def calculate_travel_time_simple(distance_meters, accel_mps2):
    """
    Given distance of trip and acceleration, calculate travel time by solving for t in the equation x = 0.25 * a * t^2,
    where x is distance and a is acceleration, and calculate the top speed of the trip. Returns travel time and top
    speed.
    """
    time = math.sqrt(4 * distance_meters / accel_mps2)
    speed = accel_mps2 * time * 0.5
    return [time, speed]


trip_data = calculate_travel_time_simple(distance_meters, accel_mps2)
trip_seconds = trip_data[0]
top_speed_mps = trip_data[1]


# Convert the calculated travel time into meaningful units.
def convert_travel_time(trip_seconds):
    """
    Given the travel time in seconds, determine whether at least one year would pass during the trip, then reduce the
    remaining seconds by a number of seconds equivalent to that many years. Repeat for months (deprecated), weeks,
    days, hours, and minutes. Returns the duration of the trip in those combined units. Note that the result shows how
    many of a unit pass after accounting for higher-order units; if a trip takes 10 days (1 week and 3 days), the days
    returned will be 3.
    """
    trip_time = trip_seconds
    years = 0
    months = 0
    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    if trip_time >= 31536000:
        years = math.trunc(trip_time / 31536000)
        trip_time = trip_time - 31536000 * years
    # This block calculated months, which I stopped using because a month of ~30.5 days is not as intuitive as I'd like.
    '''if trip_time >= 2628000:
        months = math.trunc(trip_time / 2628000)
        trip_time = trip_time - 2628000 * months'''
    if trip_time >= 604800:
        weeks = math.trunc(trip_time / 604800)
        trip_time = trip_time - 604800 * weeks
    if trip_time >= 86400:
        days = math.trunc(trip_time / 86400)
        trip_time = trip_time - 86400 * days
    if trip_time >= 3600:
        hours = math.trunc(trip_time / 3600)
        trip_time = trip_time - 3600 * hours
    if trip_time >= 60:
        minutes = math.trunc(trip_time / 60)
        trip_time = trip_time - 60 * minutes
    seconds = trip_time
    return [years, weeks, days, hours, minutes, seconds]


travel_time = convert_travel_time(trip_seconds)
years = travel_time[0]
# months = travel_time[1]
weeks = travel_time[1]
days = travel_time[2]
hours = travel_time[3]
minutes = travel_time[4]
seconds = math.trunc(round(travel_time[5], 0))


# Print the metrics for the trip.
def print_results(distance_meters, burn, top_speed_mps, years, weeks, days, hours, minutes, seconds):
    """
    Given the trip distance in meters, the acceleration in g, the calculated top speed, and the calculated number of
    years, weeks, days, hours, minutes, and seconds that the trip takes, print for the user their total distance
    traveled in kilometers, their acceleration in g, their top speed in kilometers per hour, and their total travel
    time. Three time formats are currently supported (examples given for a trip from Earth to Eris with a distance of
    67.864 au and a constant acceleration of 1 g):
    1) longform written time (3 weeks, 2 days, 13 hours, 27 minutes, 13 seconds)
    2) the international ISO 8601 format with months removed (P3W2D13HT27M13S)
    3) ISO 8601 for years, weeks, and days, and a traditional clock format for hours, minutes, and seconds
        (3W2D 13:27:13)
    All three formats are enabled by default; to disable a format, comment out or delete its print line at the end of
    this function (formats are printed in the order listed above).
    """
    print "Distance traveled: {0:.3f} km".format(distance_meters / 1000)
    print "Burn value: {0} g".format(burn)
    print "Top speed: {0:.3f} km/h".format(top_speed_mps * 3.6)
    if years == 1:
        years_text = "{0} year, ".format(years)
        years_note = "{0}Y".format(years)
    elif years > 1:
        years_text = "{0} years, ".format(years)
        years_note = "{0}Y".format(years)
    else:
        years_text = ""
        years_note = ""
    # This block formatted the outputs for the now-defunct month unit.
    '''if months == 1:
        months_text = "{0} month, ".format(months)
        months_note = "{0}M".format(months)
    elif months > 1:
        months_text = "{0} months, ".format(months)
        months_note = "{0}M".format(months)
    else:
        months_text = ""
        months_note = ""'''
    if weeks == 1:
        weeks_text = "{0} week, ".format(weeks)
        weeks_note = "{0}W".format(weeks)
    elif weeks > 1:
        weeks_text = "{0} weeks, ".format(weeks)
        weeks_note = "{0}W".format(weeks)
    else:
        weeks_text = ""
        weeks_note = ""
    if days == 1:
        days_text = "{0} day, ".format(days)
        days_note = "{0}D".format(days)
    elif days > 1:
        days_text = "{0} days, ".format(days)
        days_note = "{0}D".format(days)
    else:
        days_text = ""
        days_note = ""
    if hours == 1:
        hours_text = "{0} hour, ".format(hours)
        hours_note = "{0}H".format(hours)
        hours_clock = "{0:02d}".format(hours)
    elif hours > 1:
        hours_text = "{0} hours, ".format(hours)
        hours_note = "{0}H".format(hours)
        hours_clock = "{0:02d}".format(hours)
    else:
        hours_text = ""
        hours_note = ""
        hours_clock = "{0:02d}".format(hours)
    if minutes == 1:
        minutes_text = "{0} minute, ".format(minutes)
        minutes_note = "{0}M".format(minutes)
        minutes_clock = "{0:02d}".format(minutes)
    elif minutes > 1:
        minutes_text = "{0} minutes, ".format(minutes)
        minutes_note = "{0}M".format(minutes)
        minutes_clock = "{0:02d}".format(minutes)
    else:
        minutes_text = ""
        minutes_note = ""
        minutes_clock = "{0:02d}".format(minutes)
    if seconds == 1:
        seconds_text = "{0} second, ".format(seconds)
        seconds_note = "{0}S".format(seconds)
        seconds_clock = "{0:02d}".format(seconds)
    elif seconds > 1:
        seconds_text = "{0} seconds, ".format(seconds)
        seconds_note = "{0}S".format(seconds)
        seconds_clock = "{0:02d}".format(seconds)
    else:
        seconds_text = ""
        seconds_note = ""
        seconds_clock = "{0:02d}".format(seconds)
    print ("Travel time: {0}{1}{2}{3}{4}{5}".format(years_text, weeks_text, days_text, hours_text, minutes_text,
                                                    seconds_text)).strip(", ")
    print "Travel time: P{0}{1}{2}T{3}{4}{5}".format(years_note, weeks_note, days_note, hours_note, minutes_note,
                                                     seconds_note)
    print "Travel time: {0}{1}{2} {3}:{4}:{5}".format(years_note, weeks_note, days_note, hours_clock, minutes_clock,
                                                      seconds_clock)


print_results(distance_meters, burn, top_speed_mps, years, weeks, days, hours, minutes, seconds)
