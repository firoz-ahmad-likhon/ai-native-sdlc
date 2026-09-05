# Intent: Spring Boot Sample Project

## Goal
Learn Spring Boot fundamentals and exercise the full AI-native SDLC loop (intent → generated code → test → review) using a minimal, low-risk sample app.

## Scope
One Spring Boot web app exposing two REST endpoints.

Explicitly out of scope:
- Persistence / database
- Authentication
- Frontend UI
- Deployment / cloud config

## Endpoints

### `GET /hello`
Returns a hello world greeting, e.g. `{ "message": "Hello, World!" }`.

### `GET /sum?a={number}&b={number}`
Returns the sum of `a` and `b` as JSON, e.g. `{ "result": 7 }`.

## Acceptance Criteria
- App builds and starts via `docker compose up` (no separate local Maven/JDK setup required).
- `GET /hello` returns 200 with the expected greeting.
- `GET /sum?a=3&b=4` returns 200 with `{ "result": 7 }`.
- Missing or invalid `a`/`b` params return a 400 with a clear error (basic validation, not exhaustive).

## Tech Notes
- Java + Spring Boot (Maven), Spring Web starter only; keep dependencies minimal since this is a learning sandbox.
- App must be runnable via `docker compose up` — a `Dockerfile` builds the Spring Boot app, and a `docker-compose.yml` spins it up, so the whole thing starts with one command.

## Next Steps (not part of this task)
Use this intent doc as input to scaffold the actual project (source, `pom.xml`, `Dockerfile`, `docker-compose.yml`) under e.g. `spring_boot/` (or similar) in a follow-up step.
