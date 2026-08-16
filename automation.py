"""
Playwright Python Automation Script: Multi-Tab Interaction & Verification
==========================================================================
Automates opening the test website, clicking through all 3 tabs (Dashboard,
Analytics, Settings), verifying tab panels, checking ARIA states, and capturing
screenshots with configurable delays between tab clicks.
"""

import os
import sys
import time
import argparse
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Setup local static file server
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress verbose HTTP server logs


def start_local_server(directory: Path, port: int = 8080):
    os.chdir(directory)
    server = HTTPServer(('127.0.0.1', port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server


def run_tab_automation(
    headless: bool = False,
    browser_type: str = "chromium",
    slow_mo: int = 400,
    tab_delay: float = 1.5,
    screenshots_dir: Path = None,
):
    base_dir = Path(__file__).parent.resolve()
    website_dir = base_dir / "website"
    
    if screenshots_dir is None:
        screenshots_dir = base_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)

    port = 8765
    server = start_local_server(website_dir, port)
    target_url = f"http://127.0.0.1:{port}/index.html"
    delay_ms = int(tab_delay * 1000)

    print("=" * 60)
    print("🚀 PLAYWRIGHT TAB AUTOMATION TEST RUNNER")
    print("=" * 60)
    print(f"Target URL     : {target_url}")
    print(f"Browser Engine : {browser_type}")
    print(f"Headless Mode  : {headless}")
    print(f"Slow Motion    : {slow_mo}ms")
    print(f"Tab Click Delay: {tab_delay}s ({delay_ms}ms)")
    print(f"Screenshots    : {screenshots_dir.resolve()}")
    print("-" * 60)

    results = []

    with sync_playwright() as p:
        browser_launcher = getattr(p, browser_type)
        browser = browser_launcher.launch(headless=headless, slow_mo=slow_mo)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        try:
            # 1. Navigate to test website
            print(f"\n[Step 1] Navigating to test page: {target_url}")
            page.goto(target_url)
            expect(page).to_have_title("Playwright Automation Test Site - Tabbed Interface")
            print("  ✓ Page loaded successfully with correct title.")
            page.wait_for_timeout(delay_ms)

            # Tab 1: Dashboard
            print(f"\n[Step 2] Testing Tab 1: Dashboard (with {tab_delay}s delay)")
            tab_dashboard = page.locator("#tab-dashboard")
            panel_dashboard = page.locator("#panel-dashboard")
            
            # Click Tab 1
            tab_dashboard.click()
            page.wait_for_timeout(delay_ms)

            expect(tab_dashboard).to_have_attribute("aria-selected", "true")
            expect(panel_dashboard).to_be_visible()
            expect(page.locator("#dashboard-heading")).to_have_text("System Overview & Activity")
            
            # Screenshot Tab 1
            screenshot_path_1 = screenshots_dir / "01_tab_dashboard.png"
            page.screenshot(path=str(screenshot_path_1))
            print(f"  ✓ Tab 1 active and verified. Screenshot saved: {screenshot_path_1.name}")
            results.append(("Tab 1: Dashboard", "PASSED", screenshot_path_1.name))

            # Tab 2: Analytics
            print(f"\n[Step 3] Testing Tab 2: Analytics (with {tab_delay}s delay)")
            tab_analytics = page.locator("#tab-analytics")
            panel_analytics = page.locator("#panel-analytics")

            # Click Tab 2
            tab_analytics.click()
            page.wait_for_timeout(delay_ms)

            expect(tab_analytics).to_have_attribute("aria-selected", "true")
            expect(tab_dashboard).to_have_attribute("aria-selected", "false")
            expect(panel_analytics).to_be_visible()
            expect(panel_dashboard).not_to_be_visible()
            expect(page.locator("#analytics-heading")).to_have_text("Performance Analytics & Insights")
            expect(page.locator("#active-tab-status")).to_have_text("Active: Analytics")

            # Screenshot Tab 2
            screenshot_path_2 = screenshots_dir / "02_tab_analytics.png"
            page.screenshot(path=str(screenshot_path_2))
            print(f"  ✓ Tab 2 active and verified. Screenshot saved: {screenshot_path_2.name}")
            results.append(("Tab 2: Analytics", "PASSED", screenshot_path_2.name))

            # Tab 3: Settings
            print(f"\n[Step 4] Testing Tab 3: Settings (with {tab_delay}s delay)")
            tab_settings = page.locator("#tab-settings")
            panel_settings = page.locator("#panel-settings")

            # Click Tab 3
            tab_settings.click()
            page.wait_for_timeout(delay_ms)

            expect(tab_settings).to_have_attribute("aria-selected", "true")
            expect(tab_analytics).to_have_attribute("aria-selected", "false")
            expect(panel_settings).to_be_visible()
            expect(panel_analytics).not_to_be_visible()
            expect(page.locator("#settings-heading")).to_have_text("Automation & Environment Settings")
            expect(page.locator("#active-tab-status")).to_have_text("Active: Settings")

            # Optional interaction in Tab 3: Click Save Settings button
            btn_save = page.locator("#btn-save-settings")
            btn_save.click()
            page.wait_for_timeout(500)
            expect(page.locator("#save-status")).to_contain_text("Settings saved successfully!")
            print("  ✓ Triggered interactive element on Tab 3 (Save Settings).")

            # Screenshot Tab 3
            screenshot_path_3 = screenshots_dir / "03_tab_settings.png"
            page.screenshot(path=str(screenshot_path_3))
            print(f"  ✓ Tab 3 active and verified. Screenshot saved: {screenshot_path_3.name}")
            results.append(("Tab 3: Settings", "PASSED", screenshot_path_3.name))

            # Verify total click counter in footer
            expect(page.locator("#click-counter")).to_have_text("3")
            print("  ✓ Click counter verified (3 tab transitions recorded).")

        except Exception as e:
            print(f"\n❌ Error during execution: {e}")
            raise
        finally:
            context.close()
            browser.close()
            server.shutdown()

    print("\n" + "=" * 60)
    print("📊 EXECUTION SUMMARY")
    print("=" * 60)
    for name, status, screenshot in results:
        print(f"  • {name:<20} : {status} (Captured: {screenshot})")
    print("=" * 60)
    print("🎉 All 3 tabs were successfully clicked, tested, and verified!\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Playwright 3-Tab Automation Runner")
    parser.add_argument("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium", help="Browser engine")
    parser.add_argument("--slow-mo", type=int, default=400, help="Delay in ms between Playwright operations")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay in seconds after each tab click (default: 1.5s)")
    args = parser.parse_args()

    run_tab_automation(
        headless=args.headless,
        browser_type=args.browser,
        slow_mo=args.slow_mo,
        tab_delay=args.delay,
    )
