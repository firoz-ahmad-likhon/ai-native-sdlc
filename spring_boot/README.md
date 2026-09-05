# Spring Boot Sample

Minimal two-endpoint Spring Boot app. No persistence, auth, or frontend.

> **Windows note:** `make` isn't available out of the box on native Windows.
> Use WSL, Git Bash with `make` installed, or `choco install make` / `scoop
> install make` — or just run the plain command shown under each `make`
> target below (e.g. `docker compose up --build` instead of `make run`).

## Run

```bash
make run
```

App serves on `http://localhost:8080`. Stop with `make down`.

`make run` wraps `docker compose up --build`; `make down` wraps `docker compose down`.

## Endpoints

| Method | Path | Example | Response |
|---|---|---|---|
| GET | `/hello` | `curl localhost:8080/hello` | `200 {"message": "Hello, World!"}` |
| GET | `/sum` | `curl "localhost:8080/sum?a=3&b=4"` | `200 {"result": 7}` |

Missing or non-numeric `a`/`b` on `/sum` returns `400 {"error": "..."}`.

## Test

```bash
make test
```

`make test` wraps `mvn test` (requires local Maven + JDK 17).

Without local Maven/JDK, run it in a container from `spring_boot/`:

```bash
docker run --rm -v "$(pwd):/app" -w /app maven:3.9-eclipse-temurin-17 mvn -B test
```

## Lint & format

Checks formatting (Spotless, Google Java Format) and style (Checkstyle, non-blocking):

```bash
mvn spotless:check checkstyle:check
```

Auto-fix formatting:

```bash
mvn spotless:apply
```

Without local Maven/JDK, prefix either with the same Docker wrapper as above, e.g.:

```bash
docker run --rm -v "$(pwd):/app" -w /app maven:3.9-eclipse-temurin-17 mvn -B spotless:check checkstyle:check
```

## Docs

- [`intent/spring_boot/intent.md`](../intent/spring_boot/intent.md) — goal and scope
- [`design/spring_boot/spec.md`](../design/spring_boot/spec.md) — implementation design
- [`plans/spring_boot/plan.md`](../plans/spring_boot/plan.md) — what was built and how it was verified
