"""Validate the public GitHub calendar and generate a self-owned SVG.

Only Python's standard library is required. No personal access token.
Public HTML is not a versioned API: fail instead of publishing invented data
if the structure changes. Failed runs leave committed art intact.
"""
import argparse
import calendar
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ['#20202d', '#392853', '#634195', '#9563d4', '#c1a0f6']


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells, self.labels = {}, {}
        self.label_id = None
        self.parts, self.total_parts = [], []
        self.in_total = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('td', 'rect') and 'data-date' in a:
            if a['data-date'] in self.cells:
                raise ValueError('Duplicate calendar date')
            self.cells[a['data-date']] = {'id': a.get('id'), 'level': int(a['data-level'])}
        if tag == 'tool-tip':
            self.label_id, self.parts = a.get('for'), []
        if tag == 'h2' and a.get('id') == 'js-contribution-activity-description':
            self.in_total = True

    def handle_data(self, value):
        if self.label_id is not None:
            self.parts.append(value)
        if self.in_total:
            self.total_parts.append(value)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.label_id is not None:
            self.labels[self.label_id] = ''.join(self.parts).strip()
            self.label_id = None
        if tag == 'h2':
            self.in_total = False


def parse_calendar(source, username):
    parser = CalendarParser()
    parser.feed(source)
    days = []
    for date, cell in sorted(parser.cells.items()):
        dt.date.fromisoformat(date)
        label = parser.labels.get(cell['id'], '')
        match = re.match(r'^(No|[\d,]+) contributions? on\b', label)
        if not match or cell['level'] not in range(5):
            raise ValueError(f'Unrecognized calendar cell or tooltip: {date}')
        count = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
        if (count == 0) != (cell['level'] == 0):
            raise ValueError(f'Count/level mismatch: {date}')
        days.append({'date': date, 'count': count, 'level': cell['level']})
    if not 365 <= len(days) <= 372:
        raise ValueError(f'Expected a full-year calendar, received {len(days)} days')
    first, last = (dt.date.fromisoformat(days[i]['date']) for i in (0, -1))
    if first.weekday() != 6:
        raise ValueError('Calendar is missing its initial Sunday')
    expected = [str(first + dt.timedelta(days=i)) for i in range((last - first).days + 1)]
    if [d['date'] for d in days] != expected:
        raise ValueError('Calendar has missing dates')
    if abs((dt.datetime.now(dt.timezone.utc).date() - last).days) > 2:
        raise ValueError('GitHub returned an outdated calendar')
    total = sum(d['count'] for d in days)
    heading = re.search(r'([\d,]+)\s+contributions?', ''.join(parser.total_parts))
    if not heading or int(heading[1].replace(',', '')) != total:
        raise ValueError('Daily counts do not match the displayed GitHub total')
    return {'username': username, 'source': f'https://github.com/users/{username}/contributions', 'from': str(first), 'through': str(last), 'total': total, 'days': days}


def fetch(username):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}', username):
        raise ValueError('Invalid GitHub username')
    request = urllib.request.Request(f'https://github.com/users/{username}/contributions', headers={'User-Agent': 'BEY-profile-calendar/1.0', 'Accept': 'text/html', 'Accept-Language': 'en-US'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return parse_calendar(response.read().decode('utf-8'), username)
        except (OSError, ValueError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def render(data):
    days = data['days']
    first = dt.date.fromisoformat(days[0]['date'])
    sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="294" viewBox="0 0 1000 294" role="img" aria-labelledby="title desc">',
        '<title id="title">BEY — GitHub contribution calendar</title>',
        f'<desc id="desc">{data["total"]} contributions from {data["from"]} to {data["through"]}. Real GitHub data, refreshed daily.</desc>',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}.graph{animation:reveal .5s ease-out 8.6s both}.day{animation:reveal .5s ease-out both}@keyframes reveal{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){.day,.graph{animation:none}}</style><g class="graph">',
        '<rect x="1" y="1" width="998" height="292" rx="18" fill="#101117" stroke="#302b40"/>',
        '<text x="32" y="38" fill="#6ee7c7" font-size="16">~ $ git activity --last-year</text>',
        '<text x="966" y="38" text-anchor="end" fill="#82798f" font-size="13">SMALL STEPS. REAL PROGRESS.</text>',
        '<path d="M32 57H968" stroke="#282534"/>']
    months = set()
    for day in days:
        date = dt.date.fromisoformat(day['date'])
        col, row = divmod((date - sunday).days, 7)
        month = (date.year, date.month)
        if date.day <= 7 and row == 0 and month not in months:
            months.add(month)
            parts.append(f'<text x="{74 + col * 16}" y="86" fill="#82798f" font-size="11">{calendar.month_abbr[date.month]}</text>')
        parts.append(f'<rect class="day" x="{74 + col * 16}" y="{101 + row * 16}" width="12" height="12" rx="3" fill="{PALETTE[day["level"]]}" style="animation-delay:{(8.6 + col * .012 + row * .025):.3f}s"><title>{date}: {day["count"]} contributions</title></rect>')
    for row, label in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        parts.append(f'<text x="32" y="{111 + row * 16}" fill="#82798f" font-size="11">{label}</text>')
    active = sum(d['count'] > 0 for d in days)
    parts += ['<path d="M32 228H968" stroke="#282534"/>',
        f'<text x="32" y="263" fill="#e6ddf3" font-size="17">{data["total"]:,} contributions <tspan fill="#82798f" font-size="13">/ {active} active days</tspan></text>',
        f'<text x="540" y="263" fill="#82798f" font-size="12">through {data["through"]}</text>',
        '<text x="801" y="263" fill="#82798f" font-size="11">Less</text>']
    for index, color in enumerate(PALETTE):
        parts.append(f'<rect x="{838 + index * 17}" y="252" width="12" height="12" rx="3" fill="{color}"/>')
    parts += ['<text x="930" y="263" fill="#82798f" font-size="11">More</text>', '</g></svg>']
    return '\n'.join(parts) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', default='buremiyen')
    data = fetch(parser.parse_args().username)
    art = render(data)
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data/contributions.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'assets/contributions.svg').write_text(art, encoding='utf-8')
    print(f"Validated {len(data['days'])} days / {data['total']} contributions through {data['through']}")


if __name__ == '__main__':
    main()
