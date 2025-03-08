import streamlit as st

# Define the pages
page_1 = st.Page("page1.py", title="Lapse Date")
page_2 = st.Page("page2.py", title="Lapse Chart")
page_3 = st.Page("page3.py", title="Calories Data")
page_4 = st.Page("page4.py", title="Calories Chart")

# Set up navigation
pg = st.navigation([page_1, page_2, page_3, page_4])

# Run the selected page
pg.run()