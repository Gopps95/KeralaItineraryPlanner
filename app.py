from datetime import datetime, timedelta

import openai
import streamlit as st
from dotenv import load_dotenv

from gtts import gTTS
from io import BytesIO

hide_menu = """
<style>
#MainMenu {
  visibility: hidden;
}
</style>
"""

load_dotenv()

openai.api_key = st.secrets["openai_api_key"]

now_date = datetime.now()

# round to nearest 15 minutes
now_date = now_date.replace(minute=now_date.minute // 15 * 15, second=0, microsecond=0)

# split into date and time objects
now_time = now_date.time()
now_date = now_date.date() + timedelta(days=1)


def generate_prompt(values):
    """
    Generates a prompt for OpenAI based on trip details.

    Args:
        values (dict): A dictionary containing trip details.

    Returns:
        str: The generated prompt.
    """

    return f'''
Prepare a personalized travel itinerary for a trip to {values["destinationCountry"]}, based on the following information:

* Budget: ${values["budget"]}
* Travel Style: {values["travelStyle"]}
* Interests: {", ".join(values["interests"])}
* Accommodation Type: {values["accommodationType"]}
* Transportation Type: {values["transportationType"]}
* Activity Type: {", ".join(values["activityType"])}
* Cuisine Type: {values["cuisineType"]}
* Trip Duration: {values["tripDuration"]} days
* Language: {values["language"]}

Additional Notes: {values["additional_information"]}
'''.strip()


def submit():
    prompt = generate_prompt(st.session_state)

    # generate output
    output = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.45,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=0,
        max_tokens=1024,
    )

    st.session_state["output"] = output["choices"][0]["text"]


# Initialization
if "output" not in st.session_state:
    st.session_state["output"] = "--"

st.title("Tour Inspirer")
st.subheader("Let's craft your dream trip!")
# st.markdown(hide_menu, unsafe_allow_html=True)

with st.form(key="trip_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Destination")
        destination_country = st.text_input("Country", key="destinationCountry")
        st.form_submit_button("Submit", on_click=submit)

    with c2:
        st.subheader("Trip Details")

        budget = st.number_input("Budget", key="budget", min_value=0)
        travel_style = st.selectbox(
            "Travel Style",
            ("Relaxation", "Adventure", "Culture", "Luxury", "Foodie", "Other"),
            key="travelStyle",
        )
        interests = st.multiselect(
            "Interests",
            (
                "History",
                "Nature",
                "Art",
                "Music",
                "Food",
                "Beaches",
                "Adventure Sports",
                "Shopping",
                "Nightlife",
                "Other",
            ),
            key="interests",
        )
        accommodation_type = st.selectbox(
            "Accommodation Type",
            (
                "Hotel",
                "Hostel",
                "Airbnb",
                "Vacation Rental",
                "Boutique Hotel",
                "Other",
            ),
            key="accommodationType",
        )
        transportation_type = st.selectbox(
            "Transportation Type",
            (
                "Flight",
                "Train",
                "Bus",
                "Car Rental",
                "Public Transportation",
                "Other",
            ),
            key="transportationType",
        )
        activity_type = st.multiselect(
            "Activity Type",
            (
                "Sightseeing",
                "Museums",
                "Outdoor Activities",
                "Performances",
                "Local Experiences",
                
            
                "Relaxation",
                "Theme Parks",
                "Family-Friendly",
                "Solo Travel",
                "Other",
            ),
            key="activityType",
        )
        cuisine_type = st.multiselect(
            "Cuisine Type",
            (
                "Local",
                "International",
                "Specific Cuisine (e.g., Italian, Thai)",
                "Other",
            ),
            key="cuisineType",
        )
        trip_duration = st.number_input("Trip Duration (days)", key="tripDuration", min_value=1)
        language = st.selectbox("Language", ("English", "French", "Spanish", "Other"), key="language")
        additional_information = st.text_area("Additional notes?", height=200, key="additional_information")

    with c3:
        st.subheader("Generate Tour Plan")
        st.button("Generate", on_click=submit)

st.subheader("Generated Tour Plan")

# Audio Generation
sound_file = BytesIO()
tts = gTTS(st.session_state.output, lang=st.session_state["language"])
tts.write_to_fp(sound_file)

if st.session_state.output != "--":
    st.audio(sound_file)

st.write(st.session_state.output)

# DALL-E Image Generation
st.subheader("Cool Photos for Your Destination")

num_images = st.slider("How many photos do you want to see?", 1, 10)

img_response = openai.Image.create(
    prompt=f"Cool images of {destination_country}",
    n=num_images,
    size="256x256",
)

for i in range(num_images):
    img_url = img_response["data"][i]["url"]
    st.image(img_url, width=512)

