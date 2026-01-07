
# Security Constraints

- No network or filesystem reads outside provided stub dir in model outputs.
- No shell execution strings in generated code.
- No credentials, tokens or PII in code or comments.
- Always validate/escape external input; but prefer pure functions here.
