#!/usr/bin/env python
"""
Quick API Test Script - Test all endpoints locally
Run: python test_api.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Test data
test_user = {
    "username": "testuser1",
    "email": "test1@example.com",
    "password": "test_password_123",
    "role": "analyst"
}

test_admin = {
    "username": "admin_user",
    "email": "admin@example.com",
    "password": "admin_pass_123",
    "role": "admin"
}

test_viewer = {
    "username": "viewer_user",
    "email": "viewer@example.com",
    "password": "viewer_pass_123",
    "role": "viewer"
}


def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_register_users():
    """Test user registration"""
    print("\n🔍 Testing User Registration...")
    
    tokens = {}
    
    # Register analyst
    print("  → Registering Analyst...")
    response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        tokens['analyst'] = data['access_token']
        print(f"  ✓ Analyst registered: {data['username']}")
    else:
        print(f"  ✗ Error: {response.text}")
    
    # Register admin
    print("  → Registering Admin...")
    response = requests.post(f"{BASE_URL}/api/auth/register", json=test_admin)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        tokens['admin'] = data['access_token']
        print(f"  ✓ Admin registered: {data['username']}")
    else:
        print(f"  ✗ Error: {response.text}")
    
    # Register viewer
    print("  → Registering Viewer...")
    response = requests.post(f"{BASE_URL}/api/auth/register", json=test_viewer)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        tokens['viewer'] = data['access_token']
        print(f"  ✓ Viewer registered: {data['username']}")
    else:
        print(f"  ✗ Error: {response.text}")
    
    return tokens


def test_login(tokens):
    """Test user login"""
    print("\n🔍 Testing Login...")
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": test_user['username'], "password": test_user['password']}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Login successful")
        return response.json()
    else:
        print(f"✗ Error: {response.text}")
        return None


def test_create_records(tokens):
    """Test creating financial records"""
    print("\n🔍 Testing Record Creation...")
    
    headers = {"Authorization": f"Bearer {tokens['analyst']}"}
    
    records = [
        {
            "amount": 5000,
            "record_type": "income",
            "category": "salary",
            "description": "Monthly salary",
            "transaction_date": (datetime.now() - timedelta(days=15)).isoformat()
        },
        {
            "amount": 1500,
            "record_type": "expense",
            "category": "food",
            "description": "Monthly groceries",
            "transaction_date": (datetime.now() - timedelta(days=10)).isoformat()
        },
        {
            "amount": 800,
            "record_type": "expense",
            "category": "utilities",
            "description": "Electricity bill",
            "transaction_date": (datetime.now() - timedelta(days=5)).isoformat()
        }
    ]
    
    record_ids = []
    for i, record_data in enumerate(records, 1):
        print(f"  → Creating record {i}...")
        response = requests.post(
            f"{BASE_URL}/api/records",
            json=record_data,
            headers=headers
        )
        print(f"  Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            record_ids.append(data['id'])
            print(f"  ✓ Record created: ID={data['id']}")
        else:
            print(f"  ✗ Error: {response.text}")
    
    return record_ids


def test_get_records(tokens):
    """Test retrieving records"""
    print("\n🔍 Testing Get Records...")
    
    headers = {"Authorization": f"Bearer {tokens['analyst']}"}
    
    response = requests.get(
        f"{BASE_URL}/api/records?skip=0&limit=10",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Retrieved {len(data['records'])} records")
        print(f"  Total count: {data['total_count']}")
    else:
        print(f"✗ Error: {response.text}")


def test_dashboard(tokens):
    """Test dashboard summary"""
    print("\n🔍 Testing Dashboard Summary...")
    
    headers = {"Authorization": f"Bearer {tokens['analyst']}"}
    
    response = requests.get(
        f"{BASE_URL}/api/dashboard/summary",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Dashboard data retrieved:")
        print(f"  Total Income: ${data['total_income']}")
        print(f"  Total Expenses: ${data['total_expenses']}")
        print(f"  Net Balance: ${data['net_balance']}")
        print(f"  Recent Records: {len(data['recent_records'])}")
        print(f"  Categories: {len(data['category_wise_totals'])}")
    else:
        print(f"✗ Error: {response.text}")


def test_access_control(tokens):
    """Test role-based access control"""
    print("\n🔍 Testing Access Control...")
    
    record_data = {
        "amount": 1000,
        "record_type": "income",
        "category": "bonus",
        "description": "Test record",
        "transaction_date": datetime.now().isoformat()
    }
    
    # Try with viewer (should fail)
    print("  → Viewer trying to create record (should fail)...")
    headers = {"Authorization": f"Bearer {tokens['viewer']}"}
    response = requests.post(
        f"{BASE_URL}/api/records",
        json=record_data,
        headers=headers
    )
    print(f"  Status: {response.status_code}")
    if response.status_code == 403:
        print("  ✓ Correctly blocked viewer from creating record")
    else:
        print(f"  ✗ Expected 403, got {response.status_code}")


def test_user_management(tokens):
    """Test user management endpoints"""
    print("\n🔍 Testing User Management...")
    
    headers = {"Authorization": f"Bearer {tokens['admin']}"}
    
    # Get current user
    print("  → Getting current user...")
    response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ Current user: {data['username']} ({data['role']})")
    
    # List users (admin only)
    print("  → Listing all users (admin only)...")
    response = requests.get(f"{BASE_URL}/api/users?skip=0&limit=10", headers=headers)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ Found {len(data)} users")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  FINANCE BACKEND API TEST SUITE")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server at {BASE_URL}")
        print("Make sure the server is running:")
        print("  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    try:
        # Run tests
        test_health()
        tokens = test_register_users()
        test_login(tokens)
        record_ids = test_create_records(tokens)
        test_get_records(tokens)
        test_dashboard(tokens)
        test_access_control(tokens)
        test_user_management(tokens)
        
        print("\n" + "="*60)
        print("  ✓ ALL TESTS COMPLETED")
        print("="*60)
        print("\n📚 API Documentation available at:")
        print(f"  - Swagger UI: {BASE_URL}/docs")
        print(f"  - ReDoc: {BASE_URL}/redoc")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    main()
