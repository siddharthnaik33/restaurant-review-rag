import streamlit as st
from tools import review_retriever

st.set_page_config(
    page_title="Restaurant Review Search",
    page_icon="🍽️",
    layout="wide"
)

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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍽️ Restaurant Review Search Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Agentic RAG based semantic search system using CSV, ChromaDB, Sentence Transformers and LangChain</div>',
    unsafe_allow_html=True
)

st.write("")

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
st.sidebar.write("Python")
st.sidebar.write("Streamlit")
st.sidebar.write("ChromaDB")
st.sidebar.write("Sentence Transformers")
st.sidebar.write("LangChain")

st.subheader("🔎 Ask your restaurant review question")

query = st.text_input(
    "Enter your query",
    placeholder="Example: Which restaurant serves the best biryani in Hyderabad?"
)

search_button = st.button("🔍 Search Reviews", use_container_width=True)

if search_button:
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching relevant restaurant reviews..."):
            result = review_retriever.invoke(query)

        st.success("Search completed!")

        st.markdown("""
        <div class="card">
            <h3>📌 Search Results</h3>
        </div>
        """, unsafe_allow_html=True)

        st.text_area(
            "Retrieved Reviews",
            value=result,
            height=350
        )

st.divider()

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

st.subheader("🧩 How this system works")

st.markdown("""
1. Restaurant reviews are loaded from a CSV file.
2. Missing values and duplicate reviews are cleaned.
3. Review text is converted into embeddings using Sentence Transformers.
4. Embeddings and metadata are stored in ChromaDB.
5. User enters a natural language question.
6. ChromaDB retrieves semantically similar reviews.
7. The assistant displays relevant restaurant review results.
""")

st.divider()

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

st.caption("Built using Python, Streamlit, ChromaDB, Sentence Transformers and LangChain.")