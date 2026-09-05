# Design Spec: Spring Boot Sample Project

Implements: [`intent/spring_boot/intent.md`](../../intent/spring_boot/intent.md)

## Overview
A minimal Spring Boot web app exposing two REST endpoints — `/hello` and `/sum` — runnable end-to-end via `docker compose up`. No persistence, auth, or frontend, per the intent's stated scope.

## Project Layout
```
spring_boot/
  pom.xml
  Dockerfile
  docker-compose.yml
  src/main/java/com/example/demo/
    DemoApplication.java
    controller/HelloController.java
    controller/SumController.java
    dto/SumResponse.java
    exception/GlobalExceptionHandler.java
  src/test/java/com/example/demo/
    HelloControllerTest.java
    SumControllerTest.java
```

## Dependencies (`pom.xml`)
- Java 17+, Spring Boot 3.x
- `spring-boot-starter-web`
- `spring-boot-starter-test` (test scope)
- Packaged as an executable jar (`spring-boot-maven-plugin`)

## Class-Level Design

| Class | Responsibility |
|---|---|
| `DemoApplication` | Standard `@SpringBootApplication` entry point. |
| `HelloController` | `@RestController`, `GET /hello` → `{"message": "Hello, World!"}`. |
| `SumController` | `@RestController`, `GET /sum` with `@RequestParam int a, @RequestParam int b` → `SumResponse(a + b)`. |
| `SumResponse` | Simple record/POJO: `{ result: int }`. |
| `GlobalExceptionHandler` | `@RestControllerAdvice` catching `MissingServletRequestParameterException` / `MethodArgumentTypeMismatchException` → 400 with `{"error": "..."}`. |

Note: Spring's built-in parameter binding already rejects missing or non-numeric `a`/`b` with a 400 before the controller method runs — no manual validation code is needed. `GlobalExceptionHandler` only needs to shape that rejection into the JSON error body described below.

## Docker Design

**`Dockerfile`** — multi-stage build:
1. Build stage: `maven:3.9-eclipse-temurin-17` — copy source, run `mvn package`.
2. Runtime stage: `eclipse-temurin:17-jre` — copy the built jar, `ENTRYPOINT ["java","-jar","app.jar"]`.

**`docker-compose.yml`** — single `app` service built from the Dockerfile, exposing port `8080:8080`. No other services (no DB, per intent's out-of-scope list).

## Endpoint Contract

| Method | Path | Params | Success Response | Error Response |
|---|---|---|---|---|
| GET | `/hello` | — | `200 {"message": "Hello, World!"}` | — |
| GET | `/sum` | `a` (int), `b` (int) | `200 {"result": <a+b>}` | `400 {"error": "..."}` if `a`/`b` missing or non-numeric |

## Traceability
This spec implements every acceptance criterion in `intent/spring_boot/intent.md`:
- Runs via `docker compose up` (Dockerfile + docker-compose.yml above).
- `/hello` and `/sum` match the intent's endpoint definitions exactly.
- Invalid/missing `sum` params return 400 as required.

Out-of-scope items carried over unchanged: persistence/database, authentication, frontend UI, deployment/cloud config.

## Next Steps (not part of this spec)
Scaffold the actual project files (`pom.xml`, Java classes, `Dockerfile`, `docker-compose.yml`) from this spec in a follow-up step.
