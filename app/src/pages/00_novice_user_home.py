import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Novice Trader, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View My Portfolio', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_novice_user_portfolio.py')

if st.button('View Verified Profiles and Follow', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_novice_user_view_profile.py') 

if st.button('Check Posted Notifications', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_novice_user_check_notifications.py')

if st.button('Financial AI Consultant (Novice)', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/97_reg_chatbot.py') 

if st.button('Stock Analysis', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/04_novice_user_stock_analysis.py')

