import streamlit as st

# Define username and password
username = "abc"
password = "abc"

# Define Streamlit app
def app():
    # Set page title
    st.set_page_config(page_title="Login Page")

    # Create login form
    st.subheader("Login")
    user_input = st.text_input("Enter username")
    pass_input = st.text_input("Enter password", type="password")

    # Check if login details are correct
    if st.button("Submit"):
        if user_input == username and pass_input == password:
            st.success("Login successful!")
            st.write("Click the button below to visit the website.")
            # Display button to hyperlink to website
            st.button("Visit website", on_click=redirect_to_website)
        else:
            st.error("Incorrect username or password")

# Function to redirect to website
def redirect_to_website():
    st.experimental_set_query_params(token="abc123")
    st.experimental_redirect("https://khushalj-streamlit-csv-pie-newlogin-32ttdc.streamlit.app/")

# Run the Streamlit app
if __name__ == '__main__':
    app()
