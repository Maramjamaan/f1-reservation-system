import streamlit as st
import requests

# =====================================================================
# 1. RACE CLASS (Encapsulates Individual Event Logic)
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
        if self.status == "Available":
            return "available", "AVAILABLE TO BOOK"
        elif self.status == "Full":
            return "full", "SOLD OUT"
        return "completed", "COMPLETED"

    def calculate_ticket_price(self, tier, quantity):
        multiplier = self.TICKET_TIERS.get(tier, 1.0)
        return (self.base_price * multiplier) * quantity


# =====================================================================
# 2. DRIVER CLASS (Encapsulates Driver Standings Logic)
# =====================================================================
class Driver:
    def __init__(self, name, constructor, position, points, nationality, code):
        self.name = name
        self.constructor = constructor
        self.position = int(position)
        self.points = float(points)
        self.nationality = nationality
        self.code = code
        
    def get_summary_text(self):
        return f"{self.code} competes for {self.constructor} ({self.nationality})"


# =====================================================================
# 3. FAN HUB ENGINE (The Main Controller Class / Backend)
# =====================================================================
class FanHubEngine:
    VALID_MEMBERSHIP_CODES = ["F1CLUB2026", "POLEPOSITION", "VIPPASS"]
    
    def __init__(self, raw_races_data):
        self.races = {name: Race(name, data) for name, data in raw_races_data.items()}

    def filter_races(self, query):
        if not query:
            return list(self.races.values())
        return [
            race for race in self.races.values()
            if query.lower() in race.name.lower() or query.lower() in race.country.lower()
        ]

    def fetch_all_22_drivers(self):
        # Using the standard modern Jolpica fallback path mirror for current season data
        url = "https://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
        try:
            response = requests.get(url, timeout=5).json()
            raw_list = response["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            
            all_drivers = []
            for item in raw_list:
                driver_obj = Driver(
                    name=f"{item['Driver']['givenName']} {item['Driver']['familyName']}",
                    constructor=item["Constructors"][0]["name"],
                    position=item["position"],
                    points=item["points"],
                    nationality=item["Driver"]["nationality"],
                    code=item["Driver"].get("code", item["Driver"]["familyName"][:3].upper())
                )
                all_drivers.append(driver_obj)
            return all_drivers
            
        except Exception:
            # Full 22-grid simulation profile matching current season configurations
            constructors = ["Red Bull", "McLaren", "Ferrari", "Mercedes", "Aston Martin", "Alpine", "Haas", "RB", "Williams", "Sauber"]
            names = ["Max Verstappen", "Lando Norris", "Charles Leclerc", "Oscar Piastri", "Carlos Sainz", "Lewis Hamilton", "George Russell", "Sergio Perez", "Fernando Alonso", "Lance Stroll", "Nico Hulkenberg", "Oliver Bearman", "Yuki Tsunoda", "Liam Lawson", "Pierre Gasly", "Esteban Ocon", "Alex Albon", "Franco Colapinto", "Gabriel Bortoleto", "Valtteri Bottas", "Zhou Guanyu", "Jack Doohan"]
            codes = ["VER", "NOR", "LEC", "PIA", "SAI", "HAM", "RUS", "PER", "ALO", "STR", "HUL", "BEA", "TSU", "LAW", "GAS", "OCO", "ALB", "COL", "BOR", "BOT", "ZHO", "DOO"]
            
            return [
                Driver(names[i], constructors[i % 10], i + 1, max(0, 250 - (i * 12)), "International", codes[i])
                for i in range(22)
            ]


# =====================================================================
# 4. RAW DATA SOURCE[cite: 1]
# =====================================================================
RAW_RACES = {
    "Spanish Grand Prix": {"Round": 9, "Country": "Spain", "Flag": "ESP", "Price": 400, "Location": "Circuit de Barcelona-Catalunya", "Time": "16:00", "Date": "2026-06-14", "Display Date": "12 - 14 Jun", "Status": "Completed"},
    "Austrian Grand Prix": {"Round": 10, "Country": "Austria", "Flag": "AUT", "Price": 550, "Location": "Red Bull Ring, Spielberg", "Time": "16:00", "Date": "2026-06-28", "Display Date": "26 - 28 Jun", "Status": "Full"},
    "British Grand Prix": {"Round": 11, "Country": "Great Britain", "Flag": "GBR", "Price": 750, "Location": "Silverstone Circuit", "Time": "17:00", "Date": "2026-07-05", "Display Date": "03 - 05 Jul", "Status": "Available"},
    "Belgian Grand Prix": {"Round": 12, "Country": "Belgium", "Flag": "BEL", "Price": 620, "Location": "Circuit de Spa-Francorchamps", "Time": "16:00", "Date": "2026-07-19", "Display Date": "17 - 19 Jul", "Status": "Full"},
    "Hungarian Grand Prix": {"Round": 13, "Country": "Hungary", "Flag": "HUN", "Price": 480, "Location": "Hungaroring, Budapest", "Time": "16:00", "Date": "2026-07-26", "Display Date": "24 - 26 Jul", "Status": "Available"},
    "Dutch Grand Prix": {"Round": 14, "Country": "Netherlands", "Flag": "NED", "Price": 580, "Location": "Circuit Zandvoort", "Time": "16:00", "Date": "2026-08-23", "Display Date": "21 - 23 Aug", "Status": "Available"},
    "Italian Grand Prix": {"Round": 15, "Country": "Italy", "Flag": "ITA", "Price": 650, "Location": "Autodromo Nazionale Monza", "Time": "16:00", "Date": "2026-09-06", "Display Date": "04 - 06 Sep", "Status": "Available"},
    "Spanish Grand Prix - Madrid": {"Round": 16, "Country": "Spain", "Flag": "ESP", "Price": 695, "Location": "Madrid Circuit", "Time": "16:00", "Date": "2026-09-13", "Display Date": "11 - 13 Sep", "Status": "Available"},
    "Azerbaijan Grand Prix": {"Round": 17, "Country": "Azerbaijan", "Flag": "AZE", "Price": 450, "Location": "Baku City Circuit", "Time": "14:00", "Date": "2026-09-27", "Display Date": "25 - 27 Sep", "Status": "Available"},
    "Singapore Grand Prix": {"Round": 18, "Country": "Singapore", "Flag": "SIN", "Price": 800, "Location": "Marina Bay Street Circuit", "Time": "15:00", "Date": "2026-10-11", "Display Date": "09 - 11 Oct", "Status": "Full"},
    "United States Grand Prix": {"Round": 19, "Country": "United States", "Flag": "USA", "Price": 700, "Location": "Circuit of The Americas, Austin", "Time": "23:00", "Date": "2026-10-25", "Display Date": "23 - 25 Oct", "Status": "Available"},
    "Mexican Grand Prix": {"Round": 20, "Country": "Mexico", "Flag": "MEX", "Price": 500, "Location": "Autodromo Hermanos Rodriguez", "Time": "23:00", "Date": "2026-11-01", "Display Date": "30 Oct - 01 Nov", "Status": "Available"},
    "Brazilian Grand Prix": {"Round": 21, "Country": "Brazil", "Flag": "BRA", "Price": 600, "Location": "Interlagos, Sao Paulo", "Time": "20:00", "Date": "2026-11-08", "Display Date": "06 - 08 Nov", "Status": "Available"},
    "Las Vegas Grand Prix": {"Round": 22, "Country": "Las Vegas", "Flag": "USA", "Price": 900, "Location": "Las Vegas Strip Circuit", "Time": "06:00", "Date": "2026-11-21", "Display Date": "19 - 21 Nov", "Status": "Available"},
    "Qatar Grand Prix": {"Round": 23, "Country": "Qatar", "Flag": "QAT", "Price": 700, "Location": "Lusail International Circuit", "Time": "19:00", "Date": "2026-11-29", "Display Date": "27 - 29 Nov", "Status": "Available"},
    "Abu Dhabi Grand Prix": {"Round": 24, "Country": "Abu Dhabi", "Flag": "UAE", "Price": 850, "Location": "Yas Marina Circuit", "Time": "17:00", "Date": "2026-12-06", "Display Date": "04 - 06 Dec", "Status": "Available"}
}

# =====================================================================
# 5. INITIALIZE ENGINE & SETUP
# =====================================================================
hub = FanHubEngine(RAW_RACES)

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
    <div class="f1-main-title">F1 Ticket and Ultimate Fan Hub</div>
    <div class="f1-subtitle">A clean object-oriented ecosystem built for the 2026 Formula 1 Championship season.</div>
</div>
""", unsafe_allow_html=True)

tab_booking, tab_analytics, tab_guide = st.tabs([
    "Ticket Reservations", "Live Standings Analytics", "Grid Regulations Guide"
])

# ---------------------------------------------------------------------
# TAB 1: TICKET RESERVATIONS[cite: 1]
# ---------------------------------------------------------------------
with tab_booking:
    st.write("## Search for a Race")
    search_query = st.text_input("Filter schedule by race or country name:").strip()
    filtered_list = hub.filter_races(search_query)

    if not filtered_list:
        st.warning("No race matching that criteria was found.")
    else:
        for i in range(0, len(filtered_list), 2):
            col1, col2 = st.columns(2)
            chunk = filtered_list[i:i + 2]

            for col, race in zip([col1, col2], chunk):
                with col:
                    css_status, status_label = race.get_status_styles()
                    st.markdown(f"""
                    <div class="f1-card">
                        <div class="f1-round">[{race.flag}] ROUND {race.round_num}</div>
                        <div class="f1-country">{race.country}</div>
                        <div class="f1-race-name">Formula 1 {race.name} 2026</div>
                        <div class="f1-date">{race.display_date}</div>
                        <div class="f1-info">Location: {race.location}</div>
                        <div class="f1-info">Time: {race.time}</div>
                        <div class="f1-info">Starting Base Price: {race.base_price} SAR</div>
                        <div class="f1-info">Status: <span class="{css_status}">{status_label}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                    if race.status == "Available":
                        if st.button("Select Race Packages", key=f"sel_{race.name}"):
                            st.session_state["active_race_obj"] = race
                    elif race.status == "Full":
                        st.warning("All configurations booked out.")
                    else:
                        st.info("Event session concluded.")

    if "active_race_obj" in st.session_state:
        race_obj = st.session_state["active_race_obj"]
        st.write("---")
        _, center_col, _ = st.columns([0.5, 3, 0.5])

        with center_col:
            st.markdown('<div class="center-section">', unsafe_allow_html=True)
            st.write("## Configure Package Parameters")
            st.write(f"Active Session Selection: {race_obj.name} | Location: {race_obj.location}")
            
            qty = st.number_input("Desired Ticket Volume Allocation:", min_value=1, max_value=10, value=1)
            tier_selected = st.selectbox("Seating Selection Track Category:", options=list(Race.TICKET_TIERS.keys()))
            promo_entered = st.text_input("VIP Coupon Token Validation:").strip().upper()

            raw_subtotal = race_obj.calculate_ticket_price(tier_selected, qty)
            
            if promo_entered in FanHubEngine.VALID_MEMBERSHIP_CODES:
                calculated_base = raw_subtotal * 0.85
                st.success("Verification confirmed. 15% discount mapped.")
            else:
                calculated_base = raw_subtotal

            final_gross_total = calculated_base * 1.15

            st.write("### Billing Transaction Balance Matrix")
            cb1, cb2 = st.columns(2)
            with cb1:
                st.write("**Base Raw Calculation Subtotal:**\n\n**Total Gross Fees (With 15% VAT Value):**")
            with cb2:
                st.write(f"{raw_subtotal:,.2f} SAR\n\n### **{final_gross_total:,.2f} SAR**")

            if st.button("Finalize Purchase Pipeline Execution", use_container_width=True):
                st.success("Payment authorized via ledger records.")
                with st.container(border=True):
                    st.write(f"OFFICIAL ACCESS VOUCHER PASSPORT: {race_obj.name}")
                    st.write(f"Volume: {qty} Tickets under tier alignment: [ {tier_selected} ]")
                    st.write(f"Track Target: {race_obj.location} | Date Window: {race_obj.display_date} @ {race_obj.time}")
                    st.metric("Total Settled Costs Summary", f"{final_gross_total:,.2f} SAR")

# ---------------------------------------------------------------------
# TAB 2: LIVE STANDINGS ANALYTICS (All 22 Drivers)
# ---------------------------------------------------------------------
with tab_analytics:
    st.header("World Drivers Championship Roster Positions")
    st.write("Real-time live championship values matching all 22 active slots on the current grid.")
    
    driver_filter = st.text_input("Filter array rows by driver name or team constructor identity:").strip().lower()
    active_drivers = hub.fetch_all_22_drivers()
    
    for driver in active_drivers:
        if driver_filter and (driver_filter not in driver.name.lower() and driver_filter not in driver.constructor.lower()):
            continue
            
        with st.container(border=True):
            cr, cd, cp = st.columns([1, 4, 2])
            with cr:
                st.markdown(f"## `Rank {driver.position}`")
            with cd:
                st.subheader(driver.name)
                st.write(driver.get_summary_text())
            with cp:
                st.metric(label="Championship Points Allocation", value=f"{driver.points:,.0f} PTS")

# ---------------------------------------------------------------------
# TAB 3: GRID REGULATIONS GUIDE
# ---------------------------------------------------------------------
with tab_guide:
    st.header("Fan Education Knowledgebase Matrix")
    guide_selection = st.selectbox("Select informative data module track:", ["Track Flags Information", "Tyre Compound Design Spec"])
    if guide_selection == "Track Flags Information":
        st.markdown("* Yellow Flag: Track structural obstacle hazard located ahead. Decelerate safely.\n* Green Flag: Obstacle clean. Full throttle limits authorized.\n* Red Flag: High severity asset incident collision. Session track visibility closed.")
    else:
        st.markdown("* Soft Compound: High track adhesion properties with fast carcass breakdown timelines.\n* Medium Compound: Standard strategic operational balance setting.\n* Hard Compound: Designed for prolonged operating endurance windows at a lower raw speed curve performance index.")