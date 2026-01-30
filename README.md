# GitHub Webhook Receiver

A Flask application that receives GitHub webhook events (Push, Pull Request, Merge) and displays them in a real-time dashboard.

## Features

- Receives GitHub webhook events via POST endpoint
- Stores events in MongoDB with structured schema
- Real-time dashboard that polls every 15 seconds
- Supports Push, Pull Request, and Merge events

## Prerequisites

- Python 3.8+
- Docker & Docker Compose (for MongoDB)

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd webhook-repo
```

### 2. Start MongoDB

```bash
docker-compose up -d
```

### 3. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure environment (optional)

```bash
cp .env.example .env
edit .env file accordingly
```

### 5. Run the application

```bash
python run.py
```

The application will be available at `http://localhost:5000`
