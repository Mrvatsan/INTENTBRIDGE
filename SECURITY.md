# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within IntentBridge, please follow these steps:

1. **Do not** open a public GitHub issue.
2. Email the security concern to the maintainer with a detailed description.
3. Include steps to reproduce the vulnerability if possible.
4. Allow reasonable time for a fix before public disclosure.

## Security Best Practices

- Never commit `.env` files or API keys to version control.
- Always use the `.env.example` file as a template.
- Keep dependencies updated to their latest secure versions.
- Use environment-specific configurations for production deployments.
- Rotate `SECRET_KEY` values regularly in production.
