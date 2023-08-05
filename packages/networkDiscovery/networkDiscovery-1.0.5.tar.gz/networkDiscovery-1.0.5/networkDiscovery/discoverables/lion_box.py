"""Discover Lion Box."""
from . import SSDPDiscoverable


class Discoverable(SSDPDiscoverable):
    """Add support for discovering Lion Box."""

    def get_entries(self):
        """Get all the LionBox uPnP entries."""
        return self.find_by_device_description({
            "friendlyName": "little_creator",
            "modelName": "little_lion_gateway"
        })
