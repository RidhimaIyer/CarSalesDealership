from app import db 
from datetime import datetime 

class SaleModel(db.Model):
    __tablename__ = "invoice"

    invoice_id = db.Column(db.Integer, primary_key = True)
    date_of_purchase = db.Column(db.DateTime, nullable=False)
    net_tax = db.Column(db.Float)
    net_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
    dealer_id = db.Column(db.Integer, db.ForeignKey("dealers.dealer_id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id"))

    invoice_line_item = db.relationship("SaleLineItemModel", back_populates="invoice", lazy=True)

    def __init__(self, date_of_purchase, dealer_id, customer_id, employee_id,net_tax, net_price):
        self.date_of_purchase = date_of_purchase
        self.dealer_id = dealer_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.net_tax = net_tax
        self.net_price = net_price 

    def toJson(self):
        '''converts sale object to json'''
        return {
            "invoice_id": self.invoice_id,
            "date_of_purchase": self.date_of_purchase,
            "net_tax": self.net_tax,
            "net_price": self.net_price,
            "dealer_id": self.dealer_id,
            "customer_id": self.customer_id,
            "employee_id": self.customer_id,
            # "invoice_line_item": self.invoice_line_item,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }

    @classmethod
    def add_invoice(cls, data_obj):
        '''classmethod to add invoice object'''
        new_invoice = cls(
            date_of_purchase = data_obj.get("date_of_purchase"),
            net_tax = data_obj.get("net_tax", 0),
            net_price = data_obj.get("net_price", 0),
            dealer_id = data_obj.get("dealer_id"),
            customer_id = data_obj.get("customer_id"),
            employee_id = data_obj.get("employee_id")
        )
        db.session.add(new_invoice)
        db.session.commit()

    @classmethod 
    def get_invoice_by_id(cls, invoice_id):
        '''classmethod to get invoice by id'''
        invoice_obj = cls.query.filter_by(invoice_id = invoice_id).first()
        return invoice_obj.toJson() if invoice_obj else None 

    @classmethod 
    def get_invoice_by_date(cls, dealer_id, start_dt, end_dt):
        '''classmethod to get invoice by dealer_id and date_of_purchase range '''
        invoice_objs = cls.query.filter_by(dealer_id=dealer_id).filter(SaleModel.date_of_purchase >= start_dt).filter(SaleModel.date_of_purchase <= end_dt).all()
        return [invoice_obj.toJson() if invoice_obj else None for invoice_obj in invoice_objs]

    @classmethod 
    def get_invoice_by_cust_date(cls, dealer_id, customer_id, start_dt, end_dt):
        '''classmethod to get invocie by dealer_id for a cusotmer based on date_of_purchase range '''
        invoice_objs = cls.query.filter_by(dealer_id=dealer_id).filter_by(customer_id=customer_id).filter(SaleModel.date_of_purchase >= start_dt).filter(SaleModel.date_of_purchase <= end_dt).all()
        return [invoice_obj.toJson() if invoice_obj else None for invoice_obj in invoice_objs]

    @classmethod 
    def update_invoice(cls, invoice_id, req_data):
        '''classmethod to update invoice'''
        invoice_obj = cls.query.filter_by(invoice_id = invoice_id).first()
        if invoice_obj:
            for key,val in req_data.items():
                if key == "date_of_purchase":
                    val = datetime.strptime(val, "%Y-%m-%d")
                if hasattr(invoice_obj, key):
                    setattr(invoice_obj, key,val)
            db.session.commit()
            return True 
        return False 

    @classmethod 
    def delete_invoice(cls, invoice_id):
        '''classmethod to delte invoice'''
        invoice_obj = cls.query.filter_by(invoice_id=invoice_id)
        if invoice_obj.first():
            invoice_obj.delete()
            db.session.commit()
            return True 
        return False 
