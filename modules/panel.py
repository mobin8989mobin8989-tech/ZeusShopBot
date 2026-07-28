# ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI Panel Manager
# ==========================================================


import requests
import json
import uuid
import time
import urllib3
from urllib.parse import urlencode


from config import (
    PANEL_URL,
    PANEL_USERNAME,
    PANEL_PASSWORD,
    INBOUND_ID
)


urllib3.disable_warnings()





class Panel:


    def __init__(self):

        self.url = PANEL_URL.rstrip("/")

        self.session = requests.Session()

        self.login()





    # ======================================================
    # Login
    # ======================================================

    def login(self):

        response = self.session.post(

            f"{self.url}/login",

            data={

                "username": PANEL_USERNAME,

                "password": PANEL_PASSWORD

            },

            verify=False,

            timeout=20

        )


        if response.status_code != 200:

            raise Exception(
                "❌ 3X-UI Login Failed"
            )


        return True





    # ======================================================
    # Generate UUID
    # ======================================================

    def generate_uuid(self):

        return str(uuid.uuid4())






    # ======================================================
    # Generate Username
    # ======================================================

    def generate_username(

        self,

        telegram_id

    ):

        return (

            f"zeus_{telegram_id}_"

            f"{int(time.time())}"

        )






    # ======================================================
    # Get Inbounds
    # ======================================================

    def get_inbounds(self):


        response = self.session.get(

            f"{self.url}/panel/api/inbounds/list",

            verify=False,

            timeout=20

        )


        data = response.json()



        if not data.get("success"):

            raise Exception(

                "❌ Cannot get inbounds"

            )



        return data.get("obj", [])






    # ======================================================
    # Get Selected Inbound
    # ======================================================

    def get_inbound(self):


        inbounds = self.get_inbounds()



        for inbound in inbounds:


            if int(inbound["id"]) == int(INBOUND_ID):


                return inbound




        raise Exception(

            "❌ Inbound ID not found"

        )
            # ======================================================
    # Create Client
    # ======================================================

    def create_client(

        self,

        telegram_id,

        days,

        traffic_gb

    ):


        client_uuid = self.generate_uuid()



        username = self.generate_username(

            telegram_id

        )



        expire_time = int(

            time.time()

            +

            (days * 86400)

        ) * 1000





        total_bytes = (

            traffic_gb

            *

            1024

            *

            1024

            *

            1024

        )





        client = {


            "id": client_uuid,


            "email": username,


            # ذخیره آیدی تلگرام کاربر

            "tgId": str(telegram_id),



            "enable": True,


            "totalGB": total_bytes,


            "expiryTime": expire_time,


            "limitIp": 0,


            "reset": 0


        }





        return client









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





        settings = json.loads(

            inbound["settings"]

        )





        client = self.create_client(

            telegram_id,

            days,

            traffic_gb

        )





        clients = settings.get(

            "clients",

            []

        )



        clients.append(

            client

        )



        settings["clients"] = clients






        payload = {


            "id": inbound["id"],


            "settings": json.dumps(

                settings

            )


        }






        response = self.session.post(


            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",


            json=payload,


            verify=False,


            timeout=30


        )






        data = response.json()






        if not data.get("success"):



            raise Exception(


                data.get(

                    "msg",

                    "Create Client Failed"

                )

            )






        link = self.create_vless_link(

            inbound,

            client

        )







        return {


            "username": client["email"],


            "uuid": client["id"],


            "subscription_url": link


        }
            # ======================================================
    # Create VLESS Link
    # ======================================================

    def create_vless_link(

        self,

        inbound,

        client

    ):



        # گرفتن هاست از آدرس پنل

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





        # تنظیمات شبکه

        stream = json.loads(

            inbound.get(

                "streamSettings",

                "{}"

            )

        )





        network = stream.get(

            "network",

            "tcp"

        )





        security = stream.get(

            "security",

            "none"

        )





        params = {


            "type": network,


            "encryption": "none",


            "security": security


        }





        # اگر TCP بود

        tcp_settings = stream.get(

            "tcpSettings",

            {}

        )



        if tcp_settings:



            header = tcp_settings.get(

                "header",

                {}

            )



            if header.get("type"):



                params["headerType"] = header["type"]






        # اگر Host وجود داشت

        if "host" in tcp_settings:



            params["host"] = tcp_settings["host"]





        query = urlencode(params)






        remark = inbound.get(

            "remark",

            "Zeus"

        )







        link = (


            f"vless://{client['id']}@"


            f"{host}:{inbound['port']}?"


            f"{query}"


            f"#{remark}"


        )





        return link











    # ======================================================
    # Get User Services
    # ======================================================

    def get_user_services(

        self,

        telegram_id

    ):



        inbound = self.get_inbound()





        settings = json.loads(

            inbound["settings"]

        )





        result = []





        for client in settings.get(

            "clients",

            []

        ):



            if client.get(

                "tgId"

            ) == str(telegram_id):



                result.append(

                    client

                )





        return result










    # ======================================================
    # Delete Service
    # ======================================================

    def delete_service(

        self,

        username

    ):



        inbound = self.get_inbound()





        settings = json.loads(

            inbound["settings"]

        )





        clients = settings.get(

            "clients",

            []

        )





        settings["clients"] = [

            c for c in clients

            if c.get("email") != username

        ]






        response = self.session.post(



            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",



            json={


                "id": inbound["id"],



                "settings": json.dumps(

                    settings

                )


            },



            verify=False,

            timeout=30

        )





        return response.json()
            # ======================================================
    # Renew Service
    # ======================================================

    def renew_service(

        self,

        username,

        days,

        traffic_gb

    ):



        inbound = self.get_inbound()





        settings = json.loads(

            inbound["settings"]

        )





        found = False






        for client in settings.get(

            "clients",

            []

        ):



            if client.get(

                "email"

            ) == username:



                client["expiryTime"] = int(

                    time.time()

                    +

                    (days * 86400)

                ) * 1000






                client["totalGB"] = (

                    traffic_gb

                    *

                    1024

                    *

                    1024

                    *

                    1024

                )




                found = True

                break






        if not found:


            raise Exception(

                "❌ Service not found"

            )






        response = self.session.post(



            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",



            json={


                "id": inbound["id"],



                "settings": json.dumps(

                    settings

                )


            },



            verify=False,

            timeout=30

        )





        return response.json()







    # ======================================================
    # Get All Clients
    # ======================================================

    def get_all_clients(self):


        inbound = self.get_inbound()



        settings = json.loads(

            inbound["settings"]

        )



        return settings.get(

            "clients",

            []

        )
