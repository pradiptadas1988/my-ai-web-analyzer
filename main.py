import streamlit as st
from scrape_website import (
    scrape_html_site,
    get_body_content,
    process_content,
    split_dom_content
)
from analyze_data import analyze_dom_element

st.title("AI Web Analyzer")
url = st.text_input("Enter the website url you want to analyze: ")

if st.button("Scrape Web"):
    if url:
        st.write('Scrapping the website...')
        html_content = scrape_html_site(url)
        body_content = get_body_content(html_content)
        cleaned_body_content = process_content(body_content)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_body_content

        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_body_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Generate Content"):
        if parse_description:
            print("Generating the content...")
            st.write("Generating the content...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            print("Chunks ready...")
            st.write("Chunks ready...")
            generated_results = analyze_dom_element(dom_chunks, parse_description)
            print(generated_results)
            st.write(generated_results)
            print("Generation of content Successful!!!")