# Pest Management Chatbot

A chatbot system that leverages indigenous agricultural knowledge for pest management, using a rule-based approach and Prolog for knowledge representation.

## Features

- Rule-based chatbot for agricultural pest management
- Prolog knowledge base integration
- Indigenous knowledge representation
- Responsive web interface
- Containerized deployment with Docker

## Prerequisites

- Docker
- Docker Compose

## Setup and Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pest-management-chatbot
   ```

2. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

3. The application will be available at:
   - Web Interface: http://localhost
   - API Endpoint: http://localhost/api/chat

4. To stop the application:
   ```
   docker-compose down
   ```

### For Windows Users

Use the provided batch file to start the application:
```
start_docker.bat
```

### Manual Setup (Without Docker)

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   python manage.py migrate
   ```

4. Run the development server:
   ```
   python manage.py runserver
   ```

## Docker Commands for Database Management and Development

### Accessing the PostgreSQL Database

```bash
# Connect to the PostgreSQL database
docker-compose exec db psql -U postgres -d farmlore

# View all tables
docker-compose exec db psql -U postgres -d farmlore -c "\dt"

# View data in a specific table
docker-compose exec db psql -U postgres -d farmlore -c "SELECT * FROM community_indigenousknowledge;"
```

### Running Python Scripts in Containers

```bash
# Run a Python script in the web container
docker-compose exec web python your_script.py

# Run a Django management command
docker-compose exec web python manage.py shell

# Create a superuser
docker-compose exec web python manage.py createsuperuser
```

### Database Visualization

For visualizing the database tables, you can:

1. Use the Django Admin interface at http://localhost:8000/admin/
2. Connect a database tool like pgAdmin or DBeaver to the PostgreSQL database:
   ```
   Host: localhost (with port exposed in docker-compose.yml)
   Port: 5432
   Username: postgres
   Password: your_password
   Database: farmlore
   ```
3. Use the Django shell for direct queries:
   ```bash
   docker-compose exec web python manage.py shell
   
   # Then in the shell:
   from community.models import IndigenousKnowledge
   entries = IndigenousKnowledge.objects.all()
   for entry in entries:
       print(f"ID: {entry.id}, Title: {entry.title}")
   ```

For a more comprehensive list of Docker commands for managing the FarmLore application, see the [Docker Commands Guide](docker_commands.md).

## Architecture

The application consists of three main services:

1. **Web Service**: Django application running the chatbot
2. **Database**: PostgreSQL for storing chat history and user data
3. **Nginx**: Web server for serving static files and proxying requests
4. **Ollama**: Service running the Ollama large language models. Custom models defined via local modelfiles are built into this service's Docker image.

## Extending the Knowledge Base

The system uses Prolog to represent agricultural knowledge. To extend the knowledge base:

1. Edit the `knowledgebase.pl` file
2. Add new facts and rules about pests, crops, and management practices
3. Restart the application to load the new knowledge

## Development

### Directory Structure

- `chatbot/`: Main application code
  - `services/`: Contains the chatbot implementation
  - `prolog/`: Prolog integration
  - `templates/`: HTML templates
- `pest_management/`: Django project settings
- `nginx/`: Nginx configuration
- `static/`: Static assets
- `media/`: User-uploaded content
- `prolog_integration/`: Prolog knowledge base

### Contributing

1. Create a feature branch
2. Implement your changes
3. Write tests
4. Submit a pull request 