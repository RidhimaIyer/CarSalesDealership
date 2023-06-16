from app import db 
from datetime import datetime
# from app.models.stateTaxModel import StateTaxModel
# from app.models.employeeModel import EmployeeModel

class DealerModel(db.Model):
    __tablename__ = "dealers"

    dealer_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    web_url = db.Column(db.String, nullable=False)
    street_address = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    state_tax_id = db.Column(db.Integer, db.ForeignKey("state_tax.state_tax_id"))
        
    state_tax = db.relationship("StateTaxModel")
    employees = db.relationship("EmployeeModel", back_populates="dealers", lazy=True)

    __table_args__ = (db.UniqueConstraint("name", "web_url", name="_name_web_url_uc"),)

    

    def __init__(self, name, web_url, street_address, postal_code, city, state, state_tax_id):
        self.name = name
        self.web_url = web_url
        self.street_address = street_address
        self.postal_code = postal_code
        self.city = city 
        self.state = state
        self.state_tax_id = state_tax_id


    def toJson(self):
        '''converts dealer object to json'''
        return {
            "dealer_id": self.dealer_id,
            "name": self.name,
            "web_url": self.web_url,
            "street_address": self.street_address,
            "postal_code": self.postal_code,
            "city": self.city,
            "state": self.state,
            "state_tax_id": self.state_tax_id,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        } 

    @classmethod 
    def add_dealer(cls, data_obj):
        '''classmethod to add new dealer object'''
        new_dealer = cls(
            name = data_obj.get("name"),
            web_url = data_obj.get("web_url"),
            street_address = data_obj.get("street_address"),
            postal_code = data_obj.get("postal_code"),
            city = data_obj.get("city"),
            state= data_obj.get("state"), 
            state_tax_id = data_obj.get("state_tax_id")
        )
        db.session.add(new_dealer)
        db.session.commit()

    @classmethod 
    def get_all_dealers(cls):
        '''classmethod to get all dealers'''
        dealer_objs = cls.query.all()
        return [dealer_obj.toJson() if dealer_obj else None for dealer_obj in dealer_objs]

    @classmethod 
    def get_dealer_by_id(cls, dealer_id):
        '''classmethod to get dealer by id '''
        dealer_obj = cls.query.filter_by(dealer_id=dealer_id).first()
        return dealer_obj.toJson() if dealer_obj else None 

    @classmethod
    def get_dealer_by_name_url(cls, name, web_url):
        '''classmethod to get dealer by name and web_url'''
        dealer_obj = cls.query.filter_by(name=name).filter_by(web_url=web_url).first()
        return dealer_obj.toJson() if dealer_obj else None 
 
    @classmethod 
    def get_dealers_by_state(cls, state):
        '''classmethod to get dealer by state'''
        print(state)
        dealer_objs = cls.query.filter_by(state=state).all()
        print(dealer_objs)
        return [dealer_obj.toJson() if dealer_obj else None for dealer_obj in dealer_objs]

    @classmethod 
    def update_dealer(cls, dealer_id, req_data):
        '''classmethod to update dealer by dealer_id'''
        dealer_obj = cls.query.filter_by(dealer_id = dealer_id).first()
        if dealer_obj:
            for key,val in req_data.items():
                if hasattr(dealer_obj, key):
                    setattr(dealer_obj, key, val)
            db.session.commit()
            return True 
        return False 

    @classmethod 
    def delete_dealer(cls, dealer_id):
        '''classmethod to delete dealer by dealer_id'''
        dealer_obj = cls.query.filter_by(dealer_id = dealer_id)
        if dealer_obj.first():
            dealer_obj.delete()
            db.session.commit()
            return True 
        return False 
    