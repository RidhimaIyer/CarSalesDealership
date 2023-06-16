from app import db 
from datetime import datetime 


class SaleLineItemModel(db.Model):
    __tablename__ = "invoice_line_item"

    invoice_line_item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    car_unit_price = db.Column(db.Float, nullable=False)
    item_tax = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)
    car_net_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    car_serial_no = db.Column(db.String, db.ForeignKey("cars.car_serial_no"), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice.invoice_id"))

    invoice = db.relationship("SaleModel", back_populates="invoice_line_item", lazy=True)

    def __init__(self, invoice_id, quantity, car_unit_price, item_tax, discount_percentage, car_net_price, car_serial_no ):
        self.invoice_id = invoice_id
        self.quantity = quantity
        self.car_unit_price = car_unit_price
        self.item_tax = item_tax
        self.discount_percentage = discount_percentage
        self.car_net_price = car_net_price
        self.car_serial_no = car_serial_no

    def toJson(self):
        ''' converts sale line item object to json'''
        return {
            "invoice_line_item_id": self.invoice_line_item_id,
            "invoice_id": self.invoice_id,
            "quantity": self.quantity,
            "car_unit_price": self.car_unit_price,
            "item_tax": self.item_tax,
            "discount_percentage": self.discount_percentage,
            "car_net_price": self.car_net_price,
            "car_serial_no": self.car_serial_no,
            "created_at": self.created_at,
            "modified_at": self.modified_at    
        }

    @classmethod 
    def add_invoice_line_item(cls, data_obj):
        '''classmethod to add invoice line item. it also calculates net_price based on tax and discount'''
        invoice_id = data_obj.get("invoice_id")
        cart = data_obj.get("cart")
        for item in cart:
            car_serial_no = item.get("car_serial_no")
            discount_percentage = item.get("discount_percentage", 0)
            quantity = item.get("quantity", 1)
            car_unit_price = item.get("car_unit_price")
            item_tax = item.get("state_tax")
            car_net_price = (float(car_unit_price) - float((discount_percentage % car_unit_price)) + float(item_tax)) * quantity
            new_invoice_line_item = cls(
                invoice_id = invoice_id,
                car_serial_no = car_serial_no,
                quantity = quantity,
                car_unit_price = car_unit_price,
                item_tax = item_tax,
                discount_percentage = discount_percentage,
                car_net_price = car_net_price              
            )

            db.session.add(new_invoice_line_item)

        db.session.commit()


    @classmethod
    def get_sale_line_item_by_invoice(cls,invoice_id):
        '''classmethod to get sale_line_item by invoice_id'''
        sale_line_objs = cls.query.filter_by(invoice_id=invoice_id).all()
        return [sale_line_obj.toJson() if sale_line_obj else None for sale_line_obj in sale_line_objs]
    
    @classmethod
    def get_sale_line_item_by_invoice_line_id(cls,invoice_line_item_id):
        '''classmethod to get sale_line_item by invoice_line_item_id'''
        sale_line_obj = cls.query.filter_by(invoice_line_item_id=invoice_line_item_id).first()
        return sale_line_obj.toJson() if sale_line_obj else None 
    

    @classmethod
    def update_sale_line(cls, invoice_line_item_id, req_data):
        '''classmethod to update sale line by invoice_line_item_id'''
        sale_line_obj = cls.query.filter_by(invoice_line_item_id=invoice_line_item_id).first()
        if sale_line_obj:
            for key, val in req_data.items():
                if hasattr(sale_line_obj, key):
                    setattr(sale_line_obj, key,val)
            db.session.commit()
            return True, sale_line_obj.toJson().get("invoice_id")
        return False, ""


    @classmethod
    def delete_sale_line(cls, invoice_line_item_id):
        '''classmethod to delete sale line item by invoice_line_item_id'''
        sale_line_obj = cls.query.filter_by(invoice_line_item_id = invoice_line_item_id)
        if sale_line_obj.first():
            invoice_id = sale_line_obj.first().toJson().get("invoice_id")
            sale_line_obj.delete()
            db.session.commit()
            return True, invoice_id
        return False , ""