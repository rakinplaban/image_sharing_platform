FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /stock_image_sharing_platform
COPY requirements.txt /stock_image_sharing_platform/
RUN pip install -r requirements.txt
COPY . /stock_image_sharing_platform/
