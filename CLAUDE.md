# DreamReach AI video production: rules for Claude

These rules exist because skipping them has already cost real money. They are not optional.

## The money rule
Image credits are cheap (~0.25). Video credits are not (7.5+ per clip). **Every mistake must be caught at the
prompt or still-image stage, before any video generation.** Never call a video-generation tool until the
gates below have passed **and the user has replied "go" to the stills sheet.**

## The goal: photoreal enough that the artist/brand reposts it
Every shot should look like it was filmed on a real cinema camera, not generated. In every prompt:
- **Real camera language:** name a lens and stock ("35mm lens, Kodak Vision3 500T, shot on ARRI Alexa"),
  practical light sources only (streetlights, phone screens, shop signs), natural motion blur.
- **Imperfection:** grime, wear, uneven light, people slightly out of focus, nothing too symmetrical or clean.
- **Hidden motifs must be plausible in the real world** (a scratch, a sticker, a reflection, a number plate).
  Never giant glowing shapes on buildings or windows lit in a perfect pattern. Those read as CGI and kill the realism.
- **No visible AI faces** of crew/extras unless the artist supplied consent and photos; use backs,
  silhouettes, masks, or out-of-focus faces.
- Before generating, flag any shot whose idea itself looks artificial, and propose a realistic version.

## Spend on correctness, not resolution (user decision, 14 Nov)
- **Default video model: Kling 3.0 `mode: "pro"` (7.5–10 credits). Do NOT use 4K mode.** The user upscales/finishes in CapCut.
- Put credits into **getting the shot right**: an extra still option, an end frame, or a re-roll of a broken clip.
- Images: `gpt_image_2_6`, medium quality, 2K. Don't go to high quality unless a shot fails on detail.

## Gate 1: shot bible (before writing any prompt)
For each video, write a short shot bible at the top of `prompts/<video>.md` and get it right first:
- **Location facts:** underground or above ground, interior or exterior, city, time of day, weather.
- **What is visible through every window/door:** e.g. "subway: windows show tunnel wall only, never sky or city".
- **Vehicles:** type, and **one direction of travel** per shot.
- **Text/numbers that must read correctly**, and which shots risk mirroring them (gates, doors, reflections).
- **The artist rule:** the stand-in's face is never visible.

## Gate 2: prompt lint (before generating stills)
Check every image prompt and motion prompt against the bible. Reject and rewrite any prompt that:
- doesn't **state the location fact in words** (e.g. "deep underground: no sky, no buildings outside");
- gives a motion with **two directions or an ambiguous path** ("toward and past", "comes and goes"):
  one subject, one action, one direction, and the camera stated ("locked-off static camera");
- asks for a moving object whose direction matters (vehicles, doors, gates, escalators) **without an
  end frame**. Use the model's `end_image` role to pin where it finishes, or plan to reverse it in the edit;
- asks something to rotate or swing while it carries text/numbers (the text will mirror). Keep text facing camera.

Show the user the bible and a one-line summary per shot, with any risky shots flagged, before generating.

## Gate 3: stills check (before any video credit)
Generate stills (2 per shot), then check **each still against the bible**, not just "does it look good":
- Is anything outside a window/door that contradicts the location? (city outside a subway = reject)
- Is the vehicle the right type? Are the text and numbers readable?
- Does the start frame make the planned motion physically possible?
Send the user the contact sheet with picks **and stop. Generate video only after the user says "go".**

## Gate 4: clip QC (after video, before render)
Run `python qc_sheet.py assets/<video>` and check one frame per second of every clip.
- **Wrong direction (bus reversing, door closing):** fix it for free with `"reverse": true` on that clip in
  `jobs/<video>.json`. Don't re-generate.
- **Mirrored text:** trim around it with `trim_start_s` / `duration_s`.
- Re-generate only when trimming or reversing can't fix it, and tell the user the credit cost first.

## Reporting
- Report credits used and remaining after every batch.
- Never call something "checked" unless every frame-per-second row was looked at against the bible.
