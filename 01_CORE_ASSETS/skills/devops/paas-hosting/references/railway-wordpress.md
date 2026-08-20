# Deploying WordPress on Railway

Workflow steps identified during user interaction:

1. **Log in:** Access Railway.app via GitHub.
2. **Project Setup:** New Project -> Deploy from Template -> Search "WordPress".
3. **Persistence:** Rely on pre-configured volume/database services provided by the template.
4. **Environment:** Verify DB service is linked; do not delete this service.
5. **Deployment:** Monitor the build; configure generated domain under Settings -> Domains.
6. **Persistence Check:** Note that standard Railway templates for WordPress map `wp-content/uploads` to persistent volumes automatically, ensuring data survives restarts.
