from app import db 
from datetime import datetime

class DealerInventoryModel(db.Model):
    __tablename__ = "dealer_inventory"

    dealer_inventory_id = db.Column(db.Integer, primary_key=True)
    car_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    car_serial_no = db.Column(db.String, db.ForeignKey("cars.car_serial_no"), nullable=False)
    dealer_id = db.Column(db.Integer, db.ForeignKey("dealers.dealer_id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("car_serial_no", "dealer_id", name="_car_dealer_uc"),)

    def __init__(self, car_serial_no, dealer_id, car_count):
        self.car_serial_no = car_serial_no 
        self.dealer_id = dealer_id
        self.car_count = car_count 

    def toJson(self):
        '''Converts dealer Inventory object to json'''
        return {
            "dealer_inventory_id": self.dealer_inventory_id,
            "car_serial_no": self.car_serial_no,
            "dealer_id": self.dealer_id,
            "car_count": self.car_count,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }

    @classmethod
    def add_dealer_inventory(cls, data_obj):
        '''classmethod to add new dealer inventory object'''
        new_dealer_inventory = cls(
            car_serial_no = data_obj.get("car_serial_no"),
            dealer_id = data_obj.get("dealer_id"),
            car_count = data_obj.get("car_count")
        )
        db.session.add(new_dealer_inventory)
        db.session.commit()

    @classmethod 
    def car_dealer_record_exists(cls, car_serial_no, dealer_id):
        '''classmethod to check if dealer object with same car_serial_no and dealer_id exists in db'''
        dealer_inventory_obj = cls.query.filter_by(car_serial_no=car_serial_no).filter_by(dealer_id=dealer_id).first()
        if dealer_inventory_obj:
            return True 
        return False 


    @classmethod 
    def get_all_inventory(cls):
        '''classmethod to get all inventories'''
        inventory_objs = cls.query.all()
        return [inventory.toJson() if inventory else None for inventory in inventory_objs]

    @classmethod 
    def get_inventory_by_dealer(cls, dealer_id):
        '''classmethod to get inventory by dealer_id'''
        inventory_objs = cls.query.filter_by(dealer_id=dealer_id).all()
        return [inventory.toJson() if inventory else None for inventory in inventory_objs]

    @classmethod
    def get_inventory_by_dealer_car(cls, dealer_id, car_serial_no):
        '''classmethod to get inventory by dealer_id and car_serial_no'''
        inventory_obj = cls.query.filter_by(dealer_id=dealer_id).filter_by(car_serial_no=car_serial_no).first()
        return inventory_obj.toJson() if inventory_obj else None 

    @classmethod 
    def update_dealer_inventory_count(cls, dealer_id, car_serial_no, data_obj):
        '''classmethod to update dealer by dealer_id and car_serial_no'''
        inventory_obj = cls.query.filter_by(dealer_id=dealer_id).filter_by(car_serial_no=car_serial_no).first()
        if inventory_obj:
            if "car_count" in data_obj:
                setattr(inventory_obj, "car_count", data_obj.get("car_count"))
            db.session.commit()
            return True
        return False 

    @classmethod 
    def delete_dealer_inventory(cls, dealer_id, car_serial_no):
        '''classmethod to delete inventory by dealer_id and car_serial_no'''
        inventory_obj = cls.query.filter_by(dealer_id=dealer_id).filter_by(car_serial_no=car_serial_no)
        if inventory_obj.first():
            inventory_obj.delete()
            db.session.commit()
            return True 
        return False 
