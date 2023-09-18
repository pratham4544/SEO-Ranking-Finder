import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from PIL import Image

image = Image.open('csv file fomat.png')

# Function to search for a link and return a DataFrame
def search_link(api_key, keyword, user_input_link):
    params = {
        "engine": "google",
        "q": keyword,
        "location": "Maharashtra, India",
        "google_domain": "google.co.in",
        "gl": "in",
        "hl": "en",
        "device": "mobile",
        "filter": "0",
        "num": "20",
        "api_key": api_key  # Use the provided API key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    r1 = results['organic_results']

    # Search for the link and its position
    found_links = []
    for item in r1:
        if "link" in item and item["link"] == user_input_link:
            found_links.append(item)

    if found_links:
        data_frames = []

        for link_info in found_links:
            data_frames.append(pd.DataFrame({'keyword': keyword, 'position': [link_info['position']], 'link': [link_info['link']]}))

        result_df = pd.concat(data_frames, ignore_index=True)
        return result_df
    else:
        return None

# Streamlit app
st.title("Google SEO Ranking Extractor")

# Input for SerpApi Key
st.write("For Create your api key [link](https://serpapi.com/users/sign_up)")

api_key = st.text_input("Enter your SerpApi Key:")
st.write("SerpApi Key:", api_key)

# csv file format img

st.image(image=image ,caption='csv file format should be look like')
# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded CSV file:")
    st.write(df)

    # Initialize progress bar
    progress_bar = st.progress(0)
    total_rows = len(df)
    completed_rows = 0

    # Initialize empty DataFrame to store results
    result_df = pd.DataFrame(columns=['keyword', 'position', 'link'])

    # Iterate through rows in the CSV
    for index, row in df.iterrows():
        keyword = row['keyword']
        link_to_find = row['link']
        st.write(f"Searching for link in keyword '{keyword}'...")

        # Search for the link in the Google search results using the provided API key
        link_df = search_link(api_key, keyword, link_to_find)

        if link_df is not None:
            result_df = pd.concat([result_df, link_df], ignore_index=True)

        # Update progress
        completed_rows += 1
        progress_bar.progress(completed_rows / total_rows)

    # Display the results
    if not result_df.empty:
        st.write("Found links:")
        st.write(result_df)

    # Export the results to a CSV file
    result_csv = result_df.to_csv(index=False)
    st.download_button("Download CSV", data=result_csv.encode('utf-8'), file_name="serpapi_results.csv", key='download_csv')

# To run the app, use the 'streamlit run' command in your terminal.
