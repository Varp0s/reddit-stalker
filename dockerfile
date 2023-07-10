FROM mcr.microsoft.com/playwright:v1.35.0-jammy

FROM python:3.9

RUN apt-get update && \
    apt-get install -y libnss3 libnss3-dev libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libatspi2.0-0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2   libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 \
    libx11-xcb1 libxcursor1


WORKDIR /

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

RUN playwright install

CMD ["python3", "main.py"]
