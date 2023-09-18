import streamlit as st
import pandas as pd
from serpapi import GoogleSearch

# Function to search for a link and return a DataFrame
def search_link(keyword, user_input_link):
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
        "api_key": "8ce6524803c4ec5cee0c46014a6c57d1e875e468b05f96052133ea46ce4e0033"
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
st.title("SerpApi Link Finder")

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
    result_df = pd.DataFrame(columns=['keyword', 'link', 'position'])

    # Iterate through rows in the CSV
    for index, row in df.iterrows():
        keyword = row['keyword']
        link_to_find = row['link']
        st.write(f"Searching for link in keyword '{keyword}'...")

        # Search for the link in the Google search results
        link_df = search_link(keyword, link_to_find)

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
    st.download_button("Download CSV", data=result_csv, file_name="serpapi_results.csv", key='download_csv')

# Note: You need to run the Streamlit app using the 'streamlit run' command in your terminal.
