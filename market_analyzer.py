import os
from typing import Dict, List
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
import logging
from datetime import datetime, timedelta

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

crypto_metadata = []

def fetch_crypto_data() -> List[Dict]:
    # Get top cryptocurrencies from Binance
    url = "https://api.binance.com/api/v3/ticker/24hr"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Filter for USDT pairs and format the data
        formatted_data = []
        processed_symbols = set()  # Keep track of processed symbols
        
        # Common name mappings with full names
        name_mappings = {
            'BTC': 'Bitcoin',
            'ETH': 'Ethereum',
            'BNB': 'Binance Coin',
            'SOL': 'Solana',
            'XRP': 'Ripple',
            'ADA': 'Cardano',
            'DOGE': 'Dogecoin',
            'DOT': 'Polkadot',
            'SHIB': 'Shiba Inu',
            'AVAX': 'Avalanche',
            'MATIC': 'Polygon',
            'LINK': 'Chainlink',
            'UNI': 'Uniswap',
            'AAVE': 'Aave',
            'ATOM': 'Cosmos',
            'LTC': 'Litecoin'
        }
        
        # First, process known cryptocurrencies
        for symbol, full_name in name_mappings.items():
            usdt_pair = f"{symbol}USDT"
            matching_items = [item for item in data if item['symbol'] == usdt_pair]
            
            if matching_items:
                item = matching_items[0]
                formatted_data.append({
                    "id": symbol.lower(),
                    "name": full_name,
                    "symbol": symbol,
                    "current_price": float(item['lastPrice']),
                    "market_cap_rank": len(formatted_data) + 1,
                    "price_change_24h": float(item['priceChange']),
                    "market_cap": float(item['quoteVolume']),
                    "total_volume": float(item['volume']),
                    "high_24h": float(item['highPrice']),
                    "low_24h": float(item['lowPrice']),
                    "price_change_percentage_24h": float(item['priceChangePercent'])
                })
                processed_symbols.add(symbol)
        
        # Then process remaining USDT pairs
        for item in data:
            if item['symbol'].endswith('USDT'):
                base_symbol = item['symbol'].replace('USDT', '')
                if base_symbol not in processed_symbols:
                    formatted_data.append({
                        "id": base_symbol.lower(),
                        "name": base_symbol,
                        "symbol": base_symbol,
                        "current_price": float(item['lastPrice']),
                        "market_cap_rank": len(formatted_data) + 1,
                        "price_change_24h": float(item['priceChange']),
                        "market_cap": float(item['quoteVolume']),
                        "total_volume": float(item['volume']),
                        "high_24h": float(item['highPrice']),
                        "low_24h": float(item['lowPrice']),
                        "price_change_percentage_24h": float(item['priceChangePercent'])
                    })
                    processed_symbols.add(base_symbol)
                
                # Limit to top 100 cryptocurrencies
                if len(formatted_data) >= 100:
                    break
        
        return formatted_data
    except RequestException as e:
        logger.error(f"Error fetching crypto data: {str(e)}")
        raise

def refresh_crypto_data() -> None:
    global crypto_metadata
    try:
        crypto_data = fetch_crypto_data()
        crypto_metadata = crypto_data
        logger.info(f"Successfully refreshed data for {len(crypto_data)} cryptocurrencies")
    except Exception as e:
        logger.error(f"Error refreshing crypto data: {str(e)}")
        raise

def find_crypto_by_query(query: str) -> Dict:
    query = query.lower().strip()
    
    # Common cryptocurrency names mapping
    crypto_names = {
        'btc': 'BTC',
        'bitcoin': 'BTC',
        'eth': 'ETH',
        'ethereum': 'ETH',
        'bnb': 'BNB',
        'binance': 'BNB',
        'sol': 'SOL',
        'solana': 'SOL',
        'xrp': 'XRP',
        'ripple': 'XRP',
        'ada': 'ADA',
        'cardano': 'ADA',
        'doge': 'DOGE',
        'dogecoin': 'DOGE',
        'dot': 'DOT',
        'polkadot': 'DOT',
        'shib': 'SHIB',
        'shiba': 'SHIB',
        'shibainu': 'SHIB',
        'avax': 'AVAX',
        'avalanche': 'AVAX',
        'matic': 'MATIC',
        'polygon': 'MATIC',
        'link': 'LINK',
        'chainlink': 'LINK',
        'uni': 'UNI',
        'uniswap': 'UNI',
        'aave': 'AAVE',
        'atom': 'ATOM',
        'cosmos': 'ATOM',
        'ltc': 'LTC',
        'litecoin': 'LTC'
    }
    
    # First, try exact matches with common names
    if query in crypto_names:
        symbol = crypto_names[query]
        for crypto in crypto_metadata:
            if crypto['symbol'] == symbol:
                return crypto
    
    # Then try partial matches in names and symbols
    for crypto in crypto_metadata:
        # Check if query matches the name or symbol
        if (query in crypto['name'].lower() or 
            query in crypto['symbol'].lower() or
            crypto['name'].lower() in query or 
            crypto['symbol'].lower() in query):
            return crypto
    
    # If no match found, return Bitcoin (BTC) as default
    for crypto in crypto_metadata:
        if crypto['symbol'] == 'BTC':
            return crypto
    
    return crypto_metadata[0]  # Fallback to first crypto if BTC not found

def format_response(crypto_data: Dict) -> str:
    price_change = crypto_data['price_change_percentage_24h']
    price_change_str = f"{price_change:+.2f}%" if price_change != 0 else "0.00%"
    
    # Determine market sentiment and create friendly phrases
    if price_change > 5:
        sentiment = "looking really bullish right now! 📈"
        mood = "excited"
    elif price_change > 0:
        sentiment = "showing some positive movement 📊"
        mood = "optimistic"
    elif price_change > -5:
        sentiment = "going through a bit of a dip 📉"
        mood = "cautious"
    else:
        sentiment = "having a rough time at the moment 😅"
        mood = "concerned"
    
    # Format volume in a readable way
    volume = crypto_data['total_volume']
    if volume >= 1e9:
        volume_str = f"${volume/1e9:.2f}B"
    elif volume >= 1e6:
        volume_str = f"${volume/1e6:.2f}M"
    else:
        volume_str = f"${volume:,.2f}"
    
    # Calculate volatility percentage
    volatility = abs(crypto_data['high_24h'] - crypto_data['low_24h'])/crypto_data['current_price']*100
    
    # Create a friendly, conversational response
    response = f"""Hey! Let me tell you what's happening with {crypto_data['name']} ({crypto_data['symbol']}) right now! 😊

So, {crypto_data['name']} is currently trading at ${crypto_data['current_price']:,.2f}, and it's {sentiment} The price has changed by {price_change_str} in the last 24 hours.

The market's been pretty active - the price has moved between ${crypto_data['low_24h']:,.2f} and ${crypto_data['high_24h']:,.2f}, which means we're seeing about {volatility:.1f}% volatility. That's {'quite normal' if volatility < 10 else 'pretty wild' if volatility < 20 else 'super volatile'} for crypto! 

People are trading {volume_str} worth of {crypto_data['name']} in the last 24 hours, and it's sitting at #{crypto_data['market_cap_rank']} in terms of market cap. 

I'm feeling {mood} about {crypto_data['name']} right now. Want me to show you the price chart or tell you more about what's been happening with it?"""
    
    return response

async def query_crypto_price(user_query: str, source_lang: str = "en") -> str:
    try:
        # Find matching crypto
        crypto_data = find_crypto_by_query(user_query)
        
        # Format the response
        formatted_response = format_response(crypto_data)
        
        return formatted_response
        
    except Exception as e:
        logger.error(f"Error processing query '{user_query}': {str(e)}")
        raise

# Initialize data
refresh_crypto_data()
