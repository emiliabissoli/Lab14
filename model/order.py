from datetime import datetime
from dataclasses import dataclass


@dataclass
class Order:
    order_id:int
    customer_id: int
    order_status: int
    order_date: datetime
    required_date: datetime
    shipped_date: datetime
    store_id: int
    staff_id: int

    def __hash__(self):
        return hash(self.order_id)

    def __eq__(self, other):
        if isinstance(other, Order):
            return self.order_id == other.order_id
        elif isinstance(other, int):
            return self.order_id == other
        else:
            return False

    def __str__(self):
        return f"{self.order_id}"
