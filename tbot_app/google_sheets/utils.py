"""Utils for google_sheets module."""


def make_ticket_info(ticket: dict) -> list:
    """Prepare ticket for insertion into Google Sheets."""
    return [value for value in ticket.values()]
