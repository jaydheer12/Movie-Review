import streamlit as st
import csv
import os

# ------------------ PAGE CONFIG (LIGHT MODE) ------------------
st.set_page_config(
    page_title="Movie Review App",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Force light mode
st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ TITLE ------------------
st.title("🎬 Movie Review Application")
st.write("Collecting reviews from students")

# ------------------ INPUTS ------------------
name = st.text_input("Student Name")
roll_no = st.text_input("Roll Number")

movies = (
    "RRR",
    "Baahubali",
    "Pushpa",
    "Ala Vaikunthapurramuloo",
    "Arjun Reddy"
)

movie = st.selectbox("Select Movie", movies)
review = st.text_area("Write Your Review")
rating = st.slider("Give Rating", 1, 5)

# ------------------ FILE SETUP ------------------
FILE_NAME = "reviews.csv"

def save_review(data):
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Roll No", "Movie", "Review", "Rating"])
        writer.writerow(data)

# ------------------ SUBMIT BUTTON ------------------
if st.button("Submit Review"):
    if name and roll_no and review:
        review_data = (name, roll_no, movie, review, rating)
        save_review(review_data)

        st.success("✅ Review Submitted Successfully!")
    else:
        st.error("❌ Please fill all details")

# ------------------ SHOW ALL REVIEWS ------------------
st.subheader("📋 All Reviews")

if os.path.isfile(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        if len(reader) > 1:
            for row in reader[1:]:
                st.write(
                    f"**{row[0]}** (Roll No: {row[1]})  \n"
                    f"🎥 Movie: {row[2]}  \n"
                    f"📝 Review: {row[3]}  \n"
                    f"⭐ Rating: {row[4]}"
                )
                st.divider()
        else:
            st.info("No reviews yet.")
else:
    st.info("No reviews yet.")

# ------------------ SUMMARY ------------------
st.subheader("📊 Overall Summary")

if os.path.isfile(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        if len(reader) > 1:
            ratings = [int(row[4]) for row in reader[1:]]
            avg_rating = sum(ratings) / len(ratings)

            st.success(f"⭐ Average Rating: {avg_rating:.2f}")
            st.info(f"👥 Total Students Reviewed: {len(ratings)}")
