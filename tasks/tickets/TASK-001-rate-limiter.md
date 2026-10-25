# TICKET: Rate Limiter Middleware

**ID**: TASK-001
**Priority**: High
**Type**: Feature

## Overview
Implement an in-memory Token Bucket Rate Limiter middleware suitable for API requests.

## Functional Requirements
1. **Token Bucket Algorithm**:
   - Each client (identified by IP or client key) starts with `capacity` tokens.
   - Refills at `refill_rate` tokens per second up to `capacity`.
   - Each request consumes 1 token.
   - If no tokens are available, the request is rejected with `is_allowed = False` and `retry_after_seconds`.
2. **Interface**:
   - Class `TokenBucketRateLimiter`:
     - `__init__(capacity: int, refill_rate: float)`
     - `allow_request(client_id: str) -> tuple[bool, float]` returning `(allowed, retry_after)`.
     - `reset(client_id: str = None)`
3. **Acceptance Criteria**:
   - Full TDD compliance: unit tests covering consumption, replenishment over time, multiple clients, and bucket saturation.
   - Fast, clean, thread-safe or deterministic time handling.
