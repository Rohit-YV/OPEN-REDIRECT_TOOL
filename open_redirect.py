import argparse
import subprocess
import sys
import requests
import time

def run_external_tools(domains_file):
    """Runs external tools to gather URLs and returns the gathered URLs."""
    # Example tools (Replace with actual tools or commands as needed)
    commands = [
        "gau", "hakrawler", "waybackurls", "katana"
    ]
    
    gathered_urls = []
    
    for command in commands:
        try:
            process = subprocess.Popen([command, domains_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                gathered_urls.extend(stdout.decode('utf-8').splitlines())
            else:
                print(f"Error running {command}: {stderr.decode('utf-8')}", file=sys.stderr)
        except FileNotFoundError:
            print(f"Command {command} not found.", file=sys.stderr)
    
    return gathered_urls

def replace_and_check(urls, test_url, delay):
    """Replace parts of URLs with test URL and check for vulnerabilities."""
    for url in urls:
        test_url_with_replacement = url.replace("abcd", test_url)
        print(f"Testing: {test_url_with_replacement}")
        try:
            response = requests.get(test_url_with_replacement, allow_redirects=True)
            if test_url in response.text:
                print(f"{test_url_with_replacement} \033[0;31mVulnerable\n")
        except requests.RequestException as e:
            print(f"Error: {e}", file=sys.stderr)
        time.sleep(delay)

def main(domains_file, test_url, delay):
    gathered_urls = run_external_tools(domains_file)
    filtered_urls = [url for url in gathered_urls if 'http' in url]
    replace_and_check(filtered_urls, test_url, delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check URLs for vulnerabilities.")
    parser.add_argument("-d", "--domains", required=True, help="File containing list of domains.")
    parser.add_argument("-t", "--testurl", required=True, help="URL to check for vulnerability.")
    parser.add_argument("-l", "--delay", type=float, default=1.0, help="Delay between requests in seconds.")
    args = parser.parse_args()

    main(args.domains, args.testurl, args.delay)
