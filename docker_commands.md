# Docker Commands for FarmLore

This document provides useful Docker commands for managing the FarmLore application, accessing the database, and running scripts within containers.

## Basic Docker Commands

### Starting and Stopping the Application

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart a specific service (e.g., web)
docker-compose restart web

# View logs for all services
docker-compose logs

# View logs for a specific service with follow option
docker-compose logs -f web
```

## Database Management

### Accessing the PostgreSQL Database

```bash
# Connect to the PostgreSQL database
docker-compose exec db psql -U postgres -d farmlore

# Backup the database
docker-compose exec db pg_dump -U postgres -d farmlore > backup_$(date +%Y%m%d).sql

# Restore a database backup
cat backup_file.sql | docker-compose exec -T db psql -U postgres -d farmlore
```

### Useful PostgreSQL Commands

Once connected to the PostgreSQL database, you can use these commands:

```sql
-- List all tables
\dt

-- Describe a specific table
\d+ community_indigenousknowledge

-- View all entries in a table
SELECT * FROM community_indigenousknowledge;

-- View specific columns
SELECT id, title, verification_status FROM community_indigenousknowledge;

-- Filter entries
SELECT * FROM community_indigenousknowledge WHERE verification_status = 'pending';

-- Count entries
SELECT COUNT(*) FROM community_indigenousknowledge;

-- Join tables to get more information
SELECT k.title, u.username 
FROM community_indigenousknowledge k 
JOIN community_knowledgekeeper kk ON k.keeper_id = kk.id 
JOIN auth_user u ON kk.user_id = u.id;

-- Exit PostgreSQL
\q
```

## Running Python Scripts and Commands

### Execute Python Scripts in the Web Container

```bash
# Run a specific Python script
docker-compose exec web python your_script.py

# Run a Django management command
docker-compose exec web python manage.py shell

# Create a superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Check migration status
docker-compose exec web python manage.py showmigrations
```

### Using Django Shell for Database Queries

```bash
# Start the Django shell
docker-compose exec web python manage.py shell

# Example commands to run in the shell:
# from community.models import IndigenousKnowledge
# entries = IndigenousKnowledge.objects.all()
# for entry in entries:
#     print(f"ID: {entry.id}, Title: {entry.title}, User: {entry.keeper.user.username}")
```

### Running One-off Commands

```bash
# Run a bash shell in the web container
docker-compose exec web bash

# Create a new Python file and edit it
docker-compose exec web bash -c "echo 'print(\"Hello World\")' > test.py && python test.py"

# Check the Django version
docker-compose exec web python -c "import django; print(django.get_version())"
```

## Monitoring and Debugging

### View Container Status

```bash
# List all running containers
docker-compose ps

# View container resource usage
docker stats
```

### Debugging Issues

```bash
# Check web container logs
docker-compose logs web

# Inspect a specific container
docker inspect farmlore-master_web_1

# View network settings
docker network ls
docker network inspect farmlore-master_default
```

## Database Visualization

For visualizing the database, you can use tools like:

1. **pgAdmin** - Connect to the PostgreSQL database:
   ```bash
   # Expose PostgreSQL port (add to docker-compose.yml under db service)
   # ports:
   #   - "5432:5432"
   
   # Then connect pgAdmin to:
   # Host: localhost
   # Port: 5432
   # Username: postgres
   # Password: your_password
   ```

2. **DBeaver** - Free universal database tool:
   - Download from: https://dbeaver.io/
   - Create a new PostgreSQL connection
   - Use the same connection details as above

3. **Django Admin** - Built-in visualization:
   - Access at: http://localhost:8000/admin/
   - Login with your superuser credentials

## Common Troubleshooting

```bash
# Restart all services
docker-compose restart

# Rebuild a specific service
docker-compose build web
docker-compose up -d web

# Check for errors in Django
docker-compose exec web python manage.py check

# Clear all Docker caches (when things get weird)
docker system prune -a
```

## Quick Reference for Common Tasks

| Task | Command |
|------|---------|
| Start all services | `docker-compose up -d` |
| Stop all services | `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Connect to database | `docker-compose exec db psql -U postgres -d farmlore` |
| Run Django shell | `docker-compose exec web python manage.py shell` |
| Run migrations | `docker-compose exec web python manage.py migrate` |
| Create superuser | `docker-compose exec web python manage.py createsuperuser` |
| Restart web server | `docker-compose restart web` |
| Run a Python script | `docker-compose exec web python your_script.py` |
