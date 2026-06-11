import streamlit as st
from tools import review_retriever

st.set_page_config(
    page_title="Restaurant Review Search",
    page_icon="🍽️",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
.main-title {
    font-size: 45px;
    font-weight: 800;
    color: #ff4b4b;
    text-align: center;
}
.sub-title {
    font-size: 20px;
    text-align: center;
    color: #555;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #fff3e6;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.metric-card {
    padding: 18px;
    border-radius: 12px;
    background-color: #f9f9f9;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}
.restaurant-card {
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    background-color: #ffffff;
    border-left: 7px solid #ff4b4b;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.12);
}
.restaurant-name {
    font-size: 24px;
    font-weight: 700;
    color: #ff4b4b;
}
.review-text {
    font-size: 16px;
    color: #333;
}
.footer {
    text-align: center;
    color: #666;
}
</style>
""", unsafe_allow_html=True)


# ---------- HELPER FUNCTIONS ----------
def get_stars(rating):
    full = int(float(rating))
    half = float(rating) - full >= 0.5
    stars = "⭐" * full
    if half:
        stars += "✨"
    return stars


def extract_field(text, field_name):
    for line in text.split("\n"):
        if line.strip().startswith(field_name):
            return line.split(":", 1)[1].strip()
    return "N/A"


def show_restaurant_card(restaurant):
    name = extract_field(restaurant, "Restaurant Name")
    city = extract_field(restaurant, "City")
    food_type = extract_field(restaurant, "Food Type")
    rating = extract_field(restaurant, "Rating")
    review_date = extract_field(restaurant, "Review Date")
    customer = extract_field(restaurant, "Customer Name")
    review = extract_field(restaurant, "Review Text")

    stars = get_stars(rating) if rating != "N/A" else ""

    st.markdown(
        f"""
        <div class="restaurant-card">
            <div class="restaurant-name">🍽️ {name}</div>
            <h4>{stars} &nbsp; {rating}/5</h4>
            <p><b>📍 City:</b> {city}</p>
            <p><b>🍲 Food Type:</b> {food_type}</p>
            <p><b>📅 Review Date:</b> {review_date}</p>
            <p><b>👤 Customer:</b> {customer}</p>
            <p class="review-text"><b>💬 Review:</b> {review}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- HERO IMAGE ----------
st.image(
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
    use_container_width=True
)

# ---------- TITLE ----------
st.markdown(
    '<div class="main-title">🍽️ Restaurant Review Search Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Agentic RAG based semantic search system using CSV, ChromaDB, Sentence Transformers and LangChain</div>',
    unsafe_allow_html=True
)

st.write("")

# ---------- ILLUSTRATION ----------
left, center, right = st.columns([2, 1, 2])
with center:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
        width=120
    )

# ---------- DASHBOARD METRICS ----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Restaurants", "30")
col2.metric("Cities", "3")
col3.metric("Food Categories", "8")
col4.metric("Reviews", "30")

st.divider()

# ---------- FEATURE CARDS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📄 CSV Data</h3>
        <p>Loads restaurant reviews from CSV files</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>🧠 Vector DB</h3>
        <p>Stores review embeddings in ChromaDB</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>🔍 Semantic Search</h3>
        <p>Search reviews using natural language</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Search Settings")

top_k = st.sidebar.slider(
    "Number of results",
    min_value=1,
    max_value=10,
    value=5
)

st.sidebar.info("""
This assistant retrieves restaurant reviews using semantic similarity.

You can ask about:
- Food quality
- Service
- Ambience
- Ratings
- City
- Food type
- Restaurant comparison
""")

st.sidebar.subheader("📌 Tech Stack")
st.sidebar.write("🐍 Python")
st.sidebar.write("🎈 Streamlit")
st.sidebar.write("🧠 ChromaDB")
st.sidebar.write("🔤 Sentence Transformers")
st.sidebar.write("🦜 LangChain")

# ---------- SEARCH SECTION ----------
st.subheader("🔎 Ask your restaurant review question")

query = st.text_input(
    "Enter your query",
    placeholder="Example: Which restaurant serves the best biryani in Hyderabad?"
)

search_button =st.button("🔍 Search Reviews", width="stretch") 
#st.button("🔍 Search Reviews", use_container_width=True)


if search_button:
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching relevant restaurant reviews..."):
            result = review_retriever.invoke(query)

        st.success("Search completed!")

        st.subheader("📌 Search Results")

        restaurants = result.strip().split("\n\n\n")

        for restaurant in restaurants:
            if "Restaurant Name:" in restaurant and "Rating:" in restaurant:
                show_restaurant_card(restaurant)

st.divider()

# ---------- SAMPLE QUESTIONS ----------
st.subheader("💡 Try these sample questions")

q1, q2 = st.columns(2)

with q1:
    st.markdown("""
    - Which restaurant serves the best biryani in Hyderabad?
    - Why do customers like Paradise restaurant?
    - Find restaurants with poor service reviews.
    - Suggest Italian restaurants with ratings above 4.
    - Which cafes have good ambience?
    """)

with q2:
    st.markdown("""
    - Compare Paradise and Bawarchi.
    - Find highly rated restaurants in Hyderabad.
    - Which restaurant has excellent service?
    - Suggest family-friendly restaurants.
    - What are common complaints from customers?
    """)

st.divider()

# ---------- FOOD IMAGES ----------
st.subheader("🍽 Popular Food Categories")

c1, c2, c3 = st.columns(3)

with c1:
    st.image(
        "https://images.pexels.com/photos/12737656/pexels-photo-12737656.jpeg",
        caption="Hyderabadi Biryani",
        width="stretch"
    )
with c2:
    st.image(
        "https://images.unsplash.com/photo-1513104890138-7c749659a591",
        caption="Pizza",
        use_container_width=True
    )

with c3:
    st.image(
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
        caption="Cafe",
        use_container_width=True
    )

st.divider()

# ---------- WORKFLOW ----------
st.subheader("🧩 How this system works")

st.markdown("""
1. Restaurant reviews are loaded from a CSV file.
2. Missing values and duplicate reviews are cleaned.
3. Review text is converted into embeddings using Sentence Transformers.
4. Embeddings and metadata are stored in ChromaDB.
5. User enters a natural language question.
6. ChromaDB retrieves semantically similar reviews.
7. Results are displayed as restaurant cards with ratings.
""")

st.divider()

# ---------- PROJECT FEATURES ----------
st.subheader("📊 Project Features")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.info("✅ CSV Data Ingestion")

with feature_col2:
    st.info("✅ ChromaDB Vector Storage")

with feature_col3:
    st.info("✅ Semantic Review Search")

feature_col4, feature_col5, feature_col6 = st.columns(3)

with feature_col4:
    st.info("✅ Metadata Support")

with feature_col5:
    st.info("✅ Natural Language Querying")

with feature_col6:
    st.info("✅ LangChain Tool Integration")

st.divider()

# ---------- FOOTER ----------
st.markdown(
    """
    <div class="footer">
        <h4>🍽 Restaurant Review Search System</h4>
        <p>Built with Streamlit • ChromaDB • LangChain • Sentence Transformers</p>
    </div>
    """,
    unsafe_allow_html=True
)