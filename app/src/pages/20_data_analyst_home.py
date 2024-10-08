import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View General User Data, Specific User Data, Ban/Unban Users', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_data_analyst_user_data.py')

if st.button('View All User Metrics', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_data_analyst_user_metrics.py')

if st.button('View General Verified User Data, Specific User Data, Ban/Unban Users', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/23_data_analyst_verif_users.py')

if st.button('Analyst Chat Box', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/99_analyst_chatbot.py')
