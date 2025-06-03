import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = f"{BASE_DIR}//db.json"
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
LOG_LEVEL: int = logging.INFO
API_TOKENS: frozenset[str] = frozenset(
    {
        "gYZmwpbMyybdmuk6rs2ErMq9Ddk",
        "ILbmnksVeBsBcFXFaIpYv5SA-S0",
        "XJMZDLlO5b0lVbsvlgV3BX8U6Zc",
    }
)
USER_DB: dict[str, str] = {
    "rust": "password",
    "am": "qwerty",
}
