# Playwright Python 3-Tab Automation Project

This repository provides an automated test suite using **Playwright for Python** that tests a 3-tab responsive web application.

---

## 📁 Project Structure

```
├── website/
│   ├── index.html         # Test website with 3 interactive tabs (Dashboard, Analytics, Settings)
│   ├── styles.css         # Modern styling & responsive CSS
│   └── app.js             # Tab activation logic & ARIA management
├── automation.py          # Standalone Playwright automation runner with CLI options & reporting
├── test_tabs.py           # Pytest test suite for automated CI/CD runs
├── requirements.txt       # Python dependencies (playwright, pytest, pytest-playwright)
├── screenshots/           # Auto-saved screenshots of each tab interaction
└── README.md
```

---

## ⚡ Standard Execution Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
playwright install chromium
```

### 2. Run the Automation Script

Run in headed mode (shows the browser clicking through the tabs with visual pacing):
```powershell
python automation.py
```

Run in headless mode (silent background execution):
```powershell
python automation.py --headless
```

Run with custom browser, speed, or tab delay adjustments:
```powershell
# Custom 2-second delay between tab clicks
python automation.py --delay 2.0

# Combine slow-mo and tab delay
python automation.py --browser chromium --slow-mo 500 --delay 2.0
```

### 3. Run with Pytest
```powershell
pytest test_tabs.py -v
```

---

## 🤖 Running in an Agentic Way via Antigravity CLI (`agy`)

The Antigravity CLI (`agy`) allows you to run this automation workflow in a fully autonomous, agent-driven way where the AI agent manages the environment, runs the tests, analyzes results, diagnoses issues, and verifies screenshots automatically.

### Step 1: Open the Project in `agy` CLI
Navigate to the project root and launch `agy`:
```powershell
cd c:\Users\sande\Documents\antigravity\Agentic_Automation_Playwright

agy
```

### Step 2: Agentic Goal Execution
Once inside the interactive `agy` shell, you can use high-level natural language instructions or slash commands:

#### Option A: Interactive Agent Prompt
Simply prompt the agent:
```text
Run the Playwright tab automation with a 1.5s delay, verify that all 3 tabs (Dashboard, Analytics, Settings) are clicked successfully, and confirm that all screenshots are generated.
```

#### Option B: Using the `/goal` Slash Command
For thorough, autonomous end-to-end execution:
```text
/goal Run automation.py with --delay 2.0, verify all 3 tab transitions and ARIA attributes, inspect the screenshots in screenshots/, and provide a comprehensive test report.
```

#### Option C: Non-Interactive / One-Shot CLI Execution
You can also trigger `agy` directly from your PowerShell terminal without entering the interactive prompt:
```powershell
agy -p "Run python automation.py --headless --delay 1.0, verify the test results, and report if all tabs passed."
```

---

## 🌐 Natural Language Automation with Playwright MCP Server

Using a **Playwright Model Context Protocol (MCP) Server** is an **exceptionally powerful and accurate approach** for natural language automation.

### Why Playwright MCP Server is a Great Approach:
1. **Direct Tool-Level Control**: Instead of asking the agent to generate and execute Python code files, the Playwright MCP server exposes browser primitives (`navigate`, `click`, `fill`, `hover`, `screenshot`, `evaluate`) directly as LLM tools.
2. **High Precision & DOM Awareness**: The agent reads the live accessibility tree and DOM attributes in real-time, allowing it to accurately target `#tab-analytics`, verify `aria-selected="true"`, or read text values without selector hallucination.
3. **Interactive & Exploratory QA**: You can perform dynamic exploratory testing using conversational English (e.g. *"Click on Settings, toggle headless mode off, and click Save"*).
4. **Self-Healing & Script Authoring**: The agent can explore the web page via MCP and automatically generate or fix Python Playwright test scripts.

---

### ⚙️ How to Configure Playwright MCP Server in Antigravity / `agy`

Add the Playwright MCP server to your Antigravity MCP configuration file:

**Location**: `~/.gemini/config/mcp_config.json` (or `.agents/mcp_config.json` in your workspace)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"]
    }
  }
}
```

> **Note:** Requires Node.js (`npm`/`npx`) installed on your system.

---

### 💬 Natural Language Prompting Examples with MCP

Once configured, launch `agy` and prompt naturally:

#### Example 1: Multi-Tab Verification Flow
> *"Navigate to `http://127.0.0.1:8765/index.html`. Click each of the 3 tabs (Dashboard, Analytics, Settings) with a 2-second pause, assert that each panel becomes visible, and take a screenshot of each tab."*

#### Example 2: Interactive State Verification
> *"Click the 'Settings' tab, select '60 seconds' from the Execution Timeout dropdown, click the 'Save Preferences' button, and verify the confirmation message."*

#### Example 3: Data Inspection & Analytics Check
> *"Switch to the 'Analytics' tab and tell me the DOM Content Loaded and Action Latency metrics shown on the screen."*

---

### ⚖️ Comparison: Playwright MCP vs. Python Playwright Script

| Capability | Playwright Python Script (`automation.py`) | Playwright MCP Server |
| :--- | :--- | :--- |
| **Best For** | CI/CD Pipelines, Fast Regression Runs, Deterministic Testing | Exploratory Testing, Natural Language QA, Dynamic Scenarios |
| **Execution Speed** | Ultra-fast (milliseconds) | Step-by-step LLM tool calls (seconds) |
| **Input Format** | Code (`python`, `pytest`) | Plain English / Conversational Prompts |
| **Flexibility** | Static test logic | Dynamic adaptation to UI changes & spontaneous instructions |
| **Error Recovery** | Fails on broken selectors | Dynamically inspects DOM to find updated selectors |

**Recommended Hybrid Workflow:**
- Use **Playwright MCP Server** for rapid natural language testing, exploratory QA, and prototyping.
- Export or generate **Playwright Python Scripts** for automated regression and CI/CD pipelines.

---

## 📸 Automated Screenshots Captured
Every run automatically captures screenshots for each tab state:
- `screenshots/01_tab_dashboard.png` (Dashboard overview)
- `screenshots/02_tab_analytics.png` (Performance analytics)
- `screenshots/03_tab_settings.png` (Preferences and settings)
