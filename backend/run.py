import subprocess
import time
import uvicorn
from app.core.config import settings

def start_docker_dependencies():
    print("Orchestrating PostgreSQL database container...")
    
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: Docker command not found. Assuming Postgres is managed externally.")
        return

    try:
        subprocess.run(["docker", "compose", "up", "-d", "db"], cwd="..", check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["docker-compose", "up", "-d", "db"], cwd="..", check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error starting database container: {e}")
            return

    print("Waiting for database container (fashop_db) to become healthy...")
    max_retries = 15
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format={{.State.Health.Status}}", "fashop_db"],
                capture_output=True,
                text=True,
                check=True
            )
            status = result.stdout.strip()
            if status == "healthy":
                print("Database container is healthy and ready to accept connections!")
                break
        except subprocess.CalledProcessError:
            pass
        
        print(f"   [Attempt {attempt}/{max_retries}] Waiting for database healthcheck...")
        time.sleep(1.5)
    else:
        print("Warning: Healthcheck timed out. Booting local server anyway...")

if __name__ == "__main__":
    start_docker_dependencies()
    
    print("Starting local Uvicorn development server...")
    uvicorn.run(
        'app.main:app',
        host='0.0.0.0',
        port=8000,
        reload=settings.debug,
        log_level='info'
    )