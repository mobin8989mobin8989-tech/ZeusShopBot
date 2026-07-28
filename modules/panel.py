# ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI Panel Manager PRO
# Part 1/3
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

        self.headers = {
            "Content-Type": "application/json"
        }

        self.login()



    # ======================================================
    # Login 3X-UI
    # ======================================================

    def login(self):


        # اگر توکن واقعی 3x-ui وجود داشت
        if PANEL_TOKEN:


            self.headers = {

                "Authorization": PANEL_TOKEN,

                "Content-Type":
                "application/json"

            }

            return True




        try:

            response = self.session.post(

                f"{self.url}/login",

                json={

                    "username":
                    PANEL_USERNAME,

                    "password":
                    PANEL_PASSWORD

                },

                verify=False,

                timeout=20

            )


        except Exception as e:

            raise Exception(
                f"❌ Login Connection Error\n{e}"
            )




        if response.status_code != 200:

            raise Exception(

                f"❌ 3X-UI Login Failed\n"
                f"Status: {response.status_code}\n"
                f"{response.text}"

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


        if "headers" not in kwargs:

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

                f"❌ API Error\n{response.text}"

            )





    # ======================================================
    # UUID Generator
    # ======================================================


    def generate_uuid(self):

        return str(
            uuid.uuid4()
        )





    # ======================================================
    # Get Inbounds
    # ======================================================


    def get_inbounds(self):


        data = self.request(

            "GET",

            f"{self.url}/panel/api/inbounds/list"

        )



        if not isinstance(data, dict):

            raise Exception(
                "❌ Invalid API Response"
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


            if str(inbound.get("id")) == str(INBOUND_ID):

                return inbound




        raise Exception(

            f"❌ Inbound {INBOUND_ID} Not Found"

        )
            # ======================================================
    # Generate Username
    # ======================================================


    def generate_username(self, telegram_id):


        return (

            f"zeus_{telegram_id}_"

            f"{int(time.time())}"

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

            (

                time.time()

                +

                days * 86400

            )

            *

            1000

        )



        total_bytes = int(

            traffic_gb

            *

            1024

            *

            1024

            *

            1024

        )




        return {


            "id":
            client_uuid,


            "email":
            username,


            "tgId":
            str(telegram_id),


            "enable":
            True,


            "totalGB":
            total_bytes,


            "expiryTime":
            expire_time,


            "limitIp":
            0,


            "reset":
            0

        }





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


            settings_raw = inbound.get(

                "settings",

                "{}"

            )



            if isinstance(settings_raw, str):

                settings = json.loads(

                    settings_raw

                )

            else:

                settings = settings_raw



        except Exception as e:


            raise Exception(

                f"❌ Invalid inbound settings\n{e}"

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

            json.dumps(

                settings

            )

        }




        result = self.request(

            "POST",

            f"{self.url}/panel/api/inbounds/update/{inbound['id']}",

            json=payload

        )





        if not result.get(

            "success",

            False

        ):


            raise Exception(

                result.get(

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

            "Zeus VPN"

        )




        return (

            f"vless://"

            f"{client['id']}@"

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


            settings_raw = inbound.get(

                "settings",

                "{}"

            )


            if isinstance(settings_raw, str):

                settings = json.loads(

                    settings_raw

                )

            else:

                settings = settings_raw



        except:


            return []





        result = []



        for client in settings.get(

            "clients",

            []

        ):



            if str(

                client.get(

                    "tgId",

                    ""

                )

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

            inbound.get(

                "settings",

                "{}"

            )

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

            json.dumps(

                settings

            )

        }





        return self.request(

            "POST",

            f"{self.url}/panel/api/inbounds/update/{inbound['id']}",

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

            inbound.get(

                "settings",

                "{}"

            )

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

                    (

                        time.time()

                        +

                        days * 86400

                    )

                    *

                    1000

                )





                client["totalGB"] = int(

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

            json.dumps(

                settings

            )

        }





        return self.request(

            "POST",

            f"{self.url}/panel/api/inbounds/update/{inbound['id']}",

            json=payload

        )








    # ======================================================
    # Get All Clients
    # ======================================================


    def get_all_clients(self):


        inbound = self.get_inbound()



        settings = json.loads(

            inbound.get(

                "settings",

                "{}"

            )

        )



        return settings.get(

            "clients",

            []

        )
