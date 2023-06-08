from colorama import Fore, Back, Style
from tabulate import tabulate
from prompt_toolkit import prompt
from termcolor import cprint
from pyfiglet import figlet_format
import pandas as pd

class BikeShareAnalyzer:
    """
    A class for selecting and analyzing bike share data for different cities.
    """

    CITY_DATA = {'chicago': 'data/chicago.csv','new york': 'data/new_york_city.csv','washington': 'data/washington.csv'}
    cities = [("Chicago", "CHI"),("New York", "NY"), ("Washington", "WA")]
    months = [("January", "JAN"), ("February", "FEB"), ("March", "MAR"), ("April", "APR"), ("May", "MAY"), ("June", "JUN")]
    days = [("Monday", "MON"), ("Tuesday", "TUE"), ("Wednesday", "WED"), ("Thursday", "THU"), ("Friday", "FRI"), ("Saturday", "SAT"), ("Sunday", "SUN")]

    def __init__(self):
        """
        Initializes the BikeShareAnalyzer class and displays the splash screen.
        """
        cprint(figlet_format('Bike share EDA', font='starwars'),'yellow', 'on_red', attrs=['bold'])
    
    def start(self):
        """
        Starts the bike share data analysis process by soliciting user input and displaying the corresponding statistics.
        """
        while True:
            # Select a city
            city = self.get_selection(self.cities, "city")
            if city is None:
                self.restart()
                continue
            else:
                self.display_selection("city", city)

            # Select a time filter
            time_filter = self.get_time_filter()
            self.display_selection("time filter", time_filter)

            month = 'all'
            day = 'all'

            # Select a specific day or month if applicable
            if time_filter.lower() == 'day':
                day = self.get_selection(self.days, "day")
                if day is None:
                    self.restart()
                    continue
                else:
                    self.display_selection("day", day)
            elif time_filter.lower() == 'month':
                month = self.get_selection(self.months, "month")
                if month is None:
                    self.restart()
                    continue
                else:
                    self.display_selection("month", month)
            elif time_filter.lower() == 'both':
                day = self.get_selection(self.days, "day")
                if day is None:
                    self.restart()
                    continue
                else:
                    self.display_selection("day", day)
                month = self.get_selection(self.months, "month")
                if month is None:
                    self.restart()
                    continue
                else:
                    self.display_selection("month", month)
            # Load and analyze the data
            df = self.load_data(city.lower(), month.lower(), day.lower())
            self.display_statistics(df)
            self.display_raw_data(df) 
            break
    def display_raw_data(self, df):
        """
        Displays the raw data to the user in chunks until they choose to stop.

        Args:
            df (pandas.DataFrame): The DataFrame containing the bike share data.

        """
        view_data = 'yes'
        start_loc = 0
        while view_data.lower() == 'yes':
            print(Back.CYAN + Fore.BLACK + f"Raw Data ({start_loc+1}:{start_loc+5}):" + Style.RESET_ALL)
            table = df.iloc[start_loc:start_loc+5]
            print(Fore.BLUE + tabulate(table, headers='keys', tablefmt='pretty') + Fore.RESET)

            start_loc += 5
            view_data = input("Do you wish to view more raw data? Enter 'yes' or 'no': ")
    def display_selection(self, selection_type, selection_value):
        """
        Displays the user's selection for a specific category.

        Args:
            selection_type (str): The type of selection (e.g., "city", "time filter").
            selection_value (str): The user's selection value.

        """
        print(Back.CYAN + Fore.BLACK + f"You selected: {selection_value} for {selection_type}" + Style.RESET_ALL)

    def restart(self):
        """
        Displays a restart message.
        """
        print(Back.YELLOW + Fore.BLACK + "Restarting..." + Style.RESET_ALL)

    def display_statistics(self, df):
        """
        Displays the computed statistics based on the selected data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        """
        statistics = {
            "Popular times of travel": [
                ["Most common month", self.most_common_month(df)],
                ["Most common day of week", self.most_common_day_of_week(df)],
                ["Most common hour of day", self.most_common_hour_of_day(df)]
            ],
            "Popular stations and trip": [
                ["Most common start station", self.most_common_start_station(df)],
                ["Most common end station", self.most_common_end_station(df)],
                ["Most common trip from start to end", self.most_common_trip(df)]
            ],
            "Trip duration": [
                ["Total travel time", self.total_travel_time(df)],
                ["Average travel time", self.average_travel_time(df)]
            ],
            "User info": [
                ["Counts of each user type", self.counts_of_each_user_type(df)],
                ["Counts of each gender", self.counts_of_each_gender(df)],
                ["Earliest birth year", self.earliest_birth_year(df)],
                ["Most recent birth year", self.most_recent_birth_year(df)],
                ["Most common birth year", self.most_common_birth_year(df)]
            ]
        }

        for group, stats in statistics.items():
            print(Back.CYAN + Fore.BLACK + f"\n{group.upper()}:" + Style.RESET_ALL)
            table = [[key, value] for key, value in stats]
            print(Fore.BLUE + tabulate(table, headers=["Statistic", "Value"], tablefmt="pretty") + Fore.RESET)


    def print_options(self, options, header):
        """
        Prints the available options for a specific category.

        Args:
            options (list): A list of available options.
            header (str): The category header.

        """
        print(Back.GREEN + Fore.BLACK + Style.BRIGHT + f"AVAILABLE {header.upper()}:" + Style.RESET_ALL)
        table = [[index, option, abbr] for index, (option, abbr) in enumerate(options, start=1)]
        print(Fore.BLUE + tabulate(table, headers=["Index", header.capitalize(), "Abbreviation"], tablefmt="pretty") + Fore.RESET)

    def get_selection(self, options, prompt_message):
        """
        Solicits user input for selecting an option.

        Args:
            options (list): A list of available options.
            prompt_message (str): The prompt message.

        Returns:
            str: The user's selected option.

        """
        self.print_options(options, prompt_message)
        while True:
            print(Fore.YELLOW + f"Which {prompt_message.upper()} do you want to select? You can select by index, abbreviation, or name. Type 'restart' to start over or 'exit' to quit." + Fore.RESET)
            selected_option = prompt("> ")

            if selected_option.lower() == 'restart':
                return None
            elif selected_option.lower() == 'exit':
                exit(0)
            elif selected_option.isdigit() and 1 <= int(selected_option) <= len(options):
                return options[int(selected_option) - 1][0]
            elif any(selected_option.lower() == abbr.lower() for _, abbr in options):
                return next((option for option, abbr in options if abbr.lower() == selected_option.lower()), None)
            elif any(selected_option.lower() == option.lower() for option, _ in options):
                return selected_option.upper()
            else:
                print(Fore.RED + "Invalid selection. Please try again." + Fore.RESET)

    def get_time_filter(self):
        """
        Solicits user input for selecting a time filter.

        Returns:
            str: The user's selected time filter.

        """
        while True:
            print(Fore.YELLOW + "Select a time filter: 'Day', 'Month' , 'Both', or 'None' for no filter." + Fore.RESET)
            filter_option = prompt("> ")
            if filter_option.lower() in ['day', 'month', 'both', 'none']:
                return filter_option
            else:
                print(Fore.RED + "Invalid selection. Please try again." + Fore.RESET)

    def load_data(self, city, month, day):
        """
        Loads and filters the bike share data for the specified city, month, and day.

        Args:
            city (str): The name of the city to analyze.
            month (str): The name of the month to filter by, or "all" to apply no month filter.
            day (str): The name of the day of the week to filter by, or "all" to apply no day filter.

        Returns:
            pandas.DataFrame: The filtered DataFrame containing the bike share data.

        """
        # Load data file into a DataFrame
        df = pd.read_csv(self.CITY_DATA[city])
        # Convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # Extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        # Filter by month if applicable
        if month != 'all':
            index = next((i for i, v in enumerate(self.months) if v[0].lower() == month), None)
            month = index+1
            # Filter by month to create the new DataFrame
            df = df[df['month'] == month]
        # Filter by day of week if applicable
        if day != 'all':
            # Filter by day of week to create the new DataFrame
            df = df[df['day_of_week'] == day.title()]
        
        return df

    def most_common_month(self, df):
        """
        Computes the most common month of travel based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            str: The name of the most common month.

        """
        month_counts = df['Start Time'].dt.month.value_counts()
        most_common_month = month_counts.idxmax()
        month_name = self.months[most_common_month - 1][0]  
        return month_name

    def most_common_day_of_week(self, df):
        """
        Computes the most common day of the week for travel based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            str: The most common day of the week.

        """
        return df['Start Time'].dt.day_name().mode()[0]

    def most_common_hour_of_day(self, df):
        """
        Determines the most common hour of the day for bike share rides.

        Args:
            df (pandas.DataFrame): The DataFrame containing the bike share data.

        Returns:
            str: The most common hour of the day in AM/PM format.

        """
        hour_counts = df['Start Time'].dt.hour.value_counts()
        most_common_hour = hour_counts.idxmax()
        am_pm = 'AM' if most_common_hour < 12 else 'PM'
        hour = most_common_hour % 12 if most_common_hour % 12 != 0 else 12
        return f"{hour} {am_pm}"

    def most_common_start_station(self, df):
        """
        Computes the most common start station for bike rides based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            str: The most common start station.

        """
        return df['Start Station'].mode()[0]

    def most_common_end_station(self, df):
        """
        Computes the most common end station for bike rides based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            str: The most common end station.

        """
        return df['End Station'].mode()[0]

    def most_common_trip(self, df):
        """
        Computes the most common trip (combination of start and end stations) for bike rides based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            tuple: The most common trip, represented as a tuple with the start and end stations.

        """
        trip_counts = df.groupby(['Start Station', 'End Station']).size()
        most_common_trip = trip_counts.idxmax()
        return most_common_trip[0], most_common_trip[1]

    def total_travel_time(self, df):
        """
        Computes the total travel time for bike rides based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            str: The total travel time in the format "HH Hours, MM Minutes, and SS Seconds".

        """
        total_seconds = df['Trip Duration'].sum()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours} Hours, {minutes} Minutes, and {seconds} Seconds"


    def average_travel_time(self, df):
        """
        Computes the average travel time for bike rides based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            str: The average travel time in the format "HH Hours, MM Minutes, and SS Seconds".

        """
        average_seconds = df['Trip Duration'].mean()
        hours, remainder = divmod(average_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours} Hours, {minutes} Minutes, and {seconds} Seconds"

    def counts_of_each_user_type(self, df):
        """
        Computes the counts of each user type (subscriber or customer) based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            list: A list of lists, where each inner list contains the user type and its corresponding count.

        """
        user_type_counts = df['User Type'].value_counts().reset_index()
        user_type_counts.columns = ['User Type', 'Count']
        return user_type_counts.values.tolist()

    def counts_of_each_gender(self, df):
        """
        Computes the counts of each gender (male or female) based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            list: A list of lists, where each inner list contains the gender and its corresponding count.

        """
        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']
            return gender_counts.values.tolist()
        else:
            return [['Gender', 'No data available']]
    def earliest_birth_year(self, df):
        """
        Computes the earliest birth year of bike share users based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            int or str: The earliest birth year if available, or "No data available" otherwise.

        """
        if 'Birth Year' in df.columns:
            return int(df['Birth Year'].min())
        else:
            return 'No data available'


    def most_recent_birth_year(self, df):
        """
        Computes the most recent birth year of bike share users based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            int or str: The most recent birth year if available, or "No data available" otherwise.

        """
        if 'Birth Year' in df.columns:
            return int(df['Birth Year'].max())
        else:
            return 'No data available'


    def most_common_birth_year(self, df):
        """
        Computes the most common birth year of bike share users based on the bike share data.

        Args:
            df (pandas.DataFrame): The filtered DataFrame containing the bike share data.

        Returns:
            int or str: The most common birth year if available, or "No data available" otherwise.

        """
        if 'Birth Year' in df.columns:
            return int(df['Birth Year'].mode()[0])
        else:
            return 'No data available'

        
if __name__ == '__main__':
    bikeShareAnalyzer = BikeShareAnalyzer()
    bikeShareAnalyzer.start()
