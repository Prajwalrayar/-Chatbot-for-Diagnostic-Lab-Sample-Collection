FIELDS = [
    "name",
    "phone",
    "email",
    "test_name",
    "date",
    "time"
]

QUESTIONS = {
    "name": "Please enter your full name:",
    "phone": "Enter your phone number:",
    "email": "Enter your email address:",
    "test_name": "Which lab test do you want? (Blood / Urine / Full Body Checkup)"
}

def initialize_state(st):
    if "booking_data" not in st.session_state:
        st.session_state.booking_data = {}
        st.session_state.step = 0
        st.session_state.saved = False

def get_current_field(st):
    return FIELDS[st.session_state.step]

def save_text_answer(st, answer):
    field = get_current_field(st)
    st.session_state.booking_data[field] = answer
    st.session_state.step += 1

def save_date(st, date):
    st.session_state.booking_data["date"] = str(date)
    st.session_state.step += 1

def save_time(st, time):
    st.session_state.booking_data["time"] = time
    st.session_state.step += 1

def is_complete(st):
    return st.session_state.step >= len(FIELDS)

def get_summary(st):
    b = st.session_state.booking_data
    return f"""
### 🧪 Booking Summary
- **Name:** {b['name']}
- **Phone:** {b['phone']}
- **Email:** {b['email']}
- **Test:** {b['test_name']}
- **Date:** {b['date']}
- **Time:** {b['time']}
"""
