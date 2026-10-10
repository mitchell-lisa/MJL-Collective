// Client login on preview deployments.
//
// In production, /clients is rewritten to the live client portal (vercel.json)
// and this does nothing. On a preview deployment of this site, /clients goes
// to the preview of the redesigned portal instead, so the two previews are
// looked at together. The target can be changed with PORTAL_PREVIEW_URL in the
// project's Preview environment variables without a code change.
export const config = { matcher: ["/clients", "/clients/:path*"] };

const DEFAULT_PORTAL_PREVIEW =
  "https://mjl-client-portal-git-redesign-s-dae1cb-mitchell-lisas-projects.vercel.app";

export default function middleware(request) {
  if (process.env.VERCEL_ENV !== "preview") return; // production and local: unchanged
  const base = (process.env.PORTAL_PREVIEW_URL || DEFAULT_PORTAL_PREVIEW).replace(/\/+$/, "");
  const url = new URL(request.url);
  return Response.redirect(base + url.pathname + url.search, 307);
}
