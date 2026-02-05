#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for AI Chatbot
Tests all CRUD operations, Claude AI integration, and context memory
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class ChatbotAPITester:
    def __init__(self, base_url: str = "https://ai-chat-llm.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.session_id = None

    def log_test(self, name: str, success: bool, details: str = "", response_data: Dict = None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = {
            "test_name": name,
            "status": status,
            "success": success,
            "details": details,
            "response_data": response_data
        }
        self.test_results.append(result)
        print(f"{status} - {name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")

    def test_api_health(self) -> bool:
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.api_base}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                details += f", Response: {response.json()}"
            self.log_test("API Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("API Health Check", False, f"Connection error: {str(e)}")
            return False

    def test_create_session(self) -> bool:
        """Test creating a new chat session"""
        try:
            response = requests.post(f"{self.api_base}/chat/sessions", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.session_id = data.get('session_id')
                details = f"Created session: {self.session_id}"
                self.log_test("Create Chat Session", True, details, data)
                return True
            else:
                self.log_test("Create Chat Session", False, 
                            f"Status: {response.status_code}", 
                            {"text": response.text})
                return False
        except Exception as e:
            self.log_test("Create Chat Session", False, f"Error: {str(e)}")
            return False

    def test_get_sessions(self) -> bool:
        """Test retrieving all chat sessions"""
        try:
            response = requests.get(f"{self.api_base}/chat/sessions", timeout=10)
            success = response.status_code == 200
            
            if success:
                sessions = response.json()
                details = f"Retrieved {len(sessions)} sessions"
                self.log_test("Get Chat Sessions", True, details, {"count": len(sessions)})
                return True
            else:
                self.log_test("Get Chat Sessions", False, 
                            f"Status: {response.status_code}", 
                            {"text": response.text})
                return False
        except Exception as e:
            self.log_test("Get Chat Sessions", False, f"Error: {str(e)}")
            return False

    def test_send_message(self, message: str, session_id: Optional[str] = None) -> Dict:
        """Test sending a message to the chatbot"""
        try:
            payload = {
                "message": message,
                "session_id": session_id or self.session_id
            }
            
            print(f"    Sending message: '{message}'")
            response = requests.post(f"{self.api_base}/chat", json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                assistant_msg = data.get('assistant_message', '')[:100] + "..." if len(data.get('assistant_message', '')) > 100 else data.get('assistant_message', '')
                details = f"AI Response: {assistant_msg}"
                self.log_test("Send Message", True, details, data)
                return data
            else:
                self.log_test("Send Message", False, 
                            f"Status: {response.status_code}", 
                            {"text": response.text})
                return {}
        except Exception as e:
            self.log_test("Send Message", False, f"Error: {str(e)}")
            return {}

    def test_get_messages(self, session_id: str) -> List[Dict]:
        """Test retrieving messages for a session"""
        try:
            response = requests.get(f"{self.api_base}/chat/sessions/{session_id}/messages", timeout=10)
            
            if response.status_code == 200:
                messages = response.json()
                details = f"Retrieved {len(messages)} messages for session {session_id}"
                self.log_test("Get Session Messages", True, details, {"count": len(messages)})
                return messages
            else:
                self.log_test("Get Session Messages", False, 
                            f"Status: {response.status_code}", 
                            {"text": response.text})
                return []
        except Exception as e:
            self.log_test("Get Session Messages", False, f"Error: {str(e)}")
            return []

    def test_context_memory(self) -> bool:
        """Test multi-turn conversation with context memory"""
        if not self.session_id:
            self.log_test("Context Memory Test", False, "No session available")
            return False

        try:
            # First message - establish context
            print("    Testing context memory with multi-turn conversation...")
            response1 = self.test_send_message("My name is Alice and I love pizza.")
            if not response1:
                return False

            # Wait a moment for processing
            time.sleep(2)

            # Second message - test if AI remembers context
            response2 = self.test_send_message("What's my name and what do I love?")
            if not response2:
                return False

            # Check if AI response contains context from first message
            ai_response = response2.get('assistant_message', '').lower()
            has_name = 'alice' in ai_response
            has_preference = 'pizza' in ai_response
            
            success = has_name and has_preference
            details = f"AI remembered name: {has_name}, preference: {has_preference}"
            self.log_test("Context Memory Test", success, details)
            return success

        except Exception as e:
            self.log_test("Context Memory Test", False, f"Error: {str(e)}")
            return False

    def test_delete_session(self, session_id: str) -> bool:
        """Test deleting a chat session"""
        try:
            response = requests.delete(f"{self.api_base}/chat/sessions/{session_id}", timeout=10)
            success = response.status_code == 200
            
            if success:
                details = f"Deleted session: {session_id}"
                self.log_test("Delete Chat Session", True, details)
                return True
            else:
                self.log_test("Delete Chat Session", False, 
                            f"Status: {response.status_code}", 
                            {"text": response.text})
                return False
        except Exception as e:
            self.log_test("Delete Chat Session", False, f"Error: {str(e)}")
            return False

    def test_mongodb_persistence(self) -> bool:
        """Test that data persists in MongoDB"""
        if not self.session_id:
            return False

        try:
            # Send a message
            test_message = "This is a persistence test message"
            response = self.test_send_message(test_message)
            if not response:
                return False

            # Wait for data to be saved
            time.sleep(1)

            # Retrieve messages and verify persistence
            messages = self.test_get_messages(self.session_id)
            if not messages:
                return False

            # Check if our test message is in the retrieved messages
            user_messages = [msg for msg in messages if msg['role'] == 'user']
            found_message = any(test_message in msg['content'] for msg in user_messages)
            
            success = found_message
            details = f"Message persisted in MongoDB: {found_message}"
            self.log_test("MongoDB Persistence Test", success, details)
            return success

        except Exception as e:
            self.log_test("MongoDB Persistence Test", False, f"Error: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive Backend API Testing")
        print("=" * 60)

        # Basic connectivity
        if not self.test_api_health():
            print("❌ API health check failed. Stopping tests.")
            return False

        # Session management tests
        self.test_create_session()
        self.test_get_sessions()

        # Chat functionality tests
        if self.session_id:
            # Basic message test
            self.test_send_message("Hello! Can you tell me about yourself?")
            
            # Context memory test
            self.test_context_memory()
            
            # Persistence test
            self.test_mongodb_persistence()
            
            # Message retrieval test
            self.test_get_messages(self.session_id)
            
            # Cleanup test
            self.test_delete_session(self.session_id)

        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")

        # Print failed tests
        failed_tests = [test for test in self.test_results if not test['success']]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test_name']}: {test['details']}")

        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = ChatbotAPITester()
    success = tester.run_comprehensive_test()
    
    # Save detailed results
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_tests': tester.tests_run,
            'passed_tests': tester.tests_passed,
            'success_rate': (tester.tests_passed/tester.tests_run)*100 if tester.tests_run > 0 else 0,
            'test_results': tester.test_results
        }, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())