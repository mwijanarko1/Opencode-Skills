# Security Audit

Target: user-provided URL(s). Probe subdomains: `app.`, `www.`, `api.`, `admin.`, `staging.`, `dev.` Recon only—no exploitation.

## Flow

1. **Discovery:** Fetch homepage, extract links/src/action, robots.txt, sitemap, probe paths
2. **Headers:** Check HSTS, X-Content-Type-Options, X-Frame-Options, CSP, CORS (not `*`)
3. **Endpoints:** Probe `/api`, `/api/auth`, `/admin`, `/login`, `/.env`, `/.git/config`, `/graphql`—record status, content-type
4. **Third-party:** List external domains, identify GA/GTM/Tally/etc., check for exposed IDs
5. **Disclosure:** Search index, meta tags, source maps, error pages
6. **Compliance:** Forms/PII collected, consent banner, GDPR/COPPA for child-facing

## Report

Markdown: domain, date, risk (LOW|MODERATE|HIGH|CRITICAL), scope table, Critical/High/Medium/Low findings (Observed|Risk|Recommendation), endpoint table, positive observations, recommendations by priority, compliance notes.

Risk: CRITICAL=auth bypass/creds/RCE; HIGH=permissive CORS/missing CSP/exposed keys; MEDIUM=index disclosure/PII no consent; LOW=minor metadata.

Tools: `curl -sI`, `curl -sL`, mcp_web_fetch, grep. Save to `security-report-[domain].md`.
