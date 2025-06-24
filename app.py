from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 🧱 Initialize DB
def init_db():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 🧾 Common layout template
base_template = '''
<!DOCTYPE html>
<html>
<head>
<title>Banking App</title>
<style>
    body { font-family: Arial; background: #f2f2f2; margin: 0; }
    header { background: #004080; color: white; padding: 15px; text-align: center; }
    nav { display: flex; background: #e0e0e0; justify-content: space-around; padding: 10px; }
    nav a { text-decoration: none; color: #004080; font-weight: bold; }
    section { padding: 20px; background: white; margin: 20px; border-radius: 5px; }
    input, button { padding: 8px; margin: 5px; width: 250px; }
    table { border-collapse: collapse; width: 100%; margin-top: 15px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
</style>
</head>
<body>
<header><h2>🏦 Banking Application</h2></header>
<nav>
<a href="/create">Create Account</a>
<a href="/balance">Check Balance</a>
<a href="/deposit">Deposit</a>
<a href="/withdraw">Withdraw</a>
<a href="/statement">Statement</a>
</nav>
<section>
  {{ content | safe }}
</section>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(base_template, content="<h3>Welcome to the Banking App</h3>")

# 👤 Create Account
@app.route('/create', methods=['GET', 'POST'])
def create():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        balance = float(request.form['balance'])
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
        conn.commit()
        conn.close()
        msg = f"Account for {name} created successfully with ₹{balance:.2f}"
    form = '''
<h3>Create Account</h3>
<form method="post">
            Name: <input type="text" name="name" required><br>
            Initial Balance: <input type="number" name="balance" required><br>
<button type="submit">Create</button>
</form>
<p>{}</p>
    '''.format(msg)
    return render_template_string(base_template, content=form)

# 💰 Check Balance
@app.route('/balance', methods=['GET', 'POST'])
def balance():
    msg = ''
    if request.method == 'POST':
        account_id = request.form['account_id']
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT name, balance FROM accounts WHERE id=?", (account_id,))
        row = c.fetchone()
        conn.close()
        if row:
            msg = f"Account: {row[0]} | Balance: ₹{row[1]:.2f}"
        else:
            msg = "Account not found."
    form = '''
<h3>Check Balance</h3>
<form method="post">
            Account ID: <input type="number" name="account_id" required><br>
<button type="submit">Check</button>
</form>
<p>{}</p>
    '''.format(msg)
    return render_template_string(base_template, content=form)

# 💵 Deposit
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    msg = ''
    if request.method == 'POST':
        account_id = request.form['account_id']
        amount = float(request.form['amount'])
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        if c.rowcount == 0:
            msg = "Account not found."
        else:
            msg = f"₹{amount:.2f} deposited successfully."
            # Record transaction
            c.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)",
                     (account_id, 'deposit', amount))
        conn.commit()
        conn.close()
    form = '''
<h3>Deposit Amount</h3>
<form method="post">
            Account ID: <input type="number" name="account_id" required><br>
            Amount: <input type="number" name="amount" required><br>
<button type="submit">Deposit</button>
</form>
<p>{}</p>
    '''.format(msg)
    return render_template_string(base_template, content=form)

# 💸 Withdraw
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    msg = ''
    if request.method == 'POST':
        account_id = request.form['account_id']
        amount = float(request.form['amount'])
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        row = c.fetchone()
        if not row:
            msg = "Account not found."
        elif row[0] < amount:
            msg = "Insufficient balance."
        else:
            c.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
            # Record transaction
            c.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)",
                     (account_id, 'withdraw', amount))
            conn.commit()
            msg = f"₹{amount:.2f} withdrawn successfully."
        conn.close()
    form = '''
<h3>Withdraw Amount</h3>
<form method="post">
            Account ID: <input type="number" name="account_id" required><br>
            Amount: <input type="number" name="amount" required><br>
<button type="submit">Withdraw</button>
</form>
<p>{}</p>
    '''.format(msg)
    return render_template_string(base_template, content=form)

# 📄 Statement
@app.route('/statement', methods=['GET', 'POST'])
def statement():
    msg = ''
    transactions = []
    if request.method == 'POST':
        account_id = request.form['account_id']
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # Get account name
        c.execute("SELECT name FROM accounts WHERE id=?", (account_id,))
        account_row = c.fetchone()
        
        if account_row:
            account_name = account_row[0]
            # Get transactions
            c.execute("SELECT type, amount, timestamp FROM transactions WHERE account_id=? ORDER BY timestamp DESC", 
                     (account_id,))
            transactions = c.fetchall()
            msg = f"Statement for {account_name} (ID: {account_id})"
        else:
            msg = "Account not found."
        conn.close()

    form = '''
<h3>Check Statement</h3>
<form method="post">
            Account ID: <input type="number" name="account_id" required><br>
<button type="submit">View Statement</button>
</form>
<p>{}</p>
'''.format(msg)

    # Display transactions if available
    if transactions:
        form += '''
<table>
    <tr>
        <th>Type</th>
        <th>Amount (₹)</th>
        <th>Timestamp</th>
    </tr>
'''
        for t in transactions:
            form += f'''
    <tr>
        <td>{t[0].capitalize()}</td>
        <td>{t[1]:.2f}</td>
        <td>{t[2]}</td>
    </tr>
'''
        form += '</table>'
    
    return render_template_string(base_template, content=form)

# ▶️ Run App
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5006)
