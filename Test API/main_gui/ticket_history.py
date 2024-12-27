from ticket_logic import ticket_history

def ticket_history_logic():
    # Create a string to display ticket history
    history_text = ""
    for ticket in ticket_history:
        history_text += f"Member ID: {ticket['member_id']}\n"
        history_text += f"Ticket Notes: {ticket['ticket_notes']}\n"
        history_text += f"Category: {ticket['category']}\n"
        history_text += f"Assignee: {ticket['assignee']}\n\n"

    return history_text
