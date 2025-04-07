# Running the Application with Docker

This guide explains how to run the AI Interview System using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10.0 or higher)
- Docker Compose (version 1.29.0 or higher)
- Git

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd interview-chi-chat
```

2. Create a `.env` file in the root directory and configure the environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and start the containers:
```bash
docker-compose up --build
```

This will start three services:
- Frontend (http://localhost:80)
- Backend (http://localhost:8000)
- OpenSearch (http://localhost:9200)

## Development Mode

For development, you can run the services with hot-reloading:

```bash
# Start the services
docker-compose up

# In a separate terminal, run the backend with hot-reloading
docker-compose exec backend uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, run the frontend with hot-reloading
docker-compose exec frontend npm start
```

## Accessing the Services

- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- OpenSearch: http://localhost:9200

## Managing the Services

```bash
# Stop all services
docker-compose down

# Stop and remove all containers, networks, and volumes
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for a specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f opensearch
```

## Troubleshooting

1. **Port Conflicts**
   - If you encounter port conflicts, modify the port mappings in `docker-compose.yml`

2. **OpenSearch Memory Issues**
   - If OpenSearch fails to start due to memory issues, adjust the memory settings in `docker-compose.yml`:
     ```yaml
     environment:
       - "OPENSEARCH_JAVA_OPTS=-Xms256m -Xmx256m"
     ```

3. **Environment Variables**
   - Ensure all required environment variables are set in the `.env` file
   - The application won't start without a valid OpenAI API key

4. **Volume Permissions**
   - If you encounter permission issues with volumes, you may need to adjust the permissions:
     ```bash
     sudo chown -R $USER:$USER .
     ```

## Production Deployment

For production deployment:

1. Set appropriate environment variables
2. Use HTTPS for all services
3. Configure proper security settings
4. Set up monitoring and logging
5. Use a reverse proxy (e.g., Nginx) for the frontend

Example production configuration:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [OpenSearch Documentation](https://opensearch.org/docs/latest/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html) 