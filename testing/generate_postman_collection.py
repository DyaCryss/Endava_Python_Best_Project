
import json
import uuid
from pathlib import Path

# Load test cases
with open("manual_test_cases.json") as f:
    test_cases = json.load(f)

# Optional descriptions for each folder
folder_descriptions = {
    "pow": "Tests for the /pow endpoint that calculates base^exponent.",
    "fibonacci": "Tests for the /fibonacci endpoint that returns the n-th Fibonacci number.",
    "factorial": "Tests for the /factorial endpoint that returns the factorial of a number.",
    "auth": "Tests for authentication and access control with tokens.",
    "error": "Tests for error handling scenarios such as missing params and bad JSON.",
    "cache": "Tests to validate response caching for expensive operations like Fibonacci.",
    "logging": "Tests to confirm API activity is written to logs."
}

# Add extra test cases directly here
test_cases["error"] = [
    {
        "test_id": "ERR-01",
        "method": "GET",
        "endpoint": "/fibonacci",
        "expected_output": {"error": "422 Unprocessable Entity"}
    },
    {
        "test_id": "ERR-02",
        "method": "POST",
        "endpoint": "/pow",
        "input": "{ base: 2, exponent: 2",  # malformed
        "expected_output": {"error": "400 Bad Request"},
        "headers": {"Content-Type": "application/json"}
    }
]

test_cases["cache"] = [
    {
        "test_id": "CACHE-01",
        "method": "GET",
        "endpoint": "/fibonacci?n=25",
        "expected_output": {"result": "cached or computed"}
    }
]

test_cases["logging"] = [
    {
        "test_id": "LOG-01",
        "method": "GET",
        "endpoint": "/factorial?n=3",
        "expected_output": {"result": 6}
    }
]

# Helper to create a Postman request item
def create_postman_request(name, method, url, body=None, headers=None):
    return {
        "name": name,
        "request": {
            "method": method,
            "header": [
                {"key": k, "value": v, "type": "text"} for k, v in (headers or {}).items()
            ],
            "url": {
                "raw": "{{base_url}}" + url,
                "host": ["{{base_url}}"],
                "path": url.lstrip("/").split("/")
            },
            "body": {
                "mode": "raw",
                "raw": json.dumps(body, indent=2) if isinstance(body, dict) else (body or "")
            } if method in ("POST", "PUT") else None
        },
        "response": []
    }

# Create the Postman collection
collection = {
    "info": {
        "name": "Microservices API Tests",
        "_postman_id": str(uuid.uuid4()),
        "description": "Postman collection generated from manual test cases and extra system-level tests",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": []
}

# Organize by folder (group)
for group, cases in test_cases.items():
    folder = {
        "name": group.upper(),
        "description": folder_descriptions.get(group, ""),
        "item": []
    }
    for case in cases:
        method = case.get("method", "GET").upper()
        endpoint = case.get("endpoint")
        if not endpoint:
            if group == "pow":
                endpoint = "/pow"
                method = "POST"
            elif group == "fibonacci":
                endpoint = f"/fibonacci?n={case['input']['n']}"
                method = "GET"
            elif group == "factorial":
                endpoint = f"/factorial?n={case['input']['n']}"
                method = "GET"
            else:
                continue
        body = case.get("input") if method in ("POST", "PUT") else None
        headers = case.get("headers", {})
        folder["item"].append(create_postman_request(case["test_id"], method, endpoint, body, headers))
    collection["item"].append(folder)

# Write to Postman JSON file
with open("postman_collection_microservice.json", "w") as f:
    json.dump(collection, f, indent=2)

print("✅ Postman collection with extended system-level test folders written.")
