# 🚨 Руководство по устранению неполадок - Система управления стоматологической практикой

## 🎯 Общие принципы диагностики

При возникновении проблем следуйте систематическому подходу:
1. **Определите симптомы** - что именно не работает
2. **Проверьте логи** - найдите сообщения об ошибках  
3. **Воспроизведите проблему** - убедитесь в стабильности ошибки
4. **Примените решение** - используйте проверенные методы
5. **Протестируйте результат** - убедитесь в устранении проблемы

## 🔍 Диагностические команды

### Быстрая проверка состояния системы

```bash
# Статус всех сервисов
docker-compose -f docker-compose.prod.yml ps

# Проверка доступности приложения
curl -I http://localhost:8000/auth/login/

# Проверка базы данных
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres

# Использование ресурсов
docker stats --no-stream

# Место на диске
df -h
```

### Просмотр логов

```bash
# Логи всех сервисов (последние 100 строк)
docker-compose -f docker-compose.prod.yml logs --tail=100

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
docker-compose -f docker-compose.prod.yml logs -f nginx

# Логи Django внутри контейнера
docker-compose -f docker-compose.prod.yml exec web tail -f /app/logs/django.log
```

## 🌐 Проблемы с доступом к сайту

### ❌ Сайт не открывается (Connection refused)

**Симптомы:**
- Браузер показывает "Не удается получить доступ к сайту"
- Timeout при подключении
- ERR_CONNECTION_REFUSED

**Диагностика:**
```bash
# Проверка запущенных сервисов
docker-compose -f docker-compose.prod.yml ps

# Проверка портов
netstat -tulpn | grep :80
netstat -tulpn | grep :8000

# Проверка логов nginx
docker-compose -f docker-compose.prod.yml logs nginx
```

**Решения:**

1. **Перезапуск сервисов:**
```bash
docker-compose -f docker-compose.prod.yml restart nginx
docker-compose -f docker-compose.prod.yml restart web
```

2. **Проверка конфигурации nginx:**
```bash
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

3. **Полная перезагрузка:**
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### ❌ Сайт открывается, но показывает ошибку 500

**Симптомы:**
- Белая страница с "Server Error (500)"
- Внутренняя ошибка сервера

**Диагностика:**
```bash
# Проверка логов Django
docker-compose -f docker-compose.prod.yml logs web | grep ERROR

# Проверка подключения к базе данных
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

**Решения:**

1. **Проверка настроек базы данных:**
```bash
# Вход в Django shell
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
```

2. **Применение миграций:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

3. **Перезапуск с очисткой:**
```bash
docker-compose -f docker-compose.prod.yml restart web
```

### ❌ Статические файлы не загружаются (CSS/JS)

**Симптомы:**
- Сайт открывается, но без стилей
- 404 ошибки для файлов .css и .js
- Страница выглядит "сломанной"

**Диагностика:**
```bash
# Проверка статических файлов в контейнере
docker-compose -f docker-compose.prod.yml exec web ls -la /app/staticfiles/css/

# Проверка конфигурации nginx для статики
docker-compose -f docker-compose.prod.yml exec nginx cat /etc/nginx/nginx.conf | grep static
```

**Решения:**

1. **Пересборка статических файлов:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

2. **Перезапуск nginx:**
```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

3. **Полная пересборка контейнера:**
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🗄️ Проблемы с базой данных

### ❌ Ошибка подключения к базе данных

**Симптомы:**
- "Database connection failed"
- "FATAL: password authentication failed"
- "could not connect to server"

**Диагностика:**
```bash
# Статус контейнера базы данных
docker-compose -f docker-compose.prod.yml ps db

# Проверка готовности PostgreSQL
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres

# Логи базы данных
docker-compose -f docker-compose.prod.yml logs db
```

**Решения:**

1. **Перезапуск базы данных:**
```bash
docker-compose -f docker-compose.prod.yml restart db
# Подождите 30 секунд для полной загрузки
sleep 30
```

2. **Проверка переменных окружения:**
```bash
# Проверка паролей в .env файле
cat .env | grep POSTGRES_PASSWORD
```

3. **Восстановление из резервной копии:**
```bash
# При критических ошибках базы данных
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres stomatology_db < backup_latest.sql
```

### ❌ Ошибки миграций Django

**Симптомы:**
- "Migration failed"
- "Table already exists"
- "Column does not exist"

**Диагностика:**
```bash
# Проверка статуса миграций
docker-compose -f docker-compose.prod.yml exec web python manage.py showmigrations

# Проверка состояния базы данных
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

**Решения:**

1. **Применение миграций:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

2. **Фальшивое применение проблемной миграции:**
```bash
# Если миграция уже была применена вручную
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --fake app_name migration_name
```

3. **Сброс миграций (ОСТОРОЖНО!):**
```bash
# Только в крайнем случае - потеря данных!
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate app_name zero
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## 👤 Проблемы с пользователями и авторизацией

### ❌ Не могу войти в систему

**Симптомы:**
- "Invalid username or password"
- Форма входа не принимает правильные данные
- Перенаправление на страницу входа после ввода данных

**Диагностика:**
```bash
# Проверка существования пользователя
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username='your_username').exists()
>>> user = User.objects.get(username='your_username')
>>> user.is_active
>>> user.check_password('your_password')
```

**Решения:**

1. **Сброс пароля пользователя:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='your_username')
>>> user.set_password('new_password')
>>> user.save()
```

2. **Создание нового суперпользователя:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

3. **Активация заблокированного пользователя:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='your_username')
>>> user.is_active = True
>>> user.save()
```

### ❌ Проблемы с правами доступа

**Симптомы:**
- "Permission denied"
- Пользователь не видит своих пациентов
- Ошибки доступа к админ-панели

**Диагностика:**
```bash
# Проверка групп пользователя
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='username')
>>> user.groups.all()
>>> user.is_staff
>>> user.is_superuser
```

**Решения:**

1. **Добавление в группу "Врачи":**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from django.contrib.auth.models import User, Group
>>> user = User.objects.get(username='username')
>>> doctors_group = Group.objects.get(name='Врачи')
>>> user.groups.add(doctors_group)
```

2. **Предоставление прав персонала:**
```bash
>>> user = User.objects.get(username='username')
>>> user.is_staff = True
>>> user.save()
```

## 📊 Проблемы с диаграммами и измерениями

### ❌ Диаграммы не отображаются

**Симптомы:**
- Пустая область вместо диаграммы
- Ошибка "Chart is not defined"
- Диаграмма не загружается

**Диагностика:**
```bash
# Проверка доступности Chart.js
curl -I https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js

# Проверка данных для диаграммы
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from measurements.models import Measurement
>>> Measurement.objects.filter(patient_id=1).count()
```

**Решения:**

1. **Очистка кэша браузера:**
   - Нажмите Ctrl+F5 (или Cmd+Shift+R на Mac)
   - Откройте Developer Tools → Network → Disable cache

2. **Проверка подключения к CDN:**
```html
<!-- В шаблоне должно быть -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js"></script>
```

3. **Перезагрузка страницы с диаграммой:**
```bash
# Проверка API данных диаграммы
curl "http://localhost:8000/api/measurements/radar_chart_data/?patient_id=1"
```

### ❌ Некорректные баллы в измерениях

**Симптомы:**
- Баллы не рассчитываются автоматически
- Неправильные значения на диаграмме
- Ошибки в расчете общего балла

**Диагностика:**
```bash
# Проверка диапазонов оценок
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from indicators.models import Indicator, ScoringRange
>>> indicator = Indicator.objects.get(name='Курение')
>>> ScoringRange.objects.filter(indicator=indicator)
```

**Решения:**

1. **Проверка настроек диапазонов оценок:**
   - Перейдите в админ-панель → Диапазоны оценок
   - Убедитесь, что все диапазоны настроены правильно
   - Проверьте отсутствие пересечений в диапазонах

2. **Пересчет существующих измерений:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from measurements.models import MeasurementValue
>>> for mv in MeasurementValue.objects.all():
...     mv.save()  # Триггер пересчета балла
```

## 📄 Проблемы с PDF отчетами

### ❌ PDF не генерируются

**Симптомы:**
- Кнопка PDF не работает
- Ошибка при генерации отчета
- Пустой или поврежденный PDF файл

**Диагностика:**
```bash
# Проверка библиотек для PDF
docker-compose -f docker-compose.prod.yml exec web python -c "
import reportlab
import base64
import io
print('PDF libraries OK')
"

# Проверка места на диске
df -h
```

**Решения:**

1. **Установка недостающих библиотек:**
```bash
# Если нужно установить дополнительные пакеты
docker-compose -f docker-compose.prod.yml exec web pip install reportlab Pillow
```

2. **Очистка временных файлов:**
```bash
# Очистка места на диске
docker system prune -a
```

3. **Проверка данных для отчета:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from measurements.models import Measurement
>>> m = Measurement.objects.filter(patient_id=1).first()
>>> m.measurementvalue_set.all()
```

## 🔧 Системные проблемы

### ❌ Нехватка места на диске

**Симптомы:**
- "No space left on device"
- Ошибки записи в логи
- Невозможность сохранения данных

**Диагностика:**
```bash
# Проверка использования диска
df -h

# Размер Docker данных
docker system df

# Большие файлы в системе
du -sh /var/lib/docker/*
```

**Решения:**

1. **Очистка Docker:**
```bash
# Удаление неиспользуемых образов и контейнеров
docker system prune -a

# Удаление старых логов
docker-compose -f docker-compose.prod.yml exec web find /app/logs -name "*.log" -mtime +30 -delete
```

2. **Очистка системных логов:**
```bash
# Очистка системных журналов
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=100M
```

### ❌ Высокое использование памяти

**Симптомы:**
- Медленная работа системы
- "Out of memory" ошибки
- Перезапуски контейнеров

**Диагностика:**
```bash
# Использование памяти контейнерами
docker stats --no-stream

# Общее использование памяти
free -m

# Процессы, потребляющие память
top -o %MEM
```

**Решения:**

1. **Перезапуск сервисов:**
```bash
docker-compose -f docker-compose.prod.yml restart
```

2. **Добавление swap файла:**
```bash
# Создание 2GB swap файла
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Добавление в /etc/fstab для постоянного использования
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

3. **Ограничение памяти для контейнеров:**
```yaml
# В docker-compose.prod.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
```

## 🚨 Экстренное восстановление

### Полный сбой системы

**Пошаговый план восстановления:**

1. **Остановка всех сервисов:**
```bash
docker-compose -f docker-compose.prod.yml down
```

2. **Проверка файловой системы:**
```bash
# Проверка места на диске
df -h

# Проверка системных ошибок
dmesg | tail -20
```

3. **Восстановление из резервной копии:**
```bash
# Запуск только базы данных
docker-compose -f docker-compose.prod.yml up -d db

# Ожидание готовности
sleep 30

# Восстановление данных
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres stomatology_db < backup_latest.sql
```

4. **Постепенный запуск сервисов:**
```bash
# Запуск веб-приложения
docker-compose -f docker-compose.prod.yml up -d web

# Проверка работоспособности
curl -f http://localhost:8000/auth/login/

# Запуск nginx
docker-compose -f docker-compose.prod.yml up -d nginx
```

### Контрольный чек-лист после восстановления

- [ ] Все сервисы запущены: `docker-compose ps`
- [ ] База данных доступна: `pg_isready`
- [ ] Сайт открывается: `curl -I http://localhost:8000`
- [ ] Авторизация работает
- [ ] Пациенты отображаются корректно
- [ ] Диаграммы загружаются
- [ ] PDF отчеты генерируются

## 📞 Служба поддержки

### Информация для технической поддержки

При обращении в службу поддержки предоставьте:

1. **Описание проблемы:**
   - Что вы пытались сделать
   - Что произошло вместо ожидаемого результата
   - Воспроизводится ли проблема стабильно

2. **Системная информация:**
```bash
# Версия системы
cat /etc/os-release

# Версии Docker
docker --version
docker-compose --version

# Статус сервисов
docker-compose -f docker-compose.prod.yml ps
```

3. **Логи ошибок:**
```bash
# Сохранение логов в файл
docker-compose -f docker-compose.prod.yml logs > system_logs.txt
```

4. **Конфигурация:**
   - Содержимое .env файла (БЕЗ паролей!)
   - Версия приложения
   - Последние изменения в системе

### Временные обходные пути

**Если система критически не работает:**

1. **Переключение на резервный сервер** (если доступен)
2. **Использование локальной копии** для критичных данных
3. **Документирование проблем** в бумажном виде до восстановления
4. **Уведомление пользователей** о проблемах и времени восстановления

---

## 🎯 Профилактика проблем

### Регулярное обслуживание

**Ежедневно:**
- Проверка логов на ошибки
- Мониторинг использования ресурсов
- Контроль доступности сервисов

**Еженедельно:**
- Создание резервных копий
- Очистка старых логов
- Проверка обновлений безопасности

**Ежемесячно:**
- Полное тестирование восстановления
- Анализ производительности
- Обновление документации

### Мониторинг и алерты

**Настройка автоматических проверок:**
```bash
#!/bin/bash
# monitoring.sh - скрипт для cron

# Проверка доступности
if ! curl -f http://localhost:8000/auth/login/ > /dev/null 2>&1; then
    echo "ALERT: Сайт недоступен $(date)" | mail -s "System Alert" admin@example.com
fi

# Проверка места на диске
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
    echo "ALERT: Диск заполнен на $DISK_USAGE% $(date)" | mail -s "Disk Space Alert" admin@example.com
fi
```

**Успешного устранения неполадок! 🔧**