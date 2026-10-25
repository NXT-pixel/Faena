# Feature: User Activity Logger

## Problem Statement
We need a lightweight service that logs user actions (user_id, action, timestamp) and allows querying actions for a user.

## Requirements
1. Implement an ActivityLogger class with `log_action(user_id, action)` and `get_actions(user_id)`.
2. Persist actions in-memory or in a file.
3. Include unit tests covering normal logging, filtering, and empty queries.
