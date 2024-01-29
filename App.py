import mysql.connector
import streamlit as st
st.set_page_config("CURD")
# Function to create a record in the database
def create_record(conn, id, name, gender, city):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO HUI (id, name, gender, city) VALUES (%s, %s, %s, %s)", (id, name, gender, city))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        st.error(f"Error creating record: {e}")
        return False

# Function to read a record from the database
def read_record(conn, id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM HUI WHERE id = %s", (id,))
        record = cursor.fetchone()
        if record:
            return record
        else:
            st.warning("Record not found.")
            return None
    except mysql.connector.Error as e:
        st.error(f"Error reading record: {e}")
        return None

# Function to update a record in the database
def update_record(conn, id, name, gender, city):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE HUI SET name = %s, gender = %s, city = %s WHERE id = %s", (name, gender, city, id))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        st.error(f"Error updating record: {e}")
        return False

# Function to delete a record from the database
def delete_record(conn, id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM HUI WHERE id = %s", (id,))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        st.error(f"Error deleting record: {e}")
        return False

# Establish database connection
try:
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='db'
    )
    if con.is_connected():
        st.success("Connected to MySQL database!")
except mysql.connector.Error as e:
    st.error(f"Error connecting to MySQL database: {e}")

# Streamlit UI

st.header("Create-Update-Read-Delete")

# Button for CRUD operations
operation = st.radio("Select operation:", ('Create', 'Read', 'Update', 'Delete'))

if operation == 'Create':
    id = st.text_input("ID")
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])
    city = st.text_input("City")
    create = st.button("Create")
    if create:
        if id and name and gender and city:
            success = create_record(con, id, name, gender, city)
            if success:
                st.success("Record created successfully!")
            else:
                st.error("Failed to create record. Please check the inputs.")
        else:
            st.warning("Please fill in all the fields.")

elif operation == 'Read':
    id = st.text_input("Enter record ID to read:")
    read = st.button("Read")
    if read:
        if id:
            record = read_record(con, id)
            if record:
                st.write(f"Record ID: {record[0]}")
                st.write(f"Name: {record[1]}")
                st.write(f"Gender: {record[2]}")
                st.write(f"City: {record[3]}")
        else:
            st.warning("Please enter a record ID.")

elif operation == 'Update':
    id = st.text_input("Enter record ID to update:")
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])
    city = st.text_input("City")
    update = st.button("Update")
    if update:
        if id and name and gender and city:
            success = update_record(con, id, name, gender, city)
            if success:
                st.success("Record updated successfully!")
            else:
                st.error("Failed to update record. Please check the inputs.")
        else:
            st.warning("Please fill in all the fields.")

elif operation == 'Delete':
    id = st.text_input("Enter record ID to delete:")
    delete = st.button("Delete")
    if delete:
        if id:
            success = delete_record(con, id)
            if success:
                st.success("Record deleted successfully!")
            else:
                st.error("Failed to delete record. Please check the inputs.")
        else:
            st.warning("Please enter a record ID.")
