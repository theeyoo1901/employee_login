from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

# ----- Mock data (in-memory) -----
USER = {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "joined": "2024-02-10",
    "bio": "Full-stack tinkerer"
}

NOTIFICATIONS = [
    {"id": 1, "text": "Order #1001 has shipped", "read": False},
    {"id": 2, "text": "New discount: 15% off electronics", "read": False},
    {"id": 3, "text": "Password changed successfully", "read": True},
]

ORDERS = [
    {"id": 1001, "item": "Wireless Mouse", "date": "2025-09-10", "status": "Shipped"},
    {"id": 1002, "item": "Mechanical Keyboard", "date": "2025-09-12", "status": "Processing"},
    {"id": 1003, "item": "USB-C Hub", "date": "2025-08-29", "status": "Delivered"},
]

# ----- Routes -----
@app.route("/")
def home():
    unread_count = sum(1 for n in NOTIFICATIONS if not n["read"])
    recent_orders = ORDERS[:3]
    return render_template("home.html", user=USER, unread_count=unread_count, recent_orders=recent_orders)

@app.route("/notifications")
def notifications():
    return render_template("notifications.html", notifications=NOTIFICATIONS)

@app.route("/notifications/mark_read", methods=["POST"])
def mark_notification_read():
    data = request.get_json() or {}
    nid = data.get("id")
    if nid is None:
        return jsonify({"error": "id required"}), 400
    for n in NOTIFICATIONS:
        if n["id"] == nid:
            n["read"] = True
            return jsonify({"ok": True})
    return jsonify({"error": "notification not found"}), 404

@app.route("/orders")
def orders():
    return render_template("orders.html", orders=ORDERS)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        bio = request.form.get("bio", "").strip()
        if name:
            USER["name"] = name
        if email:
            USER["email"] = email
        USER["bio"] = bio
        return redirect(url_for("profile"))
    return render_template("profile.html", user=USER)

@app.route("/api/unread_count")
def api_unread_count():
    return jsonify({"unread": sum(1 for n in NOTIFICATIONS if not n["read"])})

if __name__ == "__main__":
    app.run(debug=True)
