import sqlite3
from flask import Flask, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users VALUES ('admin', '12345')")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        mode = request.form.get("mode", "safe")
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        if mode == "unsafe":
            # Vulnerable string concatenation (Lab demonstration only)
            query = f"SELECT * FROM users WHERE username = '{u}' AND password = '{p}'"
            cur.execute(query)
        else:
            # Safe parameterized query
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (u, p))
        row = cur.fetchone()
        conn.close()
        msg = "Login Successful!" if row else "Invalid Credentials"
    return f'''
    <h2>SQLite Login (Parameterized vs Concatenated)</h2>
    <form method="POST">
      Username: <input name="username"><br><br>
      Password: <input name="password" type="password"><br><br>
      Mode:
      <select name="mode">
        <option value="safe">Parameterized (Safe)</option>
        <option value="unsafe">Concatenated (Vulnerable)</option>
      </select><br><br>
      <button type="submit">Login</button>
    </form>
    <p><b>{msg}</b></p>
    '''

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
