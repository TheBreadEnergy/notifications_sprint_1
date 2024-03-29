from fastapi import Query
from fastapi_pagination import Page

PaginatedPage = Page.with_custom_options(
    size=Query(10, description="Page size", ge=1),
    page=Query(1, description="Page number", ge=1),
)
