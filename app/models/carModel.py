from app import db 
from datetime import datetime

class CarModel(db.Model):
    __tablename__ = "cars"

    car_id = db.Column(db.Integer, primary_key=True)
    car_serial_no = db.Column(db.String, unique = True, nullable=False)
    make = db.Column(db.String)
    model = db.Column(db.String)
    year = db.Column(db.String)
    color = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, car_serial_no, price, make=None, model=None, year=None, color=None):
        self.car_serial_no = car_serial_no
        self.price = price 
        self.make = make 
        self.model = model
        self.year = year 
        self.color = color 
    
    def toJson(self):
        ''' Converts Car Object to json'''
        return {
            "car_id": self.car_id,
            "car_serial_no": self.car_serial_no,
            "make": self.make,
            "model": self.model,
            "year":  self.year,
            "color": self.color,
            "price": self.price,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }

    @classmethod 
    def  add_car(cls, data_obj):
        ''' Classemethod to add new car object'''
        new_car = cls(
            car_serial_no = data_obj.get("car_serial_no"),
            make = data_obj.get("make", None),
            model = data_obj.get("model", None),
            year = data_obj.get("year", None),
            color = data_obj.get("color", None),
            price = data_obj.get("price")
        )
        db.session.add(new_car)
        db.session.commit()

    @classmethod 
    def get_car_by_serial(cls, car_serial_no):
        '''Classmethod to get car object based on car_serial_no'''
        car_obj = cls.query.filter_by(car_serial_no = car_serial_no).first()
        return car_obj.toJson() if car_obj else None 

    @classmethod 
    def get_all_cars(cls):
        '''classmethod to get all cars in db'''
        car_list = cls.query.all()
        return [car.toJson() if car else None for car in car_list ]

    @classmethod 
    def update_car_record(cls, car_serial_no, req_data):
        '''classmethod to update cars based on serial_no '''
        car_obj = cls.query.filter_by(car_serial_no=car_serial_no).first()
        
        if car_obj:
            for key,val in req_data.items():
                if hasattr(car_obj, key):
                    setattr(car_obj, key, val)
            db.session.commit()
            return True 
        
        return False 

    @classmethod 
    def delete_car(cls, car_serial_no):
        '''classmethod to delete car based on serial_no'''
        car_obj = cls.query.filter_by(car_serial_no=car_serial_no)
        if car_obj.first():
            car_obj.delete()
            db.session.commit()
            return True 
        return False 




    
        
