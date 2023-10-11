
import streamlit as st
import time

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    mins, secs = divmod(remainder, 60)
    return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))

def countdown_timer(seconds):
    timer_placeholder = st.empty()
    progress_bar = st.progress(0)
    text_element = st.empty()

    while seconds:
        timer_text = format_time(seconds)
        timer_placeholder.text(timer_text)

        # Update progress bar
        progress_percentage = 1 - seconds / initial_seconds
        progress_percentage = max(0, min(1, progress_percentage))  # Ensure it's within [0, 1]
        progress_bar.progress(progress_percentage)

        # Display time remaining and elapsed time
        time_remaining_str = format_time(seconds)
        elapsed_str = format_time(initial_seconds - seconds)
        text_element.text(f"Time Remaining: {time_remaining_str} | Elapsed Time: {elapsed_str}")

        time.sleep(1)
        seconds -= 1

    # Display final values
    timer_placeholder.text("00:00:00")
    progress_bar.progress(1.0)
    text_element.text(f"Time Remaining: 00:00:00 | Elapsed Time: {format_time(initial_seconds)}")
    st.success("Time's up!")

def main():
    st.title("Countdown Timer")
    user_input = st.number_input("Enter time in hours (e.g., 1.5 for 1 hour 30 minutes):", min_value=0.001)

    if st.button("Start Timer"):
        try:
            global initial_seconds
            initial_seconds = int(user_input * 60 * 60)  # Convert hours to seconds
            if initial_seconds > 0:
                countdown_timer(initial_seconds)
            else:
                st.error("Please enter a valid time format.")
        except ValueError:
            st.error("Please enter a valid time format.")

if __name__ == '__main__':
    main()