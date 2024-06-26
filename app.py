# import
## batteries
import os
import base64
## 3rd party
import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from bridgernadesigner.run import design_bridge_rna

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
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;700&display=swap');
body * {
    font-family: 'IBM Plex Sans', sans-serif !important;
}
code, pre,input[type="text"], table, th, td {
    font-family: 'Courier New', Courier, monospace !important;
}
table, td {
    background-color: #2D8EFF !important;
    color: white !important;
}
a {
    color: white !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Main
## Title
image_base64 = get_image_as_base64('img/arc-logo-white.png')
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
col1, col2, col3 = st.columns([0.29, 0.01, 0.70])
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
    st.table(df)
    with stylable_container('btn-calc', css_styles='button { margin-left: 45px; width: 55%; }'):
        st.session_state['calc_button'] = st.button('Design Bridge RNA')
    
def create_stockholm_table():
    DF = pd.DataFrame({
        'Key': ['#=GC', 'L', 'R', 'H', 'C', 'l', 'r', 'h', 'c'],
        'Description': [
            'guides', 'left target guide (LTG)', 'right target guide (RTG)', 
            'TBL handshake guide (TBL-HSG)', 'TBL core-binding guide', 
            'left donor guide (LDG)', 'right donor guide (RDG)', 
            'DBL handshake guide (DBL-HSG)', 'DBL core-binding guide'
        ]
    })
    return DF.to_markdown(index=False)

# Output
if target != '' and donor != '':
    ## Submit button
    if st.session_state['calc_button'] or st.session_state['brna'] is not None:
        # check input
        if len(target) != 14 or len(donor) != 14:
            st.error('Please enter 14 bp sequences for both target and donor.')
            st.stop()
        # Output
        with st.spinner('Calculating...'):
            # Calculate bridge RNA
            st.markdown('#### Bridge RNA')
            try:
                st.session_state['brna'] = design_bridge_rna(target, donor)
            except Exception as e:
                st.error(f'Error: {e}')
                st.session_state['brna'] = None
            # Display output
            if st.session_state['brna'] is not None:
                tab1, tab2 = st.tabs(['stockholm', 'fasta (with annealing oligos)'])
                with tab1:
                    # stockholm tab
                    st.markdown('##### STOCKHOLM')
                    stockholm = st.session_state['brna'].format_stockholm()
                    st.markdown(f'```\n{stockholm}\n```')
                    col1,col2,col3 = st.columns([0.3, 0.6, 0.1])
                    ## download link
                    with col1:
                        with stylable_container('dtl-stockholm', css_styles='button { height: 48px; width: 100%; }'):
                            st.download_button(
                                label='Download stockholm',
                                data=stockholm,
                                file_name='bridge-rna.sto',
                                mime='text/plain'
                            )
                    with col2:
                        with st.expander('Stockholm format key'):
                            st.write(create_stockholm_table())
                with tab2:
                    # fasta tab
                    st.markdown('##### FASTA')
                    # annealing oligos
                    include_an_oligos = st.checkbox('Include annealing oligos?', value=False)
                    if include_an_oligos:
                        col1a,col2a = st.columns([0.5, 0.5])
                        with col1a:
                            lh_overhang = st.text_input(
                                '5\' overhang for annealing oligos.', 
                                value='TAGC'
                            )
                        with col2a:
                            rh_overhang = st.text_input(
                                '3\' overhang for annealing oligos', 
                                value='GGCC'
                            )
                    else:
                        lh_overhang = None
                        rh_overhang = None
                    # fasta generation
                    fasta = st.session_state['brna'].format_fasta(
                        include_annealing_oligos=include_an_oligos,
                        lh_overhang=lh_overhang,
                        rh_overhang=rh_overhang
                    )
                    st.markdown(f"```\n{fasta}\n```")
                    ## download link
                    col1,col2 = st.columns([0.3, 0.7])
                    with col1:
                        # download
                        st.download_button(
                            label='Download fasta',
                            data=fasta,
                            file_name='bridge-rna.fasta',
                            mime='text/plain',
                        )
                        

st.divider()
st.markdown("""
### References
            
Durrant, M.G., Perry, N.T., Pai, J.J. et al.
Bridge RNAs direct programmable recombination of target and donor DNA. 
Nature 630, 984-993 (2024). https://doi.org/10.1038/s41586-024-07552-4

Hiraizumi, M., Perry, N.T., Durrant, M.G. et al.
Structural mechanism of bridge RNA-guided recombination.
Nature 630, 994–1002 (2024). https://doi.org/10.1038/s41586-024-07570-2
""")
st.markdown("""
### Code
            
View the code and obtain the CLI tool from [GitHub](https://github.com/hsulab-arc/BridgeRNADesigner)
""")

