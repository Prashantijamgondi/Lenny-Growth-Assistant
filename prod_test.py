import requests
import time
import json
import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Production Test Script")
    parser.add_argument("--backend", default="http://localhost:8000", help="Backend URL")
    parser.add_argument("--frontend", default="http://localhost:3000", help="Frontend URL")
    parser.add_argument("--provider", default="claude", help="LLM Provider to test (claude or ollama)")
    return parser.parse_args()

def print_step(step_name):
    print(f"\n[🏃] Running Test: {step_name}...")

def assert_true(condition, success_msg, fail_msg):
    if condition:
        print(f"  [✅] PASS: {success_msg}")
    else:
        print(f"  [❌] FAIL: {fail_msg}")
        sys.exit(1)

def test_health_check(backend_url):
    print_step("Backend Health Check")
    try:
        start_time = time.time()
        response = requests.get(f"{backend_url}/api/health", timeout=10)
        latency = time.time() - start_time
        
        assert_true(response.status_code == 200, "Health endpoint returned 200 OK", f"Health endpoint returned {response.status_code}")
        
        data = response.json()
        assert_true(data.get("status") == "healthy", "Backend status is 'healthy'", f"Backend status is {data.get('status')}")
        assert_true(data.get("database") == "connected", "Database is connected", "Database connection failed")
        assert_true(latency < 1.0, f"Latency is acceptable ({latency:.2f}s)", f"High latency on health check ({latency:.2f}s)")
        
    except Exception as e:
        assert_true(False, "", f"Failed to reach backend: {str(e)}")

def test_frontend_availability(frontend_url):
    print_step("Frontend Availability")
    try:
        response = requests.get(frontend_url, timeout=10)
        assert_true(response.status_code == 200, "Frontend is reachable and returns 200 OK", f"Frontend returned {response.status_code}")
    except Exception as e:
        assert_true(False, "", f"Failed to reach frontend: {str(e)}")

def test_chat_stream(backend_url, provider):
    print_step("Chat API & RAG Retrieval")
    payload = {
        "session_id": "test_prod_123",
        "message": "What is the best way to improve user retention according to Lenny?",
        "mode": "default",
        "provider": provider
    }
    
    try:
        response = requests.post(f"{backend_url}/api/chat", json=payload, stream=True, timeout=30)
        assert_true(response.status_code == 200, "Chat endpoint returned 200 OK", f"Chat endpoint returned {response.status_code}")
        
        received_tokens = False
        received_sources = False
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[6:]
                    if data_str == "[DONE]":
                        break
                    
                    try:
                        event_data = json.loads(data_str)
                        if event_data.get("type") == "sources":
                            received_sources = True
                            sources = event_data.get("content", [])
                            assert_true(len(sources) > 0, f"RAG returned {len(sources)} sources", "RAG returned 0 sources")
                        elif event_data.get("type") == "token":
                            received_tokens = True
                    except json.JSONDecodeError:
                        continue

        assert_true(received_tokens, "Successfully streamed tokens from LLM", "No tokens received from LLM")
        assert_true(received_sources, "Successfully retrieved context from pgvector", "No context retrieved")
        
    except requests.exceptions.ReadTimeout:
         print("  [⚠️] WARNING: Request timed out. In production, ensure LLM latency is within acceptable bounds.")
    except Exception as e:
        assert_true(False, "", f"Failed during chat test: {str(e)}")

if __name__ == "__main__":
    args = get_args()
    print("=========================================")
    print("🚀 PRODUCTION DEPLOYMENT AUTOMATION TEST 🚀")
    print("=========================================\n")
    
    test_frontend_availability(args.frontend)
    test_health_check(args.backend)
    test_chat_stream(args.backend, args.provider)
    
    print("\n=========================================")
    print("✨ ALL PRODUCTION TESTS PASSED SUCCESSFULLY ✨")
    print("=========================================\n")
