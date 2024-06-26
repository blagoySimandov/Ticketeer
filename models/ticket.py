import uuid
from ..database import int_to_decimal ,select_query,select_in_query
orderMap = {
    "Price Ascending": 'price ASC',
    'Price Descending': 'price DESC',
    'Soonest': 'event_date DESC',
    'Latest':'event_date ASC',
}
class Ticket:
    __tablename__ = 'tickets'
    def __init__(self, event_name, event_date, venue, ticket_type, price, seat_number, seller_id,ticket_filename ,id=uuid.uuid4()):
        self.event_name = event_name
        self.event_date = event_date
        self.venue = venue
        self.ticket_type = ticket_type
        self.price = price
        self.seat_number = seat_number
        self.seller_id = seller_id
        self.id = id
        self.ticket_filename = ticket_filename
    def __str__(self):
        return f"Event: {self.event_name}\nDate: {self.event_date}\nVenue: {self.venue}\nType: {self.ticket_type}\nPrice: {self.price}\nQuantity: {self.quantity}\nSeat Number: {self.seat_number}\nSeller ID: {self.seller_id}\nID: {self.id}\nTicket Filename: {self.ticket_filename}"
    def formatted_price(self):
        return int_to_decimal(self.price)
    @classmethod
    def fetch_tickets(cls,db,page,page_size,order,text,t_type=None):
        fields = ['event_name', 'datetime(event_date) event_date', 'venue', 'ticket_type', 'price', 'seat_number', 'seller_id', 'ticket_filename', 'id']
        conditions = ['sold!=TRUE']
        like_conditions = []
        if t_type != None:
            conditions.append(f'ticket_type={t_type}')
        if text != None and text != "":
            like_conditions.append(f"event_name LIKE '{text}%'")
            like_conditions.append(f"event_name LIKE '%{text}'")
            like_conditions.append(f"event_name LIKE '%{text}%'")

        query,params = select_query('tickets',fields, order_by=orderMap[order], limit=page_size, offset=page_size * page, like_conditions=like_conditions,*conditions)
        count_q,p = select_query('tickets', ("COUNT(*) as count",),like_conditions=like_conditions, *conditions)
        print(query)
        print(params)
        ticket_records = db.execute(query,params).fetchall()
        count = db.execute(count_q,p).fetchone()

        ticket_list = []
        for record in ticket_records:
            print(record['price'])
            ticket_list.append(cls(
                event_name = record['event_name'],
                event_date = record['event_date'],
                venue = record['venue'],
                ticket_type = record['ticket_type'],
                price = record['price'],
                seat_number = record['seat_number'],
                seller_id = record['seller_id'],
                id= record['id'],
                ticket_filename = record['ticket_filename'],
            ))
        return ticket_list, int(count['count'])
    @classmethod
    def fetch_tickets_by_ids(cls,db,ids):
        fields = ['event_name', 'datetime(event_date) event_date', 'venue', 'ticket_type', 'price', 'seat_number', 'seller_id', 'ticket_filename', 'id']
        ticket_records,params = select_in_query(ids,"tickets",fields)
        ticket_records=db.execute(ticket_records,params).fetchall()
        ticket_list=[]               
        for record in ticket_records:
            ticket_list.append(cls(
                event_name = record['event_name'],
                event_date = record['event_date'],
                venue = record['venue'],
                ticket_type = record['ticket_type'],
                price = record['price'],
                seat_number = record['seat_number'],
                seller_id = record['seller_id'],
                id= record['id'],
                ticket_filename = record['ticket_filename'],
            ))
        return ticket_list
    #TODO: Use a method instead of composition principles. (use self)
    def insert_ticket(ticket,db):
        db.execute("""
        INSERT INTO tickets (id,event_name, event_date, venue, ticket_type, price, seat_number, seller_id, ticket_filename,sold)
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?,'FALSE')
        """, (
        str(ticket.id),
        ticket.event_name,
        ticket.event_date,
        ticket.venue,
        ticket.ticket_type,
        ticket.price,
        ticket.seat_number,
        ticket.seller_id,
        str(ticket.ticket_filename)
    ))
    def change_ticket_status(self,db):
        id = self.id
        db.execute("""
            UPDATE tickets SET sold='TRUE' where id = ? 
            """,(id,))
def sum_prices_of_tickets(t_list:list)->int:
    sum = 0
    for t in t_list:
        # Perform some processing on each object in the list
        sum+=int(t.price)
    return sum
