import asyncio
import aiohttp
import time
import argparse
import statistics

async def fetch(session, url, method='GET', data=None):
    start_time = time.time()
    try:
        if method == 'GET':
            async with session.get(url) as response:
                await response.read()
                status = response.status
        elif method == 'POST':
            async with session.post(url, json=data) as response:
                await response.read()
                status = response.status
        else:
            raise ValueError("Unsupported HTTP method")
        end_time = time.time()
        return status, end_time - start_time, None
    except Exception as e:
        end_time = time.time()
        return None, end_time - start_time, e

async def benchmark_endpoint(session, name, url, method, data, num_requests):
    print(f"Starting benchmark for {name} ({method} {url}) with {num_requests} concurrent requests...")
    
    tasks = []
    for _ in range(num_requests):
        tasks.append(fetch(session, url, method, data))
        
    results = await asyncio.gather(*tasks)
    
    successes = 0
    failures = 0
    latencies = []
    
    for status, latency, error in results:
        if status and 200 <= status < 300:
            successes += 1
            latencies.append(latency)
        else:
            failures += 1
            
    if latencies:
        avg_latency = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
    else:
        avg_latency = min_latency = max_latency = 0
        
    print(f"--- Results for {name} ---")
    print(f"Total Requests: {num_requests}")
    print(f"Successful: {successes}")
    print(f"Failed: {failures}")
    if successes > 0:
        print(f"Average Latency: {avg_latency:.4f} seconds")
        print(f"Min Latency: {min_latency:.4f} seconds")
        print(f"Max Latency: {max_latency:.4f} seconds")
    print("-" * 30 + "\n")

async def main():
    parser = argparse.ArgumentParser(description="EV Battery Quantum API Benchmarker")
    parser.add_argument('--base-url', type=str, default='http://localhost:8000', help='Base URL of the API')
    parser.add_argument('--concurrency', type=int, default=50, help='Number of concurrent requests')
    args = parser.parse_args()

    base_url = args.base_url.rstrip('/')
    health_url = f"{base_url}/health"
    optimize_url = f"{base_url}/optimize"

    # Dummy payload for optimize endpoint - modify as per actual API requirements
    optimize_payload = {
        "temperature": 25.0,
        "soc": 0.8,
        "soh": 0.95
    }

    async with aiohttp.ClientSession() as session:
        await benchmark_endpoint(session, "Health Check", health_url, 'GET', None, args.concurrency)
        await benchmark_endpoint(session, "Optimize", optimize_url, 'POST', optimize_payload, args.concurrency)

if __name__ == '__main__':
    asyncio.run(main())
