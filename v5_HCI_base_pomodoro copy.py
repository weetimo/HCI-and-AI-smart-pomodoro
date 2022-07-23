import streamlit as st
import time


def combined_count_down(ts, break_ts):
    if st.button("END WORK"):
        ts = 0
        
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(0.01)
            ts -= 1
        
        st.success("Work cycle over! Time for a break!")
        

    with st.empty(): 
        st.header("You are now taking a break!")
        if st.button("END BREAK"):
            break_ts = 0
        
        while break_ts:
            mins, secs = divmod(break_ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(0.01)
            break_ts -= 1
        
        st.success("Break time up!")
       

    return

st.title("Pomodoro")
time_minutes = st.number_input('Enter the study time in minutes ', min_value=1, max_value=50, value=25)
global break_time_minutes
break_time_minutes = st.number_input('Enter the break time in minutes ', min_value=1, max_value=50, value=5)
subject_array = ["Machine Learning", "HCI and AI", "Service Design Studio", "HASS"]
global subject
subject = st.selectbox('Subject: ', subject_array)

load = st.button("LFG")

#initialise session state 
if "load_state" not in st.session_state:
    st.session_state.load_state = False

if load and st.session_state.load_state:
    st.session_state.load_state = True
    st.write("You are now working on: ", subject)
    combined_count_down(time_minutes*60, break_time_minutes*60)
    
    fatigue_score = st.slider('Fatigue score: ', min_value=1, max_value=10, value=0)
    


