# BEY profile art

The README uses three self-contained SVG images. Original design for Burhan
Emin Yenier; the supplied mascot is preserved as `assets/mascot.png` and embedded
unchanged in the hero. No scripts, external fonts, or third-party stats images
are required to display the profile.

`scripts/build_hero.py` creates the hero and toolkit. Run it with Python 3.11+
after changing the identity, tools, or mascot. It needs no extra dependencies.

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

All motion settles after a short entrance; the cursor blinks four times.
`prefers-reduced-motion` disables animations. Content remains visible when CSS
animation is unsupported. The README's expandable text version provides a
readable alternative on narrow screens and for assistive technologies.

Approach inspired by [Avi Vashishta's animated profile write-up](https://www.avivashishta.com/blog/build-animated-github-profile-readme).
The layout, copy, palette, mascot presentation, and generators are original.
