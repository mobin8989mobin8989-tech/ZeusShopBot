# ==========================================================
# ZeusShopBot
# modules/support.py
# ==========================================================

from datetime import datetime


class SupportManager:

    def __init__(self):

        self.tickets = []

    def create_ticket(

        self,

        user_id,

        message

    ):

        ticket = {

            "id": len(self.tickets) + 1,

            "user_id": user_id,

            "message": message,

            "status": "open",

            "answer": None,

            "created_at": datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        }

        self.tickets.append(ticket)

        return ticket

    def get_ticket(

        self,

        ticket_id

    ):

        for ticket in self.tickets:

            if ticket["id"] == ticket_id:

                return ticket

        return None

    def get_all_tickets(self):

        return self.tickets

    def answer_ticket(

        self,

        ticket_id,

        answer

    ):

        ticket = self.get_ticket(ticket_id)

        if ticket:

            ticket["status"] = "closed"

            ticket["answer"] = answer

        return ticket

    def user_tickets(

        self,

        user_id

    ):

        return [

            ticket

            for ticket in self.tickets

            if ticket["user_id"] == user_id

        ]


support = SupportManager()
