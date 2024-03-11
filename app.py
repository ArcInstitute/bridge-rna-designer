# import
## batteries
import os
import base64
## 3rd party
import pandas as pd
import streamlit as st
## package
from bridge_rna_designer.run import design_bridge_rna

# Functions
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

# Set custom styles
font_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;700&display=swap');
body * {
    font-family: 'IBM Plex Sans', sans-serif !important;
}
code, pre {
    font-family: 'Courier New', monospace !important;
}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

# Main
## Title
image_base64 = get_image_as_base64("img/arc-logo-white.png")
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <a href="https://arcinstitute.org/tools/cas13d" target="_blank">
            <img src="{image_base64}" alt="ARC Institute Logo" style="vertical-align: middle; margin-left: 2px; margin-right: 15px;" width="60" height="60">
        </a>
        <span class='app-title'>
            <h2>Bridge RNA Design Tool</h2>
        </span>
    </div>
    <div>
        <p>
           Given 14 bp target and donor sequences, 
           this tool will return a candidate 177 nt bridge RNA
           that should work with the wild-type bridge recombinase
           (IS621).
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Session states
if 'brna' not in st.session_state:
    st.session_state.brna = None
if 'calc_button' not in st.session_state:
    st.session_state.calc_button = False

# Input
col1, col2, col3 = st.columns([0.30, 0.05, 0.65])
with col1:
    st.markdown('#### Input')
    target = st.text_input('Target sequence (14 bp)', value='ATCGGGCCTACGCA')
    donor = st.text_input('Donor sequence (14 bp)', value='ACAGTATCTTGTAT')    
with col3:
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
    st.dataframe(df)
    if len(target) == 14 and len(donor) == 14:
        st.session_state['calc_button'] = st.button('Design Bridge RNA')
    

# Output
if target != '' and donor != '':
    ## Submit button
    if st.session_state['calc_button'] or st.session_state['brna'] is not None:
        # Output
        with st.spinner("Calculating..."):
            # Calculate bridge RNA
            st.markdown('#### Bridge RNA')
            brna = None
            try:
                st.session_state['brna'] = design_bridge_rna(target, donor)
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state['brna'] = None
            # Display output
            if st.session_state['brna'] is not None:
                tab1, tab2 = st.tabs(['stockholm', 'fasta'])
                with tab1:
                    # stockholm
                    st.markdown('##### STOCKHOLM')
                    stockholm = st.session_state['brna'].format_stockholm()
                    st.markdown(f"```\n{stockholm}\n```")
                    ## download link
                    st.download_button(
                        label="Download stockholm",
                        data=stockholm,
                        file_name='bridge-rna.sto',
                        mime='text/plain',
                    )
                with tab2:
                    # fasta
                    fasta = st.session_state['brna'].format_fasta()
                    st.markdown('##### FASTA')
                    st.text(fasta)
                    ## download link
                    st.download_button(
                        label="Download fasta",
                        data=fasta,
                        file_name='bridge-rna.fasta',
                        mime='text/plain',
                    )





