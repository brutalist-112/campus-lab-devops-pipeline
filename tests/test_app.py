"""
Unit tests for Campus Lab Resources Management REST API.
Compatible with both pytest and python's built-in unittest.
"""

import sys
import os
import unittest
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import app


class CampusLabApiTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test"""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_check(self):
        """Test 1: Health endpoint returns HTTP 200 and UP status"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "UP")
        self.assertEqual(data["service"], "campus-lab-resources-api")

    def test_get_all_resources(self):
        """Test 2: GET /api/resources returns HTTP 200 and non-empty inventory"""
        response = self.client.get("/api/resources")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("resources", data)
        self.assertGreater(data["count"], 0)

    def test_get_resource_by_valid_and_invalid_id(self):
        """Test 3: GET /api/resources/<id> returns 200 for valid ID and 404 for invalid ID"""
        # Valid ID
        res_valid = self.client.get("/api/resources/1")
        self.assertEqual(res_valid.status_code, 200)
        data_valid = json.loads(res_valid.data)
        self.assertEqual(data_valid["id"], 1)

        # Invalid ID
        res_invalid = self.client.get("/api/resources/9999")
        self.assertEqual(res_invalid.status_code, 404)

    def test_create_new_resource_and_validation(self):
        """Test 4: POST /api/resources creates new resource, rejects missing required fields"""
        # Valid creation
        new_item = {
            "name": "Arduino Mega Starter Kit",
            "lab": "Robotics Lab",
            "type": "Microcontroller",
            "status": "Available"
        }
        res_create = self.client.post(
            "/api/resources",
            data=json.dumps(new_item),
            content_type="application/json"
        )
        self.assertEqual(res_create.status_code, 201)
        data_create = json.loads(res_create.data)
        self.assertIn("resource", data_create)
        self.assertEqual(data_create["resource"]["name"], "Arduino Mega Starter Kit")

        # Invalid creation (missing 'lab')
        bad_item = {"name": "Incomplete Item"}
        res_bad = self.client.post(
            "/api/resources",
            data=json.dumps(bad_item),
            content_type="application/json"
        )
        self.assertEqual(res_bad.status_code, 400)


if __name__ == "__main__":
    unittest.main()
