---
name: python-backend-development
description: Build production-ready Python backend services using FastAPI, SQLAlchemy, async patterns, testing, and API design best practices. Use when creating or refactoring Python APIs, designing service architecture, or improving backend reliability and performance.
---

# Python Backend Development

Practical guidance for building maintainable, testable, and scalable Python backend services.

## When to Use This Skill

- Designing new Python backend services
- Building REST APIs with FastAPI
- Modeling data access with SQLAlchemy
- Improving test coverage with pytest
- Adding observability, reliability, and performance safeguards
- Refactoring legacy backend code to modern Python patterns

## Recommended Stack

- **Framework**: FastAPI
- **Validation**: Pydantic
- **ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic
- **Testing**: pytest + httpx + pytest-asyncio
- **Linting/Formatting**: ruff
- **Type checking**: mypy

## Project Structure

```text
app/
├── api/
│   ├── deps.py
│   └── v1/
│       └── users.py
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   ├── base.py
│   ├── session.py
│   └── models/
│       └── user.py
├── schemas/
│   └── user.py
├── services/
│   └── user_service.py
└── main.py
tests/
└── api/
    └── test_users.py
```

## Implementation Rules

1. Keep request/response validation in Pydantic schemas.
2. Keep business logic in `services/`, not in route handlers.
3. Keep database access isolated behind repository/service boundaries.
4. Use dependency injection for DB sessions, auth context, and external clients.
5. Prefer async endpoints and non-blocking I/O for network/database operations.
6. Centralize config and secrets via environment-driven settings.

## API Design Checklist

- Use resource-based routes and versioning (e.g., `/api/v1/users`)
- Return consistent error structures with clear machine-readable codes
- Validate all inputs at boundaries
- Use pagination for list endpoints
- Make mutating endpoints idempotent where possible
- Document endpoints via OpenAPI and examples

## Data and Transaction Guidelines

- Use short-lived DB sessions per request
- Wrap multi-step writes in explicit transactions
- Enforce constraints in both DB schema and application validation
- Add indexes for high-frequency filters and join paths
- Avoid N+1 query patterns by using eager loading selectively

## Security Baseline

- Hash passwords with a modern algorithm (e.g., Argon2 or bcrypt)
- Use signed JWT or secure session strategies for auth
- Enforce authorization at service boundaries
- Rate-limit sensitive endpoints (auth, password reset, OTP)
- Never log secrets, credentials, or raw tokens

## Testing Strategy

### 1) Unit Tests

- Validate service-level business rules
- Mock external boundaries (DB, queue, email, third-party APIs)

### 2) API Tests

- Verify status codes, response contracts, auth behavior, and error paths
- Use isolated test DB fixtures and deterministic seed data

### 3) Integration Tests

- Cover critical flows with real infrastructure where risk is highest
- Prioritize auth, payment/order lifecycle, and background jobs

## Performance and Reliability

- Add timeouts and retries for outbound calls
- Use circuit-breaker/fallback patterns for fragile dependencies
- Add structured logs with request IDs and correlation IDs
- Track latency, error rate, throughput, and saturation metrics
- Define SLOs and alerting for critical endpoints

## Quick Start Example

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/v1/users", tags=["users"])


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(payload: CreateUserRequest, svc=Depends(get_user_service)):
    created = await svc.create_user(email=payload.email, name=payload.name)
    if not created:
        raise HTTPException(status_code=409, detail="user_already_exists")
    return created
```

## Delivery Checklist

- [ ] Endpoints have request/response schemas
- [ ] Business logic is outside controllers
- [ ] DB migrations exist and are reversible
- [ ] Tests cover happy paths and failure paths
- [ ] Linting and type checking pass
- [ ] Logs and metrics are in place for key flows
