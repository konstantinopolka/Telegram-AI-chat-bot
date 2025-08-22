# Bot Project: Docker & Docker Compose Guide

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Docker Compose](https://docs.docker.com/compose/) (included with Docker Desktop)
- WSL2 integration enabled (if using Windows)

## Project Structure

```
/
├── src/                # Bot source code
├── requirements/       # Python requirements files
├── main.py             # Bot entry point
├── docker/
│   ├── Dockerfile      # Dockerfile for bot
│   ├── docker-compose.yml
│   └── database.env    # Database environment variables
```

## Quick Start

1. **Configure Environment Variables**

   - Edit `docker/database.env` for database credentials.
   - Create a `.env` file in `docker/` for bot-specific environment variables (if needed).

2. **Build and Start Services**

   Open a terminal in the `docker/` directory and run:

   ```sh
   docker-compose up --build -d
   ```

   This will:
   - Build the bot image
   - Start the PostgreSQL database and bot containers in the background

3. **Check Running Containers**

   ```sh
   docker-compose ps
   ```

4. **View Logs**

   ```sh
   docker-compose logs bot
   ```

5. **Stop Services**

   ```sh
   docker-compose down
   ```

## Development Tips

- For SQLite development, mount your `dev.db` file in `docker-compose.yml` under the `bot` service.
- To rebuild the bot image after code changes, use:
  ```sh
  docker-compose up --build bot
  ```

## Troubleshooting

- **Permission denied errors:**  
  Add your user to the Docker group and restart your terminal:
  ```sh
  sudo usermod -aG docker $USER
  ```

- **Docker not detected in VS Code:**  
  Make sure Docker Desktop is running and WSL2 integration is enabled.

## Useful Commands

- Build images:  
  ```sh
  docker-compose build
  ```
- Restart services:  
  ```sh
  docker-compose restart
  ```
- Remove all containers and volumes:  
  ```sh
  docker-compose down -v
  ```

---

**For more details, see the official [Docker Compose documentation](https://docs.docker.com/compose/).**