from app import db 
from datetime import datetime 
# from app.models.dealerModel import DealerModel

class EmployeeModel(db.Model):
    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    dealer_id = db.Column(db.Integer, db.ForeignKey("dealers.dealer_id"))

    dealers = db.relationship("DealerModel", back_populates="employees", lazy=True)

    def __init__(self, first_name, last_name, dealer_id):
        self.first_name = first_name
        self.last_name = last_name 
        self.dealer_id = dealer_id 

    def toJson(self):
        '''converts employee object to json'''
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dealer_id": self.dealer_id,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }

    @classmethod 
    def add_employee(cls, data_obj):
        '''classmethod to add new employee'''
        new_employee = cls(
            first_name = data_obj.get("first_name"),
            last_name = data_obj.get("last_name"),
            dealer_id = data_obj.get("dealer_id"),
        )
        db.session.add(new_employee)
        db.session.commit()

    @classmethod
    def get_all_employees(cls):
        '''classmethod to list all employees'''
        employee_objs = cls.query.all()
        return [employee_obj.toJson() if employee_obj else None for employee_obj in employee_objs]

    @classmethod 
    def get_employee_by_id(cls, id):
        '''classmethod to get employee by id '''
        employee_obj = cls.query.filter_by(employee_id=id).first()
        return employee_obj.toJson() if employee_obj else None 

    @classmethod 
    def get_employee_by_dealer(cls, dealer_id):
        '''classmethod to get employee by dealer'''
        employee_objs = cls.query.filter_by(dealer_id = dealer_id).all()
        return [employee_obj.toJson() if employee_obj else None for employee_obj in employee_objs]

    @classmethod
    def update_employee(cls, employee_id, req_data):
        '''classmethod to update employee by employee_id'''
        employee_obj = cls.query.filter_by(employee_id=employee_id).first()
        if employee_obj:
            for key, val in req_data.items():
                if hasattr(employee_obj, key):
                    setattr(employee_obj, key, val)
            db.session.commit()
            return True 
        return False 

    @classmethod 
    def delete_employee(cls, employee_id):
        '''classmethod to delete employee by employee_id'''
        employee_obj = cls.query.filter_by(employee_id=employee_id)
        if employee_obj.first():
            employee_obj.delete()
            db.session.commit()
            return True 
        return False 
        