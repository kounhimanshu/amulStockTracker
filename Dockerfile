FROM python:3.11-slim

# 🧱 System deps for Playwright and Chromium
RUN apt-get clean && rm -rf /var/lib/apt/lists/* && \
    apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y --no-install-recommends \
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
        xdg-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 🔧 Set working directory
WORKDIR /app

# 🔁 Copy requirements first to leverage Docker cache
COPY requirements.txt .

# 📦 Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (only)
RUN python -m playwright install chromium

# 📁 Copy app code
COPY . .

# 🚀 Start the script
CMD ["python", "main.py"]
