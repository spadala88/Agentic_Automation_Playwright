"""
Pytest test suite for 3-tab website automation using Playwright with tab delays.
Run with: pytest test_tabs.py -v
"""

import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


@pytest.fixture(scope="session")
def test_server():
    base_dir = Path(__file__).parent.resolve()
    website_dir = base_dir / "website"
    os.chdir(website_dir)
    server = HTTPServer(('127.0.0.1', 8766), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    yield "http://127.0.0.1:8766/index.html"
    server.shutdown()


def test_navigate_and_click_three_tabs(page: Page, test_server: str):
    # Delay duration in milliseconds (1.0 second per tab)
    TAB_DELAY_MS = 1000

    # 1. Navigate
    page.goto(test_server)
    expect(page).to_have_title("Playwright Automation Test Site - Tabbed Interface")
    page.wait_for_timeout(TAB_DELAY_MS)

    # 2. Test Tab 1: Dashboard
    tab_1 = page.locator("#tab-dashboard")
    panel_1 = page.locator("#panel-dashboard")
    tab_1.click()
    page.wait_for_timeout(TAB_DELAY_MS)

    expect(tab_1).to_have_attribute("aria-selected", "true")
    expect(panel_1).to_be_visible()
    expect(page.locator("#dashboard-heading")).to_have_text("System Overview & Activity")

    # 3. Test Tab 2: Analytics
    tab_2 = page.locator("#tab-analytics")
    panel_2 = page.locator("#panel-analytics")
    tab_2.click()
    page.wait_for_timeout(TAB_DELAY_MS)

    expect(tab_2).to_have_attribute("aria-selected", "true")
    expect(tab_1).to_have_attribute("aria-selected", "false")
    expect(panel_2).to_be_visible()
    expect(panel_1).not_to_be_visible()
    expect(page.locator("#analytics-heading")).to_have_text("Performance Analytics & Insights")

    # 4. Test Tab 3: Settings
    tab_3 = page.locator("#tab-settings")
    panel_3 = page.locator("#panel-settings")
    tab_3.click()
    page.wait_for_timeout(TAB_DELAY_MS)

    expect(tab_3).to_have_attribute("aria-selected", "true")
    expect(tab_2).to_have_attribute("aria-selected", "false")
    expect(panel_3).to_be_visible()
    expect(panel_2).not_to_be_visible()
    expect(page.locator("#settings-heading")).to_have_text("Automation & Environment Settings")

    # 5. Verify total clicks
    expect(page.locator("#click-counter")).to_have_text("3")
