# SSL Certificate Setup Instructions for Fazaa Django Project

## Overview
This guide will help you set up SSL certificates for your Django application running on Docker. The setup includes Let's Encrypt SSL certificates with automatic renewal.

## Prerequisites
- Your Django application is running on a VPS with Docker and Docker Compose
- Your domain `faazza.com` is pointing to your server IP `168.231.127.170`
- Port 80 and 443 are open on your server
- You have sudo access on your server

## Quick Setup (Automated)

### Option 1: Use the Automated Script
1. Upload all the modified files to your server
2. Make the setup script executable:
   ```bash
   chmod +x ssl_setup.sh
   ```
3. Run the setup script:
   ```bash
   sudo ./ssl_setup.sh
   ```

The script will automatically:
- Stop existing containers
- Create necessary directories
- Set up temporary nginx configuration
- Obtain SSL certificates
- Configure automatic renewal
- Restart containers with SSL support

## Manual Setup (Step by Step)

If you prefer to do it manually or if the automated script fails:

### Step 1: Stop Current Containers
```bash
sudo docker-compose down
```

### Step 2: Create SSL Directories
```bash
sudo mkdir -p /var/lib/docker/volumes/fazaa_certbot_webroot/_data/.well-known/acme-challenge
sudo mkdir -p /var/lib/docker/volumes/fazaa_letsencrypt_certs/_data
sudo mkdir -p /var/lib/docker/volumes/fazaa_letsencrypt_lib/_data
sudo chown -R 1000:1000 /var/lib/docker/volumes/fazaa_certbot_webroot/_data
sudo chmod -R 755 /var/lib/docker/volumes/fazaa_certbot_webroot/_data
```

### Step 3: Create Temporary nginx Configuration
Create a backup of your current nginx config:
```bash
cp nginx/nginx.conf nginx/nginx.conf.backup
```

Create a temporary nginx config for certificate generation:
```bash
cat > nginx/nginx.conf.temp << 'EOF'
server {
    listen 80;
    server_name faazza.com www.faazza.com 168.231.127.170;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri $uri/ =404;
    }
    
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
```

Replace the nginx config temporarily:
```bash
cp nginx/nginx.conf.temp nginx/nginx.conf
```

### Step 4: Start Containers
```bash
sudo docker-compose up -d --build
```

Wait for containers to be ready (about 30 seconds).

### Step 5: Test Webroot Access
```bash
echo "test" | sudo tee /var/lib/docker/volumes/fazaa_certbot_webroot/_data/test.txt > /dev/null
curl -f http://faazza.com/test.txt
sudo rm /var/lib/docker/volumes/fazaa_certbot_webroot/_data/test.txt
```

### Step 6: Obtain SSL Certificate
```bash
sudo certbot certonly \
    --webroot \
    --webroot-path /var/lib/docker/volumes/fazaa_certbot_webroot/_data \
    --email admin@faazza.com \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    -d faazza.com \
    -d www.faazza.com
```

### Step 7: Copy Certificates to Docker Volumes
```bash
sudo cp -r /etc/letsencrypt/* /var/lib/docker/volumes/fazaa_letsencrypt_certs/_data/
sudo chown -R root:root /var/lib/docker/volumes/fazaa_letsencrypt_certs/_data
```

### Step 8: Restore Full nginx Configuration
```bash
cp nginx/nginx.conf.backup nginx/nginx.conf
```

### Step 9: Restart with SSL
```bash
sudo docker-compose down
sudo docker-compose up -d --build
```

### Step 10: Set Up Automatic Renewal
```bash
(sudo crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --webroot --webroot-path /var/lib/docker/volumes/fazaa_certbot_webroot/_data --post-hook 'docker-compose -f $(pwd)/docker-compose.yml restart nginx'") | sudo crontab -
```

## Verification

### Test SSL Certificate
```bash
curl -I https://faazza.com
```

### Check SSL Rating
Visit: https://www.ssllabs.com/ssltest/analyze.html?d=faazza.com

### Verify Automatic Renewal
```bash
sudo crontab -l
```

## Troubleshooting

### Common Issues

1. **Certificate request fails with 404 error**
   - Check if your domain DNS is pointing to the correct IP
   - Verify nginx is serving the webroot correctly
   - Test: `curl -f http://faazza.com/.well-known/acme-challenge/test`

2. **nginx fails to start with SSL config**
   - Check if certificates exist: `sudo ls -la /var/lib/docker/volumes/fazaa_letsencrypt_certs/_data/live/faazza.com/`
   - Check nginx logs: `docker-compose logs nginx`

3. **HTTPS redirect not working**
   - Verify Django settings have `SECURE_SSL_REDIRECT = True`
   - Check if `DEBUG = False` in production

### Useful Commands

```bash
# Check nginx logs
docker-compose logs nginx

# Check certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log

# Test certificate renewal
sudo certbot renew --dry-run --webroot --webroot-path /var/lib/docker/volumes/fazaa_certbot_webroot/_data

# Check certificate expiration
sudo certbot certificates

# Restart nginx only
docker-compose restart nginx
```

## Security Features Enabled

✅ **SSL/TLS Encryption** - All traffic encrypted with Let's Encrypt certificates  
✅ **HTTP to HTTPS Redirect** - Automatic redirection from HTTP to HTTPS  
✅ **HSTS (HTTP Strict Transport Security)** - Prevents downgrade attacks  
✅ **Secure Cookies** - Session and CSRF cookies only sent over HTTPS  
✅ **Security Headers** - XSS protection, content type sniffing protection  
✅ **Perfect Forward Secrecy** - Modern cipher suites  
✅ **Automatic Certificate Renewal** - Certificates renew automatically  

## Next Steps

1. Test your website: https://faazza.com
2. Update any hardcoded HTTP URLs in your application to HTTPS
3. Update your mobile app API endpoints to use HTTPS
4. Monitor certificate renewal logs periodically

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review nginx and certbot logs
3. Verify DNS settings
4. Ensure firewall allows ports 80 and 443

Your SSL certificate will be automatically renewed every 60 days by the cron job.