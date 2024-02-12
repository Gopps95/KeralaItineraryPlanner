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
    return f'''
Generate a personalized travel itinerary for a trip to {values['destinationCountry']} with a budget of {values['budget']}. 
The traveler is interested in a {values['travelStyle']} vacation and enjoys {values['interestsNew']}. 
They are looking for {values['accommodationType']} accommodations and prefer {values['transportationType']} transportation. 
The itinerary should include {values['activityType']} activities and {values['cuisineType']} dining options. 
Please provide a detailed itinerary with daily recommendations for {values['tripDuration']} days, including suggested destinations, activities, and dining options. 
The itinerary should be written in {values['language']}.
'''.strip()


def submit():    
    prompt = generate_prompt(st.session_state)

    # generate output
    output = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0.45,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=0,
        max_tokens=1024
    )
    
    # GPT-3 Prompt Generated
    st.session_state['output'] = output['choices'][0]['text']

# Initialization
if 'output' not in st.session_state:
    st.session_state['output'] = '--'

st.title('Tour Inspirer')
st.subheader('Let us plan your tour!')
# st.markdown(hide_menu, unsafe_allow_html=True)

with st.form(key='trip_form'):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader('Destination')
        st.text_input('Destination Country', key='destinationCountry')
        st.number_input('Budget', key='budget')
        st.selectbox('Travel Style', ('Relaxing', 'Adventure', 'Cultural', 'Exploration'), key='travelStyle')
        st.text_input('Interests', key='interestsNew')
        st.form_submit_button('Submit', on_click=submit)

    with c2:
        st.subheader('Arrival')
        st.selectbox('Arrival To', ('Airport', 'Train Station', 'Bus Station', 'Ferry Terminal', 'Port', 'Other'), key='arrival_to')
        st.date_input('Arrival Date', value=now_date, key='arrival_date')
        st.time_input('Arrival Time', value=now_time, key='arrival_time')

    with c3:
        st.subheader('Departure')
        st.selectbox('Departure From', ('Airport', 'Train Station', 'Bus Station', 'Ferry Terminal', 'Port', 'Other'), key='departure_from')
        st.date_input('Departure Date', value=now_date + timedelta(days=1), key='departure_date')
        st.time_input('Departure Time', value=now_time, key='departure_time')

    st.text_area('Additional information?', height=200, value='I want to visit as many places as possible! (respect time)', key='additional_information')

st.subheader('Generated Tour Plan')

# Audio Generation
sound_file = BytesIO()
tts = gTTS(st.session_state.output, lang='en')
tts.write_to_fp(sound_file)

if (st.session_state.output != "--"):
    st.audio(sound_file)

st.write(st.session_state.output)

# DALL-E Image Generation
st.subheader('Cool Pics of your Destination')

num_images = st.slider("How many photos do you want to see?", 1, 10)

img_response = openai.Image.create(
    prompt='Cool images of {}'.format(st.session_state.get('destinationCountry', '')),
    n = num_images,
    size="256x256")

for i in range(num_images):
    img_url = img_response['data'][i]['url']
    st.image(img_url, width=512)
