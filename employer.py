import streamlit as st


def employer_page(username):
    st.title(f"Employer Page ({username})")
    st.write("Here are the reports from all employees:")

    # Example report files
    report_files = ["report1.pdf", "report2.pdf", "report3.pdf"]

    for report_file in report_files:
        st.write(report_file)

    st.write("Select a report to download:")
    selected_report = st.selectbox("", report_files)
    if st.button("Download Report"):
        # TODO: Implement report download logic
        st.write(f"Downloading {selected_report}...")
