# DocLM

DocLM is an advanced document reading and interaction platform powered by the ChatGPT API. It allows users to upload, read, and interact with various document formats using natural language. 

## Features

- **AI-Powered Interaction:** Query and interact with documents using natural language.
- **Multi-Format Support:** Manage PDFs, notes, and other document types.
- **Insight Extraction:** Extract summaries and key points automatically.
- **User-Friendly Interface:** Clean and modern design for productivity.

## Development Roadmap

1. **Setup and Configuration**
   - Set up Docker environment and networks.
   - Deploy MySQL and Adminer for database management.
2. **Development Environment**
   - Build and deploy the development server.
   - Set up the question-UI for front-end interaction.
3. **Production Environment**
   - Build and deploy the production server.
4. **Nginx Configuration**
   - Configure Nginx for reverse proxy and load balancing.
5. **API Integration**
   - Integrate the GPT server for handling queries.

## Deployment Instructions

### Prerequisites

- A server with Docker installed.

### SSH into Server

```
ssh -i ~/.ssh/tx_ubuntu.pem ubuntu@43.139.103.223
```

### Create Docker Network
```
docker network create --driver=bridge --subnet=192.168.0.0/24 chat-with-pdf-all-network
```

### MySQL Setup
```
cd mysql
docker-compose -f docker-compose.yaml up -d

make rund
```

### Adminer Setup
```
cd adminer
docker-compose -f docker-compose.yaml up -d

make rund
```

### Server (Development)
```
cd server
docker build -t robot-server:dev -f dev/Dockerfile .
docker-compose -f dev/docker-compose.yaml up -d

make docker && make rund
```

### Server (Production)
```
cd server
docker build -t robot-server:dev -f prod/Dockerfile .
docker-compose -f prod/docker-compose.yaml --env-file prod/.env up -d

make docker && make rund
```

### Question-UI
```
cd question-ui
docker build -t question-ui:dev -f deploy/Dockerfile .
docker-compose -f deploy/docker-compose.yaml up -d

make docker && make rund
```

### Nginx
```
cd nginx
docker build -t nginx:dev -f Dockerfile .
docker-compose -f docker-compose.yaml up -d

make docker && make rund
```

### GPT Server Test
```
curl http://149.28.157.168:8000/gpt -X POST -d '{"auth_code":"heros","question":"hello"}'
```