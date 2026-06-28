import streamlit as st

st.set_page_config(
    page_title="F1 Fan Hub",
    layout="wide"
)

# Clean, modern minimalist grid style design configurations
st.markdown("""
<style>
.f1-header {
    background: var(--secondary-background-color);
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 25px;
    border: 1px solid var(--border-color);
    text-align: center;
}
.f1-main-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text-color);
    margin-bottom: 5px;
}
.f1-subtitle {
    color: var(--text-color);
    opacity: 0.7;
    font-size: 16px;
}
.f1-card {
    background: var(--secondary-background-color);
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 16px;
    border: 1px solid var(--border-color);
}
.f1-country {
    font-size: 24px;
    font-weight: 800;
    color: var(--text-color);
}
.f1-meta {
    font-size: 14px;
    opacity: 0.8;
    margin: 4px 0;
}
.status-badge {
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 700;
    display: inline-block;
    margin-top: 6px;
}
.status-available { background-color: rgba(34, 197, 94, 0.15); color: #22c55e; }
.status-completed { background-color: rgba(113, 113, 122, 0.15); color: #71717a; }
.center-section { max-width: 800px; margin: auto; text-align: center; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# RACE OBJECT BLUEPRINT (OOP)
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
        self.base_price = data["Price"]
        self.location = data["Location"]
        self.display_date = data["Display Date"]
        self.status = data["Status"]

    def get_badge_html(self):
        if self.status == "Available":
            return '<span class="status-badge status-available">AVAILABLE TO BOOK</span>'
        return '<span class="status-badge status-completed">COMPLETED SESSSION</span>'

    def calculate_ticket_price(self, tier, quantity):
        multiplier = self.TICKET_TIERS.get(tier, 1.0)
        return (self.base_price * multiplier) * quantity


# =====================================================================
# CORE APPLICATION ENGINE
# =====================================================================
class TicketBookingEngine:
    VALID_PROMO_CODES = ["F1CLUB2026", "POLEPOSITION", "VIPPASS"]

    def __init__(self, raw_data):
        self.races = [Race(name, data) for name, data in raw_data.items()]

    def search_races(self, query):
        if not query:
            return self.races
        return [
            race for race in self.races
            if query.lower() in race.name.lower() or query.lower() in race.country.lower()
        ]


# Real 2026 Season Calendar Dataset Context Ledger
RAW_RACES = {
    "Australian Grand Prix": {"Round": 1, "Country": "Australia", "Price": 450, "Location": "Albert Park, Melbourne", "Display Date": "06 - 08 Mar", "Status": "Completed"},
    "Chinese Grand Prix": {"Round": 2, "Country": "China", "Price": 400, "Location": "Shanghai Circuit", "Display Date": "13 - 15 Mar", "Status": "Completed"},
    "Japanese Grand Prix": {"Round": 3, "Country": "Japan", "Price": 500, "Location": "Suzuka Circuit", "Display Date": "27 - 29 Mar", "Status": "Completed"},
    "Miami Grand Prix": {"Round": 6, "Country": "United States", "Price": 700, "Location": "Miami International Autodrome", "Display Date": "01 - 03 May", "Status": "Completed"},
    "Canadian Grand Prix": {"Round": 7, "Country": "Canada", "Price": 600, "Location": "Circuit Gilles Villeneuve", "Display Date": "22 - 24 May", "Status": "Completed"},
    "Monaco Grand Prix": {"Round": 8, "Country": "Monaco", "Price": 850, "Location": "Circuit de Monaco", "Display Date": "05 - 07 Jun", "Status": "Completed"},
    "Barcelona-Catalunya Grand Prix": {"Round": 9, "Country": "Spain", "Price": 400, "Location": "Circuit de Barcelona-Catalunya", "Display Date": "12 - 14 Jun", "Status": "Completed"},
    "Austrian Grand Prix": {"Round": 10, "Country": "Austria", "Price": 550, "Location": "Red Bull Ring, Spielberg", "Display Date": "26 - 28 Jun", "Status": "Available"},
    "British Grand Prix": {"Round": 11, "Country": "Great Britain", "Price": 750, "Location": "Silverstone Circuit", "Display Date": "03 - 05 Jul", "Status": "Available"},
    "Belgian Grand Prix": {"Round": 12, "Country": "Belgium", "Price": 620, "Location": "Circuit de Spa-Francorchamps", "Display Date": "17 - 19 Jul", "Status": "Available"},
    "Abu Dhabi Grand Prix": {"Round": 24, "Country": "Abu Dhabi", "Price": 900, "Location": "Yas Marina Circuit", "Display Date": "04 - 06 Dec", "Status": "Available"}
}

# Instantiate layout context engine natively
booking_system = TicketBookingEngine(RAW_RACES)

# Render main layout text block
st.markdown("""
<div class="f1-header">
    <div class="f1-main-title">F1 Ticket and Fan Hub</div>
    <div class="f1-subtitle">Browse schedule listings. Select sub-pages in the side navigation panel entries to view live points tables.</div>
</div>
""", unsafe_allow_html=True)

st.write("## Search Live Track Options")
search_input = st.text_input("Filter grand prix catalog rows by location or country identity:").strip()
filtered_races = booking_system.search_races(search_input)

# Render layout cards dynamically using loops
for i in range(0, len(filtered_races), 2):
    col1, col2 = st.columns(2)
    pair = filtered_races[i:i + 2]

    for col, race in zip([col1, col2], pair):
        with col:
            st.markdown(f"""
            <div class="f1-card">
                <div class="f1-country">Round {race.round_num}: {race.country}</div>
                <div class="f1-meta">Official Track Title: {race.name}</div>
                <div class="f1-meta">Venue Location Target: {race.location}</div>
                <div class="f1-meta">Weekend Schedule Window: {race.display_date}</div>
                <div class="f1-meta">Package Value Pricing: {race.base_price} SAR</div>
                {race.get_badge_html()}
            </div>
            """, unsafe_allow_html=True)

            if race.status == "Available":
                if st.button("Configure Booking Options", key=f"btn_{race.name}"):
                    st.session_state["selected_booking_race"] = race
            else:
                st.info("Registration window closed for concluded events.")

# Render operational checkout section block if an object is selected
if "selected_booking_race" in st.session_state:
    selected_race = st.session_state["selected_booking_race"]
    st.write("---")
    _, checkout_col, _ = st.columns([0.5, 3, 0.5])

    with checkout_col:
        st.markdown('<div class="center-section">', unsafe_allow_html=True)
        st.write("### Complete Package Checkout Parameters")
        st.write(f"Target Choice: **{selected_race.name}** | Base Fee: **{selected_race.base_price} SAR**")
        
        ticket_qty = st.number_input("Desired Ticket Volume:", min_value=1, max_value=10, value=1)
        tier_choice = st.selectbox("Seating Categorization Track:", options=list(Race.TICKET_TIERS.keys()))
        promo_token = st.text_input("Promo Code Coupon Auth:").strip().upper()

        # Run math operations via class methods cleanly
        base_fees = selected_race.calculate_ticket_price(tier_choice, ticket_qty)
        
        if promo_token in TicketBookingEngine.VALID_PROMO_CODES:
            discounted_fees = base_fees * 0.85
            st.success("Authorization code verified. 15% discount applied.")
        else:
            discounted_fees = base_fees

        gross_fees_total = discounted_fees * 1.15

        st.write("#### Order Cost Summary")
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.write("**Base Multiplier Subtotal:**\n\n**Gross Final Total (Includes 15% VAT):**")
        with sub_col2:
            st.write(f"{base_fees:,.2f} SAR\n\n### **{gross_fees_total:,.2f} SAR**")

        if st.button("Finalize System Ticket Purchase", use_container_width=True):
            st.success("Transaction authorized cleanly.")
            with st.container(border=True):
                st.write(f"OFFICIAL SECTOR ACCESS VOUCHER: {selected_race.name}")
                st.write(f"Units: {ticket_qty} x [ {tier_choice} ] Seating Tier Configuration")
                st.write(f"Track: {selected_race.location} | Window: {selected_race.display_date}")
                st.metric("Total Debited Base Sum Balance", f"{gross_fees_total:,.2f} SAR")