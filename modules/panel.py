# ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI Panel Manager FIXED
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
    # Safe JSON Parser
    # ======================================================

    def parse_json(self, data):

        if isinstance(data, dict):

            return data


        if isinstance(data, str):

            try:

                return json.loads(data)

            except:

                return {}


        return {}



    # ======================================================
    # Login
    # ======================================================

    def login(self):

        r = self.session.post(

            f"{self.url}/login",

            data={

                "username": PANEL_USERNAME,

                "password": PANEL_PASSWORD

            },

            verify=False,

            timeout=20

        )


        if r.status_code != 200:

            raise Exception(
                "3X-UI Login Failed"
            )


        return True



    # ======================================================
    # UUID
    # ======================================================

    def generate_uuid(self):

        return str(uuid.uuid4())



    # ======================================================
    # Username
    # ======================================================

    def generate_username(self, telegram_id):

        return f"zeus_{telegram_id}_{int(time.time())}"



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
                "Cannot get inbounds"
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


        uid = self.generate_uuid()


        username = self.generate_username(

            telegram_id

        )


        expire = int(

            time.time()

            +

            days * 86400

        ) * 1000



        total = (

            traffic_gb

            *

            1024

            *

            1024

            *

            1024

        )



        return {


            "id": uid,

            "email": username,

            "tgId": str(telegram_id),

            "enable": True,

            "totalGB": total,

            "expiryTime": expire,

            "limitIp": 0,

            "reset": 0

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



        settings = self.parse_json(

            inbound.get("settings")

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



        clients.append(client)



        settings["clients"] = clients




        payload = {


            "id": inbound["id"],


            "settings": json.dumps(settings)

        }





        r = self.session.post(

            f"{self.url}/panel/api/inbounds/update/{INBOUND_ID}",

            json=payload,

            verify=False,

            timeout=30

        )



        result = r.json()



        if not result.get("success"):

            raise Exception(

                result.get(

                    "msg",

                    "Create failed"

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
    # VLESS Link
    # ======================================================

    def create_vless_link(

        self,

        inbound,

        client

    ):


        host = (

            self.url

            .replace("https://","")

            .replace("http://","")

            .split("/")[0]

        )



        stream = self.parse_json(

            inbound.get(

                "streamSettings"

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



        query = urlencode(params)



        return (

            f"vless://{client['id']}@"

            f"{host}:{inbound['port']}?"

            f"{query}"

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


        settings = self.parse_json(

            inbound.get("settings")

        )


        result=[]


        for c in settings.get(

            "clients",

            []

        ):


            if c.get("tgId") == str(telegram_id):

                result.append(c)



        return result
