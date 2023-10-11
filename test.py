import streamlit as st
import time
from datetime import datetime, timedelta

def main():
    st.title("Timer with Stop Button")

    # Check if the timer has started
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Input for the timer duration
    timer_duration_hours = st.number_input("Enter Timer Duration (in hours):", min_value=0.01, step=0.01)

    # Display the current time
    st.write(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Display the start button and stop button in parallel
    col1, col2 = st.columns(2)

    with col1:
        start_button = st.button("Start Timer")

        # Check if the start button is clicked
        if start_button:
            # Calculate the end time only if the timer is not already started
            if st.session_state.start_time is None:
                st.session_state.start_time = datetime.now()
                st.session_state.end_time = st.session_state.start_time + timedelta(hours=timer_duration_hours)

    with col2:
        # Check if the timer has started
        if st.session_state.start_time is not None:
            # Display the stop button
            stop_button = st.button("Stop Timer")

    # Check if the timer has started
    if st.session_state.start_time is not None:
        # Display the countdown timer
        st.write("Countdown Timer:")
        text_element = st.empty()

        while datetime.now() < st.session_state.end_time:
            time_remaining = st.session_state.end_time - datetime.now()
            time_remaining_str = str(time_remaining).split('.')[0]  # Display hours and minutes only
            text_element.text(f"Time Remaining: {time_remaining_str}")

            # Check if the stop button is clicked
            if stop_button:
                break

            time.sleep(1)

        # Timer expired or stopped
        st.write("Timer stopped or expired!")

        # Record the time in hours and minutes
        time_recorded = f"{time_remaining.seconds // 3600}:{(time_remaining.seconds // 60) % 60}:{time_remaining.seconds % 60}"
        st.write(f"Time Recorded: {time_recorded}")


if __name__ == "__main__":
    main()