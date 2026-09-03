// Contact form handler, ported from the previous Next.js site's
// app/api/contact/route.ts. Two branded emails per submission, via Resend:
//   1. A notification to Mitchell's inbox (must succeed).
//   2. A confirmation to the visitor, signed by Mitchell (best effort).
// RESEND_API_KEY lives in the Vercel project's environment variables, never
// in this repo. mjlcollective.com is a verified sending domain in Resend, so
// mail goes out as form@mjlcollective.com. The mark is self-hosted at
// /assets/mark-email.png (absolute URL, since email clients need one).

const site = {
  name: "MJL Collective",
  legalName: "MJL Collective LLC",
  domain: "mjlcollective.com",
  url: "https://mjlcollective.com",
  email: "mitchelljordanlisa@gmail.com",
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const LOGO = `${site.url}/assets/mark-email.png`;

const esc = (s) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

// Shared shell: cement ground, hairline-bordered panel, serif voice.
function shell(inner) {
  return `<!DOCTYPE html>
<html><body style="margin:0;padding:0;background-color:#eceeec;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#eceeec;">
<tr><td align="center" style="padding:40px 16px;">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;background-color:#f5f6f5;border:1px solid #cfd3d0;">
<tr><td style="padding:36px 40px 40px 40px;font-family:Georgia,'Times New Roman',serif;color:#1b1c1b;">
${inner}
</td></tr>
</table>
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;">
<tr><td style="padding:16px 8px;font-family:Helvetica,Arial,sans-serif;font-size:11px;letter-spacing:0.08em;color:#888b88;">
&copy; 2026 ${site.legalName} &middot; <a href="${site.url}" style="color:#888b88;">${site.domain}</a>
</td></tr>
</table>
</td></tr>
</table>
</body></html>`;
}

const logoImg = (width) =>
  `<img src="${LOGO}" width="${width}" alt="${site.name}" style="display:block;border:0;max-width:100%;height:auto;" />`;

const signoff = `
<p style="margin:32px 0 0 0;font-size:16px;line-height:1.6;">Thank you,</p>
<p style="margin:14px 0 0 0;font-size:15px;line-height:1.5;">Mitchell Lisa</p>
<div style="margin:22px 0 0 0;">${logoImg(132)}</div>
<p style="margin:16px 0 0 0;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#4e504e;">Build. Maintain. Grow.</p>
<p style="margin:10px 0 0 0;font-family:Helvetica,Arial,sans-serif;font-size:12px;"><a href="${site.url}" style="color:#1b1c1b;">${site.domain}</a></p>`;

function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") {
    try { return JSON.parse(req.body); } catch { return null; }
  }
  return null;
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  const data = readBody(req);
  if (!data) return res.status(400).json({ error: "Bad request" });

  const field = (k, max) => (typeof data[k] === "string" ? data[k].trim().slice(0, max) : "");

  // Honeypot: real visitors never see this field. Pretend success for bots.
  if (field("company", 200)) return res.status(200).json({ ok: true });

  const name = field("name", 200);
  const business = field("business", 200);
  const email = field("email", 200);
  const phone = field("phone", 60);
  const message = field("message", 4000);

  if (!name || !email || !message || !EMAIL_RE.test(email)) {
    return res.status(400).json({ error: "Please fill in your name, a valid email, and a message." });
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ error: "Form not configured" });

  const from = `${site.name} <form@${site.domain}>`;
  const firstName = name.split(/\s+/)[0];
  const msgHtml = esc(message).replace(/\n/g, "<br />");

  const send = (payload) =>
    fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

  // 1. The notification to Mitchell.
  const rows = [["Name", name], ["Business", business], ["Email", email], ["Phone", phone]]
    .filter(([, v]) => v)
    .map(([k, v]) => `<tr>
<td style="padding:7px 16px 7px 0;font-family:Helvetica,Arial,sans-serif;font-size:11px;letter-spacing:0.18em;color:#888b88;vertical-align:top;white-space:nowrap;">${k.toUpperCase()}</td>
<td style="padding:7px 0;font-size:15px;line-height:1.5;color:#1b1c1b;">${esc(v)}</td>
</tr>`)
    .join("");

  const notifyHtml = shell(`
<div style="margin:0 0 28px 0;">${logoImg(104)}</div>
<p style="margin:0;font-family:Helvetica,Arial,sans-serif;font-size:11px;letter-spacing:0.22em;color:#888b88;">NEW INQUIRY</p>
<h1 style="margin:10px 0 22px 0;font-size:26px;font-weight:normal;line-height:1.2;">${esc(name)}${business ? `, ${esc(business)}` : ""}</h1>
<table role="presentation" cellpadding="0" cellspacing="0" style="border-top:1px solid #cfd3d0;padding-top:6px;">${rows}</table>
<div style="margin:22px 0 0 0;padding:16px 20px;border-left:2px solid #1b1c1b;background-color:#eceeec;font-size:15px;line-height:1.6;">${msgHtml}</div>
<p style="margin:24px 0 0 0;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#4e504e;">Reply to this email to answer ${esc(firstName)} directly.</p>`);

  const notifyText = [
    `Name: ${name}`,
    business && `Business: ${business}`,
    `Email: ${email}`,
    phone && `Phone: ${phone}`,
    "",
    message,
    "",
    "Sent from the mjlcollective.com contact form.",
  ].filter((l) => l !== "").join("\n");

  const notifyRes = await send({
    from,
    to: [site.email],
    reply_to: email,
    subject: `Website inquiry from ${name}${business ? ` (${business})` : ""}`,
    html: notifyHtml,
    text: notifyText,
  });
  if (!notifyRes.ok) return res.status(502).json({ error: "Send failed" });

  // 2. The confirmation to the visitor. Best effort; the inquiry is already
  // safely delivered, so a failure here never surfaces an error.
  const confirmHtml = shell(`
<h1 style="margin:0 0 18px 0;font-size:28px;font-weight:normal;line-height:1.2;">Got your message, ${esc(firstName)}.</h1>
<p style="margin:0;font-size:16px;line-height:1.65;">Your note is in my inbox. I read every message personally, and I will get back to you shortly with next steps.</p>
<div style="margin:24px 0 0 0;padding:16px 20px;border-left:2px solid #cfd3d0;color:#4e504e;font-size:14px;line-height:1.6;">${msgHtml}</div>
${signoff}`);

  const confirmText = `Got your message, ${firstName}.

Your note is in my inbox. I read every message personally, and I will get back to you shortly with next steps.

Thank you,
Mitchell Lisa
${site.name}
Build. Maintain. Grow.
${site.url}`;

  try {
    await send({
      from,
      to: [email],
      reply_to: site.email,
      subject: `${site.name} got your message`,
      html: confirmHtml,
      text: confirmText,
    });
  } catch {
    // ignore: notification already delivered
  }

  return res.status(200).json({ ok: true });
};
