# 🏥 Stomatology Practice Management System - Production Deployment

## 📋 Prerequisites

- Docker and Docker Compose installed
- Git installed
- Domain name (optional, for HTTPS)
- SSL certificates (optional, for HTTPS)

## 🚀 Quick Start (Local Production)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd app

# Copy environment file
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` file with your production settings:

```bash
# Required - Generate strong passwords
POSTGRES_PASSWORD=your_very_strong_database_password_here
SECRET_KEY=your_django_secret_key_minimum_50_characters_long

# Required - Update with your domain
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,http://localhost:8000

# Optional - Email configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 3. Generate Secret Key

```bash
# Generate Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Build and Start Services

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to start (30-60 seconds)
docker-compose -f docker-compose.prod.yml logs -f
```

### 5. Initialize Database

```bash
# Run database migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser account
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files (if needed)
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 6. Access Application

- **Application**: http://localhost:8000
- **With Nginx**: http://localhost (if nginx service is enabled)

## 🌐 Production Server Deployment

### Server Requirements

- Ubuntu 20.04+ or CentOS 8+
- 2GB+ RAM
- 20GB+ disk space
- Docker and Docker Compose

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Logout and login again for group changes
```

### 2. Application Deployment

```bash
# Create application directory
sudo mkdir -p /opt/stomatology
sudo chown $USER:$USER /opt/stomatology
cd /opt/stomatology

# Clone repository
git clone <your-repo-url> .

# Configure environment
cp .env.example .env
nano .env  # Edit with production values
```

### 3. SSL Setup (HTTPS)

```bash
# Install Certbot
sudo apt install certbot -y

# Get SSL certificate (replace with your domain)
sudo certbot certonly --standalone -d your-domain.com

# Update nginx.conf to enable HTTPS section
nano nginx.conf
```

### 4. Start Production Services

```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d --build

# Initialize database
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## 🔧 Management Commands

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
```

### Backup Database

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres stomatology_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres stomatology_db < backup_file.sql
```

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Stop Services

```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Stop and remove volumes (⚠️ DANGER: Deletes database)
docker-compose -f docker-compose.prod.yml down -v
```

## 🛡️ Security Checklist

### Required Security Steps

- [ ] Change default passwords in `.env`
- [ ] Generate strong Django SECRET_KEY
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Configure CSRF_TRUSTED_ORIGINS
- [ ] Enable HTTPS in production
- [ ] Set up firewall (UFW)
- [ ] Configure regular backups
- [ ] Update system packages regularly

### Firewall Configuration

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22

# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Check status
sudo ufw status
```

## 📊 Monitoring and Maintenance

### Health Checks

```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps

# Test application
curl http://localhost:8000/auth/login/

# Check database
docker-compose -f docker-compose.prod.yml exec db psql -U postgres -c "SELECT version();"
```

### Performance Monitoring

```bash
# Resource usage
docker stats

# Disk usage
df -h
docker system df
```

### Regular Maintenance

```bash
# Clean unused Docker resources
docker system prune -a

# Update system packages
sudo apt update && sudo apt upgrade -y

# Restart services (if needed)
docker-compose -f docker-compose.prod.yml restart
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Restart database
docker-compose -f docker-compose.prod.yml restart db
```

**Static Files Not Loading**
```bash
# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

**Permission Errors**
```bash
# Fix file permissions
sudo chown -R $USER:$USER /opt/stomatology
```

**Memory Issues**
```bash
# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📞 Support

### Important Files

- **Application Code**: `/opt/stomatology/`
- **Database Data**: Docker volume `postgres_data`
- **Static Files**: Docker volume `static_volume`
- **Logs**: `docker-compose logs`

### Backup Strategy

1. **Database**: Daily automated backups
2. **Code**: Version control (Git)
3. **Static Files**: Included in static volume
4. **Environment**: Backup `.env` file securely

### Contact

For technical support or issues:
- Check logs first: `docker-compose -f docker-compose.prod.yml logs`
- Review this documentation
- Contact system administrator

---

## 🎉 Congratulations!

Your Stomatology Practice Management System is now running in production mode with:

- ✅ Multi-doctor patient segregation
- ✅ Secure authentication system
- ✅ Interactive hexagonal radar charts
- ✅ Population analytics and group statistics
- ✅ Professional medical interface
- ✅ Production-ready Docker deployment
- ✅ Nginx reverse proxy with rate limiting
- ✅ SSL/HTTPS support
- ✅ Database persistence
- ✅ Health monitoring

**Access your application**: http://your-domain.com (or http://localhost:8000)

**Default admin**: Login with the superuser account you created during setup.