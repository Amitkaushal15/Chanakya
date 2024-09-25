import requests

# Function to handle multiple URLs
def check_urls(url_list):
    for url in url_list:
        # URL validation
        if not url.startswith('http'):
            print(f"Skipping invalid URL: {url} (Must start with http or https)")
            continue
        
        try:
            # Request with redirect handling
            response = requests.get(url, allow_redirects=True, timeout=10)
            
            # Print results
            print(f"\nChecking URL: {url}")
            if response.history:  # Check if there was a redirect
                print(f"Redirected from {response.url} to {response.history[-1].url}")
            if response.status_code == 200:
                print(f"Success! Status Code: {response.status_code}")
            elif response.status_code == 301:
                print("Moved Permanently")
            elif response.status_code == 302:
                print("Found - redirect")
            elif response.status_code == 404:
                print("Error 404: Page not found")
            elif response.status_code == 403:
                print("Error 403: Permission Denied")
            elif response.status_code == 500:
                print("Error 500: Internal Server Error")
            else:
                print(f"Received unexpected status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")

# Main logic to take input and call the function
urls_input = input("Enter URLs separated by commas: ")

# Split input by comma and strip whitespace
urls = [url.strip() for url in urls_input.split(",")]

# Call the function to check URLs
check_urls(urls)
