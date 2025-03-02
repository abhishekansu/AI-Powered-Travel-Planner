import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# ✅ Securely Fetch API Key from Streamlit Secrets
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Validate API Key
if GOOGLE_API_KEY is None:
    st.error("Error: GOOGLE_API_KEY not found in .env file.")
    # Handle the error appropriately (e.g., exit the script)
else:
    # Your code that uses the API key
    print("GOOGLE_API_KEY Loaded.")

# ✅ Function to fetch AI-generated travel options
def get_travel_options(source, destination):
    system_prompt = SystemMessage(
        content="You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with estimated costs, duration, and relevant travel tips."
    )
    user_prompt = HumanMessage(
        content=f"I am traveling from {source} to {destination}. Suggest travel options with estimated cost, duration, and important details."
    )

    # ✅ Initialize AI model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

# ✅ Streamlit UI
st.title("🚀SimplifyTravels - AI Based Travel Recommendations")
st.markdown("Enter your travel details to get AI-generated travel options including cost estimates and travel tips.")

# ✅ User Inputs
source = st.text_input("🛫 Enter Source Location", placeholder="E.g., Ukraine")
destination = st.text_input("🛬 Enter Destination", placeholder="E.g., Russia")

if st.button("🔍 Find Travel Options"):
    if source.strip() and destination.strip():
        with st.spinner("🔄 Search best travelling options available..."):
            travel_info = get_travel_options(source, destination)
            st.success("✅ Travel Recommendations:")
            st.markdown(travel_info)
    else:
        st.warning("⚠️ Please enter both source and destination locations.")