import time
import requests

def test_pipeline():
    print("🚀 [TEST] Initiating Quantum Battery Optimization pipeline via API...")
    url = "http://localhost:8000/optimize"
    
    # Example battery configuration parameters
    payload = {
        "parameters": {
            "layers": 4, 
            "learningRate": 0.01, 
            "iterations": 100,
            "target_chemistry": "NMC",
            "cooling_mechanism": "Liquid"
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"\n📡 [API RESPONSE] Status Code: {response.status_code}")
        print(f"📦 [API PAYLOAD]: {response.json()}")
        
        if response.status_code == 200:
            task_id = response.json().get("task_id")
            print(f"\n✅ Successfully triggered background optimization. Task ID: {task_id}")
            print(f"   (In the real app, the frontend connects to WebSockets via /ws/logs/{task_id} to stream results)")
            
            # Now we query the status endpoint
            print("\n⏳ Waiting for Celery worker to pick up the task...")
            time.sleep(2)
            
            status_url = f"http://localhost:8000/status/{task_id}"
            status_res = requests.get(status_url)
            print(f"📊 [TASK STATUS]: {status_res.json()}")
        else:
            print("\n❌ Failed to trigger optimization.")
            
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
        print("   Make sure the Docker containers (api, redis, celery) are fully running.")

if __name__ == "__main__":
    test_pipeline()
