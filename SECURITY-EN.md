# Security Policy

## Reporting a vulnerability
**Do not open a public issue for security vulnerabilities.**

Report privately via email to the maintainers (address listed in the repo settings) or via a private security advisory (GitHub → Security → Report a vulnerability).

Please include:
- A minimal reproduction (code/config snippet)
- Impact description
- Suggested fix (if any)

We aim to acknowledge reports within 72 hours and ship a fix within 14 days for confirmed issues.

## Scope
In scope: routing logic, pruning logic, verification signal handling, chain-store versioning, any code that executes or evaluates external content.

Out of scope: general LLM prompt-injection discussion (upstream models), documentation typos.

## Disclosure policy
We follow coordinated disclosure: fixes are released before public details, with credit to the reporter unless anonymity is requested.
