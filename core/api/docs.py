from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

# Schema view for API documentation
schema_view = get_schema_view(
    title="Discuss API",
    description="API for the Discuss social platform",
    version="1.0.0"
)

# Documentation view
docs_view = include_docs_urls(
    title="Discuss API Documentation",
    description="RESTful API for the Discuss social platform"
)