import streamlit as st
from login import login_page, switch_page
from employee import employee_page
from employer import employer_page


def main():
    session = st.session_state.setdefault("switch_page", {})
    if "page_name" not in session:
        session["page_name"] = "login"

    if session["page_name"] == "login":
        login_page(switch_page)
    elif session["page_name"] == "employee":
        employee_page(session["username"])
    elif session["page_name"] == "employer":
        employer_page(session["username"])


if __name__ == "__main__":
    main()
