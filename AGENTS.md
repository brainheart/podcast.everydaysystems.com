# Project Instructions

This repo hosts the static Everyday Systems Podcast site. Optimize for making the monthly episode-publishing workflow smooth from a short, natural-language prompt.

## Default Behavior

When the user asks to add or update a podcast episode, proceed with reasonable assumptions and placeholders. Do not block on missing URLs or missing final metadata unless the requested change cannot be made safely.

The user will often add an episode in passes:

1. First pass: raw script and some images are available; YouTube, MP3, or discussion links may be missing.
2. Later passes: add YouTube URL, MP3 URL, discussion URL, updated blurb, extra images, or corrections.

For missing external URLs, use `null` in `metadata/episodes.json` and commented placeholders in the episode HTML where appropriate. When the missing information arrives later, patch the relevant page, metadata, and rebuilt index.

## Repository Shape

- Main generated podcast list: `index.html`
- Episode metadata source: `metadata/episodes.json`
- Episode pages: `episode/NNN/index.html`
- Raw transcript files, when provided: `episode/NNN/NNN.txt`
- Episode-specific assets: `episode/NNN/assets/`
- Index builder: `scripts/build_index.py`
- Index rendering logic: `scripts/podcast_index.py`
- Tests: `tests/`

## New Episode Workflow

When adding a new episode:

1. Inspect recent episode pages, especially the latest 3-5 episodes, and follow their conventions.
2. Inspect `metadata/episodes.json` and add the new episode object near the top, preserving descending episode order.
3. Create `episode/NNN/index.html` from the transcript/script.
4. Copy or reference episode assets under `episode/NNN/assets/`.
5. Insert requested images at the appropriate transcript locations.
6. Rebuild the main index:
   `python3 scripts/build_index.py`
7. Validate JSON:
   `python3 -m json.tool metadata/episodes.json >/dev/null`
8. Run tests:
   `python3 -m unittest discover -s tests`
9. Report what changed and call out any remaining placeholders.

## Episode Metadata

Each episode object in `metadata/episodes.json` should include:

- `number`
- `title`
- `release_date`
- `blurb`
- `youtube_id`
- `youtube_url`
- `mp3_url`
- `discuss_url`
- `image_files`
- `length_minutes`

Use `null` for unknown URLs. Use `0` for unknown length unless a duration can be derived from a local or linked MP3.

For YouTube URLs:

- Extract the video ID from `youtu.be`, `youtube.com/watch`, or similar URLs.
- Store the clean canonical URL without tracking params:
  `https://www.youtube.com/watch?v=VIDEO_ID`
- Store `youtube_id` as just the video ID.
- Use the privacy-enhanced embed host in episode pages:
  `https://www.youtube-nocookie.com/embed/VIDEO_ID?modestbranding=1&amp;rel=0&amp;playsinline=1`

For MP3 URLs:

- If an MP3 URL is known, include it in `mp3_url`, add a centered `Download mp3` link to the page, and include `associatedMedia` in the page JSON-LD following existing page conventions.
- If only a local MP3 file exists, do not link to the local file from the public page. Use it only to infer `length_minutes` when possible.
- Prefer `ffprobe` for local duration; fall back to `afinfo` on macOS if needed.

For discussion URLs:

- Add the URL to `discuss_url`.
- Add a centered bottom-of-page `Discuss` link.
- Rebuild `index.html` so the front page links to the discussion thread.
- The current forum domain may be either `bb.everydaysystems.com` or an older `everydaysystems.com/bb` URL. Use the URL provided by the user.

## Episode Page Conventions

Follow existing static HTML style rather than introducing a template framework.

The episode page should include:

- Standard `<meta charset>`, viewport, and meta description.
- Title in the form:
  `Everyday Systems Podcast — Episode NNN: TITLE`
- JSON-LD with `PodcastEpisode`, `name`, `episodeNumber`, `partOfSeries`, `url`, and `description`.
- The breadcrumb paragraph:
  `Everyday Systems: Podcast : Episode NNN`
- The `<h1>` matching the title.
- `In this episode: BLURB`
- YouTube iframe if `youtube_id` is known.
- Commented YouTube placeholder if YouTube is not yet known.
- Centered MP3 download link if `mp3_url` is known.
- Commented MP3 placeholder if MP3 URL is not yet known.
- Transcript paragraphs in `<p>` tags.
- Bottom author/copyright block.
- Bottom `Discuss` link if `discuss_url` is known.
- Commented discussion placeholder if discussion URL is not yet known.
- The existing year script:
  `<script src="/assets/js/year.js?v=2" defer></script>`

Use existing local linking style for prior episodes, for example `../103/`, when adding relevant cross-links. Add only obvious and helpful links; do not over-link every repeated mention.

## Transcripts And Scripts

The user may provide scripts as:

- A raw `.txt` file already in `episode/NNN/`
- A pasted transcript
- A Google Docs link
- A local exported file

Raw text files are easiest. If a Google Docs link is public and readable, use it. If it is private or inaccessible from the coding environment, ask the user for a public/export link or a `.txt` export, but continue with any available local materials if possible.

When converting text to HTML:

- Preserve paragraph order.
- Escape HTML special characters.
- Convert normal paragraphs to `<p>...</p>`.
- Use simple emphasis, links, and `<strong>` only when helpful and consistent with existing pages.
- Avoid large stylistic rewrites of the transcript.
- Keep comments/placeholders concise and easy to search.

## Images And Assets

Store episode-specific images under:

`episode/NNN/assets/`

When the user mentions images but they are not in the episode folder, check likely local places such as the episode asset folder and `~/Downloads` before asking.

For transcript screenshots or images meant to be viewed in detail:

- Insert the image at the relevant paragraph.
- Wrap the image in a link to the full-size asset.
- Add a small centered note under it:
  `Click image to expand`
- Use useful alt text.
- Keep page display width responsive, usually `width:100%`.
- For tall phone screenshots, constrain display width, for example `max-width:360px`, while linking to full size.

For images intended only for YouTube art/thumbnail:

- Do not insert them into the episode HTML unless the user asks.
- Do not include them in `image_files` unless they are page-relevant.

Use `image_files` in metadata for images that appear in or materially support the episode page. Keep paths relative to the repo root, such as:

`episode/104/assets/aristocal-work-week.png`

## Updating Existing Episodes

When the user provides a missing URL or correction after the first pass:

1. Update `metadata/episodes.json`.
2. Update `episode/NNN/index.html`.
3. Rebuild `index.html` with `python3 scripts/build_index.py`.
4. Run `python3 -m unittest discover -s tests`.
5. Verify with `rg` that placeholders were removed or retained intentionally.

Examples:

- New YouTube URL: add `youtube_id`, clean `youtube_url`, replace commented embed placeholder with live iframe, rebuild index.
- New discussion URL: add `discuss_url`, replace bottom placeholder with live `Discuss` link, rebuild index.
- New blurb: update metadata, page meta description, JSON-LD description, `In this episode`, and rebuild index.
- New MP3 URL: add `mp3_url`, add download link, add JSON-LD `associatedMedia`, rebuild index.

## Generated Files And Tests

`index.html` is generated from `metadata/episodes.json`. Do not hand-edit the episode list in `index.html`; update metadata and run:

`python3 scripts/build_index.py`

After changes, run:

`python3 -m unittest discover -s tests`

For small documentation-only changes, tests are not required, but validate by reading the changed file back.

## Git And Workspace Hygiene

Do not revert unrelated user changes. If the worktree has unrelated changes, ignore them unless they directly affect the requested episode workflow.

Use `rg` / `rg --files` for searches where possible.

Use `apply_patch` for manual edits.

In the final response, summarize the files changed, mention any placeholders that remain, and include verification performed.
