import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
             
cities = ['chicago','new york city','washington']
months = ['january','february','march','april','may','june','all']
days =['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city= str(input('Enter the city that you want to view the data from. Choices are: Chicago, New York City, or Washington: ')).lower()
        
        if city in cities:
            break    
        else:
            print('Please choose a valid city name.')
            
    # get user input for month (all, january, february, ... , june)
    while True:
        month= str(input('Enter the month that you want to view the data from. Months available are from January to June. Type All if you want to view the full data set: ')).lower()
    
        if month in months:
            break
        else:
            print('Please choose a valid month.')     
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:    
        day= str(input('Enter the day that you want to view the data from. Days available are from Sunday to Saturday. Type All if you want to view the full data set: ')).lower()
        
        if day in days:
            break    
        else:
            print('Please choose a valid day.')
            
    #summarise results
    print('\nYou have chosen the following:\ncity: {},\nmonth: {},\nday: {}'.format(city.title(), month.title(), day.title()))
    
    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']= df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        
        df = df[df['day_of_week'] == day.title()]
        
    return df
    

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    
    #map to month
    print('The most popular month is: {}'.format(months[popular_month - 1].title()))

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    
    #map to day
    print('The most popular day is: {}'.format(popular_dow.title()))

    # display the most common start hour
   
    popular_hour = df['hour'].mode()[0]
    
    #map to hour
    print('The most popular hour is: {}:00'.format(popular_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station= df['Start Station'].mode()[0]
    print('The most popular start station is: {}'.format(popular_start_station))
    
    # display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    print('The most popular end station is: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_combination= (df['Start Station'] + " to " + df ['End Station']).mode()[0]
    print('The most popular combination is: {}'.format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = int(df['Trip Duration'].sum())
    print('Total travel time: {} minutes'.format(datetime.timedelta(seconds = total_time)))
    
    # display mean travel time
    mean_time = int(df['Trip Duration'].mean()) // 60
    print('Mean travel time: {} minutes'.format(mean_time))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types= df['User Type'].value_counts()
    
    print('Counts of user types:\n{}'.format(user_types))

    #Skip Washington Gender and Birth Year columns
    try:
        # Display counts of gender
        gender_count= df['Gender'].value_counts()
        print('\nCounts of gender:\n{}'.format(gender_count))
        # Display earliest, most recent, and most common year of birth
        earliest_year= int(df['Birth Year'].min())
        most_recent_year= int(df['Birth Year'].max())
        popular_year= int(df['Birth Year'].mode()[0])
        print('\nEarliest year :{}, most recent year: {}, and most common year of birth: {}'.format(earliest_year,most_recent_year,popular_year))
    except:
        print('\nGender: no data available\n\nDOB: no data available')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    # Ask users to view five rows of individual data trip
    view_data = input('\nWould you like to view 5 rows of individual data trip? Enter yes or no.\n')
    start_loc= 0
    
    #Display five rows of individual data trip
    while True:
        print(df.iloc[start_loc:start_loc + 5])
        start_loc +=5
        view_data = input("\nDo you wish to continue? Enter yes or no: ").lower()
        
        if view_data.lower() !='yes':
            break
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
