import argparse
import requests
import re
import sys

# Banner
print("""

 ██╗███╗   ██╗███████╗██████╗ ██╗   ██╗███████╗██████╗  
 ██║████╗  ██║██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗ 
 ██║██╔██╗ ██║█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝ 
 ██║██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗ 
 ██║██║ ╚████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║ 
 ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ 

                      Directory Traversal Tester FinderFunder: by Muhmmad Qasim

""")

# Command-line argument parser
parser = argparse.ArgumentParser(description="Test for Directory Traversal vulnerabilities.")
parser.add_argument("-u", "--url", required=True, help="The URL to test for Directory Traversal vulnerabilities.")
parser.add_argument("-p", "--payloads", required=True, help="The path to a file containing a list of custom payloads to test.")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
parser.add_argument("-s", "--save", help="Save only successful payloads to a file.")
args = parser.parse_args()

# Read the payloads from the specified file
with open(args.payloads) as f:
    payloads = [line.strip() for line in f.readlines()]

# URL to test
url = args.url + "/"

# Loop through each payload
for i, payload in enumerate(payloads):
    # Send a request with the payload as the filename
    response = requests.get(url + payload)

    # Define the color variable
    if response.status_code == 200:
        color = "\033[92m"
    else:
        color = "\033[91m"

    # Check if the response contains any interesting data
    interesting_data = (
        "root" in response.text
        or "passwd" in response.text
        or "etc" in response.text
    )

    # Print the result
    if args.verbose:
        print(f"[{response.status_code:5}] {i+1}/{len(payloads)} {payload} => {color}{response.reason}\033[0m")
        if response.status_code == 200 and interesting_data:
            sys.stdout.write(color + f"  {response.text[:256]}" + "\033[0m")
            print()
        else:
            print()
    else:
        if response.status_code == 200 and interesting_data:
            print(f"\033[92mDirectory Traversal vulnerability found! Payload: {payload}\033[0m")
            print(response.text)
            if args.save:
                with open(args.save, "a") as f:
                    f.write(payload + "\n")
        else:
            print(f"Payload {payload} did not reveal any interesting data (200).")
