# ==========================================================
# ZeusShopBot
# modules/plans.py
# ==========================================================

from config import PLANS


class PlanManager:

    def get_all(self):

        return PLANS

    def get(
        self,
        plan_key
    ):

        return PLANS.get(plan_key)

    def exists(
        self,
        plan_key
    ):

        return plan_key in PLANS

    def price(
        self,
        plan_key
    ):

        plan = self.get(plan_key)

        if plan:

            return plan["price"]

        return 0

    def volume(
        self,
        plan_key
    ):

        plan = self.get(plan_key)

        if plan:

            return plan["volume"]

        return 0

    def days(
        self,
        plan_key
    ):

        plan = self.get(plan_key)

        if plan:

            return plan["days"]

        return 0

    def name(
        self,
        plan_key
    ):

        plan = self.get(plan_key)

        if plan:

            return plan["name"]

        return "Unknown Plan"


plans = PlanManager()
