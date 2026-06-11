import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from src.db import save_appointment
from src.hospital import get_hospitals, send_confirmation_email

_SPECIALTIES = [
    "General Physician", "neurologist", "dermatologist", "cardiologist",
    "orthopedist", "pediatrician", "gynecologist", "psychiatrist", "dentist",
    "oncologist", "endocrinologist", "ophthalmologist", "urologist",
    "gastroenterologist", "pulmonologist", "ent", "rheumatologist",
    "radiologist", "nephrologist", "allergist", "surgeon",
]


def _render_table(hospitals: list[dict], show_all: bool) -> None:
    rows = [dict(h) for h in (hospitals if show_all else hospitals[:5])]
    for i, h in enumerate(rows, 1):
        h["#"] = i
        if isinstance(h.get("rating"), float):
            h["rating"] = f"{h['rating']:.1f}"
    st.table(pd.DataFrame(rows).set_index("#"))


def _confirm_booking(
    hospitals: list[dict],
    specialist: str,
    date,
    appt_time,
    username: str,
) -> None:
    names = [h["name"] for h in hospitals]
    hospital = st.selectbox("Select a Hospital 🏥", names)
    if st.button("Confirm Appointment ✅", use_container_width=True):
        save_appointment(username, specialist, str(date), str(appt_time), hospital)
        send_confirmation_email(
            to_email="",
            user_name=username,
            hospital=hospital,
            slot=f"{date} {appt_time}",
        )
        st.success(
            f"Appointment booked with **{specialist}** on **{date}** "
            f"at **{appt_time}** at **{hospital}**."
        )


def _handle_result(
    result: dict,
    specialist: str,
    date,
    appt_time,
    show_all: bool,
    username: str,
) -> None:
    if "error" in result:
        st.warning(result["error"])
        return
    hospitals = result.get("hospitals", [])
    if not hospitals:
        st.warning("No hospitals found for that location and specialty.")
        return
    _render_table(hospitals, show_all)
    _confirm_booking(hospitals, specialist, date, appt_time, username)


def show(username: str) -> None:
    st.subheader("Book Appointment 📅")

    specialist = st.selectbox("Specialist 🩺", _SPECIALTIES)
    date = st.date_input("Date 📅")
    appt_time = st.time_input("Time ⏰")
    show_all = st.checkbox("Show all hospitals (default: top 5)")

    mode = st.radio("Location", ["Enter Place Name", "Use Current Location"])

    if mode == "Enter Place Name":
        place = st.text_input("Place or city name")
        if st.button("Find Hospitals 🔍", use_container_width=True):
            if not place:
                st.warning("Please enter a place name.")
                return
            with st.spinner("Searching nearby hospitals…"):
                result = get_hospitals(location=place, specialization=specialist)
            _handle_result(result, specialist, date, appt_time, show_all, username)

    else:
        coords = streamlit_js_eval(
            js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
            want_output=True,
        )
        if coords:
            st.success(
                f"Location detected: {coords['latitude']:.4f}, {coords['longitude']:.4f}"
            )
            st.map([{"lat": coords["latitude"], "lon": coords["longitude"]}])
            with st.spinner("Searching nearby hospitals…"):
                result = get_hospitals(
                    latitude=coords["latitude"],
                    longitude=coords["longitude"],
                    specialization=specialist,
                )
            _handle_result(result, specialist, date, appt_time, show_all, username)
        else:
            st.info("Allow location access in your browser — the page will reload once granted.")
