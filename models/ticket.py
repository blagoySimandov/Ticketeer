class Ticket:
    def __init__(self, event_name, event_date, venue, ticket_type, price, quantity, seat_number, seller_id, ticket_pdf_filename):
        self.event_name = event_name
        self.event_date = event_date
        self.venue = venue
        self.ticket_type = ticket_type
        self.price = price
        self.quantity = quantity
        self.seat_number = seat_number
        self.seller_id = seller_id
        self.ticket_pdf_filename = ticket_pdf_filename