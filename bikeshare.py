"""
This is B. Todd Shirley's Python project script (on US bikeshare data)
for Udacity's Programming for Data Science with Python nanodegree.
"""

from random import choice
import pandas as pd
import time

# some data to make use of:

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

codes_table = { 'city':  [('chicago',       'c'),
                          ('new york city', 'n'),
                          ('washington',    'w') ],
                'month': [('january',     'jan'),
                          ('february',    'feb'),
                          ('march',       'mar'),
                          ('april',       'apr'),
                          ('may',         'may'),
                          ('june',        'jun'),
                          ('[no filter]', 'all') ],
                'day':   [('sunday',      'sun'),
                          ('monday',      'mon'),
                          ('tuesday',     'tue'),
                          ('wednesday',   'wed'),
                          ('thursday',    'thu'),
                          ('friday',      'fri'),
                          ('saturday',    'sat'),
                          ('[no filter]', 'all') ] }

messages = ("\nLet's start by choosing a city to research ...",
            "\nNext, you can pick a month to filter by, or enter 'all' to include all months:",
            "\nFinally, pick a weekday to filter by, or 'all' to include all days:")

see_table_again_mssg = ["OK, let's have another look ...",
                        "Let's have another look at your choices ...",
                        "Very well, here are those options again ...",
                        "Here are your options once more ...",
                        "Once again, your choices:"]

# and some functions:

def make_table(dictionary, key):
    """
    Creates a table to show user choices and codes for selecting them.
    inputs: a dictionary (codes_table, defined above) and one of its three keys
    output: a string containing variable information telling user how to make selections
    """
    # build left side of table:
    lines = ['For this {}:'.format(key)]
    underline = (len(lines[0]) - 1) * '-' + ' '
    lines.append(underline)
    for tup in dictionary[key]: # dictionary[key] returns a list of tuples
        # create left side of each line, with padding:
        new_line = tup[0].title() + (len(lines[0]) - len(tup[0])) * ' '
        lines.append(new_line)
    # add spaces to separate columns:
    for i in range(len(lines)):
        lines[i] += 3 * ' '
    # build right side of table:
    lines[0] += 'enter this code:'
    lines[1] += '--------------- '
    # center the codes in right column:
    code_length = len(dictionary[key][0][1])
    spaces_before_code = (len('enter this code:') - code_length) // 2 # not great form? Hard to read?
    for j in range(len(dictionary[key])):
        code = dictionary[key][j][1]
        lines[j + 2] += spaces_before_code * ' ' + code + (len('enter this code:') - spaces_before_code - len(code)) * ' '
    # put the whole table into one big (multi-line) string to return:
    table = ''''''
    for line in lines:
        table += line + '\n'
    return table

# Next we make another function to receive table, put a box around it, and return the result, again as a string:

def box_it(table):
    """
    Receives a multi-line string and returns the same, adding a neat box or border.
    """
    # First line will be the top of the box:
    # +--------------+
    # | xxxxxxxxxxxx |    
    # We need the length of any line from table:
    length = table.find('\n')
    top_and_bottom = '+-' + length * '-' + '-+'
    # Now we need to put in all lines from table, with |_ and _| on the ends (where _ is a space):
    # Process all lines of table. Use start and stop markers with the .find() string method (done above).
    # The string (table) is punctuated with \n characters that should help with adding each line
    # (set between |_ and _|, forming the sides of the box).
    stop = length
    lines = [top_and_bottom] # just the first element in a list about to be built
    start = 0
    while start + length < len(table):
        next_line = '| ' + table[start:stop] + ' |'
        lines.append(next_line)
        start = stop + 1
        stop += length + 1
    box = ''''''
    for line in lines:
        box += line + '\n'
    box += top_and_bottom
    return box


def get_filters(table, messages):
    """
    Asks user to specify a city, month, and day to analyze.
    inputs:
        (str) table - from make_table() and box_it() functions above
        (tuple) messages - three strings to display in sequence, guiding user as to city, month, and day choices
    output: a tuple containing
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nYou'll be picking a city to examine and, if you want,")
    print("you can filter its data by month and/or day of the week.")
    print("\nAll the text you enter can be either lowercase or uppercase.")

    filters = ('city', 'month', 'day')
    city_month_day = [] # perhaps not the most descriptive name; these are the city, month, and day choices to be made
    # get choices:
    for i in range(3):
        print(messages[i])
        info = make_table(table, filters[i])
        package = box_it(info) # messages, make_table(), and box_it() are defined outside of this function.
        while True:
            code_matched = False
            # display the options:
            print(package)
            code = input('Enter your selection here: ')
            # check that it's actually in the dictionary (table):
            for tup in table[filters[i]]:
                if tup[1] == code.lower():
                    code_matched = True
                    fltr = tup[0] # it's lowercase -- but watch out for 'all'!
                    break # exit for loop
            # what about entries that don't match a code from table? show a message:
            if not code_matched:
                print("\nSorry; I couldn't understand your input. Please try again:")
                continue
            text = '\nJust hit Enter to confirm {}, or enter any text to make a different choice: '.format(fltr.title())
            unsure = input(text)
            if not unsure:
                break # exit while loop
            else: # (some text was entered at unsure)
                print('\n' + choice(see_table_again_mssg))
        # we have a good choice
        # we need to allow that it may have been 'all'
        # this function is 'get_filters'; 'all' counts as a filter; the actual filtering will be done further on
        if fltr.lower() == '[no filter]':
            fltr = 'all'
        city_month_day.append(fltr)
    return tuple(city_month_day)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    input:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    output:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a DataFrame:
    df = pd.read_csv(CITY_DATA[city])

    # convert the 'Start Time' column to datetime:
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns:
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name # strings
    # keeping these new columns in the DataFrame, as they seem inocuous, even useful

    # filter by month if applicable:
    if month != 'all':
        # use the index of the months list to get the corresponding integer:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new DataFrame:
        df = df[df['Month'] == month]
        # months are given here as integers; thus the above conversion process

    # if applicable, filter by day of week ...
    if day != 'all':
        # to create the new dataframe:
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    input: the DataFrame returned by load_data()
    output: nothing is returned, but information is printed to the screen.
    """
    print('\nOK ...\n\nCalculating the most frequent times of travel ...\n')
    start_time = time.time()
    # The method used allows month, day, and hour to be handled with the same code.
    # It also allows for cases in which two or more months, days, etc., occur with equal frequency.

    # define variable names:
    hours = []
    for line in df['Start Time']:
        Zeit = str(line) # Zeit is German for 'time'
        # what if NaNs occur?
        hours.append(Zeit[11:13])
    time_span = ('month', 'day', 'hour')
    dic = (dict(), dict(), dict())
    iterable = (df['Month'], df['Day of Week'], hours)
    max_count = [] # to be appended to 3x
    most_frequent = ([], [], []) # 3 lists, each to hold one or more months, days, or hours (those whose count = the mode)

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    def restate_hour(raw):
        """This takes string input describing hours such as '07', '12', or '15'
           and returns it in the (string) form ' (7 am)', ' (12 pm)', or ' (3 pm)', respectively."""
        int24 = int(raw.strip())
        clock_time = int24 if int24 < 13 else int24 - 12
        am_pm = 'am' if int24 < 12 else 'pm'
        return ' ({} {})'.format(clock_time, am_pm)

    # loop once each for month, day, and hour:
    for i in range(3):
        for name in iterable[i]:
            if name not in dic[i]:
                dic[i][name] = 1
            else:
                dic[i][name] += 1
        # record the largest count:
        max_count.append(max(dic[i].values())) # build this list to hold 3 ints: the max counts for mon, day, hour
        for name2 in dic[i]:
            if dic[i][name2] == max_count[-1]:
                if i == 0: # (month)
                    name2 = months[name2 - 1].title() # nicer to show name of month instead of number
                elif i == 2: # (hour)
                    name2 += restate_hour(name2)
                most_frequent[i].append(name2)
        # there will be one or more items that occur most often:
        if len(most_frequent[i]) == 1:
            print("The most frequent {} is {}.".format(time_span[i], most_frequent[i][0]))
        else:
            print("The most frequent {}s are {}.".format(time_span[i], set(most_frequent[i])))

    this = eval("""'(This took %s seconds.)' % (time.time() - start_time)""")
    print('\n' + this + '\n' + '-' * len(this))


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    input: the DataFrame returned by load_data()
    output: nothing is returned, but information is printed to the screen.
    """
    # the methods employed here will be essentially the same as in time_stats(df).
    start_time = time.time()
    # create a new column to hold combinations of start, end stations:
    df['Trip'] = df['Start Station'] + ' →  ' + df['End Station']
    stations = ('start station', 'end station', 'trip')
    dic = (dict(), dict(), dict())
    iterable = (df['Start Station'], df['End Station'], df['Trip'])
    max_count = [] # to be appended to 3x
    most_frequent = ([], [], [])

    # loop once each for start station, end station, and combo (trip):
    for i in range(3):
        for name in iterable[i]:
            if name not in dic[i]:
                dic[i][name] = 1
            else:
                dic[i][name] += 1
        # record the largest count:
        max_count.append(max(dic[i].values())) # build this list to hold 3 ints: the max counts for start, end, and trip
        for name2 in dic[i]:
            if dic[i][name2] == max_count[-1]:
                most_frequent[i].append(name2)
        if len(most_frequent[i]) == 1:
            print("\nThe most common {} is\n{}.".format(stations[i], most_frequent[i][0]))
        else:
            print("\nThe most common {}s are".format(stations[i]))
            if len(most_frequent[i]) == 2:
                print('{}\nand {}.'.format(most_frequent[i][0], most_frequent[i][1]))
            else:
                for item in most_frequent[i][:-1]:
                    print(item, end = ',\n')
                print('and {}.'.format(most_frequent[i][-1]))

    # having made these reports, there's no need to retain the 'Trip' column:
    df.drop(['Trip'], axis=1, inplace=True)

    this = eval("""'(This took %s seconds.)' % (time.time() - start_time)""")
    print('\n' + this + '\n' + '-' * len(this))


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    input: the DataFrame returned by load_data()
    output: nothing is returned, but information is printed to the screen.
    """
    start_time = time.time()
    # compute and display total travel time:
    # Sum the Trip Duration amounts. They are given in seconds. Display as hours, minutes, seconds.
    seconds = 0
    for trip_length in df['Trip Duration']:
        seconds += trip_length
    record = seconds
    # For most queries, this will likely sum to more than 1 hour; but let's not assume so.
    # Break seconds into hours, minutes, seconds:
    def reduce(s):
        """This function takes a quantity of seconds and returns
           an equivalent 3-tuple expressed as (hours, minutes, seconds)."""
        if type(s) is int:
            return (s//3600, (s % 3600)//60, s % 60)
        return (int(s//3600), int((s % 3600)//60), round(s % 60, 1))

    # Display total travel time:
    hours, minutes, s = reduce(seconds)
    plural = 's' if s != 1 else ''
    if hours != 0:
        print('\nTotal trip duration: {} hours, {} minutes, and {} second{}.'.format(hours, minutes, round(s, 1), plural))
    elif minutes != 0:
        print('\nTotal trip duration: {} minutes and {} second{}.'.format(minutes, round(s, 1), plural))
    # It's scarcely imaginable that the total could ever be less than 60 seconds; thus no option is provided for that.

    # Display mean travel time:
    avg_time = round(record/len(df), 2) # (units are seconds)
    hrs, mins, secs = reduce(avg_time)
    plural = 's' if secs != 1 else ''
    if hrs != 0:
        print('Average trip duration: {} hours, {} minutes, and {} second{}.'.format(hrs, mins, round(secs, 1), plural))
    elif mins != 0:
        print('Average trip duration: {} minutes and {} second{}.'.format(mins, round(secs, 1), plural))

    this = eval("""'(This took %s seconds.)' % (time.time() - start_time)""")
    print('\n' + this + '\n' + '-' * len(this))


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    input: the DataFrame returned by load_data()
    output: nothing is returned, but information is printed to the screen.
    """
    start_time = time.time()

    # display counts of user types:
    customers, subscribers, unknown = 0, 0, 0

    for value in df['User Type']:
        if value == 'Customer':
            customers += 1
        elif value == 'Subscriber':
            subscribers += 1
        else:
            unknown += 1

    print("\nThere are {} customers and {} subscribers in this data set.".format(customers, subscribers))
    plural = 's' if unknown != 1 else ''
    if unknown > 0:
        print("However, for {} trip{}, the user type is unknown.".format(unknown, plural))
    
    # display counts of gender:
    females = 0
    males = 0
    weiss_nicht = 0 # German for 'don't know'

    if not 'Gender' in df.columns:
        print("\nSorry; no gender or birth-year data is available for Washington.")
    else:
        for value in df['Gender']:
            if value == 'Female':
                females += 1
            elif value == 'Male':
                males += 1
            else:
                weiss_nicht += 1
        
        print("\nIn {} of these trips, the rider is identified as female; in {}, male.".format(females, males))
        message = 'is {} trip'.format(weiss_nicht) if weiss_nicht == 1 else 'are {} trips'.format(weiss_nicht)
        print("There {} for which the rider's gender is unknown.".format(message))

    # Display earliest, most recent, and most common year of birth:
    # From this point on, all entries in 'Birth Year' column that are not years (convertible to int) are unwanted.
    if 'Birth Year' in df.columns:
        birth_year_counts = dict()
        years = []
        for year in df['Birth Year']:
            if str(year).lower() == 'nan' or type(year) is None:
                continue
            elif year not in birth_year_counts:
                birth_year_counts[int(year)] = 1
                years.append(int(year))
            else:
                birth_year_counts[year] += 1

        # We want to access the earliest and most-recent years in the set:
        years.sort() # (ascending)
        # position 0 will give oldest year, -1 most recent.
        most_common_years = [1100] # I trust we have no data for riders born before this year!
        counts = [0]
        for year in birth_year_counts:
            if birth_year_counts[year] > counts[-1]:
                # replace last element in counts list:
                most_common_years[-1] = year
            elif birth_year_counts[year] == counts[-1]:
                # add:
                most_common_years.append(year)
        # sort this list in-place:
        most_common_years.sort()
        
        # report the results:
        print("\nThe earliest known birth year of the riders in this group is {}.".format(years[0]))
        print("The most recent known birth year of the riders in the group is {}.".format(years[-1]))
        if len(most_common_years) == 1:
            print("The most common year of birth in the group is {}.".format(most_common_years[0]))
        else:
            print("The most common years of birth in the group are", end = " ")
            if len(most_common_years) == 2:
                print('{} and {}.'.format(most_common_years[0], most_common_years[1]))
            else:
                for item in most_common_years[:-1]:
                    print(item, end = ', ')
                print('and {}.'.format(most_common_years[-1]))

    this = eval("""'(This took %s seconds.)' % (time.time() - start_time)""")
    print('\n' + this + '\n' + '-' * len(this))


def show_raw_data(filtered_df):
    # prepare to let user view raw data:
    quit = False
    orig_length = len(filtered_df)
    # Since the row labels in the filtered DataFrame will be unpredictable,
    # but knowing them will let us specify which rows to drop (a part of the 
    # display process here), we'll use a function to find them at each viewing step:
    def get_indices(string):
        """From submitted string (containing the first five rows of a DataFrame),
           extract the (integer) row labels and return them as the elements of a list.
           input: multi-line string created from 5-line DataFrame to be dropped
           output: a list containing the integer row labels, one for each of the five records in the string"""
        # each index can be found immediately between an EOL character and white space:
        left_bracket = string.find('\n') # an integer position in string
        right_bracket = string.find(' ', left_bracket) # another
        indices = [int(string[left_bracket + 1:right_bracket])]
        # this list holds the first index; now get the other 4:
        for i in range(4):
            left_bracket = string.find('\n', right_bracket)
            right_bracket = string.find(' ', left_bracket)
            indices.append(int(string[left_bracket + 1:right_bracket]))
        return indices

    # and begin:
    print("\nOK, now you can look at the raw data from this set yourself.")
    print("Your selections returned a set containing {} records.".format(orig_length))
    print("You can look at five records at a time for as long as you like.")

    # allow user to view sets of five records until the cows come home:
    while not quit:
        counter = 0
        working = filtered_df.copy()
        first_next = 'first'
        for five_rows in range(orig_length//5):
            print("Just press Enter to see the {} five records,".format(first_next))
            finished = input("or enter any text to exit: ")
            # NOTE: While the project rubric speaks of 'yes' and 'no' responses to guide this
            # functioning, I've opted for no input (just Enter) to advance and any input to exit
            # the records-review. The reasons for these choices are ease and efficiency of use.
            if not finished:
                # display 5 records:
                print('\n', working.head(), '\n')
                # and discard them:
                these_rows = get_indices(str(working.head()))
                working.drop(these_rows, axis = 0, inplace = True)
                first_next = 'next'
                counter += 5
                percentage = round(100 * counter/orig_length, 2)
                print("You have viewed {}% of the records returned.".format(percentage))
            else: # (finished)
                quit = True
                break # exit for loop
        if not quit: # (user has viewed all or nearly all records)
            # show any last bits from DataFrame:
            if len(working) > 0:
                print("Press Enter to see the very last records,")
                all_done = input("or enter any text to exit: ")
                if not all_done:
                    print('\n', working.head(), '\n')
            #if counter/orig_length < 1: # if len(working) > 0 is logically equivalent
            print("I've now shown you the whole set!")
            print("I'm not sure whether to congratulate you on your perseverance or rebuke you as a")
            print("prodigious time waster -- but either way, I'm impressed that you made it this far!")
            again = input("Enter any text to view from the top again: ")
            if not again:
                quit = True
            else:
                print()


def main():
    """
    Gathers together and coordinates the action of all the above-defined functions and data structures.
    input: none; function calls reach outside the scope of this main function.
    output: none, but print() is used to communicate with the user.
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    while True:
        # run the selection/filtering process:
        city, month, day = get_filters(codes_table, messages)
        filtered_df = load_data(city, month, day)

        # show the search results to the user:
        advance_message = "\nPress Enter to see data on "
        metrics = ['the most popular stations and trip', 'trip duration', 'users']
        group = iter(metrics)
        
        time_stats(filtered_df)
        input(advance_message + next(group) + ': ')
        station_stats(filtered_df)
        input(advance_message + next(group) + ': ')
        trip_duration_stats(filtered_df)
        input(advance_message + next(group) + ': ')
        user_stats(filtered_df)

        show_raw_data(filtered_df)

        restart = input('\nEnter Yes or Y to restart with new choices: ')
        if restart.lower() not in ('yes', 'y'):
            break
        else:
            print("\nRight; back to the beginning!")

    print("\nThank you for playing!\n")

print()

if __name__ == "__main__":
	main()

