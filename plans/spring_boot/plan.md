# Plan: Spring Boot Sample Project

Implements: [`intent/spring_boot/intent.md`](../../intent/spring_boot/intent.md) via [`design/spring_boot/spec.md`](../../design/spring_boot/spec.md)

## Summary
Scaffolds a minimal two-endpoint Spring Boot app (`/hello`, `/sum`) from the design spec, runnable end-to-end via `docker compose up`, with no persistence, auth, or frontend per the intent's stated scope.

## Files delivered

**Build/config**
- `spring_boot/pom.xml` — Java 17, Spring Boot 3.x, `spring-boot-starter-web`, `spring-boot-starter-test` (test scope), `spring-boot-maven-plugin` for executable jar packaging. `groupId` = `com.aisdlc`, `artifactId` = `springboot-sample`.
- `spring_boot/Dockerfile` — multi-stage: build stage `maven:3.9-eclipse-temurin-17` running `mvn package`, runtime stage `eclipse-temurin:17-jre` copying the jar with `ENTRYPOINT ["java","-jar","app.jar"]`.
- `spring_boot/docker-compose.yml` — single `app` service built from the Dockerfile, `8080:8080`.

**Source (`spring_boot/src/main/java/com/aisdlc/springboot/`)**
- `SpringBootSampleApplication.java` — `@SpringBootApplication` entry point.
- `controller/HelloController.java` — `@RestController`, `GET /hello` → `{"message": "Hello, World!"}`.
- `controller/SumController.java` — `@RestController`, `GET /sum` with `@RequestParam int a, @RequestParam int b` → `SumResponse(a + b)`. Relies on Spring's default binding to reject missing/non-numeric params (no manual validation).
- `dto/SumResponse.java` — record `SumResponse(int result)`.
- `exception/GlobalExceptionHandler.java` — `@RestControllerAdvice` catching `MissingServletRequestParameterException` and `MethodArgumentTypeMismatchException`, returning `400 {"error": "..."}`.

**Tests (`spring_boot/src/test/java/com/aisdlc/springboot/`)**
- `HelloControllerTest.java` — `@WebMvcTest(HelloController.class)`, asserts 200 + expected JSON body on `/hello`.
- `SumControllerTest.java` — `@WebMvcTest(SumController.class)`, covers: valid sum (200 + correct result), missing param (400 + error body), non-numeric param (400 + error body).

## Verification steps (documented; already satisfied by the delivered code)
1. `cd spring_boot && mvn test` — `HelloControllerTest` and `SumControllerTest` pass.
2. `docker compose up --build` — app starts on port 8080 with no separate local Maven/JDK setup.
3. `curl localhost:8080/hello` → `200 {"message":"Hello, World!"}`.
4. `curl "localhost:8080/sum?a=3&b=4"` → `200 {"result":7}`.
5. `curl "localhost:8080/sum?a=3"` and `curl "localhost:8080/sum?a=x&b=4"` → both `400` with an error JSON body.
6. `docker compose down` to clean up.
