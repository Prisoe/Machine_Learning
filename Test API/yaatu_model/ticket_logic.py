import random
import requests


# Define a global list to store ticket history
ticket_history = []


def submit_ticket_logic(member_id, ticket_notes):
    # API endpoint details
    endpoint_url = "https://payload.vextapp.com/hook/3OG7JZP3RM/catch/$(keywords)"
    api_key = "RYsCkEUm.BGOGpB1p1m9p8KnWRskuJM1sGTPvD28J"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Apikey": f"Api-Key {api_key}"
    }

    # Make a POST request to the endpoint
    payload = {"payload": ticket_notes}
    response = requests.post(endpoint_url, json=payload, headers=headers)

    if response.status_code == 200 and 'application/json' in response.headers['Content-Type']:
        # Parse the JSON response
        result_json = response.json()

        # Extract the text from the JSON response
        text_value = result_json.get('text', '')

        # Extract the predicted category (keyword) from the text
        keywords_prefix = "Keywords: "
        predicted_category = text_value[len(keywords_prefix):] if text_value.startswith(keywords_prefix) else None

        # Check if the predicted category is "BIIB" and handle it separately
        if predicted_category == "Financial, Evidence, BIIB, Letters, CM":
            return handle_biib_category()

        # Get assignee based on category
        assignee = get_assignee(predicted_category)

         # Append the ticket details to the history list
        ticket_history.append({
        'member_id': member_id,
        'ticket_notes': ticket_notes,
        'category': predicted_category,
        'assignee': assignee
        })

        # Return the category and assignee to the front end
        return predicted_category, assignee
    else:
        # Handle error cases
        print("Error in API request")
        return None, None

def get_assignee(category):
    # Existing logic for getting assignee from assignee_conditions
    assignee_conditions = {
        'Financials': ['Reilly'],
        'Evidence': ['Abby', 'Merve', 'Reilly', 'Murugan'],
        'Letters': ['Merve'],
        'CM Issue': ['Murugan', 'Abby', 'Reilly', 'Merve'],
        'BIIB': ['Send back to Service Desk']
    }


    for key, values in assignee_conditions.items():
        if category in key:
            # Return a random assignee from the list
           return values[0] if values else None
        
    return None


def handle_biib_category():
    # Handle the specific case for "BIIB" category
    return "BIIB", "Send back to Service Desk"

# Implement the Check for who's available and 20% workload later...