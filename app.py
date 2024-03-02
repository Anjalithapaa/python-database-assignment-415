from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'host': 'Anjalithapa.mysql.pythonanywhere-services.com ',
    'user': 'Anjalithapa',
    'password': 'Iphone@@123.',
    'database': 'Anjalithapa$anjalithapa'
}

# Function to establish MySQL connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)

# Route for main page
@app.route('/')
def main_page():
    return render_template('index.html')

# Route for search operation
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get search criteria from form
        title = request.form['title']
        author = request.form['author']

        # Connect to the database
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Construct SQL query based on search criteria
            query = "SELECT * FROM Books WHERE 1"
            if title:
                query += f" AND Title LIKE '%{title}%'"
            if author:
                query += f" AND Author LIKE '%{author}%'"

            # Execute the query
            cursor.execute(query)
            results = cursor.fetchall()

            # Close database connection
            cursor.close()
            connection.close()

            return render_template('search_results.html', results=results)

    return render_template('search_form.html')

# Route for insert operation
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']

        # Connect to the database
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Check if ISBN already exists
            cursor.execute(f"SELECT COUNT(*) FROM Books WHERE ISBN = '{isbn}'")
            count = cursor.fetchone()[0]
            if count > 0:
                return "ISBN already exists. Please enter a unique ISBN."

            # Insert new record into the database
            insert_query = f"INSERT INTO Books (Title, Author, ISBN) VALUES ('{title}', '{author}', '{isbn}')"
            cursor.execute(insert_query)
            connection.commit()

            # Get updated table contents
            cursor.execute("SELECT * FROM Books")
            new_records = cursor.fetchall()

            # Close database connection
            cursor.close()
            connection.close()

            return render_template('insert_success.html', new_records=new_records)

    return render_template('insert_form.html')

if __name__ == '__main__':
    app.run(debug=True)
