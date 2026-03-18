"""Flask web application for DevOps CI/CD demo."""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract b from a."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide a by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    """Handle calculation requests from the UI."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided."}), 400

    try:
        a = float(data.get("a", 0))
        b = float(data.get("b", 0))
        operation = data.get("operation", "")
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid numbers provided."}), 400

    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    if operation not in operations:
        return jsonify({"error": f"Unknown operation: {operation}"}), 400

    try:
        result = operations[operation](a, b)
        return jsonify({"result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
