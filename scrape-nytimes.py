import csv
import requests
import json
import re

# Define the URL of the API endpoint
api_url = "https://www.nytimes.com/svc/community/V3/requestHandler?url=https%3A%2F%2Fwww.nytimes.com%2F2024%2F01%2F04%2Fus%2Fperry-iowa-school-shooting.html&method=get&commentSequence=0&offset=0&includeReplies=true&sort=newest&cmd=GetCommentsAll&callback=jsonp_1704830713131_89574&limit=100"  # Replace with the actual API URL

# Send an HTTP GET request to the API endpoint
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    # Use regular expression to extract the JSON content from JSONP
    jsonp_pattern = re.compile(r'jsonp_\d+_\d+\((\{.*\})\);', re.DOTALL)
    match = jsonp_pattern.search(response.text)

    if match:
        try:
            # Extract the JSON content from the match
            json_content = match.group(1)
            data = json.loads(json_content)

            # Extract comments
            comments = data.get("results", {}).get("comments", [])

            # Define CSV file name
            csv_file = "comments.csv"

            # Open the CSV file for writing
            with open(csv_file, mode='w', newline='') as csv_file:
                fieldnames = ["commentID", "userDisplayName", "userLocation", "commentBody"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write the header
                writer.writeheader()

                # Write each comment to the CSV file
                for comment in comments:
                    writer.writerow({
                        "commentID": comment["commentID"],
                        "userDisplayName": comment["userDisplayName"],
                        "userLocation": comment["userLocation"],
                        "commentBody": comment["commentBody"]
                    })

                    # Loop through replies - YOUR HOMEWORK #1
                    # Write one more row for each reply - YOUR HOMEWORK

            print(f"Comments have been exported to {csv_file}")
        except json.JSONDecodeError:
            print("Error: The JSON content inside the JSONP is not valid.")
    else:
        print("Error: JSONP format not found in the response.")
else:
    print(f"Failed to fetch data from the API. Status code: {response.status_code}")
