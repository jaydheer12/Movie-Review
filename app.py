import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Review Portal",
    page_icon="🎬",
    layout="centered"
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("reviews.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    suc_id TEXT,
    section TEXT,
    department TEXT,
    movie TEXT,
    rating REAL,
    review_text TEXT
)
""")
conn.commit()

# ---------------- SESSION STATE ----------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None  # stores ID to confirm deletion
if "refresh" not in st.session_state:
    st.session_state.refresh = False

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #0f172a; }
h1, h2, h3 { color: #38bdf8; text-align: center; }

.review-box {
    background-color: #020617;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0px;
}

.best-review {
    border: 2px solid gold;
    background-color: #1a1a2e;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #38bdf8;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TABS ----------------
tab_user, tab_admin = st.tabs(["👤 User Review", "🛠 Admin Dashboard"])

# ================= USER REVIEW =================
with tab_user:
    st.title("🎬 Movie Review Portal")
    st.subheader("Submit Your Review")

    name = st.text_input("Enter Your Name")
    suc_id = st.text_input("Enter Your SUC ID")
    section = st.text_input("Enter Your Section")
    department = st.text_input("Enter Your Department")

    movie = st.selectbox(
        "Choose a Movie",
        ["Salaar", "SVSC", "Guntur Karam", "Kalki 2898 AD", "OG"]
    )

    rating = st.slider("Give Rating (0 to 5 ⭐)", 0.0, 5.0, step=0.5)
    review_text = st.text_area("✍ Write your review")

    if st.button("Submit Review"):
        if not name.strip() or not review_text.strip():
            st.warning("⚠️ Name and Review are required")
        else:
            cursor.execute("""
                INSERT INTO reviews
                (name, suc_id, section, department, movie, rating, review_text)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, suc_id, section, department, movie, rating, review_text))
            conn.commit()
            st.session_state.submitted = True
            st.session_state.refresh = not st.session_state.refresh

    if st.session_state.submitted:
        st.success("✅ Review submitted successfully!")

# ================= ADMIN DASHBOARD =================
with tab_admin:
    st.title("🛠 Admin Dashboard")
    df_all = pd.read_sql_query("SELECT * FROM reviews ORDER BY id ASC", conn)

    if df_all.empty:
        st.info("No reviews available")
    else:
        df_users = df_all.copy()
        df_users.insert(0, "Users", range(1, len(df_users) + 1))
        df_users = df_users.drop(columns=["id"])

        st.subheader("📋 All Reviews")
        st.dataframe(df_users, use_container_width=True)

        st.subheader("👥 Users Reviewed")
        st.metric("Total Users Reviewed", len(df_users))

        st.subheader("🏆 Best Review")
        best_review = df_all.sort_values(by=["rating", "id"], ascending=[False, False]).iloc[0]
        st.markdown(f"""
        <div class="review-box best-review">
            <b>Name:</b> {best_review['name']}<br>
            <b>SUC:</b> {best_review['suc_id']} | <b>Section:</b> {best_review['section']}<br>
            <b>Movie:</b> {best_review['movie']}<br>
            ⭐ Rating: {best_review['rating']} / 5<br><br>
            {best_review['review_text']}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📊 Overall Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reviews", len(df_all))
        col2.metric("Average Rating", f"{round(df_all['rating'].mean(), 2)} ⭐")
        col3.metric("Best Movie", df_all.groupby("movie")["rating"].mean().idxmax())

        st.subheader("📈 Movie-wise Ratings")
        st.bar_chart(df_all.groupby("movie")["rating"].mean())

        st.subheader("📝 All Written Reviews")
        for idx, row in df_all.reset_index(drop=True).iterrows():
            user_number = idx + 1
            st.markdown(f"""
            <div class="review-box">
                <b>User:</b> {user_number}<br>
                <b>Name:</b> {row['name']} | <b>SUC:</b> {row['suc_id']} | <b>Section:</b> {row['section']}<br>
                <b>Movie:</b> {row['movie']}<br>
                ⭐ Rating: {row['rating']} / 5<br><br>
                {row['review_text']}
            </div>
            """, unsafe_allow_html=True)

            # Step 1: Click Remove -> mark for confirmation
            remove_key = f"remove_{row['id']}"
            if st.session_state.confirm_delete == row["id"]:
                st.warning("⚠️ Are you sure you want to delete this user?")
                if st.button("Confirm Delete", key=f"confirm_{row['id']}"):
                    cursor.execute("DELETE FROM reviews WHERE id=?", (row["id"],))
                    conn.commit()
                    st.success(f"✅ User {user_number} removed successfully!")
                    st.session_state.confirm_delete = None
                    st.experimental_rerun = None
                    st.session_state.refresh = not st.session_state.refresh
                if st.button("Cancel", key=f"cancel_{row['id']}"):
                    st.session_state.confirm_delete = None
            else:
                if st.button(f"Remove User {user_number}", key=remove_key):
                    st.session_state.confirm_delete = row["id"]
