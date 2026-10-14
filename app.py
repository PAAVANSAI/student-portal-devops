"""
Student Portal — Flask Application

A simple Flask web application that serves a Student Portal homepage
and exposes a /health endpoint for container health checks.
"""

from flask import Flask, render_template, jsonify

app = Flask(__name__)

# -------------------------------------------------------------------
# Sample student data (in a real project this would come from a DB)
# -------------------------------------------------------------------
STUDENTS = [
    {"id": "STU001", "name": "Alice Johnson", "course": "Computer Science"},
    {"id": "STU002", "name": "Bob Williams", "course": "Data Science"},
    {"id": "STU003", "name": "Charlie Davis", "course": "Cybersecurity"},
    {"id": "STU004", "name": "Diana Martinez", "course": "Cloud Computing"},
    {"id": "STU005", "name": "Ethan Brown", "course": "Software Engineering"},
]


@app.route("/")
def index():
    """Render the Student Portal homepage."""
    return render_template("index.html", students=STUDENTS)


@app.route("/health")
def health():
    """Health-check endpoint — returns HTTP 200 with JSON status."""
    return jsonify({"status": "healthy"}), 200


# -------------------------------------------------------------------
# Local development entry-point (not used in production / Docker)
# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
