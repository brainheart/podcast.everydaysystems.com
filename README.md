# podcast.everydaysystems.com

Podcast chunk of the Everyday Systems site.

The front page (`index.html`) is a sortable, filterable episode table generated
by `scripts/build_index.py` from `scripts/index_template.html`. See `AGENTS.md`
for the publishing workflow and validation commands. Shared
system names, family (group) colors, and IDs live in `metadata/systems.json`;
episode relationships to those systems live in each episode's `systems.focus`
and `systems.mentions` fields in `metadata/episodes.json`.
