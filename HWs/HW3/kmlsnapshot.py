import os
import sys
import time
from playwright.sync_api import sync_playwright


def take_kml_snapshot(kml_file, snapshot_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Load Google Earth Web
        page.goto("https://earth.google.com/web/")

        # Wait for the page to load
        page.wait_for_load_state("networkidle")

        # Click on the burger menu button
        page.click('#drawer-panel #projects #icon')

        # time.sleep(3)
        page.wait_for_load_state("load")

        page.get_by_role("button", name="Open").click()
        # time.sleep(3)
        page.wait_for_load_state("load")

        with page.expect_file_chooser() as fc_info:
            page.get_by_role(
                "option", name="Import KML file from computer").click()
        file_chooser = fc_info.value
        file_chooser.set_files(kml_file)

        time.sleep(10)
        # page.wait_for_load_state("load")

        for _ in range(2):
            page.get_by_role("button", name="Zoom Out").locator(
                "#icon").click()

        # Take a snapshot
        page.screenshot(path=snapshot_name)

        # Close the browser
        browser.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python kmlsnapshot.py [path_to_kml_file] [snapshot_name]")
    else:
        kml_file = sys.argv[1]
        snapshot_name = sys.argv[2]
        take_kml_snapshot(kml_file, snapshot_name)
        print("Snapshot saved as '%s'." % (snapshot_name))
