from app import db 
from datetime import datetime 

class StateTaxModel(db.Model):
    __tablename__ = "state_tax"

    state_tax_id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String, nullable=False, unique=True)
    tax = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, state, tax):
        self.state = state
        self.tax = tax 

    def toJson(self):
        '''converts state tax object to json'''
        return {
            "state_tax_id": self.state_tax_id,
            "state": self.state,
            "tax": self.tax,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }

    @classmethod 
    def add_state_tax(cls, data_obj):
        '''classmethod to add new state tax info'''
        new_state_tax = cls(
            state = data_obj.get("state").lower(),
            tax = data_obj.get("tax")
        )
        db.session.add(new_state_tax)
        db.session.commit()

    @classmethod 
    def get_all_state_tax(cls):
        '''classmethod to get all state tax info'''
        state_tax_objs = cls.query.all()
        return [state_tax_obj.toJson() if state_tax_obj else None for state_tax_obj in state_tax_objs]

    @classmethod 
    def get_state_by_id(cls, state_tax_id):
        '''classmethod to get state tax info by state_tax_id'''
        state_tax_obj = cls.query.filter_by(state_tax_id= state_tax_id).first()
        return state_tax_obj.toJson() if state_tax_obj else None 


    @classmethod 
    def get_state_tax(cls, state):
        '''classmethod to get state tax info by state'''
        state_tax_obj = cls.query.filter_by(state=state.lower()).first()
        return state_tax_obj.toJson() if state_tax_obj else None 

    @classmethod 
    def update_state_tax(cls, state_tax_id, data_obj):
        '''classmethod to update state tax info '''
        state_tax_obj = cls.query.filter_by(state_tax_id=state_tax_id).first()
        if state_tax_obj:
            setattr(state_tax_obj, "tax", data_obj.get("tax"))
            db.session.commit()
            return True 
        return False 

    @classmethod 
    def delete_state_tax(cls, state_tax_id):
        '''classmethod to delete state tax info'''
        state_tax_obj = cls.query.filter_by(state_tax_id=state_tax_id)
        if state_tax_obj.first():
            state_tax_obj.delete()
            db.session.commit()
            return True 
        return False 
