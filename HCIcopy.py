import streamlit as st
import time

work_cycles_count = 0
break_cycles_count = 0

def count_down(ts):
    #cancel timer
    if st.button("END WORK"):
        ts = 0
        
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(1)
            ts -= 1
            
        
        global work_cycles_count
        work_cycles_count += 1
        st.write("Time up!")
        return

def break_count_down(ts):
    st.empty()
    if st.button("END BREAK"):
        st.write("Timer Cancelled")
        return
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(1)
            ts -= 1

        st.write("Break time up!")
        global break_cycles_count
        break_cycles_count += 1
        return


def main():
    st.title("Pomodoro")
    time_minutes = st.number_input('Enter the study time in minutes ', min_value=1, value=25)
    global break_time_minutes
    break_time_minutes = st.number_input('Enter the break time in minutes ', min_value=1, value=5)
    # global time_in_seconds
    # time_in_seconds = time_minutes * 60

    if st.button("START"):
        count_down(int(time_minutes)) #change to time_minutes * 60 in deployment
        #placeholder = st.empty()
        # with placeholder.container():
        #     st.write(count_down(int(time_minutes)))
        #     st.write(break_count_down(int(break_time_minutes)))

    
        
if __name__ == '__main__':
    main()

# import streamlit as st
# import time

# st.write("# Pomodoro Timer")
# st.write("This is a simple pomodoro timer")
# st.write("It will count down from the time you enter")
# st.write("It will also show you the time left")
# st.write("It will also show you the time elapsed")

# try: 
#     time_off = int(st.number_input('Enter the time in minutes ', min_value=1, value=25)) * 60
# except Exception: 
#     st.write("Please enter a number")

# if st.button("OK"):
#     while True: 
#         st.write(time_off)
#         time.sleep(1)
#         time_off -= 1

#         if time_off == 0:
#             st.write("Time Up!")
#             break
