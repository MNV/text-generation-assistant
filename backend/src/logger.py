import logging
import structlog
from structlog.processors import (
    JSONRenderer,
    TimeStamper,
    add_log_level,
    StackInfoRenderer,
)


logging.basicConfig(
    level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
)

structlog.configure(
    processors=[
        add_log_level,
        TimeStamper(fmt="iso"),
        StackInfoRenderer(),
        structlog.processors.format_exc_info,
        JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger("text-generation-assistant")
