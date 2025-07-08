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



## 🐳 How to Run ```Docker (Headless)```

### create a .env file in the project root directory.

```bash
SMTP_USER=fromemail@gmail.com
SMTP_PASS=abcd....
EMAIL_FROM=fromemail@gmail.com
EMAIL_TO=toemail@gmail.com
EMAIL_FROM_NAME=Amul Stock Tracker
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```


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

## ✅ Example Output mail

```bash
Product: Amul Organic Trial Pack, 7 kg | 4 Products
Available: 1
Quantity: 12
Buy Now: https://shop.amul.com/en/product/amul-organic-trial-pack-7-kg-or-4-products
```

---
## 📌 Notes

- This tool mimics real user behaviour to verify that API requests work as expected.
- Handy for personal tracking dashboards or building stock-alert systems.
- Intended for educational use — respect each site’s terms of service and avoid excessive polling.

---

## 🧑‍💻 Author

Built with excitement by **Himanshu**

Connect on [LinkedIn](https://www.linkedin.com/in/kounhimanshu/)
