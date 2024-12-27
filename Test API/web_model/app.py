from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)
api_key = '#'  # Replace '#' with your actual API key


# Sample Assignee conditions
assignee_conditions = {
    'Financials': ['Reilly'],
    'Evidence': ['Abby', 'Merve', 'Reilly', 'Murugan'],
    'Letters': ['Merve'],
    'CM Issue': ['Murugan', 'Abby', 'Reilly', 'Merve'],
    'Biib': ['Send back to Service Desk']
}

def get_assignee(category):
    for key, values in assignee_conditions.items():
        if category in key:
            return values
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        ticket_notes = request.form.get('ticket_notes')

        if not member_id or not ticket_notes:
            return render_template('index.html', error='Please fill in all fields.')

        # Make a POST request to the endpoint
        endpoint_url = "https://payload.vextapp.com/hook/3OG7JZP3RM/catch/$(keywords)"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Apikey": f"Api-Key {api_key}"
        }
        payload = {"payload": ticket_notes}
        response = requests.post(endpoint_url, json=payload, headers=headers)
       

        if response.status_code == 200 and 'application/json' in response.headers['Content-Type']:
            # Parse the JSON response
            result_json = response.json()

            # Extract the text from the JSON response
            text_value = result_json.get('text', '')
            print(text_value)

            # Extract the predicted category (keyword) from the text
            keywords_prefix = "Keywords: "
            predicted_category = text_value.split(':', 1)[-1].strip() if text_value.startswith(keywords_prefix) else None
        
            

            # Get assignee based on category
            assignee_options = get_assignee(predicted_category)
            if assignee_options:
                assignee = assignee_options[0]
            else:
                assignee = 'Not Assigned'

            # Print the result in the terminal
            print("Predicted Category:", predicted_category)
            print("Assignee:", assignee)

            return render_template('result.html', keyword=predicted_category, assignee=assignee)
        else:
            return render_template('index.html', error='Error in API request.')

    return render_template('index.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
