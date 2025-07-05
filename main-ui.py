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
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    logging.info("🚀 Launching Playwright browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        context = browser.new_context()
        page = context.new_page()

        captured_headers = {}
        intercepted_once = False

        # 🔍 Intercept first matching request
        def on_request(request):
            nonlocal captured_headers, intercepted_once
            if not intercepted_once and API_URL_FRAGMENT in request.url:
                intercepted_once = True
                logging.info(f"📤 Intercepted request: {request.method} {request.url}")
                captured_headers = request.headers
                logging.debug("📨 Captured headers:")
                for k, v in captured_headers.items():
                    logging.debug(f"{k}: {v}")

        page.on("request", on_request)

        try:
            logging.info("🌐 Navigating to https://shop.amul.com/")
            page.goto("https://shop.amul.com/", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            logging.info("👀 Checking for 'Select Delivery Pincode' modal...")
            if page.locator("text=Select Delivery Pincode").is_visible():
                logging.info("✅ Modal detected.")
                input_box = page.locator('input[placeholder="Enter Your Pincode"]')
                logging.info("⌨️ Typing pincode...")
                input_box.fill(PINCODE)
                page.wait_for_timeout(1500)

                dropdown_selector = "p.item-name.text-dark.fw-semibold"
                logging.info("⏳ Waiting for dropdown suggestion to appear...")
                try:
                    suggestion = page.locator(dropdown_selector)
                    suggestion.wait_for(state="visible", timeout=15000)
                    logging.info("🖱️ Clicking on dropdown suggestion...")
                    suggestion.click()
                except Exception as e:
                    logging.exception(f"❌ Failed to detect/click dropdown: {e}")
                    return

                page.wait_for_timeout(3000)
                logging.info("🔄 Reloading page to refresh cookie/session context...")
                # page.reload(wait_until="domcontentloaded")
                # page.wait_for_timeout(5000)
            else:
                logging.warning("⚠️ Modal not detected. Skipping pincode step.")

            # # 🍪 Optional: Log cookies
            # cookies = context.cookies()
            # logging.debug("🍪 Cookies used in session:")
            # for cookie in cookies:
            #     logging.debug(json.dumps(cookie, indent=4))

            # 🧭 Navigate to product page
            logging.info("🧭 Navigating to product page to trigger API...")
            page.goto(PRODUCT_PAGE_URL, wait_until="domcontentloaded")

            # ⏳ Wait to ensure API is triggered and captured
            logging.info("⏳ Waiting for product API to trigger and capture...")
            # page.wait_for_timeout(10000)

            # ✅ Reuse captured headers in direct API call
            if captured_headers:
                logging.info("📡 Reusing captured headers to call API directly...")

                # Remove unnecessary headers like `host`, `content-length`, `connection`
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
                    logging.error(f"❌ API failed with status: {response.status}")
            else:
                logging.warning("⚠️ No headers captured. API not triggered yet?")

        except Exception as e:
            logging.exception(f"💥 Unhandled Exception: {e}")
        finally:
            logging.info("🧹 Done. Browser still open for inspection.")
            input("🔒 Press Enter to close browser...\n")
            browser.close()

if __name__ == "__main__":
    main()
