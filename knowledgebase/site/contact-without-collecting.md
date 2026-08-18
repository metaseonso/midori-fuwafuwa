---
title: Contact without collecting
tags: [site, privacy, contact, ai-reception, open]
status: partly settled — AI reception decided in principle, architecture open
updated: 2026-08-19
note: informational, not legal advice
---

# Contact without collecting

**Founder's decision: an AI reception, plus email.** Recorded 2026-08-19.

This is the one decision that moves the site off pure [[collect-nothing]], so it is worth building
deliberately. Here is what each option actually costs.

## Email — the free option

### ✅ A plain `mailto:` link collects nothing

```html
<a href="mailto:hello@midorifuwafuwa.com">Say hello</a>
```

- Opens the visitor's own mail app. **Nothing touches your server.**
- You collect nothing at all — the message arrives as an ordinary email.
- Warmer than a ticket: it's a real email from a real person.

### ❌ A contact form does collect

A form **posts data to your server.** You now hold personal data, need a privacy basis, need spam
handling, and need a retention policy. Same outcome as a mailto, with all the obligations.

**Use the mailto. Skip the form.**

*(Tradeoff: published addresses attract spam. Use a dedicated address and let your mail provider
filter.)*

## The AI reception — what it actually costs

An AI receptionist is a genuinely good fit for this studio: it performs personality the way the
research says the site should, rather than explaining it. But it is a data-collecting surface, and
pretending otherwise would be a mistake.

**What it introduces:**

| Thing | Why it matters |
|---|---|
| Visitors type messages | That is personal data, on your infrastructure |
| Conversations exist | You need a retention policy — how long, and who can see them |
| Messages go to an LLM API | Data leaves your control; the processor must be disclosed |
| Chat UI needs session state | Usually `localStorage` → a device write → see [[what-triggers-a-consent-banner]] |
| People will type personal things | Unprompted. They always do. Plan for it. |

None of this is hard. It is simply the difference between *zero* obligations and *some*.

## The elegant version — near-collect-nothing by design

An AI reception **can** be built so it collects almost nothing. The design brief:

1. **No server-side conversation storage.** Keep the transcript in the browser only. When the tab
   closes, it's gone.
2. **Zero-retention API arrangement** with the model provider, so nothing persists there either.
3. **No account, no email required.** If a visitor *wants* a reply, they choose to leave an address
   — and that is consent by action, not collection by default.
4. **Session state in memory where possible.** If `localStorage` is genuinely needed for the chat to
   function, it likely qualifies as "strictly necessary," which is exempt from consent under
   ePrivacy — but keep it to function only, never to identify.
5. **Log nothing but aggregate counts.** "47 conversations this month" is fine. Transcripts are not.

Built that way, the privacy policy gains about two sentences and no banner.

## ⚠️ Do not build this twice

**The AI reception is the same technology as [[../../productions/whimsy-fairy-journal/PROJECT|Whimsy]],
at one percent of the scale.** Both are conversational AI over personal text.

Two consequences:

1. **Whimsy's privacy architecture decision covers both.** That decision — local synthesis, private
   cloud, or zero-retention API — is still open, and it is the same decision the reception needs.
   Make it once.
2. **Sequencing:** ship the site with a **mailto only**, and add the AI reception once Whimsy's
   infrastructure exists. The site launches clean and fast; the reception arrives on infrastructure
   already built and already decided.

**If the reception is wanted at launch regardless:** put it on a separate subdomain with its own
short notice. The main site keeps its collect-nothing footing intact, and the reception carries its
own.

## Recommendation

**Launch with the mailto. Add the AI reception on Whimsy's infrastructure.** Same end state, no
duplicated work, and the site stays obligation-free until there is a real reason for it not to be.

## Related

- [[collect-nothing]] — the model this qualifies
- [[what-triggers-a-consent-banner]] — the session-state question
- [[privacy-policy-text]] — what changes when the reception ships
- [[../../productions/whimsy-fairy-journal/PROJECT|Whimsy]] — the shared infrastructure
