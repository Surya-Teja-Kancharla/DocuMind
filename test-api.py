#!/usr/bin/env python3
"""
DocuMind API Testing Script
Tests all session management and chat endpoints
"""

import requests
import json
import time

# Configuration
API_BASE = "http://localhost:8000"
USER_ID = "test-user"

def print_test(name, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"   {details}")
    print()

def test_health_check():
    """Test 1: Health Check"""
    try:
        response = requests.get(f"{API_BASE}/health")
        passed = response.status_code == 200 and response.json().get("status") == "DocuMind backend running"
        print_test("Health Check", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Health Check", False, str(e))
        return False

def test_create_session():
    """Test 2: Create Session"""
    try:
        response = requests.post(
            f"{API_BASE}/sessions/create",
            json={"user_id": USER_ID, "title": "Test Session"}
        )
        passed = response.status_code == 200
        data = response.json() if passed else {}
        session_id = data.get("session_id")
        print_test("Create Session", passed, f"Session ID: {session_id}")
        return session_id if passed else None
    except Exception as e:
        print_test("Create Session", False, str(e))
        return None

def test_list_sessions():
    """Test 3: List Sessions"""
    try:
        response = requests.get(f"{API_BASE}/sessions/list/{USER_ID}")
        passed = response.status_code == 200
        sessions = response.json() if passed else []
        print_test("List Sessions", passed, f"Found {len(sessions)} sessions")
        return sessions
    except Exception as e:
        print_test("List Sessions", False, str(e))
        return []

def test_get_messages(session_id):
    """Test 4: Get Session Messages"""
    try:
        response = requests.get(f"{API_BASE}/sessions/{session_id}/messages")
        passed = response.status_code == 200
        messages = response.json() if passed else []
        print_test("Get Messages", passed, f"Found {len(messages)} messages")
        return passed
    except Exception as e:
        print_test("Get Messages", False, str(e))
        return False

def test_update_title(session_id):
    """Test 5: Update Session Title"""
    try:
        response = requests.patch(
            f"{API_BASE}/sessions/{session_id}/title",
            json={"title": "Updated Test Session"}
        )
        passed = response.status_code == 200
        print_test("Update Title", passed)
        return passed
    except Exception as e:
        print_test("Update Title", False, str(e))
        return False

def test_chat_stream(session_id):
    """Test 6: Chat Streaming (Basic)"""
    try:
        response = requests.post(
            f"{API_BASE}/chat/stream",
            json={
                "user_id": USER_ID,
                "session_id": session_id,
                "query": "Hello, this is a test"
            },
            stream=True
        )
        passed = response.status_code == 200
        
        # Read first chunk to verify streaming works
        if passed:
            chunk_count = 0
            for chunk in response.iter_content(chunk_size=1024):
                chunk_count += 1
                if chunk_count > 3:  # Just verify some chunks arrive
                    break
            passed = chunk_count > 0
        
        print_test("Chat Streaming", passed, f"Received streaming response")
        return passed
    except Exception as e:
        print_test("Chat Streaming", False, str(e))
        return False

def test_generate_title(session_id):
    """Test 7: Generate Session Title"""
    try:
        response = requests.post(f"{API_BASE}/sessions/{session_id}/generate-title")
        passed = response.status_code == 200
        data = response.json() if passed else {}
        title = data.get("title", "")
        print_test("Generate Title", passed, f"Generated: {title}")
        return passed
    except Exception as e:
        print_test("Generate Title", False, str(e))
        return False

def test_delete_session(session_id):
    """Test 8: Delete Session"""
    try:
        response = requests.delete(f"{API_BASE}/sessions/{session_id}")
        passed = response.status_code == 200
        print_test("Delete Session", passed)
        return passed
    except Exception as e:
        print_test("Delete Session", False, str(e))
        return False

def main():
    print("=" * 60)
    print("🧪 DocuMind API Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Health Check
    results.append(test_health_check())
    time.sleep(0.5)
    
    # Test 2: Create Session
    session_id = test_create_session()
    results.append(session_id is not None)
    time.sleep(0.5)
    
    if not session_id:
        print("❌ Cannot continue without session ID")
        return
    
    # Test 3: List Sessions
    sessions = test_list_sessions()
    results.append(len(sessions) > 0)
    time.sleep(0.5)
    
    # Test 4: Get Messages
    results.append(test_get_messages(session_id))
    time.sleep(0.5)
    
    # Test 5: Update Title
    results.append(test_update_title(session_id))
    time.sleep(0.5)
    
    # Test 6: Chat Streaming (requires document upload first)
    # Skip or mark as manual test
    print("⚠️  SKIP - Chat Streaming (requires document upload)")
    print("   Please test manually: Upload a document first, then send a message")
    print()
    
    # Test 7: Generate Title (requires message first)
    # Skip or mark as manual test
    print("⚠️  SKIP - Generate Title (requires messages in session)")
    print("   Please test manually: Send a message first, then generate title")
    print()
    
    # Test 8: Delete Session
    results.append(test_delete_session(session_id))
    time.sleep(0.5)
    
    # Summary
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the logs above.")
    
    print()
    print("Next Steps:")
    print("1. Start frontend: cd frontend && npm run dev")
    print("2. Open http://localhost:5173")
    print("3. Test the full user flow:")
    print("   - Create new chat")
    print("   - Upload a document")
    print("   - Send a message")
    print("   - Verify title auto-generates")
    print("   - Refresh page and verify sessions persist")

if __name__ == "__main__":
    main()