# ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI v5.5.5
# PART 1
# ==========================================================

import json
import uuid
import time
import requests
import urllib3

from config import (
    PANEL_URL,
    PANEL_TOKEN,
    INBOUND_ID,
)

urllib3.disable_warnings()


class Panel:

    def __init__(self):

        self.url = PANEL_URL.rstrip("/")

        self.session = requests.Session()

        self.session.verify = False

        self.headers = {
            "Authorization": f"Bearer {PANEL_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self.check_connection()


    # -------------------------------------------------------
    # Check API
    # -------------------------------------------------------

    def check_connection(self):

        try:

            r = self.session.get(
                f"{self.url}/panel/api/server/status",
                headers=self.headers,
                timeout=15
            )

            try:
                data = r.json()
            except Exception:
                raise Exception(r.text)

            if not data.get("success", False):
                raise Exception(data.get("msg", "API Error"))

            return True

        except Exception as e:

            raise Exception(
                f"❌ Panel Connection Failed\n{e}"
            )


    # -------------------------------------------------------
    # Request
    # -------------------------------------------------------

    def request(self, method, endpoint, **kwargs):

        kwargs.setdefault("headers", self.headers)

        kwargs.setdefault("timeout", 20)

        r = self.session.request(
            method,
            f"{self.url}{endpoint}",
            **kwargs
        )

        try:
            return r.json()
        except Exception:
            raise Exception(r.text)


    # -------------------------------------------------------
    # UUID
    # -------------------------------------------------------

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())


    # -------------------------------------------------------
    # Username
    # -------------------------------------------------------

    @staticmethod
    def generate_username(tgid):

        return f"zeus_{tgid}_{int(time.time())}"


    # -------------------------------------------------------
    # Get Inbounds
    # -------------------------------------------------------

    def get_inbounds(self):

        data = self.request(
            "GET",
            "/panel/api/inbounds/list"
        )

        if not data.get("success", False):
            raise Exception(data.get("msg"))

        return data.get("obj", [])


    # -------------------------------------------------------
    # Get One Inbound
    # -------------------------------------------------------

    def get_inbound(self):

        for inbound in self.get_inbounds():

            if str(inbound["id"]) == str(INBOUND_ID):

                return inbound

        raise Exception(
            f"Inbound {INBOUND_ID} not found."
        )
            # -------------------------------------------------------
    # Build Client
    # -------------------------------------------------------

    def build_client(self, telegram_id, days, traffic_gb):

        return {
            "id": self.generate_uuid(),
            "flow": "",
            "email": self.generate_username(telegram_id),
            "limitIp": 0,
            "totalGB": int(traffic_gb * 1024 * 1024 * 1024),
            "expiryTime": int((time.time() + days * 86400) * 1000),
            "enable": True,
            "tgId": str(telegram_id),
            "subId": "",
            "reset": 0
        }

    # -------------------------------------------------------
    # Create Service
    # -------------------------------------------------------

    def create_service(self, telegram_id, days, traffic_gb):

        inbound = self.get_inbound()

        client = self.build_client(
            telegram_id,
            days,
            traffic_gb
        )

        payload = {
            "id": inbound["id"],
            "settings": json.dumps({
                "clients": [client]
            })
        }

        result = self.request(
            "POST",
            "/panel/api/inbounds/addClient",
            json=payload
        )

        if not result.get("success", False):
            raise Exception(
                result.get("msg", "Create client failed")
            )

        return {
            "username": client["email"],
            "uuid": client["id"],
            "client": client,
            "inbound": inbound
        }
        # ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI v5.5.5
# PART 3
# ==========================================================


    # -------------------------------------------------------
    # Generate VLESS Link
    # -------------------------------------------------------

    def generate_vless_link(self, service):

        client = service["client"]
        inbound = service["inbound"]


        settings = json.loads(
            inbound.get("settings", "{}")
        )


        stream = json.loads(
            inbound.get("streamSettings", "{}")
        )


        protocol = inbound.get(
            "protocol",
            "vless"
        )


        remark = client["email"]

        uuid = client["id"]


        port = inbound.get(
            "port",
            443
        )


        server = self.url.replace(
            "https://",
            ""
        ).replace(
            "http://",
            ""
        )


        link = (
            f"{protocol}://{uuid}@{server}:{port}"
        )


        params = []


        if stream.get("security"):

            params.append(
                f"security={stream['security']}"
            )


        if stream.get("network"):

            params.append(
                f"type={stream['network']}"
            )


        if stream.get("wsSettings"):

            ws = stream["wsSettings"]

            path = ws.get(
                "path",
                ""
            )

            host = ws.get(
                "headers",
                {}
            ).get(
                "Host",
                ""
            )


            if path:
                params.append(
                    f"path={path}"
                )


            if host:
                params.append(
                    f"host={host}"
                )


        if params:

            link += "?" + "&".join(params)


        link += f"#{remark}"


        return link



    # -------------------------------------------------------
    # Create Final Service
    # -------------------------------------------------------

    def create_subscription(
        self,
        telegram_id,
        days,
        traffic_gb
    ):


        service = self.create_service(
            telegram_id,
            days,
            traffic_gb
        )


        vless = self.generate_vless_link(
            service
        )


        return {

            "username": service["username"],

            "uuid": service["uuid"],

            "vless": vless,

            "expire": service["expire"],

            "traffic": service["traffic"]

        }
        # ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI v5.5.5
# PART 4
# ==========================================================


    # -------------------------------------------------------
    # Get Clients
    # -------------------------------------------------------

    def get_clients(self):

        inbound = self.get_inbound()

        try:

            settings = json.loads(
                inbound.get("settings", "{}")
            )

        except Exception:

            return []


        return settings.get(
            "clients",
            []
        )



    # -------------------------------------------------------
    # Find Client
    # -------------------------------------------------------

    def find_client(self, email):

        clients = self.get_clients()


        for client in clients:

            if client.get("email") == email:

                return client


        return None



    # -------------------------------------------------------
    # Delete Client
    # -------------------------------------------------------

    def delete_client(self, client_id):

        inbound = self.get_inbound()


        result = self.request(
            "POST",
            "/panel/api/inbounds/delClient",
            json={
                "id": inbound["id"],
                "clientId": client_id
            }
        )


        if not result.get(
            "success",
            False
        ):

            raise Exception(
                result.get(
                    "msg",
                    "Delete client failed"
                )
            )


        return True



    # -------------------------------------------------------
    # Update Client
    # -------------------------------------------------------

    def update_client(
        self,
        client_id,
        traffic_gb=None,
        days=None
    ):


        inbound = self.get_inbound()


        client = self.find_client(
            client_id
        )


        if not client:

            raise Exception(
                "Client not found"
            )


        if traffic_gb:

            client["totalGB"] = int(
                traffic_gb *
                1024 *
                1024 *
                1024
            )


        if days:

            client["expiryTime"] = int(
                (
                    time.time()
                    +
                    days * 86400
                )
                *
                1000
            )



        payload = {

            "id": inbound["id"],

            "settings": json.dumps({

                "clients": [
                    client
                ]

            })

        }



        result = self.request(
            "POST",
            "/panel/api/inbounds/updateClient",
            json=payload
        )


        if not result.get(
            "success",
            False
        ):

            raise Exception(
                result.get(
                    "msg",
                    "Update failed"
                )
            )


        return client
        # ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI v5.5.5
# PART 5
# ==========================================================


    # -------------------------------------------------------
    # Convert Expire Time
    # -------------------------------------------------------

    @staticmethod
    def format_expire(expire_time):

        try:

            timestamp = int(
                expire_time / 1000
            )

            return time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(timestamp)
            )

        except Exception:

            return "Unknown"



    # -------------------------------------------------------
    # Get Client Info
    # -------------------------------------------------------

    def get_client_info(self, email):

        client = self.find_client(
            email
        )


        if not client:

            raise Exception(
                "Client not found"
            )


        return {

            "username": client.get(
                "email"
            ),

            "uuid": client.get(
                "id"
            ),

            "traffic": int(
                client.get(
                    "totalGB",
                    0
                )
            ),

            "expire": self.format_expire(
                client.get(
                    "expiryTime",
                    0
                )
            ),

            "enable": client.get(
                "enable",
                False
            )

        }



    # -------------------------------------------------------
    # Reset Traffic
    # -------------------------------------------------------

    def reset_traffic(self, email):

        client = self.find_client(
            email
        )


        if not client:

            raise Exception(
                "Client not found"
            )


        client["up"] = 0

        client["down"] = 0



        inbound = self.get_inbound()


        result = self.request(
            "POST",
            "/panel/api/inbounds/updateClient",
            json={

                "id": inbound["id"],

                "settings": json.dumps({

                    "clients": [
                        client
                    ]

                })

            }
        )


        if not result.get(
            "success",
            False
        ):

            raise Exception(
                result.get(
                    "msg",
                    "Reset failed"
                )
            )


        return True
        # ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI v5.5.5
# PART 6
# ==========================================================


    # -------------------------------------------------------
    # Generate Subscription Data
    # -------------------------------------------------------

    def generate_subscription(
        self,
        email
    ):

        client = self.find_client(
            email
        )


        if not client:

            raise Exception(
                "Client not found"
            )


        inbound = self.get_inbound()


        vless = self.generate_vless_link({

            "client": client,

            "inbound": inbound

        })


        return {

            "username": email,

            "uuid": client.get(
                "id"
            ),

            "vless": vless,

            "expire": self.format_expire(
                client.get(
                    "expiryTime",
                    0
                )
            ),

            "traffic": client.get(
                "totalGB",
                0
            )

        }



    # -------------------------------------------------------
    # Build User Service Message
    # -------------------------------------------------------

    def service_message(
        self,
        data
    ):


        traffic = round(
            data["traffic"]
            /
            (1024 ** 3),
            2
        )


        return (

            "✅ سرویس شما ساخته شد\n\n"

            f"👤 نام کاربری:\n"
            f"{data['username']}\n\n"

            f"📦 حجم:\n"
            f"{traffic} GB\n\n"

            f"⏳ انقضا:\n"
            f"{data['expire']}\n\n"

            "🔗 کانفیگ VLESS:\n"
            f"{data['vless']}"

        )



    # -------------------------------------------------------
    # Check Client Status
    # -------------------------------------------------------

    def check_client(
        self,
        email
    ):

        client = self.find_client(
            email
        )


        if not client:

            return {

                "exists": False

            }



        return {

            "exists": True,

            "enable": client.get(
                "enable",
                False
            ),

            "expire": self.format_expire(
                client.get(
                    "expiryTime",
                    0
                )
            )

        }
        # ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI v5.5.5
# PART 7
# ==========================================================


    # -------------------------------------------------------
    # Extend Client Expire
    # -------------------------------------------------------

    def extend_client(
        self,
        email,
        days
    ):

        client = self.find_client(
            email
        )


        if not client:

            raise Exception(
                "Client not found"
            )


        current = int(
            client.get(
                "expiryTime",
                0
            )
        )


        now = int(
            time.time() * 1000
        )


        if current > now:

            new_expire = (
                current
                +
                days * 86400 * 1000
            )

        else:

            new_expire = (
                now
                +
                days * 86400 * 1000
            )


        client["expiryTime"] = new_expire


        inbound = self.get_inbound()


        result = self.request(
            "POST",
            "/panel/api/inbounds/updateClient",
            json={

                "id": inbound["id"],

                "settings": json.dumps({

                    "clients": [
                        client
                    ]

                })

            }
        )


        if not result.get(
            "success",
            False
        ):

            raise Exception(
                result.get(
                    "msg",
                    "Extend failed"
                )
            )


        return self.format_expire(
            new_expire
        )



    # -------------------------------------------------------
    # Add Traffic
    # -------------------------------------------------------

    def add_traffic(
        self,
        email,
        traffic_gb
    ):

        client = self.find_client(
            email
        )


        if not client:

            raise Exception(
                "Client not found"
            )


        client["totalGB"] += int(
            traffic_gb *
            1024 *
            1024 *
            1024
        )


        inbound = self.get_inbound()


        result = self.request(
            "POST",
            "/panel/api/inbounds/updateClient",
            json={

                "id": inbound["id"],

                "settings": json.dumps({

                    "clients": [
                        client
                    ]

                })

            }
        )


        if not result.get(
            "success",
            False
        ):

            raise Exception(
                result.get(
                    "msg",
                    "Traffic update failed"
                )
            )


        return client["totalGB"]
        # ==========================================================
# Zeus Shop VPN PRO
# modules/panel.py
# 3X-UI v5.5.5
# PART 8 FINAL
# ==========================================================


    # -------------------------------------------------------
    # Create User Service Final
    # -------------------------------------------------------

    def create_user_service(
        self,
        telegram_id,
        days,
        traffic_gb
    ):

        try:

            service = self.create_subscription(
                telegram_id,
                days,
                traffic_gb
            )


            return {

                "status": True,

                "username": service["username"],

                "uuid": service["uuid"],

                "config": service["vless"],

                "expire": service["expire"],

                "traffic": round(
                    service["traffic"]
                    /
                    (1024 ** 3),
                    2
                )

            }


        except Exception as e:


            return {

                "status": False,

                "error": str(e)

            }



    # -------------------------------------------------------
    # Delete User Service
    # -------------------------------------------------------

    def delete_user_service(
        self,
        email
    ):

        try:

            client = self.find_client(
                email
            )


            if not client:

                return False


            return self.delete_client(
                client["id"]
            )


        except Exception:


            return False



    # -------------------------------------------------------
    # Panel Health
    # -------------------------------------------------------

    def health_check(self):

        try:

            return self.check_connection()


        except Exception:

            return False
