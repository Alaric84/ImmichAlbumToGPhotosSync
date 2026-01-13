FROM alpine:latest

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-requests \
    bash \
    ca-certificates \
    unzip \
    curl

# Install rclone from GitHub
RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip \
    && unzip rclone-current-linux-amd64.zip \
    && cp rclone-*-linux-amd64/rclone /usr/bin/ \
    && rm -rf rclone-current-linux-amd64.zip rclone-*-linux-amd64

# Create app directory
WORKDIR /app


# Copy the main sync script
COPY immich-google-sync.py .


# The config file will be mapped from the host at runtime using -v $(pwd)/config/rclone.conf:/app/config/rclone.conf

# Run the script on container start
ENTRYPOINT ["python3", "/app/immich-google-sync.py"]