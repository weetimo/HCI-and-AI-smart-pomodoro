from lib2to3.pgen2.pgen import DFAState
import streamlit as st
import time
import pandas as pd
import datetime
import numpy as np

#CHANGE THIS TO LOCAL FILEPATH
local_CSV_filepath = '/Users/timothywee/Documents/SUTD Term 5/HCI and AI/Week 10/Smart Pomodoro/HCI-and-AI-smart-pomodoro/actual_HCI_data.csv'

if 'minutes_today' not in st.session_state:
    st.session_state['minutes_today'] = 0

if 'form_on' not in st.session_state:
    st.session_state.form_on = False

if 'dev_mode' not in st.session_state:
    st.session_state.dev_mode = False

if 'cycle_counter' not in st.session_state: 
    st.session_state['cycle_counter'] = 0

if 'break_counter' not in st.session_state: 
    st.session_state['break_counter'] = 0

if 'subject_array' not in st.session_state:
    st.session_state['subject_array'] = subject_array = ["Machine Learning", "HCI and AI", "Service Design Studio", "HASS"]

if 'multiplier' not in st.session_state:
    st.session_state['multiplier'] = 1

if 'suggested_cycle_value' not in st.session_state:
    st.session_state['suggested_cycle_value'] = 25

if 'suggested_break_value' not in st.session_state:
    st.session_state['suggested_break_value'] = 5

df = pd.read_csv(local_CSV_filepath) 

# graph_df = df[['subject', 'time_minutes']]
# graph_df['time_now'] = pd.to_datetime(graph_df['time_now'])

#st.line_chart(graph_df)

def combined_count_down(ts):
    if st.button("END WORK"):
        ts = 0
        
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(float(st.session_state['multiplier']))
            ts -= 1
        
        st.success("Work cycle over! Time for a break!")
        
        global form_on
        form_on = True
        st.session_state['cycle_counter'] += 1
        st.session_state.form_on = True


    



            # with st.empty(): 
            #     st.header("You are now taking a break!")
            #     if st.button("END BREAK"):
            #         break_ts = 0
                
            #     while break_ts:
            #         mins, secs = divmod(break_ts, 60)
            #         time_now = '{:02d}:{:02d}'.format(mins, secs)
            #         st.header(f"{time_now}")
            #         time.sleep(0.01)
            #         break_ts -= 1
                
            #     st.success("Break time up!")

    return

st.title("LFG Pomodoro")
st.caption("Learning Faster & Greater")

#st.line_chart(df)

time_minutes = st.number_input('Enter the study time in minutes ', min_value=0, max_value=50, value=st.session_state['suggested_cycle_value'])
global break_time_minutes
break_time_minutes = st.number_input('Enter the break time in minutes ', min_value=0, max_value=50, value=st.session_state['suggested_break_value'])

global subject
subject = st.selectbox('Subject: ', st.session_state.subject_array)

if st.button("LFG"):
    st.write("You are now working on: ", subject)
    combined_count_down(time_minutes * 60)

#st.write(df)

if st.session_state.form_on:

    with st.form("How was the session?"):
        effort_score = st.slider("Effort score: ", min_value=1, max_value=10, value=5)
        focus_score = st.slider("Focus score: ", min_value=1, max_value=10, value=5)
        submitted = st.form_submit_button("Submit")

        if submitted:
        #import CSV as a dataframe
        
            df.loc[len(df)] = [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), subject, time_minutes, effort_score, focus_score]
            
            df.to_csv(local_CSV_filepath, index=False) 
            st.session_state.form_on = False
            st.success('Your effort score and focus score have been recorded.')
            st.write(df)
            st.session_state['minutes_today'] += time_minutes
            
            time.sleep(2)
            # st.experimental_rerun()

            st.header("Break time!")
            ts = break_time_minutes * 60
            
            with st.empty():
                while ts:
                    mins, secs = divmod(ts, 60)
                    time_now = '{:02d}:{:02d}'.format(mins, secs)
                    st.header(f"{time_now}")
                    time.sleep(float(st.session_state['multiplier']))
                    ts -= 1
            
            st.success("Break cycle over! ")
            time.sleep(2)
            st.experimental_rerun()

#create a dataframe called graph_df from df, with only the timestamp, subject, and minutes_today columns


st.metric("LFG Pomodoro cycles today", st.session_state['cycle_counter'])
st.metric("Minutes today", st.session_state['minutes_today'])

if st.button("Tired scenario"):
    st.warning("You seem to be tired. Let the AI determine the best cycles for you.")
    time.sleep(2)
    st.session_state['suggested_cycle_value'] = 20
    st.session_state['suggested_break_value'] = 10
    st.experimental_rerun()

if st.checkbox("Dashboard"):
    st.title("Study Progress Dashboard")

    # Generating dummy metrics
    daily_avg_effort = [np.random.randint(1, 10) for i in range(1, 32)]
    daily_avg_focus = [np.random.randint(1, 10) for i in range(1, 32)]
    daily_cycles = [np.random.randint(1, 6) for i in range(1, 32)]
    daily_effort_score = [daily_avg_effort[i] * daily_cycles[i] for i in range(31)]

    # Creating dataframe data
    effort_data = pd.DataFrame(daily_effort_score, index=range(1, 32), columns=["Cycles x Average Effort Score"])
    focus_data = pd.DataFrame(daily_avg_focus, index=range(1, 32), columns=["Average Focus Score"])

    # Metrics for each subject
    st.header("These metrics show how your effort score is trending for each subject.")
    st.subheader("In the past week...")
    subject_array = ["Machine Learning", "HCI and AI", "Service Design Studio", "HASS"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Machine Learning", "7", "-2")
    col2.metric("HCI and AI", "9", "3")
    col3.metric("Service Design Studio", "3", "-4")
    col4.metric("HASS", "10", "6")

    # Horizontal line to divide the page
    st.markdown("""---""")
    st.subheader("In the past month...")
    st.header('Effort Progress') # Graph 1
    # st.subheader('This chart shows your average effort multiplied\
    #      by your number of Pomodoro cycles.')
    st.line_chart(effort_data)

    st.header('Focus Progress') # Graph 2
    # st.subheader('This chart shows your average focus.')
    st.line_chart(focus_data)

    st.header("Average Study Times") # Graph 3
    # Generate dataframe data with each hour in the day on horizontal axis
    # and different study times on vertical axis
    study_times = [np.random.randint(1, 6) for i in range(24)]
    study_times_data = pd.DataFrame(study_times, index=range(1, 25), columns=["Study Time"])
    st.bar_chart(study_times_data)

st.session_state.dev_mode = st.checkbox('dev mode')
if st.session_state.dev_mode:
    st.session_state['multiplier'] = 0.005
    st.write(df)
    #st.write(st.session_state)

st.caption("settings")
if st.checkbox("Add subject"):
    st.session_state.subject_array.append(st.text_input("Enter subject name"))
