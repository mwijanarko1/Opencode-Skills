---
name: technical-seo
description: Practical technical SEO guide for crawlability, indexation, site structure, canonicals, performance, mobile, metadata, and structured data. Use when optimizing sites for search engines, implementing SEO, auditing technical SEO, or when the user asks about sitemaps, robots.txt, Core Web Vitals, or schema markup.
---

# Technical SEO

Concise, implementable technical SEO guidance. Apply when building or auditing sites for search visibility.

## 1. Crawlability and indexation

- Link main pages from homepage and navigation (no orphan pages)
- Keep click depth shallow: important pages within 3 clicks of homepage
- Clean URL structure: lowercase, hyphens, no long query strings (e.g. `/blog/technical-seo-guide`)
- Generate XML sitemap with only canonical, indexable URLs; submit in Google Search Console (Indexing → Sitemaps)
- Maintain `robots.txt` blocking only low-value areas (login, internal search/filter URLs, staging)
- Avoid blocking core sections with `Disallow` or `noindex`

Example `robots.txt`:

```txt
User-agent: *
Disallow: /wp-admin/
Disallow: /cart/
Disallow: /checkout/
Disallow: /search?
Sitemap: https://example.com/sitemap.xml
```

## 2. Site structure and internal linking

- Group content into clear categories and subcategories (e.g. `/blog/seo/technical-seo-guide`)
- Use descriptive navigation labels and breadcrumb trails: `Home > Blog > SEO > Technical SEO`
- Every important page should have internal links from relevant content; use descriptive anchor text, not "click here"
- Fix broken internal links; avoid long redirect chains (301 → 301 → 301)

Example hierarchy:

- `/`
- `/blog/`
- `/blog/seo/`
- `/blog/seo/technical-seo-guide/`

## 3. Canonicals, duplicates, and parameters

- Use canonical tags on each page pointing to its preferred URL (self-referencing for most pages)
- For variants (tracking params, filtered listings), canonicalize to the main version when content is substantially similar
- Redirect all traffic to a single canonical host (HTTP→HTTPS, www/non-www) with 301s
- For pagination: consistent URL patterns (`/category/page/2/`) and canonical to each specific page, not always page 1

## 4. Performance and Core Web Vitals

- Optimize images: compression, WebP/AVIF, responsive sizes, lazy loading below the fold
- Minimize render-blocking JS/CSS; ship only necessary scripts; defer non-critical JS
- Use HTTP/2 or HTTP/3, enable GZIP/Brotli, leverage browser caching
- Use a CDN for static assets
- Monitor Core Web Vitals (LCP, CLS, INP) in Search Console and performance tooling

## 5. Mobile and security

- Responsive design: same HTML adapts to all screen sizes
- Mobile navigation should expose the same important links as desktop
- Avoid intrusive interstitials/popups that block content on mobile
- Serve all pages over HTTPS with valid TLS; redirect HTTP → HTTPS

## 6. Metadata and HTML semantics

- Unique, descriptive `<title>` on every indexable page, ideally including the primary topic
- One clear `<h1>` per page that matches or supports the title; logical `<h2>`, `<h3>` structure
- Meta descriptions that accurately summarize content and encourage clicks
- Descriptive `alt` attributes on meaningful images (no keyword stuffing)

## 7. Structured data (schema)

- Implement JSON-LD schema for key page types: Article, Product, FAQ, LocalBusiness
- Keep schema consistent with on-page content (no fake reviews, misleading prices)
- Test and validate with Google Rich Results Test; fix warnings or errors

Minimal Article schema:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Technical SEO Guide",
  "author": { "@type": "Person", "name": "Your Name" },
  "datePublished": "2026-03-08",
  "mainEntityOfPage": "https://example.com/blog/technical-seo-guide"
}
</script>
```

## 8. Log files, monitoring, and tooling

- Use server logs (or log analyzers) to see how bots crawl sections and spot waste (e.g. faceted URLs)
- Run periodic technical audits with an SEO crawler: broken links, 4xx/5xx, redirect chains, missing titles, canonical conflicts
- Track organic performance and index coverage in Google Search Console; fix coverage and enhancement issues

## 9. Prioritization checklist

Work in this order:

1. Crawlability and indexation (robots, sitemaps, major 4xx/5xx, canonical host)
2. Site structure, navigation, and internal linking for key pages
3. Performance and Core Web Vitals on important templates
4. Canonicals, duplicates, HTTP/HTTPS, and parameters
5. Metadata, headings, structured data on high-value pages first
6. Monitoring: crawls, logs, and Search Console reviews on a schedule

## Stack-specific implementation

When the user shares their stack (Next.js, WordPress, custom Node, etc.) and site type (blog, SaaS, ecommerce), turn this into a concrete implementation checklist tailored to that setup.
