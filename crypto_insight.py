# app.py

import streamlit as st
import asyncio
from market_analyzer import (
    refresh_crypto_data,
    query_crypto_price,
    crypto_metadata
)
import plotly.graph_objects as go
from datetime import datetime


st.set_page_config(
    page_title="Crypto Price Assistant",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stApp {
        background-color: #f5f7f9;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        height: 3em;
    }
    .st-emotion-cache-1v0mbdj {
        margin-top: 1em;
    }
    .market-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .chat-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'crypto_metadata' not in st.session_state:
    refresh_crypto_data()
    st.session_state.crypto_metadata = crypto_metadata

def format_large_number(num):
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.2f}K"
    return f"${num:.2f}"

async def handle_query():
    query = st.session_state.query_input
    if query:
        st.session_state.chat_history.append({
            "role": "user",
            "content": query
        })

        try:
            response = await query_crypto_price(query)
            crypto_data = next((crypto for crypto in st.session_state.crypto_metadata 
                                if crypto['name'].lower() in response.lower() 
                                or crypto['symbol'].lower() in response.lower()), None)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "data": crypto_data
            })
            st.session_state.query_input = ""

        except Exception as e:
            st.error(f"Error: {str(e)}")

def main():
    # Header section with gradient background
    st.markdown("""
        <div style='background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center;'>🤖 Crypto Price Assistant</h1>
            <p style='color: white; text-align: center; font-size: 1.2em;'>Ask me anything about cryptocurrency prices!</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar with improved styling
    with st.sidebar:
        st.markdown("""
            <div style='background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <h3 style='color: #1e3c72;'>⚙️ Settings</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
            <div style='background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <h3 style='color: #1e3c72;'>ℹ️ About</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        This assistant provides:
        - 📈 Current cryptocurrency prices
        - 📊 24-hour price changes
        - 💰 Trading volume
        - 📉 Price rankings
        """)
        
        if st.button("🔄 Refresh Data", key="refresh_button"):
            with st.spinner("Refreshing cryptocurrency data..."):
                refresh_crypto_data()
                st.session_state.crypto_metadata = crypto_metadata
                st.success("✅ Data refreshed successfully!")

        st.markdown("---")
        st.markdown(f"🕒 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Main content area with chat history
    chat_container = st.container()
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
                <div style='background: #e6f3ff; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                    <p><strong>You</strong>: {message['content']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                    <p><strong>Assistant</strong>: {message['content']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if "data" in message and message["data"]:
                with st.expander("📊 View Market Details"):
                    data = message["data"]
                    st.markdown("<div class='market-card'>", unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    col1.metric(
                        "💵 Current Price",
                        f"${data['current_price']:,.2f}", 
                        delta=f"{data['price_change_percentage_24h']:.2f}%"
                    )
                    col2.metric(
                        "📊 24h Volume",
                        format_large_number(data['total_volume'])
                    )
                    col3.metric(
                        "🏆 Rank",
                        f"#{data['market_cap_rank']}"
                    )
                    
                    # Generate a unique key for each chart based on timestamp and crypto data
                    chart_key = f"price_chart_{data['symbol']}_{datetime.now().timestamp()}"
                    
                    # Enhanced price range chart with unique key
                    price_range_chart = go.Figure(go.Indicator(
                        mode="number+gauge+delta",
                        value=data['current_price'],
                        delta={'reference': data['current_price'] - data['price_change_24h']},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "📈 24h Price Range", 'font': {'size': 20}},
                        gauge={
                            'axis': {'range': [data['low_24h'], data['high_24h']]},
                            'bar': {'color': "#1e3c72"},
                            'steps': [
                                {'range': [data['low_24h'], data['high_24h']], 'color': "#e6f3ff"}
                            ],
                            'threshold': {
                                'line': {'color': "#2a5298", 'width': 4},
                                'thickness': 0.75,
                                'value': data['current_price']
                            }
                        }
                    ))
                    
                    price_range_chart.update_layout(
                        height=250,
                        margin=dict(l=30, r=30, t=50, b=30),
                        paper_bgcolor='white',
                        plot_bgcolor='white'
                    )
                    
                    # Add the unique key to the plotly_chart
                    st.plotly_chart(price_range_chart, use_container_width=True, key=chart_key)
                    st.markdown("</div>", unsafe_allow_html=True)

    # Add some space at the bottom for the input box
    st.markdown("<br>" * 5, unsafe_allow_html=True)

    # Input area with improved styling
    st.markdown("<div style='background: white; padding: 1.5rem; border-radius: 10px; margin-top: 2rem;'>", unsafe_allow_html=True)
    st.text_input(
        "💬 Ask about any cryptocurrency:",
        key="query_input",
        on_change=lambda: asyncio.run(handle_query()),
        placeholder="Example: What is the current price of Bitcoin?"
    )
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()