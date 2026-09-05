# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo exercises an AI-native SDLC loop: `intent/` → `design/` → `plans/` → generated code. Each feature/project lives under a shared slug (e.g. `spring_boot`) across all four stages:

- `intent/<slug>/intent.md` — goal, scope, acceptance criteria, explicitly out-of-scope items.
- `design/<slug>/spec.md` — implementation design derived from the intent (file layout, class responsibilities, contracts). Links back to its intent doc and includes a traceability section mapping spec details to acceptance criteria.
- `plans/<slug>/plan.md` — the executed implementation plan derived from intent + spec, documenting what was actually built and how it was verified. Links back to both intent and spec docs.
- `<slug>/` at repo root — the generated project itself (e.g. `spring_boot/`).

When asked to work on a project in this repo, read the intent and spec docs for that slug first — they are the source of truth the code must match. If code needs to diverge from the spec (e.g. renaming a placeholder), update the spec doc first so intent → design → plan → code traceability stays intact, rather than letting them drift.

## `spring_boot/` project

A minimal two-endpoint Spring Boot 3.x app (Java 17), built with Maven, packaged as a Docker image. No persistence, auth, or frontend — intentionally out of scope per `intent/spring_boot/intent.md`.

### Commands

Run from `spring_boot/`:
- `mvn test` — run the JUnit test suite (`HelloControllerTest`, `SumControllerTest`).
- `mvn test -Dtest=SumControllerTest` — run a single test class.
- `mvn package` — build the executable jar.
- `docker compose up --build` — build and run the whole app (no local Maven/JDK required); serves on `localhost:8080`.
- `docker compose down` — stop and remove the container.

### Architecture

- `SpringBootSampleApplication` — standard `@SpringBootApplication` entry point.
- `controller/HelloController` — `GET /hello` → `{"message": "Hello, World!"}`.
- `controller/SumController` — `GET /sum?a={int}&b={int}` → `dto.SumResponse`. Relies entirely on Spring's default `@RequestParam` binding to reject missing/non-numeric params with a 400 — no manual validation code.
- `exception/GlobalExceptionHandler` (`@RestControllerAdvice`) — catches `MissingServletRequestParameterException` and `MethodArgumentTypeMismatchException` and reshapes them into `400 {"error": "..."}` JSON bodies.
- Package root is `com.aisdlc.springboot` (not the Spring Initializr placeholder `com.example.demo`).
- `Dockerfile` is a multi-stage build: `maven:3.9-eclipse-temurin-17` compiles the jar, `eclipse-temurin:17-jre` runs it.
