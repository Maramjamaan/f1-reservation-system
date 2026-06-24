# 🏁 Formula 1 Race Ticket Booking System

A seamless, interactive web application built with Python and Streamlit that simulates an online ticket reservation platform for F1 Grand Prix races. Users can browse events, search for specific races, manage their shopping cart, calculate totals with discounts, and securely check out.

This project was developed as part of the **Week 1: Fundamentals Application** assignment.

---

## 🚀 Live Demo
You can access the live application here: 
🔗 [F1 Ticket Reservation App](https://f1-tickets-system-b4nm9ny54urpulrxrdghan.streamlit.app/)

---

## ✨ Features & Team Contributions

Our team divided the workflow into 4 distinct roles to build a cohesive and functional application:

### 👤 Person 1: Database & Search (Browse & Search)
* **Responsibilities:** Built the core data architecture and search functionality.
* **Key Implementation:**
  * [cite_start]Designed a nested dictionary (`dict`) to store comprehensive event data (Race Name, Price, Location, Date, Time, and Available Seats)[cite: 45, 46].
  * [cite_start]Implemented `st.text_input()` to allow users to dynamically filter and search for races by city/name[cite: 47, 48].

### 👤 Person 2: Cart Management (Cart & Quantity Control)
* **Responsibilities:** Developed the logic for handling interactive user selections.
* **Key Implementation:**
  * [cite_start]Utilized `st.session_state` to ensure the shopping cart persists across Streamlit page rerenders[cite: 78, 79].
  * [cite_start]Integrated `st.number_input()` to allow users to modify ticket quantities and added buttons to dynamically add or remove tickets from the cart[cite: 75, 76, 94].

### 👤 Person 3: Calculations & Discounts (Financial Engine & UI/UX)
* **Responsibilities:** Created the calculation engine for sub-totals, ticket experiences, and the adaptive interface presentation.
* **Key Implementation:**
  * [cite_start]Designed structured **Ticket Tiers** (Standard, Premium, VIP) using a dictionary mapping to distinct price multipliers.
  * [cite_start]Wrote a custom function `calculate_total()` that maps selected cart items against the baseline event database prices combined with the experience tier multipliers[cite: 101, 103].
  * [cite_start]Integrated `lambda` functions to instantly apply promotional discount codes and compute the final VAT/tax additions[cite: 102, 119].
  * Redesigned the application's layout to be fully **adaptive**, dynamically auto-switching layout styles, text, and component borders using native Streamlit variables (`var(--text-color)`, `var(--secondary-background-color)`) when users change between **Dark and Light theme settings**.

### 👤 Person 4: Checkout & Confirmation (UI/UX & Finalization)
* **Responsibilities:** Structured the user journey finalization, invoice generation, and receipt exporting.
* **Key Implementation:**
  * [cite_start]Created the "Confirm Reservation" triggers using `st.button()`[cite: 122, 127].
  * [cite_start]Utilized `st.success()` to deliver an interactive confirmation toast[cite: 130].
  * [cite_start]Formatted a clean, professional receipt summary using `st.write()` and metrics blocks to display the final subtotal, discount offsets, and grand totals[cite: 125, 131].
  * [cite_start]Integrated a text file generation mechanism using `st.download_button()` so users can instantly export and save their final transaction receipt as a **downloadable `.txt` file**[cite: 126, 139].

---

## 🛠️ Programming Concepts Applied

To meet the project criteria, this application successfully integrates:
* **Data Types & Collections:** `str`, `int`, `float`, `bool`, along with a complex **Nested Dictionary** and **Lists**[cite: 34, 35, 154].
* [cite_start]**Control Flow:** Advanced `if / elif / else` conditional statements for search filtering, stock/status validation, and error management[cite: 42, 43, 154].
* [cite_start]**Loops:** `for` loops to render dynamic UI components, filter fields, and safely iterate through catalog operations[cite: 38, 39, 154].
* **Functions:** Clean, custom functions with parameters and explicit `return` values alongside functional `lambda` expressions[cite: 32, 33, 36, 37, 154].
* [cite_start]**Interactive & Adaptive UI:** Native Streamlit inputs (`st.text_input`, `st.number_input`, `st.button`) for seamless user interactivity integrated with dynamic theme configurations for automatic **Dark/Light mode support**[cite: 153, 154].

---

## 👥 Group Members

* **Person 1:** Rahaf Makhdoom | [GitHub Profile](https://github.com/Rahafmak)
* **Person 2:** Rana Aljuaid | [GitHub Profile](https://github.com/ranatsa9/)
* **Person 3:** Maram Alzahrani | [GitHub Profile](https://github.com/Maramjamaan)
* **Person 4:** Noura Alshowair | [GitHub Profile](https://github.com/Noura-1237)
