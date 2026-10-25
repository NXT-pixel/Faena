Create an ADR markdown file in `/docs/tech/ADRs` that is based on the template in this document that starts after the text `--- ADR Template Starts Here ---`. The file name should follow the pattern in the `FILE NAME, **IMPORTANT**` section below.

If the content of the ADR isn't clear, ask the user to answer questions one at a time until it is.

You should expect the user to provide you existing documents or a prompt to help guide you to filling out the ADR correctly.

# FILE NAME, **IMPORTANT**

The file name of the ADR should be `ADR-<four digit number with leading zeros>-<topic summary in snake case>.md`

The number you use should always be one more than the last one in `/docs/tech/ADRs`.

GOOD FILE NAMES ✅
```
/docs/tech/ADRs/ADR-0001-authentication.md
/docs/tech/ADRs/ADR-0002-authorization.md
/docs/tech/ADRs/ADR-0003-production-builds.md
```

BAD FILE NAMES ❌
```
/docs/tech/ADRs/authentication.md
/docs/tech/ADRs/ADR-2-authorization.md
/docs/tech/ADRs/ADR-00099-production-builds.md
/docs/ADR-0009-api-client.md
/docs/tech/ADRs/ADR-0004.md
```
# ADR Template 
Sourced from https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-of-the-madr-project
Originally from https://github.com/adr/madr/blob/develop/template/adr-template.md
The template in the source file [defers to the original creator](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-of-the-madr-project/LICENSE.md). The original creator is [MIT](https://github.com/adr/madr/blob/develop/LICENSE).

--- ADR Template Starts Here ---
# [short title of solved problem and solution]

* Status: [proposed | rejected | accepted | deprecated | … | superseded by [ADR-0005](0005-example.md)] <!-- optional -->
* Deciders: [list everyone involved in the decision] <!-- optional -->
* Date: [YYYY-MM-DD when the decision was last updated] <!-- optional -->

Technical Story: [description | ticket/issue URL] <!-- optional -->

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences. You may want to articulate the problem in form of a question.]

## Decision Drivers <!-- optional -->

* [driver 1, e.g., a force, facing concern, …]
* [driver 2, e.g., a force, facing concern, …]
* … <!-- numbers of drivers can vary -->

## Considered Options

* [option 1]
* [option 2]
* [option 3]
* … <!-- numbers of options can vary -->

## Decision Outcome

Chosen option: "[option 1]", because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | … | comes out best (see below)].

### Positive Consequences <!-- optional -->

* [e.g., improvement of quality attribute satisfaction, follow-up decisions required, …]
* …

### Negative Consequences <!-- optional -->

* [e.g., compromising quality attribute, follow-up decisions required, …]
* …

## Pros and Cons of the Options <!-- optional -->

### [option 1]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

### [option 2]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

### [option 3]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

## Links <!-- optional -->

* [Link type] [Link to ADR] <!-- example: Refined by [ADR-0005](0005-example.md) -->
* … <!-- numbers of links can vary -->