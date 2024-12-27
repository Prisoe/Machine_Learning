import random
import requests
import tkinter as tk


# Define a global list to store ticket history
ticket_history = []

# Define function to get the selected people in the index
assignee_vars = None



def submit_ticket_logic(member_id, ticket_notes, selected_assignees):
    assignees = selected_assignees
    global assignee_vars
    # API endpoint details
    endpoint_url = 'https://payload.vextapp.com/hook/6487BXFWX5/catch/$(keywords)'
    api_key = 'mVfYv6mq.aKJwA3XrGkh5ZVIboR8ejXjB7DwsLRqL'
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
        print(f"Returned Keyword: {predicted_category}")


        # Check if the predicted category is "BIIB" and handle it separately
        if predicted_category == "Financial, Evidence, BIIB, Letters, CM":
            return handle_biib_category()
    
    

    if assignees:
        # Check if the predicted category is in the selected assignees
        if predicted_category:
            assignee = get_least_busy_assignee(predicted_category, assignees)
        else:
            # Category is not in selected assignees
            return predicted_category, "Unassigned because BA is not available today."

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
        # Handle the case when no assignee is available
        return "Unassigned", "No available assignee for today."

def get_assignee(category):
    # Existing logic for getting assignee from assignee_conditions
    assignee_conditions = {
        'Financial': ['Reilly Lapierre', 'Gary Spence'],
        'Evidence': ['Merve Bayraktar', 'Reilly Lapierre', 'Murugan Chandran'],
        'Letters': ['Merve Bayraktar'],
        'CM': ['Murugan Chandran', 'Abby Van Sickle', 'Reilly Lapierre', 'Merve Bayraktar'],
        'BIIB': ['BIIB']
    }

    # Modify to return the list of assignees based on the category
    return assignee_conditions.get(category, [])



def handle_biib_category():
    # Handle the specific case for "BIIB" category
    return "BIIB", "BIIB (SR Approval Queue)"

# Implement the Check for who's available and 20% workload later...

def get_least_busy_assignee(category, assignees):
    assignee_ticket_count = create_assignee_ticket_count(list(assignees))
    
    if assignees:
        available_assignees = []
        # Iterate through predicted categories
        if category:
            # Get the assignee list based on the category
            assignee_list = get_assignee(category)

            if category == "BIIB":
                return "BIIB (SR Approval Queue)"
                


            # Check if the category has a specific assignee
            if assignee_list:
                # Add assignees from assignee_list if present in assignees
                available_assignees.extend([assignee for assignee in assignee_list if assignee in assignees])

        print(f"assignee List: {assignee_list}")
        print(f"assignees: {assignees}")
        print(f"available: {available_assignees}")
            

    # If available assignees found, sort them based on the ticket count
        if available_assignees:
            sorted_assignees = sorted(available_assignees, key=lambda x: assignee_ticket_count[x])
            assignee_ticket_count[sorted_assignees[0]] += 1
            print(sorted_assignees[0])
            return sorted_assignees[0]
        else:
             # If no selected assignees are available, return "Unassigned because BA is not available today."
            return "Unassigned because BA is not available today."



def create_assignee_ticket_count(assignees):
    return {assignee: 0 for assignee in assignees}
