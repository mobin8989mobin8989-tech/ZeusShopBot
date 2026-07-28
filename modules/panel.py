# ==========================================================
# ZeusShopBot
# modules/panel.py
# ==========================================================

from typing import Optional


class PanelManager:
    """
    Base Panel Manager
    """

    def __init__(self):
        self.connected = False

    def connect(self) -> bool:
        """
        Connect to panel
        """
        return False

    def create_user(
        self,
        username: str,
        volume: int,
        days: int
    ) -> Optional[dict]:
        """
        Create VPN User
        """
        raise NotImplementedError

    def update_user(
        self,
        username: str,
        volume: int,
        days: int
    ) -> bool:
        """
        Update VPN User
        """
        raise NotImplementedError

    def delete_user(
        self,
        username: str
    ) -> bool:
        """
        Delete VPN User
        """
        raise NotImplementedError

    def get_user(
        self,
        username: str
    ) -> Optional[dict]:
        """
        Get User Information
        """
        raise NotImplementedError

    def get_usage(
        self,
        username: str
    ) -> Optional[dict]:
        """
        Get User Usage
        """
        raise NotImplementedError

    def get_subscription(
        self,
        username: str
    ) -> Optional[str]:
        """
        Get Subscription Link
        """
        raise NotImplementedError
