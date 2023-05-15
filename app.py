import streamlit as st
from flask import send_from_directory
import os

# Retrieve the password from the secrets manager
PASSWORD = st.secrets["password"]

# Add a password prompt to the app
password_input = st.sidebar.text_input("Enter password", type="password")

# Check if the entered password matches the expected password
if password_input == PASSWORD:
    st.success("Access granted!")
    # Add your app code here
else:
    st.error("Access denied.")
    
    # Prevent the rest of the app from running
    st.stop()
    
# Add your app code here (if password is correct)

API_KEY = st.secrets["db_username"]

# Add a sidebar with instructions
with st.sidebar:
    st.subheader("Instructions🔬")
    st.write("To generate text, simply enter your question or prompt in the text area below and click the 'Defeat it!' button.")
    st.subheader("Current Status: ")
    st.success("Undefeated ✅")
    

st.title("💥GPT-Defeater💥")
st.subheader("Defeat Ai detection software")

# Set the values here
temperature = 0.87
length = 400
top_p = 1.0
frequency_penalty = 1.44
presence_penalty = 1.29

# Remove the UI elements for temperature, length, top p, frequency penalty, and presence penalty
input_text = st.text_area("Ask a Question:", height=200)

st.caption('Be specific, this tool can read urls as way of reference or process documentation')

if st.button("Defeat it!"):
    url = "https://api.openai.com/v1/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "text-davinci-003",
        "prompt": input_text,
        "temperature": temperature,
        "max_tokens": length,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }

    response = requests.post(url, headers=headers, json=data)
    st.balloons()

    if response.status_code == 200:
        try:
            text = response.json()["choices"][0]["text"]
            paragraphs = text.split("\n") # Split the text into paragraphs using newline character
            for p in paragraphs:
                st.write(p) # Display each paragraph on a separate line
        except KeyError as e:
            st.error(f"Error: Failed to parse response JSON: {e}")
    elif response.status_code == 400:
        error_message = response.json().get("error", "Unknown error")
        error_code = response.json().get("code", "Unknown code")
        st.error(f"Error: Bad request: {error_message} ({error_code})")
    elif response.status_code == 401:
        st.error("Error: Authentication failed. Please check your API key.")
    elif response.status_code == 429:
        st.error("Error: API rate limit exceeded. Please wait and try again later.")
    else:
        st.error(f"Error: Failed to generate text: {response.status_code} {response.reason}")

# Status at bottom
# st.subheader("Current Status: ")
# st.success("Undefeated")

#Images defeated Apps
st.sidebar.subheader("☠️Apps Defeated☠️")

col1, col2, col3 = st.columns(3)

with col1:
    st.sidebar.image("zero.webp", width=150)

with col2:
    st.sidebar.image("gra.webp", width=150)

with col3:
    st.sidebar.image("turn.webp", width=150)

# Serve the ai-plugin.json file
@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin_json():
    return send_from_directory(os.path.join(app.root_path, '.well-known'), 'ai-plugin.json')

# Add the following line after your existing code
if __name__ == '__main__':
    app.run()
