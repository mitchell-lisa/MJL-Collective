# mjlcollective.com

Static homepage for MJL Collective. The design is the "Studio, with B's steps"
direction: dark hero over the glass block, the work wall with live previews,
the Build / Maintain / Grow steps, poured-dark footer.

## Why git deployments are disabled

`vercel.json` sets `git.deploymentEnabled: false`. The Vercel project
`mjl-collective` is linked to this repository, but production
(mjlcollective.com) is currently deployed from a separate local Next.js
codebase that includes the `/api/contact` route and the branded contact
emails. Until that route is ported into this repository, a git-triggered
production deploy would replace the live site with a version whose contact
form does not submit. Previews are deployed by file upload instead.

## Going live from this repo

1. Port `/api/contact` (and its email templates) from the current Next.js
   source into `api/contact.js` as a Vercel serverless function, or keep the
   mailto contact.
2. Remove the `git.deploymentEnabled` block from `vercel.json`.
3. Confirm the Vercel project's production branch, then merge/push to it.

## Content notes

- Work previews are live iframes of the client sites, scaled to fit the
  frames; each frame links out to the real site.
- `assets/unused/` holds graded crops (stairwell, desk with the laptop
  screen blurred, sea wake) kept for future pages such as an about page.
