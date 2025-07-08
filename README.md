# 🧀 Amul Product Stock Checker (Playwright + Python)

This project is a headless browser automation script using **Playwright** to monitor stock availability of specific products (like "Amul Organic Trial Pack") from [https://shop.amul.com](https://shop.amul.com). It simulates real user behavior to bypass geo-pincode checks and directly capture and call the internal product API with valid session headers.

---

## 📦 Features

- ✅ Automatically enters delivery pincode and selects dropdown
- ✅ Navigates to specific product page
- ✅ Intercepts network request headers of actual API call
- ✅ Reuses those headers to call API directly
- ✅ Prints product availability and quantity
- ✅ Works headless (no UI) – perfect for servers or automation
- ✅ Docker-ready

---

## 🧰 Tech Stack

- Python 3.10+
- Playwright (`sync_api`)
- Docker (for containerized execution)

---

## 🚀 How to Run Locally (With UI) ```ubuntu```

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/amul-stock-checker.git
cd amul-stock-checker
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 4. Run the Script with UI

```bash
python main-ui.py
```

> The browser will open, enter the pincode, and navigate to the product page. Logs will be printed to console.

---

## 🐳 How to Run on Docker (Headless)

### 1. Build the Docker Image

```bash
docker buildx build --network=host -t amul-stock-tracker . 
```

### 2. Run the Container

```bash
docker run --rm --network=host --env-file .env amul-stock-tracker
```

> This runs the checker fully headless without a browser window. Useful for servers and CI environments.

---

## 📁 Project Structure

```
amul-stock-checker/
├── main.py            # Headless version for Docker
├── main-ui.py         # UI version for local debug/testing only
├── notifier.py        # Sends email using Gmail SMTP + .env credentials
├── schedular.py       # Runs main.py on schedule (e.g. every hour)
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker build instructions
├── .env               # SMTP credentials (incorrect values committed for security)
└── README.md          # You're reading this
```

---

## 🔧 Customization

Edit the following constants in the script to change the product or delivery area:

```python
PRODUCT_ALIAS = "amul-organic-trial-pack-7-kg-or-4-products"
PINCODE = "122003"
```

You can find product aliases by visiting the product page on [shop.amul.com](https://shop.amul.com) and copying the URL slug.

---

## ✅ Example Output

```bash
🧾 Product: Amul Organic Trial Pack (7 Kg)
📦 Available: 1
🔢 Quantity: 14
🚨 IN STOCK! Buy Now: https://shop.amul.com/en/product/amul-organic-trial-pack-7-kg-or-4-products
```

---

## 📌 Notes

- This tool mimics actual user behavior to ensure API requests work as expected.
- Useful for personal tracking or building stock alert systems.
- Designed for educational use. Respect site terms and avoid excessive polling.

---

## 🧑‍💻 Author

Built with ❤️ using Python + Playwright

