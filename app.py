import streamlit as st
import requests

# =====================================================================
# CLASS 1: Driver Class (OOP Blueprint)
# =====================================================================
class Driver:
    def __init__(self, name, constructor, position, points):
        self.name = name
        self.constructor = constructor
        self.position = position
        self.points = points
        
    def get_bio(self):
        return f"Driving for {self.constructor}, currently ranked #{self.position} in the standings."


# =====================================================================
#  CLASS 2: Dynamic Voting System Engine (Using Your Real Data)
# =====================================================================
class FanHubVoting:
    def __init__(self, database_races):
        """
        Instead of hardcoded data, this dynamically builds the voting poll 
        options from the real countries/constructors in your team's dictionary!
        """
        # 7. Python Collections: Dynamically extract unique items from your database
        unique_countries = sorted(list(set(details["Country"] for details in database_races.values())))
        
        # Initialize driver candidates based on active frontrunners
        default_drivers = ["Max Verstappen", "Lando Norris", "Charles Leclerc", "Oscar Piastri", "Lewis Hamilton"]

        # Initialize session state dictionaries if they don't exist yet
        if "driver_votes" not in st.session_state:
            st.session_state.driver_votes = {driver: 0 for driver in default_drivers}
            
        if "race_votes" not in st.session_state:
            # Dynamically sets up a vote tracking counter for every country in your database!
            st.session_state.race_votes = {country: 0 for country in unique_countries}

    def cast_driver_vote(self, driver_name):
        st.session_state.driver_votes[driver_name] += 1

    def cast_race_vote(self, country_name):
        st.session_state.race_votes[country_name] += 1

    def get_driver_results(self):
        return st.session_state.driver_votes

    def get_race_results(self):
        return st.session_state.race_votes


# =====================================================================
#  Live Data Fetching Function (Live Race Analytics)
# =====================================================================
def fetch_live_standings():
    url = "https://ergast.com/api/f1/current/driverStandings.json"
    try:
        response = requests.get(url).json()
        raw_standings = response["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
        
        driver_objects = []
        for item in raw_standings[:10]: # Top 10 drivers
            driver_obj = Driver(
                name=f"{item['Driver']['givenName']} {item['Driver']['familyName']}",
                constructor=item["Constructors"][0]["name"],
                position=item["position"],
                points=item["points"]
            )
            driver_objects.append(driver_obj)
        return driver_objects
    except Exception:
        # Fallback objects using your core database style structure
        return [
            Driver("Max Verstappen", "Red Bull", "1", "219"),
            Driver("Lando Norris", "McLaren", "2", "150"),
            Driver("Charles Leclerc", "Ferrari", "3", "148")
        ]

# Initialize your layout tabs
tab1, tab2, tab3 = st.tabs(["📊 Live Analytics", "📖 Fan's Guide", "🗳️ Fan Voting Polls"])

# Instantiate the Voting Engine, passing your group's real "races" dictionary into it!
voting_system = FanHubVoting(races)

# ---------------------------------------------------------------------
# TAB 1: Live Race Analytics
# ---------------------------------------------------------------------
with tab1:
    st.header("📈 Current Driver Championship Standings")
    drivers_list = fetch_live_standings()
    
    for driver in drivers_list:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"{driver.position}. {driver.name}")
                st.write(driver.get_bio())
            with col2:
                st.metric(label="Points", value=f"{driver.points} PTS")

# ---------------------------------------------------------------------
# TAB 3: Dynamic Voting Polls
# ---------------------------------------------------------------------
with tab3:
    st.header("🗳️ Global Fan Destination Polls")
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.subheader("⭐ Driver of the Day")
        driver_choice = st.radio("Pick your top performer:", list(voting_system.get_driver_results().keys()))
        if st.button("Submit Driver Vote"):
            voting_system.cast_driver_vote(driver_choice)
            st.success(f"Vote added for {driver_choice}!")
        st.bar_chart(voting_system.get_driver_results())
        
    with v_col2:
        st.subheader("✈️ Most Anticipated Grand Prix Destination")
        # This list comes completely live from your own F1 countries list!
        race_choice = st.radio("Which circuit country are you traveling to see?", list(voting_system.get_race_results().keys()))
        if st.button("Submit Destination Vote"):
            voting_system.cast_race_vote(race_choice)
            st.success(f"Vote added for {race_choice}!")
        st.bar_chart(voting_system.get_race_results())