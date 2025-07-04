# 🏥 Advanced Stomatology Practice Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A comprehensive medical practice management system featuring interactive analytics, population statistics, and professional reporting for dental practices.**

[🚀 Quick Start](#-quick-start) • [📚 Documentation](#-documentation) • [🎯 Features](#-key-features) • [🔧 Installation](#-installation)

</div>

## 🎯 Key Features

### 👩‍⚕️ Medical Practice Management
- **Multi-doctor patient segregation** - Secure data isolation per physician
- **Comprehensive patient records** - Full CRUD with duplicate detection
- **Medical history tracking** - Audit trail for all patient changes
- **Professional user interface** - Medical-grade design with Russian localization

### 📊 Advanced Assessment System
- **Schema-based evaluations** - Configurable indicator groups (OHIP, Clinical Status)
- **Flexible scoring engine** - Automatic calculation with custom medical formulas
- **Interactive hexagonal radar charts** - Visual risk assessment with color zones
- **Real-time score calculation** - Dynamic updates as data is entered

### 📈 Population Analytics & Statistics
- **Group average calculations** - Benchmark patients against practice population
- **Z-score analysis** - Statistical outlier detection (±2σ flagging)
- **Population trends** - Track practice-wide health metrics
- **Research data generation** - Export capabilities for clinical research

### 📄 Professional Reporting
- **High-quality PDF reports** - Complete medical assessments with charts
- **Dynamic risk evaluation** - Automatic risk level calculation
- **Custom recommendations** - Personalized treatment suggestions per indicator
- **Professional formatting** - Ready for medical documentation

### 🔐 Security & Compliance
- **Role-based access control** - Doctor, Nurse, Administrator, Researcher roles
- **Session security** - 8-hour timeout with secure cookie handling
- **Data isolation** - Each doctor sees only their patients
- **Audit logging** - Complete activity tracking

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/shpriz/stom-app-gexagonal.git
cd stom-app-gexagonal

# Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# Start the system
docker-compose -f docker-compose.prod.yml up -d --build

# Initialize database
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Access the application
open http://localhost:8000
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (via Docker)
docker-compose up -d db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy                     │
│                (SSL, Rate Limiting, Static Files)         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Django Application                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │   Patients  │ │ Indicators  │ │     Measurements        │ │
│  │             │ │             │ │                         │ │
│  │ - CRUD      │ │ - Schemas   │ │ - Radar Charts          │ │
│  │ - History   │ │ - Scoring   │ │ - PDF Export            │ │
│  │ - Validation│ │ - Ranges    │ │ - Population Analytics  │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                PostgreSQL Database                         │
│              (Optimized for Medical Data)                  │
└─────────────────────────────────────────────────────────────┘
```

## 📚 Documentation

### For Users
- **[👩‍⚕️ User Guide](USER_GUIDE.md)** - Complete guide for medical staff
- **[📋 Recommendations Setup](ИНСТРУКЦИЯ_ПО_РЕКОМЕНДАЦИЯМ.md)** - Configure medical recommendations

### For Administrators  
- **[🔧 Admin Guide](ADMIN_GUIDE.md)** - System administration and configuration
- **[🚀 Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions
- **[⚙️ Technical Instructions](instructions.md)** - Setup and configuration details

### For Developers
- **[🐛 Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
- **[📝 Development Notes](CLAUDE.md)** - Technical specifications and progress

## 🛠️ Installation

### System Requirements

**Minimum:**
- 2GB RAM
- 20GB storage
- Docker & Docker Compose
- Ubuntu 20.04+ / CentOS 8+

**Recommended:**
- 4GB RAM
- 50GB storage
- SSD storage
- Dedicated domain name
- SSL certificate

### Production Deployment

1. **Server Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin -y
```

2. **Application Deployment:**
```bash
# Clone and configure
git clone https://github.com/shpriz/stom-app-gexagonal.git
cd stom-app-gexagonal
cp .env.example .env

# Edit configuration
nano .env

# Deploy
docker-compose -f docker-compose.prod.yml up -d --build
```

3. **Initialize System:**
```bash
# Setup database
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Configure indicators and schemas via admin panel
open http://your-domain.com/admin/
```

### Environment Configuration

```env
# Database
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=stomatology_db

# Django
SECRET_KEY=your_50_character_secret_key
ALLOWED_HOSTS=your-domain.com,your-ip
DEBUG=False

# Security
CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

## 🔧 Configuration

### Medical Indicators Setup

1. **Create Assessment Schemas:**
   - OHIP Quality of Life Assessment
   - Clinical Risk Profile  
   - Custom evaluation frameworks

2. **Configure Indicators:**
   - Set value ranges and units
   - Define color zones for risk levels
   - Establish scoring formulas

3. **Setup Scoring Ranges:**
   - Normal ranges (0-28 = 0 points)
   - Threshold conditions (≥20 = 2 points)
   - Exact value matching (0 = 0 points)

### User Management

1. **Create User Groups:**
   - Врачи (Doctors) - Full patient access
   - Медсестры (Nurses) - Limited access
   - Администраторы (Administrators) - System management

2. **User Profiles:**
   - Medical license information
   - Department assignments
   - Contact details

## 📊 Usage Examples

### Patient Assessment Workflow

```python
# 1. Add new patient
patient = Patient.objects.create(
    first_name="Иван",
    last_name="Петров",
    history_of_illness="12345",
    doctor=current_user
)

# 2. Create measurement
measurement = Measurement.objects.create(
    patient=patient,
    schema=schema_ohip,
    measurement_date=timezone.now()
)

# 3. Add indicator values
MeasurementValue.objects.create(
    measurement=measurement,
    indicator=ohip_indicator,
    raw_value=35,  # Automatically converted to score
    score=1  # Calculated: 29-42 = 1 point
)

# 4. Generate PDF report
pdf_content = generate_medical_report(patient, measurement)
```

### Population Analytics

```python
# Calculate group statistics
from measurements.views import GroupStatisticsView

# Get population averages
stats = GroupStatisticsView.get_group_statistics(schema_id=1)
# Returns: means, std_devs, sample_size

# Calculate z-scores for patient
z_scores = calculate_z_scores(patient_id=1, schema_id=1)
# Returns: statistical comparison to population
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test patients
python manage.py test measurements
python manage.py test indicators

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📋 API Endpoints

### Measurements API
```
GET    /api/measurements/                    # List measurements
POST   /api/measurements/                    # Create measurement
GET    /api/measurements/{id}/               # Get measurement
PUT    /api/measurements/{id}/               # Update measurement
DELETE /api/measurements/{id}/               # Delete measurement

GET    /api/measurements/radar_chart_data/   # Chart data
GET    /api/measurements/group_statistics/   # Population stats
GET    /api/measurements/patient_z_scores/   # Z-score analysis
```

### Chart Data Format
```json
{
  "labels": ["OHIP 14", "Курение", "Медикаменты"],
  "datasets": [{
    "label": "2024-01-15",
    "data": [1, 2, 0],
    "backgroundColor": "rgba(54, 162, 235, 0.2)"
  }],
  "group_averages": [0.8, 1.2, 0.5]
}
```

## 🔒 Security Features

### Authentication & Authorization
- Django session-based authentication
- Role-based permissions
- Multi-factor authentication ready
- Secure password policies

### Data Protection
- Patient data isolation per doctor
- Encrypted database connections
- Secure cookie handling
- CSRF protection
- XSS prevention

### Audit & Compliance
- Complete action logging
- User session tracking
- Data modification history
- Export capabilities for compliance

## 🚀 Performance Optimization

### Database Optimization
```sql
-- PostgreSQL tuning for medical workloads
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

### Caching Strategy
```python
# Redis caching for population statistics
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Static File Optimization
- WhiteNoise for production static files
- Nginx reverse proxy with gzip compression
- CDN-ready asset organization
- Optimized Chart.js loading

## 🔄 Backup & Recovery

### Automated Backups
```bash
#!/bin/bash
# Daily backup script
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
docker-compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U postgres stomatology_db > $BACKUP_DIR/db_$DATE.sql

# Application backup
tar -czf $BACKUP_DIR/app_$DATE.tar.gz \
  /opt/stom-app-gexagonal/media \
  /opt/stom-app-gexagonal/.env
```

### Recovery Procedures
```bash
# Database recovery
docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U postgres stomatology_db < backup_file.sql

# Application recovery
tar -xzf app_backup.tar.gz -C /opt/stom-app-gexagonal/
```

## 🆘 Support & Troubleshooting

### Common Issues

**Static Files Not Loading:**
```bash
# Rebuild static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
docker-compose -f docker-compose.prod.yml restart nginx
```

**Database Connection Issues:**
```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres
docker-compose -f docker-compose.prod.yml restart db
```

**Permission Problems:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER /opt/stom-app-gexagonal
```

### Monitoring
```bash
# System health check
docker-compose -f docker-compose.prod.yml ps
docker stats
df -h

# Application logs
docker-compose -f docker-compose.prod.yml logs -f web
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone for development
git clone https://github.com/shpriz/stom-app-gexagonal.git
cd stom-app-gexagonal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run development server
python manage.py runserver
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact & Support

- **Technical Documentation:** [Full Documentation](USER_GUIDE.md)
- **Issues & Bug Reports:** [GitHub Issues](https://github.com/shpriz/stom-app-gexagonal/issues)
- **Deployment Support:** [Deployment Guide](DEPLOYMENT.md)
- **Admin Documentation:** [Admin Guide](ADMIN_GUIDE.md)

---

<div align="center">

**Built with ❤️ for medical professionals**

*Empowering dental practices with advanced analytics and streamlined patient management*

</div>