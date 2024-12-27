import tkinter as tk
from tkinter import messagebox
import requests
from main_gui.ticket_history import ticket_history_logic

def make_api_request(input_value):
    api_key = 'sGK7q4su.ZpHqa6QhUCJKPfMm3yhBNzKVx4yQV5cE'  # Replace '#' with your actual API key

    headers = {
        'Content-Type': 'application/json',
        'Apikey': f'Api-Key {api_key}',
    }

    data = {
        "payload": input_value
    }

    url = 'https://payload.vextapp.com/hook/2BJQHIQ5YW/catch/$(keywords)'

    response = requests.post(url, json=data, headers=headers)

    # Extract the value of "text" from the response JSON
    output = response.json().get('text')

    return output

def open_system_window():
    clear_frames()
    system_frame.pack()

def store_people(people_checkboxes):
    selected_people = [person for person, var in people_checkboxes.items() if var.get() == 1]
    messagebox.showinfo("Information", f"People working today: {', '.join(selected_people)}")

def open_user_window():
    clear_frames()
    user_frame.pack()

def open_history_window():
    clear_frames()
    history_frame.pack()

     # Get the ticket history text
    history_content_label.config(text=ticket_history_logic())

def submit_issue(member_id, issue_description):
    if not member_id.isdigit() or not (len(member_id) == 9 and member_id.startswith(('1', '2', '3'))):
        messagebox.showerror("Error", "Member ID must be a 9-digit number starting with 1, 2, or 3.")
        return

    selected_people = [person for person, var in people_checkboxes.items() if var.get() == 1]
    assigned_to = assign_task(issue_description, selected_people)

    # Make API request to get the output
    output = make_api_request(issue_description)

    # Create result frame
    result_frame = tk.Frame(app)
    result_frame.pack()

    # Display output and assigned person
    output_label = tk.Label(result_frame, text=output)
    output_label.pack()

    assigned_to_label = tk.Label(result_frame, text=f"Assigned to: {assigned_to}")
    assigned_to_label.pack()


def assign_task(issue_description, selected_people):
    output = make_api_request(issue_description)
    keywords = ['Evidence', 'CM', 'Letters', 'Financial']
    candidates = []

    # Check if any keyword is present in the output
    for keyword in keywords:
        if keyword in output:
            # Find individuals who can handle the task associated with the keyword
            matching_candidates = [person for person, person_deals in deals.items() if keyword in person_deals]
            candidates.extend(matching_candidates)

    if not candidates:
        return "Unassigned"  # Return "Unassigned" if no candidates are found

    # Find the least busy candidate alphabetically with fewer or equal tasks
    available_candidates = [candidate for candidate in candidates if candidate in selected_people]
    if available_candidates:
        least_busy_candidate = min(available_candidates, key=lambda x: (task_count[x], x))
        task_count[least_busy_candidate] += 1
        return least_busy_candidate
    else:
        return "Unassigned because BA is not available today."  # Return "Unassigned" if no available candidates are found among selected people


def clear_frames():
    for frame in [system_frame, user_frame, history_frame]:
        if frame:
            frame.pack_forget()

    

app = tk.Tk()
app.title("eSMT Triage Assistant")
app.minsize(400, 300)
app.configure(bg="white")

# Define initial deals for each individual
deals = {
    'Gary': ['Financial'],
    'Abby': ['Evidence', 'CM', 'Document/Message Inbox'],
    'Merve': ['Letters', 'Evidence', 'CM'],
    'Reilly': ['Financial', 'CM', 'Evidence', 'Document/Message Inbox'],
    'Murugan': ['CM', 'Evidence'],
    'BIIB': ['BIIB']
}

# Initialize task count for each individual
task_count = {person: 0 for person in deals}

# System window
system_frame = tk.Frame(app, bg="white")

# Label and checkboxes for selecting people
label = tk.Label(system_frame, text="Select people working today:", bg="white", font=("Arial", 10))
label.pack()

people_checkboxes = {}
for person in deals.keys():
    var = tk.IntVar()
    checkbox = tk.Checkbutton(system_frame, text=person, variable=var, bg="white", font=("Arial", 10))
    checkbox.pack(anchor="w")
    people_checkboxes[person] = var

# Button to store selected people
store_button = tk.Button(system_frame, text="Update Assignees", command=lambda: store_people(people_checkboxes), bg="#1866FF", fg="white", font=("Arial", 10))
store_button.pack(pady=10)

# User window
user_frame = tk.Frame(app, bg="white")

# Entry fields and labels
member_id_label = tk.Label(user_frame, text="Member ID:", bg="white", font=("Arial", 10))
member_id_label.grid(row=0, column=0, padx=10, pady=5,sticky='w')

member_id_entry = tk.Entry(user_frame, bg="white", font=("Arial", 10))
member_id_entry.grid(row=0, column=1, padx=10, pady=5)

issue_label = tk.Label(user_frame, text="Issue Description:", bg="white", font=("Arial", 10))
issue_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

issue_entry = tk.Entry(user_frame, bg="white", font=("Arial", 10))
issue_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=(tk.W+tk.E))

submit_button = tk.Button(user_frame, text="Submit", command=lambda: submit_issue(member_id_entry.get(), issue_entry.get()), bg="#1866FF", fg="white", font=("Arial", 10))
submit_button.grid(row=4, column=0, columnspan=2, pady=10)


# History Window
history_frame = tk.Frame(app, bg="white")
# Label to display ticket history
history_content_label = tk.Label(history_frame, text="", font=("Arial", 10), bg="white")
history_content_label.pack(padx=10, pady=5)

# Main Tkinter window
top_frame = tk.Frame(app, bg='#0A3891')
top_frame.pack(fill='x')

history_button = tk.Button(top_frame, text="History", command=open_history_window, bg="#1866FF", fg="white", font=("Arial", 10))
history_button.pack(side="right", padx=10, pady=10, fill='x', expand=True)

system_button = tk.Button(top_frame, text="System", command=open_system_window, bg="#1866FF", fg="white", font=("Arial", 10))
system_button.pack(side="right", padx=10, pady=10, fill='x', expand=True)

user_button = tk.Button(top_frame, text="User", command=open_user_window, bg="#1866FF", fg="white", font=("Arial", 10))
user_button.pack(side="left", padx=10, pady=10, fill='x', expand=True)



app.mainloop()