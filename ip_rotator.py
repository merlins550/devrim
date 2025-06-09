"""Simple proxy rotation utilities."""

from typing import List, Optional

class IPRotator:
    def __init__(self, proxies: Optional[List[str]] = None):
        self.proxies = proxies or []
        self.index = 0

    def add_proxy(self, proxy: str) -> None:
        self.proxies.append(proxy)

    def next_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self.index % len(self.proxies)]
        self.index += 1
        return proxy
