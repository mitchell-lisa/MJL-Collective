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

Note: the earlier production site was a separate local Next.js codebase
whose `/api/contact` route sent the branded contact emails. This site uses
a mailto contact until that route is ported into `api/contact.js` here.

## Content notes

- Work previews are live iframes of the client sites, scaled to fit the
  frames; each frame links out to the real site.
- `assets/unused/` holds graded crops (stairwell, desk with the laptop
  screen blurred, sea wake) kept for future pages such as an about page.
