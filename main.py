from playwright.sync_api import sync_playwright
import logging
import sys
import json

# Constants
PRODUCT_ALIAS = "amul-organic-trial-pack-7-kg-or-4-products"
PRODUCT_PAGE_URL = f"https://shop.amul.com/en/product/{PRODUCT_ALIAS}"
API_URL_FRAGMENT = "/api/1/entity/ms.products"
PINCODE = "122003"

# Logging Setup
logging.basicConfig(
    level=logging.INFO,  # set to DEBUG if needed
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    logging.info("🚀 Launching Playwright browser (headless)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        captured_headers = {}
        intercepted_once = False

        def on_request(request):
            nonlocal captured_headers, intercepted_once
            if not intercepted_once and API_URL_FRAGMENT in request.url:
                intercepted_once = True
                logging.info(f"📤 Intercepted request: {request.method} {request.url}")
                captured_headers = request.headers
                for k, v in captured_headers.items():
                    logging.debug(f"{k}: {v}")

        page.on("request", on_request)

        try:
            logging.info("🌐 Navigating to homepage...")
            page.goto("https://shop.amul.com/", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            if page.locator("text=Select Delivery Pincode").is_visible():
                logging.info("✅ Modal detected. Entering pincode...")
                page.locator('input[placeholder="Enter Your Pincode"]').fill(PINCODE)
                page.wait_for_timeout(1500)

                dropdown_selector = "p.item-name.text-dark.fw-semibold"
                try:
                    page.locator(dropdown_selector).wait_for(state="visible", timeout=15000)
                    page.locator(dropdown_selector).click()
                    page.wait_for_timeout(2000)
                except Exception as e:
                    logging.warning(f"❌ Failed to select pincode dropdown: {e}")
                    return
            else:
                logging.warning("⚠️ Modal not detected. Proceeding anyway.")

            # Navigate to product page to trigger the product API
            logging.info("🧭 Navigating to product page...")
            page.goto(PRODUCT_PAGE_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(10000)  # Wait for API to fire and headers to capture

            if captured_headers:
                logging.info("📡 Using captured headers to call API directly...")
                filtered_headers = {
                    k: v for k, v in captured_headers.items()
                    if k.lower() not in ["host", "content-length", "connection"]
                }

                response = context.request.get(
                    f"https://shop.amul.com{API_URL_FRAGMENT}?q=%7B%22alias%22%3A%22{PRODUCT_ALIAS}%22%7D&limit=1",
                    headers=filtered_headers
                )

                if response.status == 200:
                    logging.info("✅ API call successful.")
                    response_json = response.json()
                    logging.info(f"📬 Full response: {response_json}")
                    logging.info(f"📩 Message: {response_json.get('messages')}")

                    product = response_json.get("data", [{}])[0]
                    logging.info(f"🧾 Product: {product.get('name')}")
                    logging.info(f"📦 Available: {product.get('available')}")
                    logging.info(f"🔢 Quantity: {product.get('inventory_quantity')}")
                else:
                    logging.error(f"❌ API failed with status code {response.status}")
            else:
                logging.warning("⚠️ No headers captured. Product API may not have been triggered.")

        except Exception as e:
            logging.exception(f"💥 Exception: {e}")
        finally:
            logging.info("🧹 Closing browser.")
            browser.close()

if __name__ == "__main__":
    main()
