# import
## batteries
import os
import base64
## 3rd party
import pandas as pd
import streamlit as st
## package
from bridge_rna_designer.run import design_bridge_rna

# functions
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return "data:image/png;base64," + encoded_string

# App init
st.set_page_config(
    page_title="Bridge RNA Design",
    page_icon="img/arc-logo.ico",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Styling
font_url_h = "https://fonts.googleapis.com/css2?family=Castoro"
st.markdown(f'<link href="{font_url_h}" rel="stylesheet">', unsafe_allow_html=True)
font_url_c = "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;700&display=swap"
st.markdown(f'<link href="{font_url_c}" rel="stylesheet">', unsafe_allow_html=True)
## Custom CSS
st.markdown("""
    <style>
    .font-castoro {
        font-family: 'Castoro', sans-serif;
    }
    .font-ibm-plex-sans {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True
)

# Main
## Title
image_base64 = get_image_as_base64("img/arc-logo-white.png")
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <a href="https://arcinstitute.org/tools/cas13d" target="_blank">
            <img src="{image_base64}" alt="ARC Institute Logo" style="vertical-align: middle; margin-left: 15px; margin-right: 30px;" width="65" height="65">
        </a>
        <span class='font-castoro'>
            <h2>Bridge RNA Design Tool</h2>
        </span>
    </div>
    <div>
        <p>Given 14 bp target and donor sequences, this tool will return a candidate 177 nt bridge RNA that should work with the wild-type bridge recombinase (IS621)</p>
    </div>
    """, unsafe_allow_html=True
)

# Input fields
## Full sequence
st.markdown('#### Input')
col1a, col2a = st.columns([0.5, 0.5])
with col1a:
    target = st.text_input('Target sequence (14 bp)', value='ATCGGGCCTACGCA')
with col2a:
    donor = st.text_input('Donor sequence (14 bp)', value='ACAGTATCTTGTAT')    

if target != '' and donor != '':
    # create dataframe for display
    st.markdown('#### Sequence Components')
    df = pd.DataFrame(
        {
            'Left (7 bp)': [target[0:7], donor[0:7]],
            'Core (2 bp)': [target[7:9], donor[7:9]],
            'Right (5 bp)': [target[9:], donor[9:]]
        },
        index=['Target', 'Donor']
    )
    st.table(df)

    ## Submit button
    if st.button('Design Bridge RNA'):
        # Output
        with st.spinner("Calculating..."):
            st.markdown('#### Bridge RNA')
            try:
                brna = design_bridge_rna(target, donor)
                st.text(brna.format_fasta())
                st.text(brna.format_stockholm())
            except Exception as e:
                st.error(f"Error: {e}")


