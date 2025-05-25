import streamlit as st
import pandas as pd
import requests

st.title("🧠 Crypto Price Prediction (LSTM)")

def get_live_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad status
        data = response.json()
        btc_price = data["bitcoin"]["usd"]
        eth_price = data["ethereum"]["usd"]
        return btc_price, eth_price
    except requests.exceptions.RequestException as e:
        st.error(f"Network/API error: {e}")
        return None, None
    except KeyError:
        st.error("Unexpected API response structure.")
        return None, None

btc_price, eth_price = get_live_prices()

# --- Modern Card UI for live prices ---
if btc_price and eth_price:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #f7931a, #ffb347);
                border-radius: 15px; padding: 20px; text-align: center;
                box-shadow: 0 4px 15px rgba(247,147,26,0.4);">
                <h3 style="color:white; margin-bottom: 10px;">Bitcoin (BTC)</h3>
                <p style="font-size: 32px; color: white; margin: 0;">${btc_price:,.2f}</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #627eea, #a3bffa);
                border-radius: 15px; padding: 20px; text-align: center;
                box-shadow: 0 4px 15px rgba(98,126,234,0.4);">
                <h3 style="color:white; margin-bottom: 10px;">Ethereum (ETH)</h3>
                <p style="font-size: 32px; color: white; margin: 0;">${eth_price:,.2f}</p>
            </div>
            """, unsafe_allow_html=True
        )
else:
    st.warning("⚠️ Failed to fetch current crypto prices.")
    
# Step 1: Select crypto
crypto = st.selectbox("Select Cryptocurrency", ("bitcoin", "ethereum"))
backend_url = "http://127.0.0.1:5000/predict/btc" if crypto == "bitcoin" else "http://127.0.0.1:5000/predict/eth"

# Step 2: Choose data input method
input_mode = st.radio("Choose input method:", ("📂 Upload CSV", "📝 Enter Manually", "🌐 Fetch Online"))

def predict(sequence):
    try:
        st.info("Sending data to backend...")
        res = requests.post(backend_url, json={"sequence": sequence})
        data = res.json()

        if res.status_code == 200:
            st.success(f"Predicted {crypto.upper()} Price: ${data['prediction']:.2f}")
            transaction_hash = data.get("tx_hash", "N/A")
            if transaction_hash != "N/A":
                explorer_link = f"https://giant-half-dual-testnet.explorer.testnet.skalenodes.com/address/{transaction_hash}"
                if st.button(f"🔗 View Transaction {transaction_hash}"):
                    st.markdown(f"[Click here to view transaction]({explorer_link})")
            st.code(f"Transaction Hash: {transaction_hash}")
        else:
            st.error(f"Backend error: {data.get('error', res.text)}")
    except Exception as e:
        st.error(f"Connection error: {e}")

# === 1. Upload CSV with selectable column ===
if input_mode == "📂 Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("CSV Preview:")
            st.dataframe(df.head())

            st.subheader("Select column with closing prices:")
            selected_column = st.selectbox("Available columns:", df.columns)

            if len(df[selected_column]) < 60:
                st.error("Need at least 60 rows in the selected column.")
            else:
                prices = df[selected_column].tail(60).tolist()
                st.success(f"Using column: {selected_column}")
                st.line_chart(prices)

                if st.button("🚀 Predict"):
                    predict(prices)
        except Exception as ex:
            st.error(f"Error reading CSV: {ex}")

# === 2. Enter Manually ===
elif input_mode == "📝 Enter Manually":
    st.write("Enter 60 prices separated by commas:")
    manual_input = st.text_area("Prices", height=150, placeholder="e.g., 10000, 10100, 10200, ...")
    if manual_input:
        try:
            prices = [float(p.strip()) for p in manual_input.split(",") if p.strip()]
            if len(prices) != 60:
                st.warning(f"Entered {len(prices)} prices. Need exactly 60.")
            else:
                st.line_chart(prices)
                if st.button("🚀 Predict"):
                    predict(prices)
        except ValueError:
            st.error("Please enter only numeric values.")

# === 3. Fetch Online ===
elif input_mode == "🌐 Fetch Online":
    st.info("Fetching prices from CoinGecko...")
    coingecko_id = "bitcoin" if crypto == "bitcoin" else "ethereum"
    try:
        days = 60
        url = f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}
        res = requests.get(url, params=params)
        data = res.json()
        if "prices" in data:
            all_prices = [price[1] for price in data["prices"]]
            prices = all_prices[-60:]  # ✅ Ensure exactly 60 entries
            st.success(f"Fetched {len(prices)} prices.")
            st.line_chart(prices)
            if st.button("🚀 Predict"):
                predict(prices)
        else:
            st.error("Failed to fetch prices.")
    except Exception as e:
        st.error(f"API error: {e}")

