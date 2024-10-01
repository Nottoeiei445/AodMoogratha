# app.py

from flask import Flask, render_template_string, request, redirect, url_for, flash
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bookTable import BookTable

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # ควรเปลี่ยนเป็นคีย์ที่ปลอดภัยจริงๆ

# Initialize the BookTable instance with 5 tables
dll = BookTable(5)

# HTML Template
template = """
<!doctype html>
<html lang="en">
<head>
    <title>Restaurant Table Booking</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 50%; margin-bottom: 30px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
        .form-container { margin-bottom: 30px; }
        .form-container form { display: inline-block; margin-right: 20px; }
        .message { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Restaurant Table Booking System</h1>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <p class="{{ category }}">{{ message }}</p>
        {% endfor %}
      {% endif %}
    {% endwith %}
    
    <h2>Filter Tables</h2>
    <form method="get" action="{{ url_for('index') }}">
        <label for="filter">Show:</label>
        <select name="filter" id="filter">
            <option value="all" {% if selected_filter == 'all' %}selected{% endif %}>All Tables</option>
            <option value="booked" {% if selected_filter == 'booked' %}selected{% endif %}>Booked Tables</option>
            <option value="unbooked" {% if selected_filter == 'unbooked' %}selected{% endif %}>Unbooked Tables</option>
        </select>
        <button type="submit">Filter</button>
    </form>
    
    <h2>Current Table Status</h2>
    <table>
        <tr>
            <th>Table Number</th>
            <th>Number of Customers</th>
            <th>Status</th>
        </tr>
        {% for table in tables %}
        <tr>
            <td>{{ table.tableNum }}</td>
            <td>{{ table.customerNum }}</td>
            <td>
                {% if table.status %}
                    Booked
                {% else %}
                    Available
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>

    <div class="form-container">
        <h2>Book a Table</h2>
        <form action="{{ url_for('book') }}" method="post">
            <label for="book_table">Table Number:</label>
            <input type="number" id="book_table" name="table" min="1" required>
            <br><br>
            <label for="customers">Number of Customers:</label>
            <input type="number" id="customers" name="customer" min="1" required>
            <br><br>
            <button type="submit">Book Table</button>
        </form>
    </div>

    <div class="form-container">
        <h2>Clear a Table</h2>
        <form action="{{ url_for('clear') }}" method="post">
            <label for="clear_table">Table Number:</label>
            <input type="number" id="clear_table" name="table" min="1" required>
            <br><br>
            <button type="submit">Clear Table</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    selected_filter = request.args.get('filter', 'all')
    
    if selected_filter == 'booked':
        tables = dll.displayBooked()
    elif selected_filter == 'unbooked':
        tables = dll.displayUnBooked()
    else:
        tables = dll.display()
    
    return render_template_string(template, tables=tables, selected_filter=selected_filter)

@app.route('/book', methods=['POST'])
def book():
    try:
        table = int(request.form['table'])
        customer = int(request.form['customer'])
        if customer < 1:
            flash("Number of customers must be at least 1.", "error")
            return redirect(url_for('index'))
        result = dll.book_table(table, customer)
        if "successfully" in result:
            flash(result, "message")
        else:
            flash(result, "error")
    except ValueError:
        flash("Invalid input. Please enter valid numbers.", "error")
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    try:
        table = int(request.form['table'])
        result = dll.clear_table(table)
        if "cleared" in result:
            flash(result, "message")
        else:
            flash(result, "error")
    except ValueError:
        flash("Invalid input. Please enter a valid table number.", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)