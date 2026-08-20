# Dealestly Static Site

DEALESTLY is a simple public link-in-bio website for a daily roundup of current Amazon, Walmart, and Target deals.

The site is intentionally static and GitHub Pages compatible. It uses plain HTML and CSS only.

## File Structure

- `index.html` - simple homepage with the brand, tagline, and link to today's deals.
- `today.html` - daily deals page. It currently contains clearly marked placeholder/demo deal cards.
- `style.css` - shared mobile-first styling.
- `archive/` - future location for archived daily deal pages or generated snapshots.

## Local Preview

Open `index.html` directly in a browser, or run a simple local static server from this folder:

```powershell
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000/
```

No Node, React, backend, database, or build step is required.

## GitHub Pages Deployment

This repository is intended to deploy from the `main` branch using GitHub Pages.

In GitHub:

1. Open the repository settings.
2. Go to Pages.
3. Set the source to deploy from a branch.
4. Choose `main` and `/root`.
5. Save.

## Future Daily Automation

The Dealestly daily workflow produces JSON files such as:

```text
C:\Users\ygan\data\dealestly-daily-YYYY-MM-DD.json
```

A future script can read that JSON and regenerate `today.html`, replacing the predictable `.deal-grid` section with live daily deal cards. The current sample cards are placeholders and should not be treated as live deals.

## Daily Update Rules

1. Never remove the GA4 tag.
2. Never remove the shared `shop_deal_click` handler.
3. Every generated SHOP DEAL link must use the required tracking data attributes.
4. Featured deal numbering must remain aligned with TikTok/video.
5. Additional deals do not receive featured deal numbers.
6. After every daily update, verify GA4 and click tracking before push.

Future Dealestly publishing runs should update only the deal content, preserve the page shell, preserve GA4, preserve the shared click-tracking JavaScript, generate deal cards using the tracking data attributes below, run analytics validation, and only then commit and push.

Required featured SHOP DEAL link contract:

```html
<a
  class="shop-button shop-deal-link"
  href="https://retailer.example/product"
  target="_blank"
  rel="noopener noreferrer"
  data-product-name="..."
  data-retailer="Amazon"
  data-current-price="44"
  data-product-url="https://retailer.example/product"
  data-deal-number="1"
  data-deal-section="featured"
>SHOP DEAL</a>
```

Required additional SHOP DEAL link contract:

```html
<a
  class="shop-button shop-deal-link"
  href="https://retailer.example/product"
  target="_blank"
  rel="noopener noreferrer"
  data-product-name="..."
  data-retailer="Target"
  data-current-price="0.99"
  data-product-url="https://retailer.example/product"
  data-deal-section="additional"
>SHOP DEAL</a>
```

Do not add `data-deal-number` to additional deals.

Run the analytics validator before pushing:

```powershell
python scripts\validate_analytics.py
```

## Future Custom Domain

GitHub Pages can later use a custom domain by adding the domain in repository Pages settings and creating a `CNAME` file in this project.
