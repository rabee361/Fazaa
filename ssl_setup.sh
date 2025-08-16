#!/bin/bash

# SSL Certificate Setup Script for Fazaa Django Project
# This script sets up SSL certificates using Let's Encrypt with Docker

set -e

echo "🔐 Starting SSL Certificate Setup for faazza.com"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
    print_warning "Running as root. This is fine for server setup."
elif ! sudo -n true 2>/dev/null; then
    print_error "This script requires sudo privileges. Please run with sudo or as root."
    exit 1
fi

# Step 1: Stop existing containers to avoid port conflicts
print_status "Stopping existing Docker containers..."
sudo docker-compose down || true

# Step 2: Create necessary directories
print_status "Creating SSL certificate directories..."
sudo mkdir -p /var/lib/docker/volumes/fazaa_certbot_webroot/_data/.well-known/acme-challenge
sudo mkdir -p /var/lib/docker/volumes/fazaa_letsencrypt_certs/_data
sudo mkdir -p /var/lib/docker/volumes/fazaa_letsencrypt_lib/_data

# Step 3: Set proper permissions
print_status "Setting proper permissions..."
sudo chown -R 1000:1000 /var/lib/docker/volumes/fazaa_certbot_webroot/_data
sudo chmod -R 755 /var/lib/docker/volumes/fazaa_certbot_webroot/_data

# Step 4: Create temporary nginx config for initial certificate request
print_status "Creating temporary nginx configuration for certificate request..."
sudo cp nginx/nginx.conf nginx/nginx.conf.backup

# Create a temporary nginx config that only handles HTTP and ACME challenges
cat > nginx/nginx.conf.temp << 'EOF'
server {
    listen 80;
    server_name faazza.com www.faazza.com 168.231.127.170;
    
    # Location for Let's Encrypt ACME challenges
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri $uri/ =404;
    }
    
    # Serve the application normally for now
    location /staticfiles/ {
        alias /home/app/staticfiles/;
    }

    location /media/ {
        alias /home/app/media/;
    }

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_pass http://web:8000;
    }

    location /ws/ {
        proxy_pass http://web:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Replace the nginx config temporarily
sudo cp nginx/nginx.conf.temp nginx/nginx.conf

# Step 5: Start containers with temporary config
print_status "Starting containers with temporary configuration..."
sudo docker-compose up -d --build

# Wait for containers to be ready
print_status "Waiting for containers to be ready..."
sleep 30

# Step 6: Test if the webroot is accessible
print_status "Testing webroot accessibility..."
echo "test" | sudo tee /var/lib/docker/volumes/fazaa_certbot_webroot/_data/test.txt > /dev/null

# Test if we can access the test file
if curl -f http://faazza.com/test.txt >/dev/null 2>&1; then
    print_status "✅ Webroot is accessible from the internet"
    sudo rm /var/lib/docker/volumes/fazaa_certbot_webroot/_data/test.txt
else
    print_warning "⚠️  Could not access test file. Proceeding anyway..."
fi

# Step 7: Obtain SSL certificate
print_status "Requesting SSL certificate from Let's Encrypt..."
sudo certbot certonly \
    --webroot \
    --webroot-path /var/lib/docker/volumes/fazaa_certbot_webroot/_data \
    --email admin@faazza.com \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    -d faazza.com \
    -d www.faazza.com

if [ $? -eq 0 ]; then
    print_status "✅ SSL certificate obtained successfully!"
else
    print_error "❌ Failed to obtain SSL certificate. Check the logs above."
    print_status "Restoring original nginx configuration..."
    sudo cp nginx/nginx.conf.backup nginx/nginx.conf
    exit 1
fi

# Step 8: Copy certificates to Docker volumes
print_status "Copying certificates to Docker volumes..."
sudo cp -r /etc/letsencrypt/* /var/lib/docker/volumes/fazaa_letsencrypt_certs/_data/
sudo chown -R root:root /var/lib/docker/volumes/fazaa_letsencrypt_certs/_data

# Step 9: Restore full nginx configuration with SSL
print_status "Restoring full nginx configuration with SSL support..."
sudo cp nginx/nginx.conf.backup nginx/nginx.conf

# Step 10: Restart containers with SSL configuration
print_status "Restarting containers with SSL configuration..."
sudo docker-compose down
sudo docker-compose up -d --build

# Wait for containers to be ready
print_status "Waiting for containers to be ready..."
sleep 30

# Step 11: Test SSL certificate
print_status "Testing SSL certificate..."
if curl -f https://faazza.com >/dev/null 2>&1; then
    print_status "✅ SSL certificate is working correctly!"
else
    print_warning "⚠️  SSL test failed. Check nginx logs: docker-compose logs nginx"
fi

# Step 12: Set up automatic renewal
print_status "Setting up automatic certificate renewal..."
(sudo crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --webroot --webroot-path /var/lib/docker/volumes/fazaa_certbot_webroot/_data --post-hook 'docker-compose -f $(pwd)/docker-compose.yml restart nginx'") | sudo crontab -

# Cleanup
sudo rm -f nginx/nginx.conf.temp

print_status "🎉 SSL setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Test your website: https://faazza.com"
echo "2. Check SSL rating: https://www.ssllabs.com/ssltest/analyze.html?d=faazza.com"
echo "3. Monitor certificate renewal: sudo crontab -l"
echo ""
echo "If you encounter any issues:"
echo "- Check nginx logs: docker-compose logs nginx"
echo "- Check certbot logs: sudo tail -f /var/log/letsencrypt/letsencrypt.log"
echo "- Verify DNS: nslookup faazza.com"