---
name: paas-hosting
description: "Deploy web apps and DBs to PaaS like Railway."
---

# PaaS Deployment

General workflow for deploying applications to Platform-as-a-Service (PaaS) providers (Railway, Render, Fly.io, Vercel).

## Workflow
1. **Source/Template Selection:** Use platform-provided templates for standard stacks (WordPress, DB-backed web apps).
2. **Environment Configuration:** Configure mandatory environment variables (DB credentials, secrets).
3. **Storage Strategy:** Verify persistent volume usage for database and uploads (e.g., `wp-content/uploads` for WordPress).
4. **Domain Assignment:** Configure custom domains or generate ephemeral hostnames.
5. **Monitoring:** Review deployment logs for startup failures (database connectivity is a common point of failure).

## Pitfalls
- **Ephemeral vs. Persistent:** Ensure the platform handles DB/File persistence automatically (e.g., Railway volumes).
- **Restart behavior:** Verify configuration survives container recreation by checking if the filesystem is read-only (standard for web-app containers).

## References
- `references/railway-wordpress.md`: Steps for deploying WordPress on Railway.
