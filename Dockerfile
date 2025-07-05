# ✅ Use slim Python image
FROM python:3.11-slim

# 🧱 Install system dependencies for Playwright & Chromium
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libasound2 \
    libgbm-dev \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && apt-get clean

# 🔧 Set working directory
WORKDIR /app

# 🔁 Copy requirements first to leverage Docker cache
COPY requirements.txt .

# 📦 Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🌍 Install Playwright + Chromium only once unless deps change
RUN python -m playwright install --with-deps

# 📁 Copy app code
COPY . .

# 🚀 Start the script
CMD ["python", "main.py"]
