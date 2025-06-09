"""Basic performance benchmark for BrowserAgentStealth."""

import time
from browser_agent_stealth import BrowserAgentStealth


def benchmark_page_load(url: str) -> float:
    agent = BrowserAgentStealth()
    agent.initialize_driver(use_stealth=False)
    start = time.time()
    agent.go_to(url)
    elapsed = time.time() - start
    agent.close_browser()
    return elapsed

if __name__ == '__main__':
    url = 'https://example.com'
    duration = benchmark_page_load(url)
    print(f'Page load time for {url}: {duration:.2f}s')
