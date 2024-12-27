import tkinter as tk
from tkinter import ttk
import requests

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

def submit_ticket_logic(member_id, ticket_notes):
    # Make a POST request to the endpoint
    endpoint_url = "https://payload.vextapp.com/hook/3OG7JZP3RM/catch/$(keywords)"
    api_key = "RYsCkEUm.BGOGpB1p1m9p8KnWRskuJM1sGTPvD28J"
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

        # Extract the predicted category (keyword) from the text
        keywords_prefix = "Keywords: "
        predicted_category = text_value[len(keywords_prefix):] if text_value.startswith(keywords_prefix) else None

        # Get assignee based on category
        assignee_options = get_assignee(predicted_category)
        if assignee_options:
            assignee = assignee_options[0]
        else:
            assignee = 'Not Assigned'

        return predicted_category, assignee
    else:
        return None, 'Error in API request.'

def submit_ticket():
    member_id = member_id_entry.get()
    ticket_notes = ticket_notes_entry.get("1.0", tk.END)

    if not member_id or len(ticket_notes) == 1:
        error_label.config(text="Error: Please fill in all fields.", foreground="red")
    else:
        error_label.config(text="", foreground="red")
        member_id_entry.delete(0, tk.END)
        ticket_notes_entry.delete("1.0", tk.END)

        # Perform the logic for submitting a ticket
        predicted_category, assignee = submit_ticket_logic(member_id, ticket_notes)

        # Display the result
        result_label.config(text=f"Predicted Category: {predicted_category}\nAssignee: {assignee}")


# GUI setup
root = tk.Tk()
root.title("Ticket Submission")

main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

title_label = ttk.Label(main_frame, text="Ticket Submission", font=('Arial', 16))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

member_id_label = ttk.Label(main_frame, text="Member ID:")
member_id_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
member_id_entry = ttk.Entry(main_frame, width=30)
member_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky=(tk.W+tk.E))

ticket_notes_label = ttk.Label(main_frame, text="Ticket Notes:")
ticket_notes_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
ticket_notes_entry = tk.Text(main_frame, height=5, width=30, relief='solid', borderwidth=1)
ticket_notes_entry.grid(row=2, column=1, padx=10, pady=5, sticky=(tk.W+tk.E))

submit_button = ttk.Button(main_frame, text="Submit", command=submit_ticket)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

error_label = ttk.Label(main_frame, text="", foreground="red")
error_label.grid(row=4, column=0, columnspan=2, pady=10)

result_label = ttk.Label(main_frame, text="", font=('Arial', 12))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
