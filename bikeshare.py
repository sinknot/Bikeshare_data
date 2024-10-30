import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {'chicago' :'chicago.csv',
             'chi': 'chicago.csv',
             'new york city' : 'new_york_city.csv',
             'nyc': 'new_york_city.csv',
             'washington': 'washington.csv',
             'wdc': 'washington.csv'}
months_list = ['all','jan'or'january', 'feb'or'february', 'mar'or'march','apr'or 'april', 'may', 'jun' or'june']
days_list = ['all','sun'or'sunday', 'mon' or 'monday','tues' or 'tuesday', 'wed' or 'wednesday', 'thurs' or 'thursday', 'fri' or 'friday', 'sat' or 'saturday']

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("select the city to get information for chicago or new york city  or washington)").lower()
    while city not in CITY_DATA.keys():
        print('invaild city selected')
        city = input("select the city to get information , chicago or new york city or washington)").lower()
        continue
    # get user input for month (all, january, february, ... , june)
    month = input('select the month needed from Jan to Jun or select all').lower()
    while month not in months_list:
        print('month selected out of range please retry or select all')
        month = input('select the month needed from Jan to Jun or select all').lower()
        continue
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day= input('select the day needed from Mon to Sun').lower()
    while day not in days_list:
        print('invalid entry please retry or select all')
        day= input('select the day needed from Mon to Sun').lower()
        continue
        
    filename= CITY_DATA[city]
    print(filename)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    start_time = time.time()
    print('Data is being processed')
 
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city],parse_dates=['Start Time','End Time'])

    # extract month and day of week from Start Time to create new columns
    df['S_month'] = df['Start Time'].dt.month
    df['S_day'] = df['Start Time'].dt.weekday
    df['S_hour'] =df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        month = months_list.index(month) + 1
        dfm = df[df.loc['S_month'] == month]
        

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        dfd = df[df.loc['S_day'] == day.title()]
        

    print('Data is processed')
    print('Data was processed in {} secs'.format(round(time.time()-start_time,2)))
    return df

def time_stats(df, month, day):
    print('Display statistics on the most frequent times of travel.')

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        mpm=df['S_month'].dropna()
        if mpm.empty:
            print('No popular month found, Please refilter')
        else:
            mpm = mpm.mode()[0]
            CM=calendar.month_abbr[mpm]
            print('Most common month is {}'.format(CM))
    else:
        D_month=df['S_month'].dropna()
        if D_month.empty:
            print('No popular month found, Please refilter')
        else:
            D_month = D_month.mode()[0]
            print('Most common month is {}'.format(D_month))
        

    # display the most common day of week
    if day == 'all':
        mcd=df['S_day'].dropna()
        if mcd.empty:
            print('No popular month found, Please refilter')
        else:
            mcd = mcd.mode()[0]
            CD= calendar.day_name[mcd]
            print('Most common day is {}'.format(CD))

    # display the most common start hour
    if day == 'all':
        mch=df['S_hour'].dropna()
        if mch.empty:
            print('No popular hour found, Please refilter')
        else:
            mch = mch.mode()[0]
            print('Most common hour is {}:00'.format(mch))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('Displaying statistics on the most popular stations and trip')

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    mcss=df['Start Station']
    if mcss.empty:
        print('No common Start Station, Please refilter')
    else:
        mcss=mcss.mode()[0]
        print('Most common Start Station is {}'.format(mcss))
    
    # display most commonly used end station
    mces=df['End Station']
    if mces.empty:
        print('No common End Station, Please refilter')
    else:
        mces=mces.mode()[0]
        print('Most common End Station is {}'.format(mces))


    # display most frequent combination of start station and end station trip
    df['sct']=df['Start Station']+' to '+df['End Station']
    mccs=df['sct'].dropna()
    if mccs.empty:
        print('No Data found , Please refilter')
    else:
        dfcc=df.groupby(df['sct']).size().sort_values(ascending=False)
        t_count=dfcc.iloc[0]
        mccs=df.pivot_table(index=['sct'], aggfunc='size').sort_values(ascending=False).index[0]
        print('Most Common combination of Start Station and End Station is from {} and their Trip count is {}'.format(mccs,t_count))
        
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    r_time=df['Trip Duration'].dropna()
    if r_time.empty:
        print('No records found, Please refilter')
    else:
        timesum=r_time.sum()
        print("Total travel time is : {} secs".format(timesum))
        # display mean travel time
        timemean=r_time.mean()
        print("Mean travel time is : {} secs".format(timemean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    if 'User Type' in df:
        u_type=df['User Type'].dropna()
        if u_type.empty:
            print('No Data found , Please refilter')
        else:
            u_type=u_type.value_counts()
            print('The user types count are {}'.format(u_type))
    # Display counts of gender
    if 'Gender' in df:
        ugender=df['Gender'].dropna()
        if ugender.empty:
            print('No Data found , Please refilter')
        else:
            ugender=ugender.value_counts()
            print('The counts of gender are {}'.format(ugender))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        ubyears=df['Birth Year'].dropna()
        if ubyears.empty:
            print('No Data found , Please refilter')
        else:
            oldest=ubyears.min()
            print('The Earliest year of birth is {}'.format(int(oldest)))
            youngest=ubyears.max()
            print('The latest year of birth is {}'.format(int(youngest)))
            mcby=ubyears.mode()[0]
            print('Most common year of birth is {}'.format(int(mcby)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    '''Displays 5 rows of raw data'''
    # collecting user input
    select=input('Do you need to show raw data? [yes/no]:')
    # Setting counter for the rows
    count =0
    while select not in ['yes','no']:
        print('That\'s invalid choice, pleas type yes or no')
        select=input('Do you need to show raw data? [yes/no]:')
    #Showing the raw data
    while select == 'yes':
        print(df.iloc[count:count+5])
        count+=5
        select=input('Do you need to show more raw data? [yes/no]:')
    if select=='no':
        print('Exiting raw data')
    
def main():
    while True:
        city, month, day = get_filters()
        print('inputs are City:{}, Month:{}, Day:{}'.format(city, month, day))
        df = load_data(city, month, day)
        if df.empty:
            print('No available data, Please refilter')
            continue
        raw_data(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
