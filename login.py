import streamlit as st


def login_page(switch_page):
    st.title("Login Page")
    account_type = st.radio("Choose account type:", ("Employer", "Employee"))
    username = st.text_input("Enter your username:")
    if st.button("Login"):
        switch_page(account_type.lower(), username)


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


def switch_page(page_name: str, username: str):
    session = st.session_state.setdefault("switch_page", {})
    session["page_name"] = page_name
    session["username"] = username.lower()


if __name__ == "__main__":
    main()
