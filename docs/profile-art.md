# BEY profile art

The README uses three self-contained SVG images. Original design for Burhan
Emin Yenier; the supplied mascot is preserved unchanged as `assets/mascot.png`.
The hero samples the mascot silhouette into 120 × 84 monochrome ASCII characters.
It excludes the purple backdrop and reduces empty source margins, retaining a
small square frame around the original face. Each row types from left to right;
the full portrait still completes in about seven seconds. No scripts, external fonts, or third-party stats images
are required to display the profile.

`scripts/build_hero.py` creates the hero and toolkit. Run it with Python 3.11+
after changing the identity, tools, or mascot. Install its portrait-only
dependency with `python -m pip install -r scripts/requirements-art.txt` first.
The daily calendar job does not install or use Pillow.

Hero and toolkit filenames include a hash of their generated content. The
generator updates the README links and removes superseded generated versions.
This gives changed art a new URL so visitors do not retain an earlier design
from a cached `raw/main` image. An unchanged rebuild keeps the same filenames.

The nine application logos are vendored in `assets/icons` from the MIT-licensed
[Skill Icons](https://github.com/tandpfun/skill-icons) set. Their upstream license
and exact source commit are included there. They are embedded as vector SVG
content, so rendering does not depend on an external icon server.

`scripts/update_contributions.py` fetches GitHub's public contribution HTML,
checks that dates are complete, tooltips match levels, data is recent, and daily
counts match the total, then generates `data/contributions.json` and
`assets/contributions.svg`. It needs no personal access token. This endpoint is
not a versioned API; a markup change fails the job and leaves committed art intact.
The calendar reflects GitHub's public display and its privacy settings.

The Action refreshes the calendar daily at approximately 09:17 Istanbul time;
GitHub may delay scheduled jobs. It also supports manual dispatch and runs when
the contribution script or workflow changes. It commits only the two generated
calendar files when their content changes, using the repository-scoped built-in
`GITHUB_TOKEN` with `contents: write`. If scheduled workflows become disabled
after repository inactivity, re-enable the workflow in GitHub's Actions tab.

The window opens first. The portrait types over about seven seconds, with one
moving cursor per row. The identity and whoami lines type in alongside it.
Application logos appear next, then the calendar grid. Motion finishes in about
ten seconds and does not loop; reloading the page replays the opening.
`prefers-reduced-motion` disables animations. Content remains visible when CSS
animation is unsupported. The README's expandable text version provides a
readable alternative on narrow screens and for assistive technologies.

Approach inspired by [Avi Vashishta's animated profile write-up](https://www.avivashishta.com/blog/build-animated-github-profile-readme).
The layout, copy, palette, mascot presentation, and generators are original.
