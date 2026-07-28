# ==========================================================
# ZeusShopBot PRO
# modules/panel.py
# 3X-UI API Manager
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
    # Request Helper
    # ======================================================

    def request(
        self,
        method,
        url,
        **kwargs
    ):

        response = self.session.request(

            method,

            url,

            verify=False,

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
                    "Cannot get inbounds"
                )

            )


        return data.get(
            "obj",
            []
        )






    # ======================================================
    # Selected Inbound
    # ======================================================

    def get_inbound(self):


        for inbound in self.get_inbounds():


            if int(inbound["id"]) == int(INBOUND_ID):

                return inbound



        raise Exception(

            "Inbound not found"

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


        return {


            "id":
                self.generate_uuid(),


            "email":
                self.generate_username(
                    telegram_id
                ),


            "tgId":
                str(telegram_id),


            "enable":
                True,


            "totalGB":
                traffic_gb
                *
                1024
                *
                1024
                *
                1024,


            "expiryTime":
                int(

                    time.time()

                    +

                    days * 86400

                )

                *

                1000,


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

            settings = json.loads(

                inbound["settings"]

            )


        except:


            settings = {

                "clients":[]

            }





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

            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",

            json=payload

        )





        if not result.get("success"):

            raise Exception(

                result.get(
                    "msg",
                    "Create failed"
                )

            )





        return {


            "username":

                client["email"],


            "uuid":

                client["id"],


            "subscription_url":

                self.create_vless_link(

                    inbound,

                    client

                )

        }







    # ======================================================
    # VLESS Link
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



        return (

            f"vless://{client['id']}@"

            f"{host}:"

            f"{inbound['port']}"

            "?"

            "type=tcp"

            "&encryption=none"

            f"#{inbound.get('remark','Zeus')}"

        )






    # ======================================================
    # User Services
    # ======================================================

    def get_user_services(

        self,

        telegram_id

    ):


        inbound = self.get_inbound()


        settings = json.loads(

            inbound["settings"]

        )


        result=[]



        for client in settings.get(
            "clients",
            []
        ):


            if client.get(
                "tgId"
            ) == str(telegram_id):


                result.append(client)



        return result
