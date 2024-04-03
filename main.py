import os
import sys
import requests
import streamlit
from streamlit_lottie import st_lottie
import pygame
from cv2 import *
import pygame.camera
from deepface import DeepFace
import time
import streamlit as st
from streamlit_option_menu import option_menu
import Food_dictionary
import Food_dataset_analysis
import Database

st.set_page_config(page_title="EMOQ-Emotion Based Food Recommendation System", page_icon=":yum:", layout="wide")
name = ""


#
# def food_recommender():
#     global food_recom_list
#     setting_dom_emo()

def emotion_detection(a):
    pygame.camera.init()
    camList = pygame.camera.list_cameras()
    if camList:
        cam = pygame.camera.Camera(camList[0], (640, 480))
        cam.start()
        time.sleep(3)
        image = cam.get_image()
        # saving the image
        pygame.image.save(image, (a + ".jpg"))
    else:
        st.write("No camera on current device")
    try:
        face_analyze = DeepFace.analyze(a + ".jpg")
        dominant_emotion = face_analyze['dominant_emotion']
        print(face_analyze)
        return dominant_emotion
    except:
        print("face not detected")
        return "Face was not Detected"


# print(Food_dictionary.comfort_food)
def state_selection():
    # INPUT STATE OF THE USER
    st.subheader("Input your current state of mind")
    available_states = ("Bored", "Tired", "Lazy", "Work_mode", 'Try_something_new!',)
    selected_state = st.selectbox("", available_states)
    return selected_state.lower()


def food_recommendation():
    # FOOD RECOMMENDATION
    st.header("Our recommendations are-")
    for i in range(3):
        st.subheader(str(i + 1) + "." + food_recom_list[i])


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# --- LOAD ASSETS---
lottie_food_choice = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ysas4vcp.json")
lottie_food_train = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_YnsM0o.json")
lottie_emotion = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_ewpty5.json")
lottie_bubble = load_lottieurl("https://assets5.lottiefiles.com/temp/lf20_ujod0D.json")
lottie_feedback = load_lottieurl("https://assets6.lottiefiles.com/private_files/lf30_ltuqrtmn.json")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Food Recommender", "Feedback"]

    )

if selected == "Home":
    left_column, right_column = st.columns(2)
    with left_column:
        st_lottie(lottie_food_choice, height=150, width=200, key="food choice")
        st.title("EMOQ :bento:")
        st.subheader("Wondering what to eat?")
        st.write("This is our Capstone project for recommending food items based on the current mood of the user")
        st.write("---")
        with st.container():
            # st_lottie(lottie_emotion, height=150, width=150)
            st.subheader("Tell us about yourself")
            # info_form="""
            # <form action="https://formsubmit.co/atharvathakur369@gmail.com" method="POST">
            #      <input type="text" name="name" required>
            #      <input type="email" name="email" required>
            #      <button type="submit">Send</button>
            # </form>"""
            # st.markdown(info_form, unsafe_allow_html=True)
            with st.form(key='info'):
                firstname = st.text_input("FirstName", placeholder="What can i call you?")
                lastname = st.text_input("LastName", placeholder="What's your last name?")
                email = st.text_input("Email", placeholder="What's your email address?")
                gender = st.selectbox("Gender", ("Male", "Female", "Other"))
                age = st.number_input("Age", step=1)
                submit_button1 = st.form_submit_button(label='Submit')

                if submit_button1:
                    name = firstname + lastname
                    Database.insert_data(name, age, gender)
                    st.write("Your information has been recorded.")

    with right_column:
        st_lottie(lottie_food_train, height=400, width=500, key="food options")

    st.write("---")

if selected == "Food Recommender":
    dominant_emo = emotion_detection(name)
    detectemodict=[]
    detectemodict.append(dominant_emo)
    print(detectemodict)
    left_column, right_column = st.columns(2)
    with left_column:
        st_lottie(lottie_food_choice, height=150, width=200, key="food choice1")
        st.title("EMOQ :bento:")
        st.write("---")
        with st.container():
            food_recom_list = []
            # detect_emo = st.button("Detect Emotion")
            # if detect_emo:
            #     dominant_emo = emotion_detection(name)
            st.subheader("You're " + dominant_emo)
            state = state_selection()
            mood = state + "_" + dominant_emo
            food_recom_list = Food_dataset_analysis.find_my_comfort_food(mood)
            food = st.button("Recommend me something delicious!")
            if food:
                food_recommendation()

            st.header("Enter a keyword related to your mood-")
            emotionalstate = st.text_input(" ", placeholder="Write here", key="emotionalstateinput")

            if emotionalstate != "":
                food_recom_list = Food_dataset_analysis.find_my_comfort_food(emotionalstate)
                st.subheader("You're " + dominant_emo)
                #st.write(dominant_emo)
                food_recommendation()
            moreRecom = st.button("More!", key='morerecom')
            if moreRecom:
                st.header("Some more food recommendations-")
                st.subheader(", ".join(food_recom_list[3:]))
    with right_column:
        st_lottie(lottie_bubble, height=600, width=600)
    st.write("---")

if selected == "Feedback":
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What are your comfort foods?")
        with st.form(key='feedback'):
            st.subheader("Your mood")
            user_mood = st.text_input("", key='mood')
            st.write("---")
            st.subheader("Your comfort food for your mood")
            comfort_food = st.text_input(" ", key='food')
            submit_button2 = st.form_submit_button(label='Submit')
            if submit_button2:
                Database.insert_feedback(comfort_food, user_mood)
                st.write("Your feedback was recorded.")
    with right_column:
        st_lottie(lottie_feedback, height=500, width=500)
