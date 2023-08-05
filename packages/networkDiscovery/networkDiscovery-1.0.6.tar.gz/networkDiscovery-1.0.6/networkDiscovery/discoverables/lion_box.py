"""Discover Lion Box."""
from . import SSDPDiscoverable


class Discoverable(SSDPDiscoverable):
    """Add support for discovering Lion Box."""

    def get_entries(self):
        """Get all the LionBox uPnP entries."""
        return self.find_by_st("urn:schemas-upnp-org:service:ConnectionManager:1")
