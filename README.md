# mjlcollective.com

Static homepage for MJL Collective. The design is the "Studio, with B's steps"
direction: dark hero over the glass block, the work wall with live previews,
the Build / Maintain / Grow steps, poured-dark footer.

## Deploying

Git deployments are enabled in `vercel.json`. The Vercel project
`mjl-collective` is linked to this repository; pushes to the production
branch deploy to mjlcollective.com, and pushes to any other branch create
preview deployments.

To make this branch the live site: in Vercel, open the mjl-collective
project, then Settings -> Git -> Production Branch, set it to
`claude/artifact-session-kfrwsz` (or merge this branch into the branch
already configured there), and redeploy. The previous production
deployment remains in the Deployments list for instant rollback.

## Pages

Five pages, one shared stylesheet and script:

- `index.html` at `/`: the glass hero, the statement, and an index of the other pages.
- `work.html` at `/work`: the live previews, then the Marks section.
- `services.html` at `/services`: the four steps and the process under them.
- `about.html` at `/about` and `contact.html` at `/contact`.
- `assets/site.css` and `assets/site.js` are shared. `vercel.json` sets
  `cleanUrls`, so `/work` serves `work.html`.

The bar and footer are the same markup on every page. When editing them,
change all five files, or regenerate the set from one template.

## Brand

`brand/` holds the logo: SVG for the lockup and the monogram, in ink and in
white, plus PNG exports on white and on ink. `brand/README.md` states the
palette, the typeface, the minimum sizes and the clear space. Every site asset
in `assets/` (the header mark, the favicon, the touch icon, the social card and
the email mark) is generated from the same geometry, so regenerate them
together rather than editing one by hand.

`logo-directions.html` is the comparison page the mark was chosen from. It is
listed in `.vercelignore` and is not deployed.

## Contact form

`api/contact.js` is a Vercel serverless function ported from the previous
Next.js site. It validates the submission, drops honeypot hits, and sends
two emails through Resend: a notification to Mitchell (reply-to set to the
visitor) and a branded confirmation to the visitor. It needs the
`RESEND_API_KEY` environment variable in the Vercel project; without it the
function returns a 500 and the form shows the "email me directly" fallback.

## Content notes

- Work previews are live iframes of the client sites, scaled to fit the
  frames; each frame links out to the real site.
- `assets/unused/` holds graded crops (stairwell, desk with the laptop
  screen blurred, sea wake) kept for future pages such as an about page.
