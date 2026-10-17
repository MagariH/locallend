from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "locallend.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            owner_name TEXT NOT NULL,
            room_number TEXT NOT NULL,
            status TEXT DEFAULT 'Available',
            borrower_name TEXT DEFAULT ''
        )
    ''')
    # Alapadatok feltöltése a demóhoz
    c.execute("SELECT COUNT(*) FROM items")
    if c.fetchone()[0] == 0:
        demo_items = [
            ("Bosch Cordless Drill", "Tools", "Alex M.", "Room 304", "Available", ""),
            ("Steam Iron & Board", "Household", "Sarah K.", "Room 212", "Available", ""),
            ("Digital Multimeter", "Electronics", "Hunor M.", "Room 418", "Available", ""),
            ("Floor Bicycle Pump", "Outdoor", "David R.", "Room 105", "On Loan", "Peter T.")
        ]
        c.executemany("INSERT INTO items (title, category, owner_name, room_number, status, borrower_name) VALUES (?, ?, ?, ?, ?, ?)", demo_items)
    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LocalLend - Dorm Resource Sharing</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen">
    <!-- Navbar -->
    <header class="bg-indigo-600 text-white shadow-md">
        <div class="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid fa-handshake-angle text-2xl"></i>
                <span class="text-2xl font-bold tracking-tight">LocalLend</span>
                <span class="text-xs bg-indigo-500 text-indigo-100 px-2 py-1 rounded-full uppercase tracking-wider font-semibold">Dorm Community</span>
            </div>
            <button onclick="toggleModal()" class="bg-white text-indigo-600 font-semibold px-4 py-2 rounded-lg shadow hover:bg-indigo-50 transition">
                <i class="fa-solid fa-plus mr-1"></i> List an Item
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-6xl mx-auto px-6 py-8">
        <!-- Hero Banner -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 mb-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
                <h1 class="text-2xl font-bold text-slate-900">Need a tool? Borrow it from your hall.</h1>
                <p class="text-slate-600 text-sm mt-1">Share household tools, electronics, and study resources easily with your neighbors.</p>
            </div>
            <div class="flex gap-2">
                <span class="inline-flex items-center gap-1.5 py-1.5 px-3 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Active Dorm Hub
                </span>
            </div>
        </div>

        <!-- Items Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for item in items %}
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-semibold px-2.5 py-0.5 rounded-md 
                            {% if item[2] == 'Tools' %}bg-amber-100 text-amber-800
                            {% elif item[2] == 'Electronics' %}bg-blue-100 text-blue-800
                            {% elif item[2] == 'Household' %}bg-purple-100 text-purple-800
                            {% else %}bg-slate-100 text-slate-800{% endif %}">
                            {{ item[2] }}
                        </span>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full
                            {% if item[5] == 'Available' %}bg-emerald-100 text-emerald-700
                            {% else %}bg-rose-100 text-rose-700{% endif %}">
                            {{ item[5] }}
                        </span>
                    </div>
                    <h3 class="text-lg font-bold text-slate-900 mb-1">{{ item[1] }}</h3>
                    <p class="text-xs text-slate-500 flex items-center gap-1 mb-4">
                        <i class="fa-solid fa-location-dot text-slate-400"></i> {{ item[4] }} &bull; Owned by {{ item[3] }}
                    </p>
                </div>

                <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
                    {% if item[5] == 'Available' %}
                    <form action="/borrow/{{ item[0] }}" method="POST" class="w-full">
                        <button type="submit" class="w-full bg-indigo-50 text-indigo-700 hover:bg-indigo-600 hover:text-white font-medium py-2 rounded-lg text-sm transition text-center">
                            Request to Borrow
                        </button>
                    </form>
                    {% else %}
                    <div class="flex items-center justify-between w-full">
                        <span class="text-xs text-slate-500">Borrowed by <b>{{ item[6] }}</b></span>
                        <form action="/return/{{ item[0] }}" method="POST">
                            <button type="submit" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-md font-medium transition">
                                Mark Returned
                            </button>
                        </form>
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </main>

    <!-- Modal for Listing Item -->
    <div id="modal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-100">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold text-slate-900">List an Item to Lend</h2>
                <button onclick="toggleModal()" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <form action="/add" method="POST" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 uppercase mb-1">Item Title</label>
                    <input type="text" name="title" required placeholder="e.g. HDMI Cable, Soldering Iron" class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 uppercase mb-1">Category</label>
                    <select name="category" class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option>Tools</option>
                        <option>Electronics</option>
                        <option>Household</option>
                        <option>Academic</option>
                        <option>Outdoor</option>
                    </select>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 uppercase mb-1">Your Name</label>
                        <input type="text" name="owner_name" required placeholder="Name" class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 uppercase mb-1">Room / Floor</label>
                        <input type="text" name="room_number" required placeholder="e.g. Room 204" class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2.5 rounded-lg text-sm transition mt-2">
                    Publish Listing
                </button>
            </form>
        </div>
    </div>

    <script>
        function toggleModal() {
            document.getElementById('modal').classList.toggle('hidden');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY id DESC")
    items = c.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, items=items)

@app.route('/add', methods=['POST'])
def add_item():
    title = request.form['title']
    category = request.form['category']
    owner_name = request.form['owner_name']
    room_number = request.form['room_number']
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO items (title, category, owner_name, room_number) VALUES (?, ?, ?, ?)",
              (title, category, owner_name, room_number))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/borrow/<int:item_id>', methods=['POST'])
def borrow_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE items SET status = 'On Loan', borrower_name = 'You (Neighbor)' WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/return/<int:item_id>', methods=['POST'])
def return_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE items SET status = 'Available', borrower_name = '' WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
