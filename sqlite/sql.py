import sqlite3
import streamlit as st

# Connect to database
conn = sqlite3.connect("STUDENT.db")
st.markdown(f"#  :green[COLLEGE LOGIN FORM]")

# Create table
conn.execute('''
    CREATE TABLE IF NOT EXISTS COLLEGE (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(100) NOT NULL,
    ROLL_NO VARCHAR(20) NOT NULL UNIQUE,
    AGE INTEGER NOT NULL
    CHECK (AGE > 0 AND AGE < 100),
    CITY VARCHAR(100) NOT NULL
)
''')

# Input fields
a= st.number_input("ENTER YOUR ROLL NO")
b = st.text_input("ENTER YOUR NAME")
c=st.number_input("ENTER THE ROLL NO")
d=st.number_input("ENTER YOUR AGE", min_value=1, max_value=100)
e = st.text_input("ENTER THE CITY")
try:
# Submit button
    if st.button("SUBMIT"):
       if a and b and c and d and e:
          conn.execute("INSERT INTO COLLEGE (ID,NAME, ROLL_NO,AGE,CITY) VALUES (?, ?,?,?,?)", (a, b, c, d, e))
          conn.commit()
          st.success("Data inserted successfully")
       else:
        st.warning("Please fill all fields")

except:
    st.error("An error occurred while inserting data. Please check your inputs.")
finally:
    conn.close()
