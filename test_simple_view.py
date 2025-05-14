import requests

def test_simple():
    try:
        response = requests.get("http://localhost:80/")
        print(f"Status code: {response.status_code}")
        print(f"Content: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_simple() 