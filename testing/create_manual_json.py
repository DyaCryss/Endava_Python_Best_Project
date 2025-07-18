"""_summary_"""
import json
from pathlib import Path

# Define test inputs and expected outputs in structured JSON format
test_cases = {
    "pow": [
        {
            "test_id": "POW-01",
            "input": {"base": 2, "exponent": 3},
            "expected_output": {"operation": "pow", "result": 8.0}
        },
        {
            "test_id": "POW-02",
            "input": {"base": 5, "exponent": 0},
            "expected_output": {"operation": "pow", "result": 1.0}
        },
        {
            "test_id": "POW-03",
            "input": {"base": 2, "exponent": -1},
            "expected_output": {"operation": "pow", "result": 0.5}
        },
        {
            "test_id": "POW-04",
            "input": {"base": "a", "exponent": "b"},
            "expected_output": {"error": "422 Unprocessable Entity"}
        }
    ],
    "fibonacci": [
        {
            "test_id": "FIB-01",
            "input": {"n": 10},
            "expected_output": {"operation": "fibonacci", "input": 10, "result": 55}
        },
        {
            "test_id": "FIB-02",
            "input": {"n": 0},
            "expected_output": {"operation": "fibonacci", "input": 0, "result": 0}
        },
        {
            "test_id": "FIB-03",
            "input": {"n": -1},
            "expected_output": {"error": "422 Unprocessable Entity"}
        },
        {
            "test_id": "FIB-04",
            "input": {"n": 25},
            "expected_output": {"operation": "fibonacci", "input": 25, "result": "cached or computed value"}
        }
    ],
    "factorial": [
        {
            "test_id": "FAC-01",
            "input": {"n": 5},
            "expected_output": {"operation": "factorial", "input": 5, "result": 120}
        },
        {
            "test_id": "FAC-02",
            "input": {"n": 0},
            "expected_output": {"operation": "factorial", "input": 0, "result": 1}
        },
        {
            "test_id": "FAC-03",
            "input": {"n": 100},
            "expected_output": {"operation": "factorial", "input": 100, "result": "large number"}
        },
        {
            "test_id": "FAC-04",
            "input": {"n": -5},
            "expected_output": {"error": "422 Unprocessable Entity"}
        }
    ],
    "auth": [
        {
            "test_id": "AUTH-01",
            "description": "Access with valid token",
            "headers": {"Authorization": "Bearer valid_token"},
            "endpoint": "/pow",
            "method": "POST",
            "input": {"base": 2, "exponent": 2},
            "expected_output": {"operation": "pow", "result": 4.0}
        },
        {
            "test_id": "AUTH-02",
            "description": "Access without token",
            "headers": {},
            "endpoint": "/pow",
            "method": "POST",
            "input": {"base": 2, "exponent": 2},
            "expected_output": {"error": "401 Unauthorized"}
        },
        {
            "test_id": "AUTH-03",
            "description": "Access with invalid token",
            "headers": {"Authorization": "Bearer invalid_token"},
            "endpoint": "/pow",
            "method": "POST",
            "input": {"base": 2, "exponent": 2},
            "expected_output": {"error": "401 Unauthorized"}
        }
    ]
}

# Write to JSON file
json_output_path = Path("manual_test_cases.json")
with open(json_output_path, "w") as json_file:
    json.dump(test_cases, json_file, indent=4)

# Provide file name for download
json_output_path.name
