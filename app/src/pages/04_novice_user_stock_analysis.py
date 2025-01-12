import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

# Set up sidebar navigation
SideBarLinks()

st.write("# Stock Analysis Dashboard")
st.write(f"### Hi, {st.session_state['first_name']}.")

# Get all available stocks
try:
    data = requests.get('http://api:4000/u/stocks').json()
    st.write("### Available Stocks")
    st.dataframe(data)
except:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

# Get and display stock recommendations
st.write("### Top Stock Recommendations")
try:
    recommendations = requests.get('http://api:4000/u/stock/recommendations').json()
    st.dataframe(recommendations)
except:
    st.write("**Important**: Could not load recommendations.")

# Individual stock analysis section
st.write("### Detailed Stock Analysis")
try:
    response = requests.get('http://api:4000/u/getTicker')
    response.raise_for_status()
    data = response.json()
    stock_names = [item["ticker"] for item in data]
    
    selected_stock = st.selectbox(
        "Select a stock to analyze:",
        options=["Select a ticker..."] + stock_names,
        index=0,
        placeholder="Select a ticker..."
    )

    if selected_stock and selected_stock != "Select a ticker...":
        try:
            # Get analysis for selected stock
            analysis = requests.get(f'http://api:4000/u/stock/analysis/{selected_stock}').json()
            
            # Create two columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Trading Signal", analysis['recommendation'])
            with col2:
                st.metric("Confidence Level", f"{analysis['confidence']:.1f}%")
            with col3:
                st.metric("Price Change", f"{analysis['indicators']['price_change']:.2f}%")

            # Create visualization of technical indicators
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=("Moving Averages", "Volume Trend", "RSI", "Signal Strength")
            )

            # Moving Averages
            fig.add_trace(
                go.Bar(
                    x=['Short MA', 'Long MA'],
                    y=[
                        analysis['indicators']['short_term_ma'],
                        analysis['indicators']['long_term_ma']
                    ],
                    name="Moving Averages"
                ),
                row=1, col=1
            )

            # Volume Trend
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=analysis['indicators']['volume_trend'],
                    title={'text': "Volume Trend"},
                    gauge={'axis': {'range': [-100, 100]}}
                ),
                row=1, col=2
            )

            # RSI
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=analysis['indicators']['rsi'],
                    title={'text': "RSI"},
                    gauge={'axis': {'range': [0, 100]}}
                ),
                row=2, col=1
            )

            # Signal Strength
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=analysis['signal'],
                    title={'text': "Signal Strength"},
                    gauge={'axis': {'range': [-3, 3]}}
                ),
                row=2, col=2
            )

            fig.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # Additional analysis details
            st.write("### Technical Analysis Details")
            details = pd.DataFrame({
                'Indicator': ['RSI', 'Volume Trend', 'Price Change', 'Short-term MA', 'Long-term MA'],
                'Value': [
                    f"{analysis['indicators']['rsi']:.2f}",
                    f"{analysis['indicators']['volume_trend']:.2f}%",
                    f"{analysis['indicators']['price_change']:.2f}%",
                    f"{analysis['indicators']['short_term_ma']:.2f}",
                    f"{analysis['indicators']['long_term_ma']:.2f}"
                ]
            })
            st.dataframe(details, hide_index=True)

            # Trading action suggestion
            st.write("### Trading Action Suggestion")
            suggestion_color = {
                "BUY": "green",
                "SELL": "red",
                "HOLD": "orange"
            }
            st.markdown(
                f"<h2 style='text-align: center; color: {suggestion_color[analysis['recommendation']]};'>"
                f"{analysis['recommendation']}</h2>",
                unsafe_allow_html=True
            )
            
            # Add to portfolio option
            if analysis['recommendation'] == "BUY":
                if st.button("Add to Portfolio"):
                    try:
                        if st.session_state['role'] == 'nov_investor_user':
                            portfolio_id = '596999'  # Emily's portfolio
                        elif st.session_state['role'] == 'ver_investor_user':
                            portfolio_id = '730368'  # Alex's portfolio
                        
                        response = requests.post(f'http://api:4000/u/addStockToPortfolio/{portfolio_id}/{selected_stock}')
                        if response.status_code == 200:
                            st.success(f"Added {selected_stock} to your portfolio!")
                        else:
                            st.error("Error adding stock to portfolio; Stock may already be in your portfolio.")
                    except Exception as e:
                        st.error(f"Error adding stock to portfolio: {e}")

        except Exception as e:
            st.error(f"Error analyzing stock: {e}")

except Exception as e:
    st.error(f"Error loading stocks: {e}")