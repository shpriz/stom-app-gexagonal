#!/bin/bash

# Deployment script for stomatology practice management system

echo "🚀 Starting deployment..."

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --settings=dental_office.settings_prod

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=dental_office.settings_prod

# Create superuser if needed (optional)
echo "👤 Creating superuser (if needed)..."
python manage.py shell --settings=dental_office.settings_prod -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "✅ Deployment completed!"
echo "🌐 Your application should now be accessible at: http://82.202.140.211/"
echo ""
echo "🔧 To restart the application:"
echo "docker-compose down && docker-compose up -d"