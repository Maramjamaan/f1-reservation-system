import streamlit as st
import requests

# =====================================================================
#  1. RACE CLASS (Encapsulates Individual Event Logic)
# =====================================================================
class Race:
    TICKET_TIERS = {
        "General Admission (Standard)": 1.0,
        "Grandstand Seating (Premium)": 1.5,
        "VIP Champions Club (Luxury)": 2.5
    }

    def __init__(self, name, data):
        self.name = name
        self.round_num = data["Round"]
        self.country = data["Country"]
        self.flag = data["Flag"]
        self.base_price = data["Price"]
        self.location = data["Location"]
        self.time = data["Time"]
        self.date = data["Date"]
        self.display_date = data["Display Date"]
        self.status = data["Status"]

    def get_status_styles(self):
        """Returns the appropriate CSS class and display text based on status."""
        if self.status == "Available":
            return "available", "AVAILABLE TO BOOK"
        elif self.status == "Full":
            return "full", "SOLD OUT"
        return "completed", "COMPLETED"

    def calculate_ticket_price(self, tier, quantity):
        """Calculates subtotal based on the selected seating tier multiplier."""
        multiplier = self.TICKET_TIERS.get(tier, 1.0)
        return (self.base_price * multiplier) * quantity


# =====================================================================
#  2. DRIVER CLASS (Encapsulates Driver Analytics)
# =====================================================================
class Driver:
    def __init__(self, name, constructor, position, points):
        self.name = name
        self.constructor = constructor
        self.position = position
        self.points = points
        
    def get_bio(self):
        return f"Driving for {self.constructor}, currently ranked #{self.position} globally."


# =====================================================================
#  3. FAN HUB ENGINE (The Main Controller Class / Backend)
# =====================================================================
class FanHubEngine:
    VALID_MEMBERSHIP_CODES = ["F1CLUB2026", "POLEPOSITION", "VIPPASS"]
    
    def __init__(self, raw_races_data):
        # Transform raw dictionary into an organized dictionary of Race objects
        self.races = {name: Race(name, data) for name, data in raw_races_data.items()}
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Safely configures memory persistence across Streamlit reruns."""
        if "driver_votes" not in st.session_state:
            st.session_state.driver_votes = {
                "Max Verstappen": 0, "Lando Norris": 0, "Charles Leclerc": 0, 
                "Oscar Piastri": 0, "Lewis Hamilton": 0
            }
        if "race_votes" not in st.session_state:
            unique_countries = sorted(list(set(race.country for race in self.races.values())))
            st.session_state.race_votes = {country: 0 for country in unique_countries}

    def filter_races(self, query):
        """Filters race objects based on user search text input."""
        if not query:
            return list(self.races.values())
        return [
            race for race in self.races.values()
            if query.lower() in race.name.lower() or query.lower() in race.country.lower()
        ]

    def fetch_live_standings(self):
        """Fetches live API telemetry and instantiates clean Driver objects."""
        url = "https://ergast.com/api/f1/current/driverStandings.json"
        try:
            response = requests.get(url).json()
            raw_standings = response["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            return [
                Driver(
                    name=f"{item['Driver']['givenName']} {item['Driver']['familyName']}",
                    constructor=item["Constructors"][0]["name"],
                    position=item["position"],
                    points=item["points"]
                ) for item in raw_standings[:10]
            ]
        except Exception:
            # Clean backup fallback objects using our class architecture
            return [
                Driver("Max Verstappen", "Red Bull", "1", "219"),
                Driver("Lando Norris", "McLaren", "2", "150"),
                Driver("Charles Leclerc", "Ferrari", "3", "148")
            ]

    def cast_driver_vote(self, name):
        st.session_state.driver_votes[name] += 1

    def cast_race_vote(self, country):
        st.session_state.race_votes[country] += 1


# =====================================================================
#  RAW DATA SOURCE[cite: 1]
# =====================================================================
RAW_RACES = {
    "Spanish Grand Prix": {"Round": 9, "Country": "Spain", "Flag": "🇪🇸", "Price": 400, "Location": "Circuit de Barcelona-Catalunya", "Time": "16:00", "Date": "2026-06-14", "Display Date": "12 - 14 Jun", "Status": "Completed"},
    "Austrian Grand Prix": {"Round": 10, "Country": "Austria", "Flag": "🇦🇹", "Price": 550, "Location": "Red Bull Ring, Spielberg", "Time": "16:00", "Date": "2026-06-28", "Display Date": "26 - 28 Jun", "Status": "Full"},
    "British Grand Prix": {"Round": 11, "Country": "Great Britain", "Flag": "🇬🇧", "Price": 750, "Location": "Silverstone Circuit", "Time": "17:00", "Date": "2026-07-05", "Display Date": "03 - 05 Jul", "Status": "Available"},
    "Belgian Grand Prix": {"Round": 12, "Country": "Belgium", "Flag": "🇧🇪", "Price": 620, "Location": "Circuit de Spa-Francorchamps", "Time": "16:00", "Date": "2026-07-19", "Display Date": "17 - 19 Jul", "Status": "Full"},
    "Hungarian Grand Prix": {"Round": 13, "Country": "Hungary", "Flag": "🇭🇺", "Price": 480, "Location": "Hungaroring, Budapest", "Time": "16:00", "Date": "2026-07-26", "Display Date": "24 - 26 Jul", "Status": "Available"},
    "Dutch Grand Prix": {"Round": 14, "Country": "Netherlands", "Flag": "🇳🇱", "Price": 580, "Location": "Circuit Zandvoort", "Time": "16:00", "Date": "2026-08-23", "Display Date": "21 - 23 Aug", "Status": "Available"},
    "Italian Grand Prix": {"Round": 15, "Country": "Italy", "Flag": "🇮🇹", "Price": 650, "Location": "Autodromo Nazionale Monza", "Time": "16:00", "Date": "2026-09-06", "Display Date": "04 - 06 Sep", "Status": "Available"},
    "Spanish Grand Prix - Madrid": {"Round": 16, "Country": "Spain", "Flag": "🇪🇸", "Price": 695, "Location": "Madrid Circuit", "Time": "16:00", "Date": "2026-09-13", "Display Date": "11 - 13 Sep", "Status": "Available"},
    "Azerbaijan Grand Prix": {"Round": 17, "Country": "Azerbaijan", "Flag": "🇦🇿", "Price": 450, "Location": "Baku City Circuit", "Time": "14:00", "Date": "2026-09-27", "Display Date": "25 - 27 Sep", "Status": "Available"},
    "Singapore Grand Prix": {"Round": 18, "Country": "Singapore", "Flag": "🇸🇬", "Price": 800, "Location": "Marina Bay Street Circuit", "Time": "15:00", "Date": "2026-10-11", "Display Date": "09 - 11 Oct", "Status": "Full"},
    "United States Grand Prix": {"Round": 19, "Country": "United States", "Flag": "🇺🇸", "Price": 700, "Location": "Circuit of The Americas, Austin", "Time": "23:00", "Date": "2026-10-25", "Display Date": "23 - 25 Oct", "Status": "Available"},
    "Mexican Grand Prix": {"Round": 20, "Country": "Mexico", "Flag": "🇲🇽", "Price": 500, "Location": "Autódromo Hermanos Rodríguez", "Time": "23:00", "Date": "2026-11-01", "Display Date": "30 Oct - 01 Nov", "Status": "Available"},
    "Brazilian Grand Prix": {"Round": 21, "Country": "Brazil", "Flag": "🇧🇷", "Price": 600, "Location": "Interlagos, São Paulo", "Time": "20:00", "Date": "2026-11-08", "Display Date": "06 - 08 Nov", "Status": "Available"},
    "Las Vegas Grand Prix": {"Round": 22, "Country": "Las Vegas", "Flag": "🇺🇸", "Price": 900, "Location": "Las Vegas Strip Circuit", "Time": "06:00", "Date": "2026-11-21", "Display Date": "19 - 21 Nov", "Status": "Available"},
    "Qatar Grand Prix": {"Round": 23, "Country": "Qatar", "Flag": "🇶🇦", "Price": 700, "Location": "Lusail International Circuit", "Time": "19:00", "Date": "2026-11-29", "Display Date": "27 - 29 Nov", "Status": "Available"},
    "Abu Dhabi Grand Prix": {"Round": 24, "Country": "Abu Dhabi", "Flag": "🇦🇪", "Price": 850, "Location": "Yas Marina Circuit", "Time": "17:00", "Date": "2026-12-06", "Display Date": "04 - 06 Dec", "Status": "Available"}
}

# =====================================================================
# INITIALIZE INTERFACE & ENGINE CONTEXT
# =====================================================================
# Spin up the central OOP engine using your dataset[cite: 1]
hub = FanHubEngine(RAW_RACES)

# Inject custom layout tokens safely
st.markdown("""
<style>
.f1-header { background: var(--secondary-background-color); padding: 30px; border-radius: 22px; margin-bottom: 25px; border: 1px solid var(--border-color); text-align: center; }
.f1-main-title { font-size: 42px; font-weight: 900; color: var(--text-color); margin-bottom: 5px; }
.f1-subtitle { color: var(--text-color); opacity: 0.8; font-size: 18px; }
.f1-card { background: var(--secondary-background-color); padding: 20px; border-radius: 18px; margin-bottom: 10px; min-height: 335px; border: 1px solid var(--border-color); }
.f1-round { color: var(--text-color); opacity: 0.6; font-size: 13px; font-weight: bold; }
.f1-country { color: var(--text-color); font-size: 28px; font-weight: 900; margin-top: 5px; }
.f1-race-name { color: var(--text-color); opacity: 0.8; font-size: 13px; text-transform: uppercase; margin-top: 4px; min-height: 35px; }
.f1-date { color: #d93829; font-size: 25px; font-weight: bold; margin-top: 14px; }
.f1-info { color: var(--text-color); font-size: 14px; margin-top: 7px; }
.available { color: #22c55e; font-weight: bold; }
.full { color: #ef4444; font-weight: bold; }
.completed { color: #71717a; font-weight: bold; }
.center-section { max-width: 900px; margin: auto; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="f1-header">
    <div class="f1-main-title">🏎️ F1 Ticket & Ultimate Fan Hub</div>
    <div class="f1-subtitle">A fully object-oriented ecosystem engineered for Formula 1 enthusiasts.</div>
</div>
""", unsafe_allow_html=True)

tab_booking, tab_analytics, tab_guide, tab_voting = st.tabs([
    "🎟— Ticket Reservations", "📊 Live Analytics", "📖 Beginner's Guide", "🗳️ Fan Voting Polls"
])

# ---------------------------------------------------------------------
#  TAB 1: TICKET RESERVATIONS (OOP Render Flow)
# ---------------------------------------------------------------------
with tab_booking:
    st.write("## Search for a Race")
    search_query = st.text_input("Filter schedule by race or country, e.g., British, Spain:").strip()
    
    # Run the filtering system method natively
    filtered_list = hub.filter_races(search_query)

    if not filtered_list:
        st.warning("No race matching that criteria was located.")
    else:
        for i in range(0, len(filtered_list), 2):
            col1, col2 = st.columns(2)
            chunk = filtered_list[i:i + 2]

            for col, race in zip([col1, col2], chunk):
                with col:
                    css_status, status_label = race.get_status_styles()
                    st.markdown(f"""
                    <div class="f1-card">
                        <div class="f1-round">{race.flag} ROUND {race.round_num}</div>
                        <div class="f1-country">{race.country}</div>
                        <div class="f1-race-name">Formula 1 {race.name} 2026</div>
                        <div class="f1-date">{race.display_date}</div>
                        <div class="f1-info">📍 {race.location}</div>
                        <div class="f1-info">⏰ {race.time}</div>
                        <div class="f1-info">💰 Base: {race.base_price} SAR</div>
                        <div class="f1-info">Status: <span class="{css_status}">{status_label}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                    if race.status == "Available":
                        if st.button("🎟️ Select Race", key=f"sel_{race.name}"):
                            st.session_state["active_race_obj"] = race
                    elif race.status == "Full":
                        st.warning("Sold out.")
                    else:
                        st.info("Event concluded.")

    # Checkout Engine Core Interface
    if "active_race_obj" in st.session_state:
        race_obj = st.session_state["active_race_obj"]
        st.write("---")
        _, center_col, _ = st.columns([0.5, 3, 0.5])

        with center_col:
            st.markdown('<div class="center-section">', unsafe_allow_html=True)
            st.write("## Configure Package Parameters")
            st.write(f"🏁 **Selected Target:** {race_obj.name} | 📍 {race_obj.location}")
            
            qty = st.number_input("Desired Ticket Volume:", min_value=1, max_value=10, value=1)
            tier_selected = st.selectbox("Seating Categorization Category:", options=list(Race.TICKET_TIERS.keys()))
            promo_entered = st.text_input("VIP Coupon Authentication:").strip().upper()

            # Execute financial calculations cleanly using OOP methods
            raw_subtotal = race_obj.calculate_ticket_price(tier_selected, qty)
            
            if promo_entered in FanHubEngine.VALID_MEMBERSHIP_CODES:
                calculated_base = raw_subtotal * 0.85
                st.success("Valid authorization code. 15% discount registered.")
            else:
                calculated_base = raw_subtotal

            final_gross_total = calculated_base * 1.15

            st.write("### 💳 Billing Summary Breakdown")
            cb1, cb2 = st.columns(2)
            with cb1:
                st.write("**Base Subtotal Value:**\n\n**Gross Final Total (Includes 15% VAT):**")
            with cb2:
                st.write(f"{raw_subtotal:,.2f} SAR\n\n### **{final_gross_total:,.2f} SAR**")

            if st.button("Finalize System Purchase Execution", use_container_width=True):
                st.success("Transaction Approved Natively! Printing Pass Ticket Context Ledger...")
                with st.container(border=True):
                    st.write(f"🎟️ **OFFICIAL RECORD PASSPORT:** {race_obj.name}")
                    st.write(f"Units: {qty} x Category [ {tier_selected} ]")
                    st.write(f"Location Target: {race_obj.location} | Date Time: {race_obj.display_date} @ {race_obj.time}")
                    st.metric("Total Debited Fees", f"{final_gross_total:,.2f} SAR")

# ---------------------------------------------------------------------
# 📊 TAB 2: LIVE ANALYTICS (OOP Data Pipeline)
# ---------------------------------------------------------------------
with tab_analytics:
    st.header("📈 Live Standings Analytics Machine")
    st.write("Direct loop processing executed on instances of parsed runtime data streams.")
    
    active_drivers = hub.fetch_live_standings()
    for driver in active_drivers:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(f"{driver.position}. {driver.name}")
                st.write(driver.get_bio())
            with c2:
                st.metric(label="Championship points", value=f"{driver.points} PTS")

# ---------------------------------------------------------------------
# 📖 TAB 3: BEGINNER'S GUIDE
# ---------------------------------------------------------------------
with tab_guide:
    st.header("📖 Fan Education Repository")
    guide_selection = st.selectbox("Select subject track:", ["Race Flags", "Compound Compounds"])
    if guide_selection == "Race Flags":
        st.markdown("* 🟨 **Yellow Flag:** Track hazard. Decelerate safely.\n* 🟩 **Green Flag:** Hazard neutralized. Maximum velocity.\n* 🟥 **Red Flag:** High-severity accident. Session aborted.")
    else:
        st.markdown("* 🔴 **Soft:** Elite friction performance, expedited wear.\n* 🟡 **Medium:** Ideal optimization parameter.\n* ⚪ **Hard:** Maximum lifecycle, reduced baseline speed profile.")

# ---------------------------------------------------------------------
# 🗳️ TAB 4: FAN VOTING POLLS (State Driven Interface Elements)
# ---------------------------------------------------------------------
with tab_voting:
    st.header("🗳️ Real-time Global Fan Opinion Metrics")
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("⭐ Driver Performance Index")
        driver_vote_input = st.radio("Pick your standout grid performer:", list(st.session_state.driver_votes.keys()))
        if st.button("Submit Driver Scorecard Ticket"):
            hub.cast_driver_vote(driver_vote_input)
            st.toast("Driver index calculation table modified successfully.")
        st.bar_chart(st.session_state.driver_votes)
        
    with col_v2:
        st.subheader("✈️ Destination Popularity Index")
        race_vote_input = st.radio("Pick your premier geographical venue target:", list(st.session_state.race_votes.keys()))
        if st.button("Submit Destination Allocation Ticket"):
            hub.cast_race_vote(race_vote_input)
            st.toast("Venue priority analytics matrix re-cached.")
        st.bar_chart(st.session_state.race_votes)