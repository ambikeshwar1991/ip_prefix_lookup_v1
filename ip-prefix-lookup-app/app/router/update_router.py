from fastapi import APIRouter, HTTPException
from app.services.trie_manager import TrieManager
from app.utils.logging_config import logger

router = APIRouter(prefix="/api/v1/reload", tags=["Prefix reload"])

@router.post("/")
def reload_prefixes():
    """
    Endpoint to manually reload the Trie from `prefixes.json`.

    This function:
    - Reads the latest `prefixes.json` file.
    - Updates the Compressed Radix Trie with new prefix data.
    - Logs every reload request for tracking.

    Returns:
        JSON response confirming successful reload or an error message.
    """
    try:
        logger.info("Reload request received. Reloading Trie from prefixes.json...")

        # Call TrieManager to reinitialize the Trie from the latest `prefixes.json`
        TrieManager.initialize_trie()

        logger.info("Trie reloaded successfully.")
        return {"message": "Trie reloaded successfully"}

    except Exception as e:
        logger.exception(f"Error reloading Trie: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reloading Trie: {str(e)}")
