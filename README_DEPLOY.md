# FlowAI Agent Deployment Guide

This project is containerized for easy deployment using Docker.

## Prerequisites
- Docker & Docker Compose installed

## Quick Start
1. **Build and Start**:
   ```bash
   docker-compose up -d
   ```
   The site will be available at `http://localhost:8080`.

2. **Check Logs**:
   ```bash
   docker-compose logs -f
   ```

3. **Stop Server**:
   ```bash
   docker-compose down
   ```

## Architecture
- **Frontend**: Served statically by Flask (`index.html`, etc.)
- **Backend API**: 
    - `/api/check_status`: Polls payment status
    - `/api/update_status`: Updates status (Admin)
- **Database**: SQLite (`orders.db`) persisted via volume mapping.

## Data Persistence
The `orders.db` and `usage_quota.json` files are mapped to the host machine. You can back up these files to preserve user data and order history.
