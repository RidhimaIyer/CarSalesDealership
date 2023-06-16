from app import db 
from datetime import datetime

class CustomerModel(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key = True)
    phone = db.Column(db.String, nullable=False)
    email_id = db.Column(db.String, nullable=False, unique=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)
    first_name= db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

    def __init__(self, phone, email_id, ssn,  first_name, last_name, address):
        self.phone = phone 
        self.email_id = email_id
        self.ssn = ssn 
        self.first_name = first_name 
        self.last_name = last_name 
        self.address = address 

    def toJson(self):
        ''' Converts Customer Object to json'''
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email_id": self.email_id,
            "address": self.address,
            "ssn": self.ssn,
            "created_at": self.created_at,
            "modified_at": self.modified_at

        }

    @classmethod 
    def  add_customer(cls, data_obj):
        '''classmethod to add new customer object'''
        new_customer = cls(
            phone = data_obj.get("phone"),
            email_id = data_obj.get("email_id"),
            ssn = data_obj.get("ssn"),
            first_name = data_obj.get("first_name"),
            last_name = data_obj.get("last_name"),
            address = data_obj.get("address")
        )
        db.session.add(new_customer)
        db.session.commit()

    @classmethod 
    def get_customer_by_email(cls, email_id):
        '''classmethod to get customer by email id '''
        customer_obj = cls.query.filter_by(email_id = email_id).first()
        return customer_obj.toJson() if customer_obj else None 

    @classmethod
    def get_all_customers(cls):
        '''classmethod to get all customers'''
        customer_list = cls.query.all()
        return [customer.toJson() if customer else None for customer in customer_list]

    @classmethod 
    def get_customer_by_id(cls, customer_id):
        '''classmethod to get customer by customer_id'''
        customer_obj = cls.query.filter_by(customer_id=customer_id).first()
        return customer_obj.toJson() if customer_obj else None 


    @classmethod
    def update_customer_record(cls, customer_id, req_data):
        '''classmethod to update customer record by customer_id'''
        customer_obj = cls.query.filter_by(customer_id=customer_id).first()
        if customer_obj:
            for key, val in req_data.items():
                if hasattr(customer_obj, key):
                    setattr(customer_obj, key,val)
            db.session.commit()
            return True 
        return False 

    @classmethod
    def delete_customer(cls, customer_id):
        '''classmethod to delete customer by customer_id'''
        customer_obj = cls.query.filter_by(customer_id = customer_id)
        if customer_obj.first():
            customer_obj.delete()
            db.session.commit()
            return True 
        return False 

