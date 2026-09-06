# The honest funnel

Same mechanics as the "comment CLAUDE" posts. Different rule: every claim in it can be checked, and the first thing anyone receives is free and complete.

## How it works

Every Reel ends with "Comment LEDGER for the real numbers. Free. No course." A viewer comments LEDGER. Within seconds they get a private reply in their DMs containing a link to the Ledger, a one-page PDF of the real 60-day numbers. The link goes to a page that shows the numbers immediately, with an optional email box underneath for the full post-mortem. Nothing is gated behind the email. The product ladder starts after that and is offered, never pushed, by a follow-up message three days later.

The reason to do it this way is not virtue. It is that this audience has been burned by exactly the other version, and the promise "free, no course in the first message" is itself the hook. Breaking it once ends the account.

## The lead magnet: The Ledger

A single page. The numbers from the research brief's case-study table, filled in from the logs, plus the five sentences that explain them. Duration, hours, tools, workflows, nodes, posts, followers, views, spend, cost per view, and the ratio: hours checking ÷ hours saved. At the bottom, one line: "The full post-mortem, the actual workflows and what I'd do differently are below if you want them. The numbers above are the whole point, and they're free."

Build it as a public page on firstdrophq.com (or the new account's domain) rather than a PDF attachment, because the DM link has to open instantly on a phone and Instagram flags file attachments.

## The product ladder

Prices are starting points for a UK creator selling to a global, mostly US audience. Every product is described by what it is, not by what it will do for the buyer.

**Tier 0, free. The Ledger.** The page above. Email optional. Expected conversion from DM to page open: high, because the ask is a tap.

**Tier 1, £29. The Build, Warts Included.** A download of the actual system: the n8n workflow exports, the FFmpeg render service in this repository, the two-pass ASS caption pipeline, the Kling and Blotato node configurations with credentials stripped, the First Drop HQ playbook and the 30-day calendar, and a README titled "What broke and when", written from the logs. Sold as "the system I actually built, including the parts that didn't work, so you don't spend 60 days finding out". Refund on request within 14 days, no reason required, stated on the sales page.

**Tier 2, £97. The Post-Mortem.** A recorded 60-to-90-minute walkthrough of the 60 days using the logs on screen: what was built each week, where the hours went, the ten things that broke ranked by cost, the moment the role changed from builder to manager, and the format mistake that made everything else irrelevant. Includes the Ledger workbook so buyers calculate their own ratio. This is the product the research says nobody has been taught: how to manage AI tools rather than build with them.

**Tier 3, £249. Don't Spend 60 Days.** A one-hour call. The buyer brings what they're building; the deliverable is a written one-page verdict on whether it can reach an audience, what to cut, and what to check before building anything else. Limited to what one person can do a week. No promises of results, and the sales page says so in those words.

**Later, if the account earns it. Manager of Machines, a monthly community** built around the weekly ledger: members post their own ratio, their own post-mortems, their own receipts. Do not launch this before the account has 90 days of its own receipts.

## The DM sequence

**Message 1, instant, triggered by the comment.**
"Here are the real numbers from 140 days, 30 products, 445 workflows and 141 views: [link]. It's one page, it's free, and there's no course on it. If you want the full post-mortem it's on the same page, but the numbers are the point."

**Message 2, three days later, only if they opened the link.**
"Did you do the ratio? Hours checking ÷ hours saved. Mine's on the page. If yours is over 1, the post-mortem walks through exactly how that happens and how to stop it. If it's under 1, ignore this, you're doing better than I was."

**Message 3, seven days later, only if they replied to either message.**
"One more thing and then I'll leave you alone. If you're mid-build and want someone to tell you whether it can actually reach people before you spend another month, that's the only paid call I do: [link]. No pitch on it, just the verdict."

No message 4.

## What to say on the sales pages

Every page carries the same three lines near the top. "Here's what this is." "Here's what it isn't." "Here's the refund policy." The "what it isn't" line does the selling, because it is the line the comment-CLAUDE pages cannot write.

## Two ways to run the automation

**Fast path: ManyChat.** Connect the Instagram account, create a keyword automation on LEDGER, paste message 1 with the link, add the three-day and seven-day follow-ups with the open and reply conditions. Working in an hour. Costs about £12 to £15 a month at this scale. This is what the comment-CLAUDE accounts use.

**Own path: n8n.** The workflow in `n8n_comment_to_dm.json` does message 1 and logs every comment to a sheet, so the account owns the data. It needs a Meta app with Instagram Messaging permissions (`instagram_manage_comments`, `instagram_manage_messages`, `instagram_business_basic`), a webhook subscription to the `comments` field on the Instagram account, and app review for the messaging permission before it works for people who aren't testers. Budget a week for the review. Until it's approved, run ManyChat. The follow-up messages need a second workflow with a wait node or a scheduled check of the sheet; the JSON deliberately does message 1 only, because that is the one that has to be instant.

## The numbers to watch

Comments per 1,000 views is the metric for the hook. DM link opens per comment is the metric for the promise. Tier 1 purchases per 100 link opens is the metric for the product. If the first two are healthy and the third is not, the product page is the problem, not the content. Do not add a product to fix a content problem or content to fix a product problem.
