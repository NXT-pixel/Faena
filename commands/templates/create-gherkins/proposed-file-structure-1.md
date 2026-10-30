# Proposed File Structure

_Plantilla extraida de commands/create-gherkins.md: se lee solo cuando hace falta, para no cargar el comando completo._

```

**Note**: Some user stories span multiple feature files. Each will be listed under relevant feature sections.

---

## Feature File: features/identity_management/user_invitation.feature

**Business Domain**: User identity and onboarding
**User Stories Covered**: UM-001 (complete), UM-002 (complete)
**Total Scenarios**: 15 scenarios

### User Story: UM-001 - User Invitation

**Source**: [PRD lines XXX-XXX](../../path/to/prd.md#LXXX-LXXX)
**Priority**: High/Medium/Low
**Target File**: `features/identity_management/user_invitation.feature`

**Acceptance Criteria:**
- [ ] AC1: Invitation applies to current tenant → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
- [ ] AC2: Cannot invite without role OR license → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
- [ ] AC3: If user exists, add to tenant → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
- [ ] AC4: If user is new, create on acceptance → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
- [ ] AC5: System sends invitation email (Validated in: all positive scenarios)
- [ ] AC6: System records invitation date/time (Validated in: all scenarios)
- [ ] AC7: Invitation appears in pending list (Validated in: all scenarios)
- [ ] AC8: Invitation expires after configured period → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
- [ ] AC9: Reserved licenses return on expiry → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
- [ ] AC10: Multiple invites activate together → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)

**Planned Scenarios:**
- [ ] Happy path: Invite with License Admin role
- [ ] Happy path: Invite with product license
- [ ] Negative: Cannot invite without role/license
- [ ] Edge case: Inviting existing user adds to tenant
- [ ] Edge case: User accepts invitation activates account
- [ ] Boundary: Expired invitation returns license
- [ ] Multi-tenant: Multiple invites activate together

**Negative Scenarios from Checklist:**
- [ ] Invalid email format
- [ ] User already active (non-pending) in tenant
- [ ] Re-sending to user with pending invite

**Cross-Cutting Concerns:**
- [ ] Audit logging validated (all state-changing scenarios)
- [ ] Email notification validated (all positive scenarios)
- [ ] Multi-tenant context clear (background + scenarios)

### User Story: UM-002 - User Account Setup

**Source**: [PRD lines YYY-YYY](../../path/to/prd.md#LYYY-LYYY)
**Priority**: High/Medium/Low
**Target File**: `features/identity_management/user_invitation.feature`

**Acceptance Criteria:**
- [ ] AC1: User clicks invitation link → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
- [ ] AC2: User creates password → [Lines TBD](features/identity_management/user_invitation.feature#LTBD)
[...continue for UM-002...]

---

## Feature File: features/license_management/license_assignment.feature

**Business Domain**: License operations and management
**User Stories Covered**: LM-003 (complete)
**Total Scenarios**: 12 scenarios

### User Story: LM-003 - License Assignment

**Source**: [PRD lines ZZZ-ZZZ](../../path/to/prd.md#LZZZ-LZZZ)
**Priority**: High/Medium/Low
**Target File**: `features/license_management/license_assignment.feature`

[Same structure as above for LM-003]

---

## Feature File: features/api/token_exchange.feature

**Business Domain**: Authentication and authorization
**User Stories Covered**: API-002 (complete), LM-009 (partial)
**Total Scenarios**: 20 scenarios

### User Story: API-002 - Token Exchange

**Source**: [PRD lines AAA-AAA](../../path/to/prd.md#LAAA-LAAA)
**Priority**: High
**Target File**: `features/api/token_exchange.feature`

[Full API-002 scenarios here]

### User Story: LM-009 - Product License Scope Check (Partial)

**Source**: [PRD lines BBB-BBB](../../path/to/prd.md#LBBB-LBBB)
**Priority**: High
**Target File**: `features/api/token_exchange.feature`
**Note**: This user story spans multiple features. See also: `features/authorization/scope_validation.feature`

**Acceptance Criteria (covered in this file):**
- [ ] AC1-AC5: Token exchange and scope retrieval → [Lines TBD](features/api/token_exchange.feature#LTBD)
- [ ] AC6-AC10: Detailed scope mapping → See `scope_validation.feature`

[Scenarios specific to token exchange flow]

---

## Traceability Matrix

| Feature File | User Story | AC# | Acceptance Criterion | Scenario Line# | Status |
|--------------|------------|-----|---------------------|----------------|---------|
| user_invitation.feature | UM-001 | AC1 | Invitation to current tenant | [L10-L20](features/identity_management/user_invitation.feature#L10-L20) | ✅ |
| user_invitation.feature | UM-001 | AC2 | Cannot invite w/o role or license | [L25-L35](features/identity_management/user_invitation.feature#L25-L35) | ✅ |
| license_assignment.feature | LM-003 | AC1 | Tenant-scoped assignment | [L12-L22](features/license_management/license_assignment.feature#L12-L22) | ✅ |
| token_exchange.feature | API-002 | AC1 | Token type detection | [L100-L110](features/api/token_exchange.feature#L100-L110) | ✅ |

---

## Coverage Gaps & Decisions

**Deliberate Exclusions:**
- [List any acceptance criteria not covered with justification]

**Open Questions:**
- [Any ambiguities in PRD requiring clarification]

**Notes:**
- [Any relevant observations about test design]
- [Rationale for user stories spanning multiple features]

---

## Completion Status

**Progress Tracking:**
- [ ] All feature files have complete scenario lists
- [ ] All acceptance criteria have scenarios (check each user story section)
- [ ] All planned scenarios written (check Planned Scenarios lists)
- [ ] All negative scenarios from checklist addressed
- [ ] All cross-cutting concerns validated (audit, email, multi-tenant)
- [ ] Traceability matrix updated with linked line numbers
- [ ] Coverage gaps documented (if any)
- [ ] Searched file for "- [ ]" pattern - ZERO unchecked boxes remain
- [ ] All feature files written to correct paths

**Final Verification:** 
DO NOT mark complete until you have:
1. Searched entire file for "- [ ]" pattern
2. Confirmed ZERO unchecked boxes remain (or all exclusions documented)
3. Verified traceability matrix has line numbers for all scenarios
4. Verified all PRD links work
5. Verified all feature file links work

Status: [ ] INCOMPLETE / [ ] COMPLETE ✅
```
