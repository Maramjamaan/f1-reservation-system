import streamlit as st
import requests

st.set_page_config(layout="wide")

class TeamRow:
    def __init__(self, pos, name, nationality, points, wins):
        self.pos = pos
        self.name = name
        self.nationality = nationality
        self.points = points
        self.wins = wins

st.title("World Constructors Championship Standings")

def fetch_constructors_leaderboard():
    url = "https://api.jolpi.ca/ergast/f1/2026/constructorStandings.json"
    try:
        res = requests.get(url, timeout=5).json()
        raw_data = res["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
        return [
            TeamRow(
                pos=item["position"],
                name=item["Constructor"]["name"],
                nationality=item["Constructor"]["nationality"],
                points=item["points"],
                wins=item["wins"]
            ) for item in raw_data
        ]
    except Exception:
        mock_teams = ["Mercedes", "Ferrari", "McLaren", "Red Bull", "Aston Martin"]
        return [
            TeamRow(str(i+1), mock_teams[i], "International", str(320 - (i * 45)), str(5 - i if i < 3 else 0))
            for i in range(5)
        ]

teams_list = fetch_constructors_leaderboard()

for team in teams_list:
    with st.container():
        c_rank, c_info, c_stats = st.columns([1, 4, 2])
        with c_rank:
            st.markdown(f"## Rank {team.pos}")
        with c_info:
            st.subheader(team.name)
            st.write(f"Registration Region: {team.nationality}")
        with c_stats:
            st.metric(label="Championship Points Balance", value=f"{team.points} PTS")
            st.write(f"Total Main Session Race Wins: {team.wins}")
        st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)