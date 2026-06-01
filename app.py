from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    conn = sqlite3.connect("threats.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM threats")
    total_threats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM threats WHERE type='IP'")
    total_ips = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM threats WHERE type='Domain'")
    total_domains = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM threats WHERE type='Hash'")
    total_hashes = cursor.fetchone()[0]

    if request.method == "POST":
        indicator = request.form["indicator"]

        cursor.execute(
            "SELECT * FROM threats WHERE indicator=?",
            (indicator,)
        )

        result = cursor.fetchone()

    conn.close()

    return render_template(
        "index.html",
        result=result,
        total_threats=total_threats,
        total_ips=total_ips,
        total_domains=total_domains,
        total_hashes=total_hashes
    )

if __name__ == "__main__":
    app.run(debug=True)