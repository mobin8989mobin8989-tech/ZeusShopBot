# ==========================================================
# ZeusShopBot PRO
# modules/panel.py
# 3X-UI Panel Manager
# Fixed API Token Version
# ==========================================================


import requests
import json
import uuid
import time
import urllib3


from config import (
    PANEL_URL,
    PANEL_TOKEN,
    INBOUND_ID
)



urllib3.disable_warnings()





class Panel:



    def __init__(self):

        self.url = PANEL_URL.rstrip("/")


        self.session = requests.Session()


        self.session.headers.update({

            "Authorization": f"Bearer {PANEL_TOKEN}",

            "Content-Type": "application/json"

        })





    # ======================================================
    # UUID
    # ======================================================

    def generate_uuid(self):

        return str(uuid.uuid4())





    # ======================================================
    # Username
    # ======================================================

    def generate_username(self, telegram_id):

        return (

            f"zeus_{telegram_id}_"

            f"{int(time.time())}"

        )






    # ======================================================
    # Get Inbounds
    # ======================================================

    def get_inbounds(self):


        r = self.session.get(

            f"{self.url}/panel/api/inbounds/list",

            verify=False,

            timeout=20

        )


        data = r.json()



        if not data.get("success"):

            raise Exception(

                data.get(

                    "msg",

                    "Get inbound failed"

                )

            )



        return data.get("obj", [])







    # ======================================================
    # Selected Inbound
    # ======================================================

    def get_inbound(self):


        for inbound in self.get_inbounds():


            if int(inbound["id"]) == int(INBOUND_ID):

                return inbound




        raise Exception(

            "Inbound پیدا نشد"

        )







    # ======================================================
    # Create Service
    # ======================================================

    def create_service(

        self,

        telegram_id,

        days,

        traffic_gb

    ):


        inbound = self.get_inbound()



        settings = inbound["settings"]



        if isinstance(settings, str):

            settings = json.loads(settings)





        client = {


            "id": self.generate_uuid(),


            "email": self.generate_username(

                telegram_id

            ),


            "tgId": str(telegram_id),


            "enable": True,


            "expiryTime":

                int(

                    time.time()

                    +

                    days * 86400

                ) * 1000,


            "totalGB":

                traffic_gb *

                1024 *

                1024 *

                1024,


            "limitIp": 0,


            "reset": 0


        }





        clients = settings.get(

            "clients",

            []

        )



        clients.append(client)



        settings["clients"] = clients





        payload = {


            "id": inbound["id"],


            "settings":

                json.dumps(settings)

        }





        r = self.session.post(


            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",


            json=payload,


            verify=False,


            timeout=30

        )





        data = r.json()



        if not data.get("success"):


            raise Exception(

                data.get(

                    "msg",

                    "Create failed"

                )

            )







        return {


            "username": client["email"],


            "uuid": client["id"],


            "subscription_url":

                self.create_link(

                    inbound,

                    client

                )

        }







    # ======================================================
    # VLESS Link
    # ======================================================

    def create_link(

        self,

        inbound,

        client

    ):


        host = (

            self.url

            .replace(

                "https://",

                ""

            )

            .replace(

                "http://",

                ""

            )

            .split("/")[0]

        )



        return (

            f"vless://{client['id']}@"

            f"{host}:{inbound['port']}"

            f"?encryption=none"

            f"#{client['email']}"

        )







    # ======================================================
    # User Services
    # ======================================================

    def get_user_services(

        self,

        telegram_id

    ):


        inbound = self.get_inbound()



        settings = inbound["settings"]



        if isinstance(settings,str):

            settings=json.loads(settings)





        result=[]



        for c in settings.get("clients",[]):


            if c.get("tgId")==str(telegram_id):


                result.append(c)



        return result
