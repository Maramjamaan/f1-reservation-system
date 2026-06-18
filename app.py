import streamlit as st

# ==================================================
# Formula 1 Ticket Reservation System - 2026 Season
# ==================================================

# =========================
# Person 1: Race Database
# =========================

f1_races = {
    1: {
        "name": "Australian Grand Prix",
        "date": "March 6-8",
        "venue": "Melbourne",
        "price": 300,
        "status": "Completed"
    },
    2: {
        "name": "Chinese Grand Prix",
        "date": "March 13-15",
        "venue": "Shanghai",
        "price": 250,
        "status": "Completed"
    },
    3: {
        "name": "Japanese Grand Prix",
        "date": "March 27-29",
        "venue": "Suzuka",
        "price": 350,
        "status": "Completed"
    },
    4: {
        "name": "Bahrain Grand Prix",
        "date": "April 10-12",
        "venue": "Sakhir",
        "price": 280,
        "status": "Cancelled"
    },
    5: {
        "name": "Saudi Arabian Grand Prix",
        "date": "April 17-19",
        "venue": "Jeddah",
        "price": 400,
        "status": "Cancelled"
    },
    6: {
        "name": "Miami Grand Prix",
        "date": "May 1-3",
        "venue": "Miami",
        "price": 600,
        "status": "Completed"
    },
    7: {
        "name": "Canadian Grand Prix",
        "date": "May 22-24",
        "venue": "Montreal",
        "price": 450,
        "status": "Completed"
    },
    8: {
        "name": "Monaco Grand Prix",
        "date": "June 5-7",
        "venue": "Monaco",
        "price": 900,
        "status": "Completed"
    },
    9: {
        "name": "Barcelona-Catalunya Grand Prix",
        "date": "June 12-14",
        "venue": "Barcelona-Catalunya",
        "price": 400,
        "status": "Completed"
    },
    10: {
        "name": "Austrian Grand Prix",
        "date": "June 26-28",
        "venue": "Spielberg",
        "price": 320,
        "status": "Available"
    },
    11: {
        "name": "British Grand Prix",
        "date": "July 3-5",
        "venue": "Silverstone",
        "price": 705.79,
        "status": "Available"
    },
    12: {
        "name": "Belgian Grand Prix",
        "date": "July 17-19",
        "venue": "Spa-Francorchamps",
        "price": 30,
        "status": "Available"
    },
    13: {
        "name": "Hungarian Grand Prix",
        "date": "July 24-26",
        "venue": "Budapest",
        "price": 200,
        "status": "Available"
    },
    14: {
        "name": "Dutch Grand Prix",
        "date": "August 21-23",
        "venue": "Zandvoort",
        "price": 750,
        "status": "Available"
    },
    15: {
        "name": "Italian Grand Prix",
        "date": "September 4-6",
        "venue": "Monza",
        "price": 233,
        "status": "Available"
    },
    16: {
        "name": "Spanish Grand Prix - Madrid",
        "date": "September 11-13",
        "venue": "Madrid",
        "price": 695,
        "status": "Available"
    },
    17: {
        "name": "Azerbaijan Grand Prix",
        "date": "September 24-26",
        "venue": "Baku",
        "price": 663.33,
        "status": "Available"
    },
    18: {
        "name": "Singapore Grand Prix",
        "date": "October 9-11",
        "venue": "Singapore",
        "price": 174.70,
        "status": "Available"
    },
    19: {
        "name": "United States Grand Prix",
        "date": "October 23-25",
        "venue": "Austin",
        "price": 79.86,
        "status": "Available"
    },
    20: {
        "name": "Mexico City Grand Prix",
        "date": "October 30 - November 1",
        "venue": "Mexico City",
        "price": 659.02,
        "status": "Available"
    },
    21: {
        "name": "Sao Paulo Grand Prix",
        "date": "November 6-8",
        "venue": "Sao Paulo",
        "price": 801.16,
        "status": "Available"
    },
    22: {
        "name": "Las Vegas Grand Prix",
        "date": "November 19-21",
        "venue": "Las Vegas",
        "price": 696.93,
        "status": "Available"
    },
    23: {
        "name": "Qatar Grand Prix",
        "date": "November 27-29",
        "venue": "Lusail",
        "price": 297.21,
        "status": "Available"
    },
    24: {
        "name": "Abu Dhabi Grand Prix",
        "date": "December 4-6",
        "venue": "Yas Marina",
        "price": 534.11,
        "status": "Available"
    }
}


# =========================
# Person 3: Calculation Functions
# =========================

def calculate_base_total(quantity, price_per_ticket):
    return quantity * price_per_ticket


apply_membership_discount = lambda total: total * 0.85


# =========================
# Streamlit App Interface
# =========================

st.title("Formula 1 Ticket Reservation System")
st.subheader("Book your 2026 Grand Prix weekend ticket")

st.write("### 2026 Formula 1 Race Calendar")

race_table = []

for race_number, race_info in f1_races.items():
    race_table.append({
        "No.": race_number,
        "Race": race_info["name"],
        "Date": race_info["date"],
        "Venue": race_info["venue"],
        "Starting Price": str(race_info["price"]) + " EUR",
        "Status": race_info["status"]
    })

st.table(race_table)


# =========================
# Person 2: User Selection
# =========================

st.write("### Customize Your Booking")

available_races = []

for race_info in f1_races.values():
    available_races.append(race_info["name"])

selected_race_name = st.selectbox(
    "Select the Grand Prix you want to attend:",
    available_races
)

selected_race = None

for race_info in f1_races.values():
    if race_info["name"] == selected_race_name:
        selected_race = race_info

st.write("**Selected Race:**", selected_race["name"])
st.write("**Date:**", selected_race["date"])
st.write("**Venue:**", selected_race["venue"])
st.write("**Status:**", selected_race["status"])


# =========================
# Person 4: Conditions + Receipt
# =========================

if selected_race["status"] == "Completed":
    st.error("This race has already taken place. Booking is closed for this Grand Prix.")
elif selected_race["status"] == "Cancelled":
    st.error("This race has been cancelled. Booking is closed for this Grand Prix.")

elif selected_race["status"] == "Available":
    st.success("This race is available for booking.")

    ticket_quantity = st.number_input(
        "How many tickets would you like to reserve?",
        min_value=1,
        max_value=10,
        value=1
    )

    has_membership = st.checkbox(
        "I have an official F1 Fan Club Membership and want 15% off"
    )

    base_total = calculate_base_total(ticket_quantity, selected_race["price"])

    if has_membership:
        final_total = apply_membership_discount(base_total)
        discount_status = "15% F1 Fan Club Discount Applied"
    else:
        final_total = base_total
        discount_status = "No discount applied"

    st.write("### Price Preview")
    st.write("**Price per Ticket:**", selected_race["price"], "EUR")
    st.write("**Quantity:**", ticket_quantity)
    st.write("**Base Total:**", round(base_total, 2), "EUR")
    st.write("**Discount:**", discount_status)
    st.write("**Final Total:**", round(final_total, 2), "EUR")

    if st.button("Confirm My Reservation"):
        st.success("Reservation Confirmed Successfully!")

        st.write("### F1 Grand Prix Ticket Reservation Receipt")

        st.info(f"""
        **Race:** {selected_race["name"]}

        **Date:** {selected_race["date"]}

        **Venue:** {selected_race["venue"]}

        **Ticket Type:** Weekend Starting Ticket

        **Price per Ticket:** {selected_race["price"]} EUR

        **Quantity:** {ticket_quantity}

        **Base Total:** {base_total:.2f} EUR

        **Discount:** {discount_status}

        **Final Total:** {final_total:.2f} EUR

        **Reservation Status:** Confirmed
        """)

else:
    st.warning("Race status is unknown. Please contact support.")
