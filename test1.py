import streamlit as st
import time
from datetime import datetime, timedelta

def main():
    st.title("Timer with Stop Button")

    # Check if the timer has started
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Input for the timer duration
    timer_duration_hours = st.number_input("Enter Timer Duration (in hours):", min_value=1, step=1)

    # Display the current time
    st.write(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Display the start button
    start_button = st.button("Start Timer")

    # Check if the start button is clicked
    if start_button:
        # Calculate the end time only if the timer is not already started
        if st.session_state.start_time is None:
            st.session_state.start_time = datetime.now()
            st.session_state.end_time = st.session_state.start_time + timedelta(hours=timer_duration_hours)

    # Check if the timer has started
    if st.session_state.start_time is not None:
        # Display the countdown timer
        st.write("Countdown Timer:")
        text_element = st.empty()
        stop_button = st.button("Stop Timer")

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


import streamlit as st
import time
from datetime import datetime, timedelta


def main():
    st.title("Timer with Stop Button")

    # Check if the timer has started
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Input for the timer duration
    timer_duration_hours = st.number_input("Enter Timer Duration (in hours):", min_value=1, step=1)

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


import streamlit as st
import time
from datetime import datetime, timedelta

def main():
    st.title("Enhanced Timer with Stop and Reset Buttons")

    # Check if the timer has started
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Input for the timer duration
    timer_duration_hours = st.number_input("Enter Timer Duration (in hours):", min_value=0.1, step=0.1)

    # Display the current time
    st.write(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Display the start, stop, and reset buttons in parallel
    col1, col2, col3 = st.columns(3)

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

    with col3:
        # Display the reset button
        reset_button = st.button("Reset Timer")

    # Display the countdown timer and progress bar if the timer has started
    if st.session_state.start_time is not None:
        # Display the countdown timer and progress bar
        st.write("Countdown Timer:")
        text_element = st.empty()
        progress_bar = st.progress(0)

        while datetime.now() < st.session_state.end_time:
            time_elapsed = datetime.now() - st.session_state.start_time
            time_remaining = st.session_state.end_time - datetime.now()
            time_remaining_str = str(time_remaining).split('.')[0]  # Display hours and minutes only
            elapsed_str = str(time_elapsed).split('.')[0]

            # Display time remaining and elapsed time
            text_element.text(f"Time Remaining: {time_remaining_str} | Elapsed Time: {elapsed_str}")

            # Update progress bar
            progress_percent = int((time_elapsed.total_seconds() / (st.session_state.end_time - st.session_state.start_time).total_seconds()) * 100)
            progress_bar.progress(progress_percent)

            # Check if the stop button is clicked
            if stop_button:
                break

            # Check if the reset button is clicked
            if reset_button:
                st.session_state.start_time = None
                break

            time.sleep(1)

        # Timer expired or stopped
        st.write("Timer stopped or expired!")

        # Record the time in hours and minutes
        time_recorded = f"{time_elapsed.seconds // 3600}:{(time_elapsed.seconds // 60) % 60}:{time_elapsed.seconds % 60}"
        st.write(f"Time Recorded: {time_recorded}")

if __name__ == "__main__":
    main()


import streamlit as st
import time
from datetime import datetime, timedelta

def main():
    st.title("Enhanced Timer with Stop and Reset Buttons")

    # Check if the timer has started
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Input for the timer duration
    timer_duration_hours = st.number_input("Enter Timer Duration (in hours):", min_value=0.1, step=0.1)

    # Display the current time
    st.write(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Display the start, stop, and reset buttons in parallel
    col1, col2, col3 = st.columns(3)

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

    with col3:
        # Display the reset button
        reset_button = st.button("Reset Timer")

    # Display the countdown timer and progress bar if the timer has started
    if st.session_state.start_time is not None:
        # Display the countdown timer and progress bar
        st.write("Countdown Timer:")
        text_element = st.empty()
        progress_bar = st.progress(0)

        while datetime.now() < st.session_state.end_time:
            time_elapsed = datetime.now() - st.session_state.start_time
            time_remaining = st.session_state.end_time - datetime.now()
            time_remaining_str = str(time_remaining).split('.')[0]  # Display hours and minutes only
            elapsed_str = str(time_elapsed).split('.')[0]

            # Display time remaining and elapsed time
            text_element.text(f"Time Remaining: {time_remaining_str} | Elapsed Time: {elapsed_str}")

            # Update progress bar
            progress_percent = int((time_elapsed.total_seconds() / (st.session_state.end_time - st.session_state.start_time).total_seconds()) * 100)
            progress_bar.progress(progress_percent)

            # Check if the stop button is clicked
            if stop_button:
                break

            # Check if the reset button is clicked
            if reset_button:
                st.session_state.start_time = None
                break

            time.sleep(1)

        # Timer expired or stopped
        st.write("Timer stopped or expired!")

        # Record the time in hours and minutes
        time_recorded = f"{time_elapsed.seconds // 3600}:{(time_elapsed.seconds // 60) % 60}:{time_elapsed.seconds % 60}"
        st.write(f"Time Recorded: {time_recorded}")

if __name__ == "__main__":
    main()
