import os
import smtplib

from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from requests.exceptions import RequestException

load_dotenv()

_MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
_SENDER_EMAIL = os.getenv("SENDER_EMAIL")
_SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

_geo = Nominatim(user_agent="carereach_locator")

_SPECIALTY_KEYWORDS: dict[str, list[str]] = {
    "General Physician": ["general physician", "general checkup", "consult"],
    "neurologist": ["neurologist", "neuro", "brain", "nerve"],
    "dermatologist": ["dermatologist", "skin", "derma"],
    "cardiologist": ["cardiologist", "cardio", "heart"],
    "orthopedist": ["orthopedist", "orthopedic", "bone", "joint"],
    "pediatrician": ["pediatrician", "child", "pediatrics"],
    "gynecologist": ["gynecologist", "gyno", "obgyn"],
    "psychiatrist": ["psychiatrist", "mental health", "psych"],
    "dentist": ["dentist", "dental", "oral"],
    "oncologist": ["oncologist", "cancer"],
    "endocrinologist": ["endocrinologist", "hormone", "gland"],
    "ophthalmologist": ["ophthalmologist", "eye", "vision"],
    "urologist": ["urologist", "urinary", "kidney"],
    "gastroenterologist": ["gastroenterologist", "gastro", "stomach"],
    "pulmonologist": ["pulmonologist", "lung", "respiratory"],
    "ent": ["ENT", "ear nose throat", "otolaryngologist"],
    "rheumatologist": ["rheumatologist", "arthritis", "autoimmune"],
    "radiologist": ["radiologist", "imaging", "radiology"],
    "nephrologist": ["nephrologist", "renal"],
    "allergist": ["allergist", "immunologist", "allergy"],
    "surgeon": ["surgeon", "surgery"],
}


def _get_gmaps():
    import googlemaps
    if not _MAPS_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY is not set.")
    return googlemaps.Client(key=_MAPS_KEY)


def get_hospitals(
    location: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    specialization: str = "hospital",
) -> dict:
    try:
        gmaps = _get_gmaps()
        keywords = _SPECIALTY_KEYWORDS.get(specialization, ["hospital"])

        if location:
            try:
                geo = _geo.geocode(location)
                if not geo:
                    return {"error": "Invalid location — could not geocode."}
                lat, lng = geo.latitude, geo.longitude
            except RequestException as exc:
                return {"error": f"Geocoding failed: {exc}"}
        elif latitude is not None and longitude is not None:
            lat, lng = latitude, longitude
        else:
            return {"error": "Provide either a location name or GPS coordinates."}

        seen: set[str] = set()
        hospitals: list[dict] = []
        for keyword in keywords:
            for place in gmaps.places_nearby(
                location=(lat, lng), radius=5000, type="hospital", keyword=keyword
            ).get("results", []):
                name = place["name"]
                if name not in seen:
                    seen.add(name)
                    hospitals.append({
                        "name": name,
                        "address": place.get("vicinity", ""),
                        "rating": place.get("rating", "N/A"),
                        "reviews": place.get("user_ratings_total", 0),
                    })

        return {"hospitals": hospitals}
    except ValueError as exc:
        return {"error": str(exc)}
    except Exception as exc:
        return {"error": str(exc)}


def send_confirmation_email(
    to_email: str, user_name: str, hospital: str, slot: str
) -> None:
    if not _SENDER_EMAIL or not _SENDER_PASSWORD or not to_email:
        return
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(_SENDER_EMAIL, _SENDER_PASSWORD)
            server.sendmail(
                _SENDER_EMAIL,
                to_email,
                (
                    f"Subject: Appointment Confirmation — CareReach\n\n"
                    f"Hi {user_name},\n\n"
                    f"Your appointment at {hospital} is confirmed for {slot}.\n\n"
                    f"Thank you for using CareReach."
                ),
            )
    except Exception:
        pass  # email is optional; never crash the app over it
