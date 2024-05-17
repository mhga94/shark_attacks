Function_list_surfhack

# Jose general cleaning function - Matt updated to add str.lower.() and some changes  to be implemented.

def clean_columns_rows(df):
    columns_drop = ["pdf","href formula", "href", "Case Number","Case Number.1","original order","Unnamed: 21","Unnamed: 22"]
    new_df_shark = df.drop(columns = columns_drop)    # removed the columns with no relevant data
    #display(new_df_shark)

    new_df = new_df_shark.drop(range(6944, len(new_df_shark))) # removed the rows with no data
    new_df_cols = [elem.rstrip().replace(" ","_") for elem in new_df.columns] # Uses list comprehension to create new column names
    new_df.columns = new_df_cols # Assigns new col names to df
    display(new_df)

    return new_df

def clean_age (df): #Jose
  """ Cleans Age column in the given Data Frame
  """
    #for the null values replace with mean Age, since is a numerical continuous data
    df3 = df.copy()
    df3["Age"] = pd.to_numeric(df3["Age"], errors='coerce')  #when encounters errors converts invalid to NaN
    df3["Age"] = df3["Age"].astype(float).round(2)   #converting to float and rounding it to 2 decimal places

    mean_age = df3["Age"].mean()
    df3["Age"].fillna(mean_age, inplace=True)# replace NaN with mean_age

    return df3


def clean_injury(df): #Jose
  """ Creates 2 new columns for upper and lower injuries
      Checks if the attack injured upper or/and lower body
  """
    df3 = df.copy()
    #new columns
    df3["LowBodyInjury"] = df["Injury"].str.contains(r'\b(?:leg|lower|legs|knee|knees|ankle|ankles|foot|feet|toe|toes|calf|calfs|thigh|thighs)\b', case=False)
    #cheking if df contains this paterns and returns a series of Booleans, with case = False we ensure this will check the patterns regardless of the string's casing
    df3["UpperBodyInjury"] = df["Injury"].str.contains(r'\b(?:head|upper|arm|arms|face|ears|ear|hand|hands|shoulder|shoulders|back|chest|forearm)\b', case=False) #same but for upperbody

    #display(df3[["Injury", "LowBodyInjury","UpperBodyInjury"]])

    return df3


def clean_fatality(df): #Jose
    """ Names the unmaned column as Fatality
        Replaces the entries for Y N and UNKOWN fatality
    """
    df3 = df.copy()
    df3.rename(columns={"Unnamed: 11": "Fatality"},inplace = True)
    df3["Fatality"]= df3["Fatality"].str.upper()
   # display(df3["Fatality"])

    df3["Fatality"] = df3["Fatality"].replace({
        "YES": "Y",
        "NO": "N",
        "F": "Y",
        " N": "N",
        "Y X 2": "Y",
        "N ": "N",
        "NQ" : "UNKNOWN",
        "M"  : "UNKNOWN",
        "N  " : "N",
        "Y  " : "Y"})

    df3["Fatality"].fillna("UNKNOWN", inplace=True) # fill null values with UNKNOWN
    return df3

# String manipulation: first letter uppercase, rest lowercase, exception for USA - Daniel
def clean_text(text):
    if text == "USA":
        return text
    else:
        cleaned_text = ' '.join([word.capitalize() for word in str(text).split()])
        return cleaned_text

# Function to map countries to continents - Daniel
def clean_country(df):
    df4 = df.copy()

    # Assuming business is only available in Asia, North America and Europe yet
    continent_to_countries = {
        # Asia
        'Asia': ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China', 'Cyprus', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen'],
        # North America
        'North America': ['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States', 'USA'],
        # Europe
        'Europe': ['Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City']
        # Add more continents and their corresponding countries as needed
    }

    # Function to get continent based on country
    def get_continent(country):
        for continent, countries in continent_to_countries.items():
            if country in countries:
                return continent
        return 'No Priority'

    df4['Continent'] = df['Country'].apply(get_continent)
    return df4


def time_clean(df):

    # Define new dictionary relating to times of day
    AM_PM_dict = {
   'AM' : ['01','02','03','04','05','06','07','08','09','10','11','mo','am','Mo'],
   'PM' : ['12','13','14','15','16','17','18','19','20','21','22','23','pm','af','Af'],
    'Night/Evening' : ['Ni','ni','ev','Ev']
   }

    # Iterate over the values in dictionary to match with first two characters of time column and replace with 'AM', 'PM' or Evening
    for key, values in AM_PM_dict.items():
        for value in values:
            df.loc[df['Time'].str[:2].str.contains(value, na=False), 'Time'] = key


    # Define new dictionary for exact matching
    AM_PM_exact = {
    'AM' : ['morning','Morning','A.M.','before noon','Dawn','before dawn'],
    'PM' : ['afternoon','Dusk','P.M.','Midday','Sunset','Midnight','Dark','before sunset']
    }

    for key, values in AM_PM_exact.items():
        for value in values:
            df.loc[df['Time'].str.contains(value, na=False), 'Time'] = key

    return df


def map_sex_inconsistency(df): #Lora
    # Define sex mapping dictionary
    sex_mapping = {
        'F': 'F',
        'M': 'M',
        'Femal': 'F',
        'Female': 'F',
        'Male': 'M',
        'female': 'F',
        'male': 'M'
    }

    # Standardize the values in the 'Sex' column
    df['Sex'] = df['Sex'].map(sex_mapping)

    # Return the updated DataFrame
    return df

def replace_nonname_values(df): #Lora
    # Define non-name values to be replaced
    non_name_values = ['Male', 'Female', 'Unknown', 'Unidentified', 'NaN', 'Child', 'Boy', 'Girl', 'Person', 'People']

    # Replace non-name values with "Unknown" in the 'Name' column
    df['Name'] = df['Name'].replace(non_name_values, 'Unknown')

    # Return the updated DataFrame
    return df


# Replace Null values with 'unknown'
df['Activity'].fillna('unknown', inplace=True)
df['Name'].fillna('unknown', inplace=True)
df['Sex'].fillna('unknown', inplace=True)

# Format the columns "title case""capitalise"
df['Activity'] = df['Activity'].str.title()
df['Name'] = df['Name'].str.title()
df['Sex'] = df['Sex'].str.capitalize()
