# =====================================================
# ZeusShopBot
# modules/orders.py
# =====================================================

from datetime import datetime


class OrderManager:

    def __init__(self):
        self.orders = []

    def create_order(
        self,
        user_id,
        plan,
        price,
        status="pending"
    ):

        order = {
            "id": len(self.orders) + 1,
            "user_id": user_id,
            "plan": plan,
            "price": price,
            "status": status,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.orders.append(order)

        return order

    def get_orders(self):

        return self.orders

    def get_user_orders(self, user_id):

        return [
            o for o in self.orders
            if o["user_id"] == user_id
        ]

    def get_order(self, order_id):

        for order in self.orders:

            if order["id"] == order_id:
                return order

        return None

    def complete_order(self, order_id):

        order = self.get_order(order_id)

        if order:

            order["status"] = "completed"

        return order

    def cancel_order(self, order_id):

        order = self.get_order(order_id)

        if order:

            order["status"] = "cancelled"

        return order
