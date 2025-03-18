import streamlit as st
from streamlit_oauth import OAuth2Component
from google.oauth2 import id_token
from google.auth.transport import requests
import json
import os

# Google OAuth credentials
CLIENT_ID = "1056807105062-1vaofhkjgbb78e2om6q0cbcecib1bvji.apps.googleusercontent.com"
CLIENT_SECRET = "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"
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"




import streamlit as st
from streamlit_oauth import OAuth2Component
from google.oauth2 import id_token
from google.auth.transport import requests

# Google OAuth credentials (Replace with your actual credentials)
# CLIENT_ID = "your-client-id.apps.googleusercontent.com"
# CLIENT_SECRET = "your-client-secret"
# AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
# TOKEN_URL = "https://oauth2.googleapis.com/token"
# REDIRECT_URI = "https://www.google.com/"  # Streamlit's default localhost
# REDIRECT_URI = "http://localhost:8501"  # Streamlit's default localhost
REDIRECT_URI = "http://localhost:8502"  # Streamlit's default localhost
# Use a space-separated string for scopes
SCOPES = "openid email profile"

# # Initialize OAuth2 component
# oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTH_URL, TOKEN_URL)

# st.title("Google Login with Streamlit")

# # OAuth2 authorization button
# result = oauth2.authorize_button("Login with Google", REDIRECT_URI, SCOPES)

# st.write("OAuth Response:", result)  # Debugging: Print the response

# main_token=""

# if result:
#     token_data = result.get("token", {})  # Get the 'token' dictionary safely
#     main_token=token_data

#     if "id_token" in token_data:
#         try:
#             # Verify ID token
#             user_info = id_token.verify_oauth2_token(token_data["id_token"], requests.Request(), CLIENT_ID)

#             user_id = user_info["sub"]  # Unique Google ID

#             st.success(f"Welcome, {user_info['name']} with user id: {user_id} ({user_info['email']})")
#             st.image(user_info["picture"], width=100)

#         except Exception as e:
#             st.error(f"Login failed: {e}")
#     else:
#         st.error("Login failed: No 'id_token' found in the token response.")


def ret_func():
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTH_URL, TOKEN_URL)
    result = oauth2.authorize_button("Login with Google", REDIRECT_URI, SCOPES)

    if result:
        token_data = result.get("token", {})  # Get the 'token' dictionary safely
        main_token=token_data

        if "id_token" in token_data:
            try:
                # Verify ID token
                user_info = id_token.verify_oauth2_token(token_data["id_token"], requests.Request(), CLIENT_ID)

                user_id = user_info["sub"]  # Unique Google ID

                # st.success(f"Welcome, {user_info['name']} with user id: {user_id} ({user_info['email']})")
                # st.image(user_info["picture"], width=100)
                return user_info

            except Exception as e:
                # st.error(f"Login failed: {e}")
                return None

        else:
            # st.error("Login failed: No 'id_token' found in the token response.")
            return None