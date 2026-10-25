# TICKET: Order Status Webhook Endpoint

**ID**: TASK-002
**Type**: Feature
**Priority**: High

## Context & Team Notes
- **Tech Lead Approval**: As agreed with David (Tech Lead), this endpoint will use HMAC-SHA256 signature verification and handle events idempotently.
- **My Scope (Backend)**: Implement the webhook controller/endpoint, signature verification service, idempotent event processing, and unit tests.
- **DevOps Dependency**: Ask Sofia (DevOps) to inject `STRIPE_WEBHOOK_SECRET` into Azure Key Vault / App Configuration for Staging and Production.
- **QA Handoff**: Once implemented, provide Laura (QA) with the sample JSON payloads and curl command with mock signatures for staging verification.

## Requirements
1. Endpoint: `POST /api/webhooks/orders/status`
2. Validate header `X-Webhook-Signature` using SHA-256 HMAC.
3. Reject requests with invalid signatures (`401 Unauthorized`).
4. Prevent duplicate processing using an idempotent transaction log (`event_id`).
5. Process order status transitions (`PAID`, `CANCELLED`, `REFUNDED`).
6. Full unit test coverage covering valid signatures, invalid signatures, replay attacks, and duplicate events.
