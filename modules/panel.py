# ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI Panel Manager PRO
# ==========================================================


import requests
import json
import uuid
import time
import urllib3


from config import (
    PANEL_URL,
    PANEL_USERNAME,
    PANEL_PASSWORD,
    PANEL_TOKEN,
    INBOUND_ID
)


urllib3.disable_warnings()



class Panel:


    def __init__(self):

        self.url = PANEL_URL.rstrip("/")

        self.session = requests.Session()

        self.headers = {}


        self.login()





    # ======================================================
    # Login
    # ======================================================

    def login(self):


        # اگر توکن داریم
        if PANEL_TOKEN:


            self.headers = {

                "Authorization":
                f"Bearer {PANEL_TOKEN}"

            }


            return True





        # ورود معمولی
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
    # Request Helper
    # ======================================================

    def request(

        self,

        method,

        url,

        **kwargs

    ):


        kwargs["verify"] = False


        if self.headers:

            kwargs["headers"] = self.headers



        response = self.session.request(

            method,

            url,

            timeout=30,

            **kwargs

        )



        try:

            return response.json()


        except:


            raise Exception(

                response.text

            )





    # ======================================================
    # UUID
    # ======================================================

    def generate_uuid(self):

        return str(uuid.uuid4())





    # ======================================================
    # Username
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


        data = self.request(

            "GET",

            f"{self.url}/panel/api/inbounds/list"

        )



        if not data.get("success"):


            raise Exception(

                data.get(

                    "msg",

                    "❌ Cannot get inbounds"

                )

            )



        return data.get(

            "obj",

            []

        )







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
# Create Client Data
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

            days * 86400

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





        try:


            settings = json.loads(

                inbound["settings"]

            )


        except:


            raise Exception(

                "❌ Invalid inbound settings"

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


            "id":

            inbound["id"],



            "settings":

            json.dumps(settings)

        }






        data = self.request(

            "POST",

            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",

            json=payload

        )





        if not data.get("success"):


            raise Exception(

                data.get(

                    "msg",

                    "❌ Create Client Failed"

                )

            )





        return {


            "username":

            client["email"],



            "uuid":

            client["id"]

            }
        # ======================================================
# Create VLESS Link
# ======================================================


    def create_vless_link(

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



        try:

            stream = json.loads(

                inbound.get(

                    "streamSettings",

                    "{}"

                )

            )

        except:

            stream = {}





        network = stream.get(

            "network",

            "tcp"

        )



        security = stream.get(

            "security",

            "none"

        )





        params = {


            "type":

            network,


            "encryption":

            "none",


            "security":

            security

        }






        query = "&".join(

            [

                f"{k}={v}"

                for k,v in params.items()

            ]

        )





        remark = inbound.get(

            "remark",

            "Zeus"

        )





        return (

            f"vless://{client['id']}@"

            f"{host}:"

            f"{inbound['port']}?"

            f"{query}"

            f"#{remark}"

        )








# ======================================================
# Get User Services
# ======================================================


    def get_user_services(

        self,

        telegram_id

    ):


        inbound = self.get_inbound()



        try:

            settings = json.loads(

                inbound["settings"]

            )

        except:

            return []





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





        payload = {


            "id":

            inbound["id"],



            "settings":

            json.dumps(settings)

        }






        return self.request(

            "POST",

            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",

            json=payload

        )








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

                    days * 86400

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





        payload = {


            "id":

            inbound["id"],



            "settings":

            json.dumps(settings)

        }






        return self.request(

            "POST",

            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",

            json=payload

        )








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
