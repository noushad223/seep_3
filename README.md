# SEEP Project

This project consists of a Svelte frontend and a Python backend.

## Prerequisites

- Docker and Docker Compose
- Python 
- Node.js (for development)
- npm (for development)

## Development Setup

1. First, install the frontend dependencies:
```bash
cd front
npm install
```

2. Start the development environment:
```bash
docker compose -f docker-compose.dev.yml up --build
```

The development server will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

### Note:
- Use `docker compose -f docker-compose.dev.yml down` to stop the development environment.

## Production Setup

1. Build and run the production environment:
```bash
docker compose -f docker-compose.prod.yml up --build

```

### Note:
- Use `docker compose -f docker-compose.prod.yml down` to stop the production environment.

The production servers will be available at:
- Frontend: http://localhost:4173
- Backend: http://localhost:8000

