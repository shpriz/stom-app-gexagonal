# 🚀 Comprehensive Deployment Guide: Advanced Stomatology Practice Management System

## 🎯 System Overview
This guide provides step-by-step instructions for deploying the advanced Django stomatology practice management system featuring:

**Core Features:**
- **Multi-doctor patient segregation** with secure data isolation
- **Interactive hexagonal radar charts** with population analytics
- **Schema-based assessments** (OHIP, Clinical Status, Custom)
- **Advanced scoring system** with flexible automatic calculation
- **Professional PDF report generation** with high-quality charts
- **Population statistics** with z-scores and outlier detection
- **Authentication & authorization** with role-based access control

**Technical Stack:**
- Django 4.2+ with REST Framework
- PostgreSQL 15 with optimized performance
- Docker & Docker Compose for containerization
- Nginx reverse proxy with security headers
- WhiteNoise for efficient static file serving
- Professional medical UI framework

## Prerequisites
- Remote server with Ubuntu 20.04+ or CentOS 8+ (minimum 2GB RAM, 20GB storage)
- SSH access to the server
- Domain name or IP address for the server
- Basic knowledge of Linux command line

## Server Setup Requirements

### 1. Update System Packages
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. Install Essential Tools
```bash
# Ubuntu/Debian
sudo apt install -y curl wget git unzip

# CentOS/RHEL
sudo yum install -y curl wget git unzip
```

## Docker Installation

### Ubuntu/Debian Installation
```bash
# Remove old Docker versions
sudo apt remove docker docker-engine docker.io containerd runc

# Install Docker dependencies
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### CentOS/RHEL Installation
```bash
# Remove old Docker versions
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# Install Docker dependencies
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker Engine
sudo yum install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Configure Docker
```bash
# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group (optional, for non-root usage)
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
# Or use: newgrp docker

# Verify Docker installation
docker --version
docker-compose --version
```

## Application Deployment

### 1. Clone the Repository
```bash
# Navigate to your preferred directory
cd /opt

# Clone the repository
sudo git clone https://github.com/shpriz/stom-app-gexagonal.git
cd stom-app-gexagonal

# Set proper permissions
sudo chown -R $USER:$USER /opt/stom-app-gexagonal
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

Required environment variables in `.env`:
```env
# Database Configuration
POSTGRES_DB=stomatology_db
POSTGRES_USER=stom_user
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django Configuration
SECRET_KEY=your_very_long_secret_key_here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-server-ip,localhost

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### 3. Generate Django Secret Key
```bash
# Generate a secure secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Production Docker Configuration
Create `docker-compose.prod.yml` if not already present:
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media
    depends_on:
      - db
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_HOST=db
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

### 5. Build and Start Services
```bash
# Build the Docker images
docker-compose -f docker-compose.prod.yml build

# Start services in detached mode
docker-compose -f docker-compose.prod.yml up -d

# Check if services are running
docker-compose -f docker-compose.prod.yml ps
```

### 6. Initialize Database
```bash
# Run database migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser account
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 7. Load Initial Data (Optional)
```bash
# If you have fixtures or initial data
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata initial_data.json
```

## Firewall Configuration

### Ubuntu (UFW)
```bash
# Enable firewall
sudo ufw --force enable

# Allow SSH
sudo ufw allow 22

# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow PostgreSQL (if external access needed)
sudo ufw allow 5432

# Check status
sudo ufw status
```

### CentOS (firewalld)
```bash
# Start firewall service
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Allow services
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=5432/tcp

# Reload firewall
sudo firewall-cmd --reload

# Check status
sudo firewall-cmd --list-all
```

## SSL Certificate Setup (Optional but Recommended)

### Using Let's Encrypt with Certbot
```bash
# Install Certbot
# Ubuntu/Debian
sudo apt install -y certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal setup
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logs

### View Application Logs
```bash
# View all service logs
docker-compose -f docker-compose.prod.yml logs

# View specific service logs
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml logs db
docker-compose -f docker-compose.prod.yml logs nginx

# Follow logs in real-time
docker-compose -f docker-compose.prod.yml logs -f web
```

### System Monitoring
```bash
# Check Docker containers status
docker ps

# Check system resources
docker stats

# Check disk usage
df -h
docker system df
```

## Backup Strategy

### Database Backup
```bash
# Create backup script
cat > /opt/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
docker-compose -f /opt/stom-app-gexagonal/docker-compose.prod.yml exec -T db pg_dump -U stom_user stomatology_db > $BACKUP_DIR/db_backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "db_backup_*.sql" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/db_backup_$DATE.sql"
EOF

# Make script executable
chmod +x /opt/backup-db.sh

# Add to crontab for daily backups
echo "0 2 * * * /opt/backup-db.sh" | sudo crontab -
```

### Application Files Backup
```bash
# Backup media files and configurations
tar -czf /opt/backups/app_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  /opt/stom-app-gexagonal/media \
  /opt/stom-app-gexagonal/.env \
  /opt/stom-app-gexagonal/docker-compose.prod.yml
```

## Maintenance Commands

### Update Application
```bash
# Navigate to application directory
cd /opt/stom-app-gexagonal

# Pull latest changes
git pull origin master

# Rebuild and restart services
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### System Cleanup
```bash
# Remove unused Docker images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Complete cleanup
docker system prune -f
```

## Security Best Practices

### 1. System Security
```bash
# Update system regularly
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
sudo yum update -y                      # CentOS/RHEL

# Install security updates automatically
sudo apt install -y unattended-upgrades  # Ubuntu/Debian
sudo yum install -y yum-cron             # CentOS/RHEL
```

### 2. SSH Security
```bash
# Edit SSH configuration
sudo nano /etc/ssh/sshd_config

# Recommended settings:
# Port 2222                    # Change default port
# PermitRootLogin no          # Disable root login
# PasswordAuthentication no   # Use key-based authentication only
# MaxAuthTries 3             # Limit login attempts

# Restart SSH service
sudo systemctl restart sshd
```

### 3. Application Security
- Use strong passwords for database and Django admin
- Enable HTTPS in production
- Regularly update dependencies
- Monitor application logs for suspicious activity
- Implement proper backup and recovery procedures

## Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check container logs
docker-compose -f docker-compose.prod.yml logs web

# Check port conflicts
sudo netstat -tulpn | grep :8000
```

#### Database Connection Issues
```bash
# Check database container
docker-compose -f docker-compose.prod.yml logs db

# Test database connection
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER /opt/stom-app-gexagonal
chmod -R 755 /opt/stom-app-gexagonal
```

### Performance Optimization
```bash
# Monitor resource usage
htop
iotop
docker stats

# Optimize PostgreSQL settings in docker-compose.prod.yml
environment:
  - POSTGRES_SHARED_BUFFERS=256MB
  - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
  - POSTGRES_WORK_MEM=4MB
```

## Support and Maintenance

### Regular Maintenance Schedule
- **Daily**: Check application logs and system resources
- **Weekly**: Update system packages and review security logs
- **Monthly**: Test backup and recovery procedures
- **Quarterly**: Review and update security configurations

### Contact Information
For technical support or questions about the deployment:
- Check application logs first
- Review this documentation
- Contact system administrator

---

**Note**: This deployment guide assumes a production environment. Adjust security settings, resource allocations, and configurations based on your specific requirements and infrastructure.