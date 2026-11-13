"""
Campus Lab Resources Management REST API
A lightweight microservice to manage and track campus laboratory equipment
(GPU servers, 3D printers, oscilloscopes, network switches, IoT kits).
"""

import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configurable environment settings (can be overridden by Kubernetes ConfigMap / Env Vars)
APP_PORT = int(os.environ.get("APP_PORT", 5000))
APP_ENV = os.environ.get("APP_ENV", "development")
CAMPUS_NAME = os.environ.get("CAMPUS_NAME", "Main Engineering Campus")

# In-memory database of laboratory resources
RESOURCES = [
    {
        "id": 1,
        "name": "NVIDIA RTX 4090 Workstation",
        "lab": "AI & Deep Learning Lab",
        "type": "Compute",
        "status": "Available",
        "allocated_to": None
    },
    {
        "id": 2,
        "name": "Ultimaker S5 3D Printer",
        "lab": "Prototyping & Robotics Lab",
        "type": "Hardware",
        "status": "In-Use",
        "allocated_to": "Student-21BCS104"
    },
    {
        "id": 3,
        "name": "Keysight Digital Storage Oscilloscope",
        "lab": "VLSI & Embedded Systems Lab",
        "type": "Testing Equipment",
        "status": "Available",
        "allocated_to": None
    },
    {
        "id": 4,
        "name": "Cisco Catalyst 9300 Switch Rack",
        "lab": "Advanced Computer Networks Lab",
        "type": "Networking",
        "status": "Maintenance",
        "allocated_to": None
    }
]


@app.route("/", methods=["GET"])
def home():
    """Welcome endpoint"""
    return jsonify({
        "message": "Welcome to Campus Lab Resources Management API",
        "campus": CAMPUS_NAME,
        "environment": APP_ENV,
        "documentation": {
            "GET /api/resources": "List all lab resources",
            "GET /api/resources/<id>": "Get resource details by ID",
            "POST /api/resources": "Register or book a lab resource",
            "GET /health": "Liveness & readiness health check endpoint"
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    Used by Jenkins CI, Kubernetes liveness/readiness probes, and Prometheus scraping.
    """
    return jsonify({
        "status": "UP",
        "service": "campus-lab-resources-api",
        "environment": APP_ENV,
        "total_resources": len(RESOURCES)
    }), 200


@app.route("/api/resources", methods=["GET"])
def get_resources():
    """
    List all campus lab resources.
    Supports filtering by query parameters: ?status=Available or ?lab=AI
    """
    status_filter = request.args.get("status")
    lab_filter = request.args.get("lab")

    results = RESOURCES
    if status_filter:
        results = [r for r in results if r["status"].lower() == status_filter.lower()]
    if lab_filter:
        results = [r for r in results if lab_filter.lower() in r["lab"].lower()]

    return jsonify({
        "count": len(results),
        "resources": results
    }), 200


@app.route("/api/resources/<int:resource_id>", methods=["GET"])
def get_resource(resource_id):
    """Retrieve a single lab resource by ID"""
    resource = next((r for r in RESOURCES if r["id"] == resource_id), None)
    if not resource:
        return jsonify({"error": f"Resource with ID {resource_id} not found"}), 404
    return jsonify(resource), 200


@app.route("/api/resources", methods=["POST"])
def create_or_book_resource():
    """
    Register a new lab resource or update booking status.
    Expected JSON:
    {
        "name": "Raspberry Pi 5 Kit",
        "lab": "IoT Systems Lab",
        "type": "Microcontroller",
        "status": "Available"
    }
    """
    data = request.get_json()
    if not data or not data.get("name") or not data.get("lab"):
        return jsonify({
            "error": "Invalid request. 'name' and 'lab' fields are mandatory."
        }), 400

    new_id = max([r["id"] for r in RESOURCES], default=0) + 1
    new_resource = {
        "id": new_id,
        "name": data.get("name"),
        "lab": data.get("lab"),
        "type": data.get("type", "General Lab Equipment"),
        "status": data.get("status", "Available"),
        "allocated_to": data.get("allocated_to", None)
    }
    RESOURCES.append(new_resource)

    return jsonify({
        "message": "Resource successfully added to campus laboratory inventory",
        "resource": new_resource
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT, debug=(APP_ENV == "development"))

# Enhanced search filter endpoint helper

