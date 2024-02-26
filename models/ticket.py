import uuid

class Ticket:
    def __init__(self, event_name, event_date, venue, ticket_type, price, quantity, seat_number, seller_id, id=uuid.uuid4()):
        self.event_name = event_name
        self.event_date = event_date
        self.venue = venue
        self.ticket_type = ticket_type
        self.price = price
        self.quantity = quantity
        self.seat_number = seat_number
        self.seller_id = seller_id
        self.id= id
    def insert_ticket(ticket,db):
        db.execute("""
        INSERT INTO tickets (id,event_name, event_date, venue, ticket_type, price, quantity, seat_number, seller_id, ticket_pdf_filename)
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        str(ticket.id),
        ticket.event_name,
        ticket.event_date,
        ticket.venue,
        ticket.ticket_type,
        ticket.price,
        ticket.quantity,
        ticket.seat_number,
        ticket.seller_id,
        ticket.ticket_pdf_filename
    ))