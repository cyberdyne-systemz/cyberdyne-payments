# Cyberdyne Payments

Java 21 / Spring Boot / Maven teaching service for the Codex enablement session. It intentionally starts with incomplete amount validation. It never transfers real money.

```sh
mvn -B -Dtest=TransferControllerTest test
mvn spring-boot:run
```

The HTTP server binds to `127.0.0.1:8080` (`PORT` overrides the port).

```sh
curl -i http://127.0.0.1:8080/transfer \
  -H 'Content-Type: application/json' \
  -d '{"sourceAccount":"acct-100","destinationAccount":"acct-200","amount":-1.25,"currency":"USD"}'
```

Read [AGENTS.md](AGENTS.md) and [the API contract](docs/api.md). Baseline tests pass but miss negative and zero boundary cases. The live task is to close that gap. CI runs tests and a Codex policy review; the strict gate rejects blocking findings and invalid review output. Advisory findings remain visible without failing the gate.

The shared [coding-policy plugin](https://github.com/cyberdyne-systemz/coding-policy) lives in its own repository. Clone and install it separately using its README. Payments owns `AGENTS.md`, API contracts, and `.github/codex/`; Developer Platform owns the plugin's skills, hook, MCP server, and tests.
