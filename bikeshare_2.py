import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def seconds_to_date(seconds):
    """
    Converts seconds's float to readable string format days, hours, minutes and seconds.

    :param seconds: float
    :return: x days, y hours, z minutes, 21 seconds

    sample:
    readable_string = seconds_to_date(972021.0)
    print(readable_string) => 11 days, 6 hours, 0 minutes, 21 seconds

    """
    seconds = int(seconds)
    days = divmod(seconds, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    return "%i days, %i hours, %i minutes, %i seconds" % (days[0], hours[0], minutes[0], minutes[1])


def get_day():
    """
    Asks user to specify a day to filter on, or choose all.
    Returns:
        (str) day - day of the week to use for the analyse, "all" for no filter
    """
    for i in range(1, len(DAYS)+1):
        print('{0:20}. {1}'.format(i, DAYS[i-1]))

    day = ''
    while True:
        try:
            day = input("\nEnter the day with Monday=1, Sunday=7 or 'all' ")
        except:
            print(" !!! Error : you must insert  :  1 - 7, or  all")
            continue

        if day == 'all':
            break
        elif day in {'1', '2', '3', '4', '5', '6', '7'}:
            day = DAYS[int(day) - 1]
            break
        else:
            continue

    return day


def get_month():
    """
    Asks user to specify a month to filter on, or choose all.
    Returns:
        (str) month - name of the month to filter by, or "all" for no filter
    """
    for i in range(1, len(MONTHS)+1):
        print('{0:20}. {1}'.format(i, MONTHS[i-1]))

    month = 'all'
    while True:
        try:
            month = input("\nEnter the month with January=1, June=6 or 'all' ")
        except:
            print(" !!! Error : you must insert  :   1 - 6, all ")
            continue

        if month == 'all':
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            # reassign the string name for the month
            month = MONTHS[int(month) - 1]
            break
        else:
            continue

    return month


def get_city():
    """
    Asks user to specify a city.
    Returns:
        (str) city - name of the city to use for the analyse
    """
    cities = []
    cities_count = 0

    for city in CITY_DATA:
        cities.append(city)
        cities_count += 1
        print('{0:20}. {1}'.format(cities_count, city.title()))

    # ask the user to input a number for a city from the list; easier for user than string input
    while True:
        try:
            city_num = int(input("\nEnter a number for the city (1 - {}):  ".format(len(cities))))
        except:
            continue

        if city_num in range(1, len(cities) + 1):
            break

    # get the city's name in string format from the list
    city = cities[city_num - 1]
    return city


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()

    # get user input for month (all, january, february, ... , june)
    month = get_month()

    # get the user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()

    # load city's data from file in dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to correct datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')

    # get month, day of week and hour from Start Time and create new columns
    df['month'] = df['Start Time'].dt.month  # range(1, 12)
    df['day_of_week'] = df['Start Time'].dt.dayofweek  # range(0, 6)
    df['hour'] = df['Start Time'].dt.hour  # range(0, 23)

    init_total_rides = len(df)
    filtered_rides = init_total_rides  # initially

    # Here , filter by month if applicable
    if month != 'all':
        # Get the correct int by MONTHS list index
        month_m = MONTHS.index(month) + 1

        # result of the filter is new dataframe
        df = df[df.month == month_m]
        month = month.title()

    # Here ,filter by day of week if applicable
    if day != 'all':
        #  Get the correct int by DAYS list index
        day_d = DAYS.index(day)  # index() returns 0-based, matches df

        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day_d]
        day = day.title()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = MONTHS[df['month'].mode()[0] - 1].title()
    print('  The most common month is :         ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    common_day = DAYS[common_day].title()
    print('   The most common day of the week is :    ', common_day)

    # display the most common start hour
    common_hour = datetime.strptime(str(df['hour'].mode()[0]), "%H").strftime("%I %p")

    print('     The most common start hour:          ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    rides = len(df)

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_station_trips = df['Start Station'].value_counts()[start_station]

    print('    The most common start station is :       ', start_station)
    print('{0:30}{1}/{2} trips'.format(' ', start_station_trips, rides))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    end_station_trips = df['End Station'].value_counts()[end_station]

    print('    The most common end station:         ', end_station)
    print('{0:30}{1}/{2} trips'.format(' ', end_station_trips, rides))

    # display most frequent combination of start station and end station trip
    df_start_end_combination_gd = df.groupby(['Start Station', 'End Station'])
    most_freq_trip_count = df_start_end_combination_gd['Trip Duration'].count().max()
    most_freq_trip = df_start_end_combination_gd['Trip Duration'].count().idxmax()

    print('    The most frequent trip is:        {}, {}'.format(most_freq_trip[0], most_freq_trip[1]))
    print('{0:30}{1} trips'.format(' ', most_freq_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print('    Total travel time:   ', total_travel_time, 'seconds')
    print('                             ', seconds_to_date(total_travel_time))

    # display mean travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print('    Total travel time:   ', total_travel_time, 'seconds')
    print('                             ', seconds_to_date(total_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for identifier in range(len(user_types)):
        val = user_types[identifier]
        user_type = user_types.index[identifier]
        print('    {0:21}'.format((user_type + ':')), val)

    # Display counts of gender
    if 'Gender' in df.columns:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        for identifier in range(len(genders)):
            val = genders[identifier]
            gender = genders.index[identifier]
            print('    {0:21}'.format((gender + ':')), val)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('    Year of Birth...')
        print('        Earliest:        ', int(df['Birth Year'].min()))
        print('        Most recent:     ', int(df['Birth Year'].max()))
        print('        Most common:     ', int(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
