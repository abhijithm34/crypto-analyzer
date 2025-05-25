# 🤖 Crypto Price Assistant

A real-time cryptocurrency price tracking application that provides friendly, conversational updates about your favorite cryptocurrencies. Built with Python and Streamlit, this app offers an intuitive interface for tracking crypto prices, market trends, and trading volumes.

## Demo

Here are a couple of screenshots showing the app in action:

![Demo Image 1](images/image1.jpg)

![Demo Image 2](images/image2.jpg)

## ✨ Features

- 💬 Natural language interface for querying cryptocurrency prices
- 📊 Real-time price data from Binance API
- 📈 Interactive price charts and market metrics
- 📱 Responsive, mobile-friendly design
- 🎯 Support for 100+ cryptocurrencies
- 😊 Friendly, conversational responses
- 🔄 Auto-refreshing market data
- 📊 Detailed market statistics
- 📈 Price volatility analysis
- 💰 Trading volume insights

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- A modern web browser

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/crypto-analyzer.git
   cd crypto-analyzer
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run crypto_insight.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The application will automatically load and fetch the latest cryptocurrency data

## 💡 Usage Guide

### Basic Queries

You can ask about any cryptocurrency using natural language:

- "What's the price of Bitcoin?"
- "Tell me about Solana"
- "How is Ethereum doing?"
- "Show me DOGE price"
- "What's happening with Cardano?"

### Understanding the Interface

1. **Main Chat Interface**
   - Type your question in the text box at the bottom
   - Press Enter to get a response
   - View detailed market information in the response

2. **Market Details**
   - Click "View Market Details" to see:
     - Current price
     - 24-hour price changes
     - Trading volume
     - Price charts
     - Market cap rank

3. **Sidebar Features**
   - Refresh data manually
   - View app information
   - Check last update time

### Example Responses

The app provides friendly, detailed responses like:

```
Hey! Let me tell you what's happening with Solana (SOL) right now! 😊

So, Solana is currently trading at $123.45, and it's looking really bullish right now! 📈 
The price has changed by +5.23% in the last 24 hours.

The market's been pretty active - the price has moved between $115.00 and $125.00, 
which means we're seeing about 8.1% volatility. That's pretty wild for crypto! 

People are trading $2.5B worth of Solana in the last 24 hours, and it's sitting at #5 
in terms of market cap. 

I'm feeling excited about Solana right now. Want me to show you the price chart or 
tell you more about what's been happening with it?
```

## 🛠️ Technical Details

### Built With

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization
- **Requests**: API communication
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

### API Integration

- Uses Binance's public API
- No API key required for basic functionality
- Real-time price updates
- 24-hour market data

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/crypto-analyzer.git
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   # Add test commands here when implemented
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to Binance for providing the free API
- Built with Streamlit's amazing framework
- Inspired by the need for user-friendly crypto tools

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/crypto-analyzer/issues) page
2. Create a new issue if your problem isn't already listed
3. Contact the maintainers directly: abhijithmeleppat@gmail.com

## 🔄 Updates

- Latest update: May 2024
- Added friendly, conversational responses
- Improved cryptocurrency data handling
- Enhanced market analysis features

---

Made with ❤️ by Abhijith.M

Happy crypto tracking! 🚀
