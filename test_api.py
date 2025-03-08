"""
Test script to verify the API connection
"""

import asyncio
import httpx
import json

# API settings
API_URL = "http://chic-nourishment-production.up.railway.app"
API_V1_PREFIX = "/api/v1"
API_BASE_URL = f"{API_URL}{API_V1_PREFIX}"

async def test_health():
    """Test the health endpoint"""
    url = f"{API_BASE_URL}/health/"
    print(f"Testing health endpoint: {url}")
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.get(url)
            print(f"Status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    print(f"Response JSON: {json.dumps(json_response, default=str)}")
                    return True
                except Exception as e:
                    print(f"Error parsing JSON response: {str(e)}")
                    print(f"Response text: {response.text[:500]}...")
            else:
                print(f"Error response: {response.text[:500]}...")
            
            return False
        except Exception as e:
            print(f"Error connecting to API: {str(e)}")
            return False

async def test_recent_predictions():
    """Test the recent predictions endpoint"""
    url = f"{API_BASE_URL}/predictions/"
    params = {"limit": 5, "offset": 0}
    print(f"Testing recent predictions endpoint: {url}")
    print(f"With params: {json.dumps(params, default=str)}")
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.get(url, params=params)
            print(f"Status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    print(f"Response JSON: {json.dumps(json_response, default=str)[:500]}...")
                    return True
                except Exception as e:
                    print(f"Error parsing JSON response: {str(e)}")
                    print(f"Response text: {response.text[:500]}...")
            else:
                print(f"Error response: {response.text[:500]}...")
            
            return False
        except Exception as e:
            print(f"Error connecting to API: {str(e)}")
            return False

async def main():
    """Run all tests"""
    print("=== Testing API Connection ===")
    health_ok = await test_health()
    print(f"Health check: {'OK' if health_ok else 'FAILED'}")
    
    print("\n=== Testing Recent Predictions ===")
    predictions_ok = await test_recent_predictions()
    print(f"Recent predictions: {'OK' if predictions_ok else 'FAILED'}")
    
    if health_ok and predictions_ok:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")

if __name__ == "__main__":
    asyncio.run(main()) 