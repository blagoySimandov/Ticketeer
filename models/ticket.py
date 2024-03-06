import uuid
from .user import User
from ..database import int_to_decimal ,select_query
orderMap = {
    "Price Ascending": 'price ASC',
    'Price Descending': 'price DESC',
    'Soonest': 'event_date DESC',
    'Latest':'event_date ASC',
}
class Ticket:
    __tablename__ = 'tickets'
    def __init__(self, event_name, event_date, venue, ticket_type, price, quantity, seat_number, seller_id,ticket_filename ,id=uuid.uuid4()):
        self.event_name = event_name
        self.event_date = event_date
        self.venue = venue
        self.ticket_type = ticket_type
        self.price = price
        self.quantity = quantity
        self.seat_number = seat_number
        self.seller_id = seller_id
        self.id= id
        self.ticket_filename = ticket_filename
    def __str__(self):
        return f"Event: {self.event_name}\nDate: {self.event_date}\nVenue: {self.venue}\nType: {self.ticket_type}\nPrice: {self.price}\nQuantity: {self.quantity}\nSeat Number: {self.seat_number}\nSeller ID: {self.seller_id}\nID: {self.id}\nTicket Filename: {self.ticket_filename}"
    def formatted_price(self):
        return int_to_decimal(self.price)
    @classmethod
    def fetch_tickets(cls,db,page,page_size,order,type=None):
        fields = ['event_name', 'datetime(event_date) event_date', 'venue', 'ticket_type', 'price', 'quantity', 'seat_number', 'seller_id', 'ticket_filename', 'id']
        conditions = []
        if type != None:
            conditions.append(f'ticket_type="{type}"')
            print(conditions)
        query = select_query('tickets',fields, order_by=orderMap[order], limit=page_size, offset=page_size * page, *conditions)
        count_q = select_query('tickets', ("COUNT(*) as count",), *conditions)
        print(count_q)
        ticket_records = db.execute(query).fetchall()
        count = db.execute(count_q).fetchone()
        ticket_list = []
        for record in ticket_records:
            ticket_list.append(cls(
                event_name = record['event_name'],
                event_date = record['event_date'],
                venue = record['venue'],
                ticket_type = record['ticket_type'],
                price = record['price'],
                quantity = record['quantity'],
                seat_number = record['seat_number'],
                seller_id = record['seller_id'],
                id= record['id'],
                ticket_filename = record['ticket_filename'],
            ))
        return ticket_list, int(count['count'])
    def insert_ticket(ticket,db):
        db.execute("""
        INSERT INTO tickets (id,event_name, event_date, venue, ticket_type, price, quantity, seat_number, seller_id, ticket_filename)
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
        str(ticket.ticket_filename)
    ))
