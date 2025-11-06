import streamlit as st
import sqlite3

# 🔗 Connect to SQLite database
conn = sqlite3.connect('directory.db', check_same_thread=False)
cursor = conn.cursor()

# 📜 Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        comments TEXT
    )
''')
conn.commit()

# 🎨 Streamlit UI
st.title("📇 Personal Directory")
st.subheader("Add New Contact")

# 🧾 Input fields
name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
comments = st.text_area("Comments")

# 💾 Save to database
if st.button("Save Contact"):
    if name and email and phone:
        cursor.execute("INSERT INTO contacts (name, email, phone, comments) VALUES (?, ?, ?, ?)",
                       (name, email, phone, comments))
        conn.commit()
        st.success("✅ Contact saved successfully!")
    else:
        st.warning("⚠️ Name, Email, and Phone are required.")

# 📂 View stored contacts with pagination
st.subheader("📜 Stored Contacts")

# 🔍 Get total number of contacts
cursor.execute("SELECT COUNT(*) FROM contacts")
total_contacts = cursor.fetchone()[0]
contacts_per_page = 10
total_pages = (total_contacts - 1) // contacts_per_page + 1

# 📄 Page selector
page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

# 🧮 Calculate offset
offset = (page_number - 1) * contacts_per_page

# 📥 Fetch paginated contacts sorted by name
cursor.execute("""
    SELECT name, email, phone, comments
    FROM contacts
    ORDER BY name ASC
    LIMIT ? OFFSET ?
""", (contacts_per_page, offset))
rows = cursor.fetchall()

# 🖥️ Display contacts
for row in rows:
    st.markdown(f"**Name:** {row[0]}")
    st.markdown(f"📧 **Email:** {row[1]}")
    st.markdown(f"📞 **Phone:** {row[2]}")
    st.markdown(f"📝 **Comments:** {row[3]}")
    st.markdown("---")

st.caption(f"Showing page {page_number} of {total_pages} ({total_contacts} total contacts)")