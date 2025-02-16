from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.router.lookup_routes import router as lookup_router
from app.router.update_router import router as update_router
from app.services.trie_manager import TrieManager
from app.utils.logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to load and manage Trie during FastAPI app lifecycle."""
    print("Initializing Trie on Startup...")
    TrieManager.initialize_trie()  # Load Trie once on startup
    yield  # Keeps Trie in memory while the app is running
    print("Shutting down... Trie resources cleaned up.")


# Initialize FastAPI application
app = FastAPI(
    lifespan=lifespan,
    title="IP Prefix Lookup API",
    description="API for performing IP lookups against cloud provider prefixes and managing prefix updates.",
    version="1.0.0",
)


# Register API routes
app.include_router(lookup_router)  # Handles IP lookups
app.include_router(update_router)

# Log that the FastAPI server has started
logger.info("FastAPI server is running.")


# Root endpoint to check service health
@app.get("/api/v1/", tags=["Health Check"], summary="API Health Check")
def health_check():
    """
    Health check endpoint to verify that the API is running.

    - **Returns**: A simple message confirming the service is operational.
    - **Example Response**:
    ```json
    {
        "message": "IP Prefix Lookup API is running."
    }
    ```
    """
    return {"message": "IP Prefix Lookup API is running."}
