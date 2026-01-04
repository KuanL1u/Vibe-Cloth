import streamlit as st
import base64
from openai import OpenAI
from ddgs import DDGS
from PIL import Image
from io import BytesIO
import json
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="StyleAI", page_icon="✨", layout="wide")

# Initialize session state for client
if 'client' not in st.session_state:
    st.session_state.client = None

# Initialize OpenAI Client (Ensure you have OPENAI_API_KEY in your env or secrets)
# For local run, you can set it here or use st.secrets
if st.session_state.client is None:
    try:
        st.session_state.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except:
        # If not in secrets, will ask user in sidebar
        pass

# --- CUSTOM CSS FOR BEAUTIFUL UI ---
def local_css():
    st.markdown("""
    <style>
        /* General Font and Background */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');
        
        .stApp {
            background-color: #FAFAFA;
            font-family: 'Lato', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #1A1A1A;
        }

        /* Custom Cards for Products */
        .product-card {
            background-color: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
            text-align: center;
            height: 100%;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        .product-img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .product-title {
            font-weight: 700;
            font-size: 1.1em;
            margin-bottom: 5px;
            color: #333;
        }
        .product-link {
            text-decoration: none;
            color: white;
            background-color: #000;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            display: inline-block;
            margin-top: 10px;
        }
        .product-link:hover {
            background-color: #333;
        }

        /* Loading Spinner Color */
        .stSpinner > div {
            border-top-color: #000 !important;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- HELPER FUNCTIONS ---

def encode_image(image_file):
    """Encodes the uploaded image to base64 for OpenAI."""
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_and_recommend(image_base64, brand, client):
    """
    1. Sends selfie to GPT-4o.
    2. Asks GPT to analyze features (skin tone, face shape).
    3. Asks GPT to generate 3 specific search queries for the Brand.
    """
    prompt = f"""
    You are a high-end fashion stylist. 
    1. Analyze the person in this selfie (gender, estimated skin tone, body build, face shape).
    2. Based on this analysis, suggest a cohesive outfit consisting of 3 distinct items (e.g., Top, Bottom, Accessory/Shoes) from the brand "{brand}".
    3. The outfit should be stylish and flatter their specific features.
    
    Return the response ONLY in JSON format with this structure:
    {{
        "analysis": "Brief analysis of the user's features and why this style suits them.",
        "items": [
            {{"query": "{brand} [specific item name and color]", "category": "Top"}},
            {{"query": "{brand} [specific item name and color]", "category": "Bottom"}},
            {{"query": "{brand} [specific item name and color]", "category": "Shoes/Accessory"}}
        ]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-5.2-2025-12-11",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
                ],
            }
        ],
        response_format={"type": "json_object"}
    )
    
    # Add error handling for None response
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("Received empty response from API. Please check your API key and quota.")
    
    print("================")
    print(content)
    print("================")
    return json.loads(content)

def search_product(query, max_retries=3):
    """Searches DuckDuckGo for the product image and link with retry logic."""
    for attempt in range(max_retries):
        try:
            # Add delay to avoid rate limiting
            if attempt > 0:
                time.sleep(2 ** attempt)  # Exponential backoff: 2s, 4s, 8s
            
            ddgs = DDGS()
            results = list(ddgs.images(query, max_results=1))
            if results:
                return results[0]  # Returns dict with 'image', 'title', 'url'
        except Exception as e:
            print(f"Search error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                # On final attempt, return None
                return None
            # Otherwise continue to retry
    return None

# --- MAIN UI ---

st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>✨ Aura & Threads</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>AI-Powered Personal Styling using GPT-4o Vision</p>", unsafe_allow_html=True)

# Sidebar for Setup
with st.sidebar:
    st.header("⚙️ Configuration")
    if st.session_state.client is None:
        api_key = st.text_input("Enter OpenAI API Key", type="password")
        if api_key:
            try:
                st.session_state.client = OpenAI(api_key=api_key)
                st.success("API Key accepted!")
            except Exception as e:
                st.error(f"Invalid API key: {e}")
    else:
        st.success("✓ OpenAI API connected")
    
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Upload a clear selfie.")
    st.markdown("2. Enter your favorite brand.")
    st.markdown("3. Let AI curate your look.")

# Main Input Area
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("Upload your Selfie", type=['jpg', 'png', 'jpeg'])
    if uploaded_file:
        st.image(uploaded_file, caption="You look great!", use_column_width=True)

with col2:
    st.markdown("### Choose your Style")
    brand_input = st.text_input("Preferred Brand (e.g., Zara, Uniqlo, Gucci)", placeholder="Type a brand name...")
    
    generate_btn = st.button("Generate Recommendations", type="primary")

# Processing Logic
if generate_btn and uploaded_file and brand_input and st.session_state.client:
    with st.spinner(f"Analyzing your features and browsing {brand_input}'s catalog..."):
        try:
            # 1. Encode Image
            base64_image = encode_image(uploaded_file)
            
            # 2. Get AI Recommendations
            ai_data = analyze_and_recommend(base64_image, brand_input, st.session_state.client)
            
            # 3. Display Analysis
            st.markdown("---")
            st.subheader("🧐 The Stylist's Take")
            st.success(ai_data["analysis"])
            
            # 4. Search and Render Items
            st.subheader(f"✨ Recommended {brand_input} Look")
            
            rec_cols = st.columns(3)
            
            for idx, item in enumerate(ai_data["items"]):
                query = item["query"]
                category = item["category"]
                
                # Search for the real item
                product_data = search_product(query)
                
                with rec_cols[idx]:
                    if product_data:
                        # Render Custom Card
                        st.markdown(f"""
                        <div class="product-card">
                            <div style="height: 200px; overflow: hidden; border-radius: 10px; margin-bottom: 10px;">
                                <img src="{product_data['image']}" class="product-img" alt="{product_data['title']}">
                            </div>
                            <div class="product-title">{category}</div>
                            <p style="font-size: 0.9em; color: #666; height: 40px; overflow: hidden;">{product_data['title'][:50]}...</p>
                            <a href="{product_data['url']}" target="_blank" class="product-link">Shop Now ↗</a>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning(f"Could not find exact match for {query}")
                        
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif generate_btn and not st.session_state.client:
    st.error("Please provide an OpenAI API Key in the sidebar.")
elif generate_btn and not uploaded_file:
    st.warning("Please upload a selfie first.")