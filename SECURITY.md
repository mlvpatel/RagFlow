# Security Policy

## Supported versions

This project is maintained on the `main` branch, which always carries the latest security patched dependencies. The most recent release receives security updates. Older snapshots are not separately maintained.

## Reporting a vulnerability

Please do not open a public issue for security problems.

Report a vulnerability privately through GitHub: open the repository Security tab and choose "Report a vulnerability". This creates a private advisory visible only to the maintainer.

You can expect an initial response within a few days. If the report is confirmed, a fix will be prepared and released, and you will be credited in the advisory unless you prefer otherwise. If it is declined, you will receive a short explanation.

## Scope

This policy covers the application code in this repository. Dependency vulnerabilities are tracked with pip-audit in CI and patched by updating the pinned versions. You are welcome to flag any that slip through.

## Known advisories

- **chromadb (GHSA-f4j7-r4q5-qw2c, critical):** a pre authentication code injection in the ChromaDB HTTP server, reachable only when the Chroma server is exposed on a network and a request sets `trust_remote_code` true against the collections endpoint. There is no patched release; 1.5.9 is the latest version. This project does not run the Chroma server. It uses Chroma in embedded mode against a local persist directory, never starts the HTTP server, and never sets `trust_remote_code`, so the vulnerable path is not present. The pin will move to a patched release as soon as one ships.
