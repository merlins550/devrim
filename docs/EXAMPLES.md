# Usage Examples

```
from browser_agent_stealth import BrowserAgentStealth
from dom_interaction import type_text, click

agent = BrowserAgentStealth()
agent.initialize_driver()
agent.go_to('https://example.com')
type_text(agent.driver, 'input[name="q"]', 'matrix ai')
click(agent.driver, 'button[type="submit"]')
```
