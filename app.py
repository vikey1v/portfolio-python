
from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage
import sqlite3

app = Flask(__name__)

# EMAIL CONFIG
EMAIL_ADDRESS = "yourgmail@gmail.com"
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"

# DATABASE INIT
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    # SAVE TO DATABASE
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
              (name, email, message))
    conn.commit()
    conn.close()

    # SEND EMAIL
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage:\n{message}")
    msg["Subject"] = "New Portfolio Contact"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").lower()

    replies = {
        "hi": "Hello 👋 I’m Vickey’s assistant. How can I help you?",
        "hello": "Hi there 👋 How can I help you today?",
        "services": "I offer Web Design, Python Backend, SEO, and Freelancing services.",
        "contact": "You can contact me using the form on this website or email vickey.dev@gmail.com",
        "price": "Pricing depends on the project. Please send a message using the contact form.",
        "technology": "I use HTML, CSS, JavaScript, Python, and Flask."
    }

    reply = "Thanks for your message 😊 Please contact me using the form."

    for key in replies:
        if key in user_msg:
            reply = replies[key]
            break

    # SAVE CHAT TO DATABASE
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_logs (user_message, bot_reply) VALUES (?, ?)",
        (user_msg, reply)
    )
    conn.commit()
    conn.close()

    return {"reply": reply}
