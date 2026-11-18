#!/usr/bin/env python3
"""Hand-written guide pages (English + Simplified Chinese): derive JSON-LD from visible text,
list the pages in sitemap.xml and check canonical/hreflang/links/images.

The HTML body is the editable source. Only the <script data-guide-schema> block and sitemap
entries are generated, so the structured data can never drift from what readers see.
Usage: python scripts/build_guides.py          (write)
       python scripts/build_guides.py --check  (fail if anything would change or a check fails)
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import html as html_lib
import json, re, sys, xml.etree.ElementTree as ET
from play_campaigns import play_url
from store_attribution import tag_store_links
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://visaphoto1tap.com'
MODIFIED = '2026-11-14'
PAGE_MODIFIED = {
    'guides/china-visa-photo-upload-failed.html': '2026-11-17',
    'guides/india-e-visa-photo-requirements.html': '2026-11-17',
    'guides/schengen-visa-photo-requirements-by-country.html': '2026-11-17',
}
LOCALES = [('en', ''), ('zh-Hans', '/zh-hans')]
TOPICS = ['guides/index.html', 'guides/china-visa-photo-upload-failed.html',
          'guides/ds-160-photo-upload-error.html', 'guides/us-visa-photo-at-home-with-phone.html',
          'guides/india-e-visa-photo-requirements.html', 'guides/schengen-visa-photo-requirements-by-country.html',
          'guides/dv-lottery-photo-requirements.html']
PLAY_TOPICS = {'guides/ds-160-photo-upload-error.html', 'guides/us-visa-photo-at-home-with-phone.html', 'guides/dv-lottery-photo-requirements.html'}
PUBLISHER = {'@type': 'Organization', 'name': 'Visa Photo 1-Tap', 'url': ORIGIN + '/'}
norm = lambda t: re.sub(r'\s+', ' ', t).strip()


def route(f):
    return '/' + f.removesuffix('index.html')


def schema(soup, f, prefix, lang):
    url = ORIGIN + prefix + route(f)
    main = soup.select_one('main')
    h1s = soup.find_all('h1')
    assert len(h1s) == 1, (f, lang, 'exactly one h1')
    headline = norm(h1s[0].get_text())
    desc = soup.select_one('meta[name=description]')['content']
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': norm(soup.select_one('.breadcrumb a').get_text()),
               'item': ORIGIN + prefix + '/'}]
    graph = []
    if f.endswith('index.html'):
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': headline, 'item': url})
        items = [{'@type': 'ListItem', 'position': i + 1, 'name': norm(a.get_text()), 'url': ORIGIN + a['href']}
                 for i, a in enumerate(soup.select('.guide-list h2 a'))]
        graph.append({'@type': 'CollectionPage', '@id': url + '#page', 'url': url, 'name': headline,
                      'description': desc, 'inLanguage': lang, 'publisher': PUBLISHER,
                      'mainEntity': {'@type': 'ItemList', 'itemListElement': items}})
    else:
        index_name = norm(soup.select('.breadcrumb a')[1].get_text())
        crumbs += [{'@type': 'ListItem', 'position': 2, 'name': index_name, 'item': ORIGIN + prefix + '/guides/'},
                   {'@type': 'ListItem', 'position': 3, 'name': headline, 'item': url}]
        img = soup.select_one('meta[property="og:image"]')['content']
        graph.append({'@type': 'Article', '@id': url + '#article', 'headline': headline, 'description': desc,
                      'url': url, 'mainEntityOfPage': url, 'inLanguage': lang, 'image': img,
                      'datePublished': main['data-published'], 'dateModified': main['data-modified'],
                      'author': PUBLISHER, 'publisher': PUBLISHER})
        faq = []
        for h3 in soup.select('section.faq-list h3'):
            parts = []
            for sib in h3.find_next_siblings():
                if sib.name == 'h3':
                    break
                parts.append(norm(sib.get_text()))
            faq.append({'@type': 'Question', 'name': norm(h3.get_text()),
                        'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(parts)}})
        assert faq, (f, lang, 'FAQ section missing')
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'url': url, 'inLanguage': lang, 'mainEntity': faq})
    graph.append({'@type': 'BreadcrumbList', 'itemListElement': crumbs})
    return {'@context': 'https://schema.org', '@graph': graph}


def local_target(href, base):
    u = urlsplit(href)
    if u.scheme or u.netloc:
        if u.netloc != 'visaphoto1tap.com':
            return None
    path = unquote(u.path) if u.path else base
    if not path.startswith('/'):
        path = base.rsplit('/', 1)[0] + '/' + path
    p = ROOT / path.lstrip('/')
    if path.endswith('/'):
        p = p / 'index.html'
    return p, u.fragment


def check(soup, f, prefix, lang, problems):
    url = ORIGIN + prefix + route(f)
    if soup.html.get('lang') != lang:
        problems.append(f'{prefix}/{f}: html lang')
    if soup.select_one('link[rel=canonical]')['href'] != url:
        problems.append(f'{prefix}/{f}: canonical')
    alts = {l['hreflang']: l['href'] for l in soup.select('link[rel=alternate][hreflang]')}
    want = {code: ORIGIN + p + route(f) for code, p in LOCALES}
    want['x-default'] = ORIGIN + route(f)
    if alts != want:
        problems.append(f'{prefix}/{f}: hreflang {alts}')
    if soup.select_one('meta[property="og:url"]')['content'] != url:
        problems.append(f'{prefix}/{f}: og:url')
    if soup.select_one('meta[property="og:title"]')['content'] != norm(soup.title.get_text()):
        problems.append(f'{prefix}/{f}: og:title differs from title')
    base = prefix + route(f) if not f.endswith('index.html') else prefix + route(f)
    for el in soup.find_all(['a', 'img', 'link', 'script']):
        href = el.get('href') or el.get('src')
        if not href or href.startswith(('mailto:', '#')) or el.get('rel') == ['alternate'] or el.get('rel') == ['canonical']:
            if href and href.startswith('#') and not soup.find(id=href[1:]):
                problems.append(f'{prefix}/{f}: missing anchor {href}')
            continue
        t = local_target(href.split('?')[0] if el.name in ('link', 'script') else href, base)
        if t is None:
            continue
        p, frag = t
        if not p.exists():
            problems.append(f'{prefix}/{f}: missing {href}')
        elif frag and p.suffix == '.html' and f'id="{frag}"' not in p.read_text():
            problems.append(f'{prefix}/{f}: missing fragment {href}')
    for img in soup.find_all('img'):
        if not img.get('alt') and img.get('alt') != '':
            problems.append(f'{prefix}/{f}: img without alt {img.get("src")}')


def main():
    checking = '--check' in sys.argv
    problems, changed = [], []
    for f in TOPICS:
        for lang, prefix in LOCALES:
            path = ROOT / (prefix.lstrip('/') + '/' + f if prefix else f)
            html = path.read_text()
            if f in PLAY_TOPICS:
                pattern = r'(<a\b[^>]*class="store play"[^>]*href=")[^"]*(")'
                html, count = re.subn(pattern, lambda m: m.group(1) + html_lib.escape(play_url('root-guides-android'), quote=True) + m.group(2), html)
                assert count == 1, (path, 'expected one Play badge')
            soup = BeautifulSoup(html, 'html.parser')
            data = json.dumps(schema(soup, f, prefix, lang), ensure_ascii=False, separators=(', ', ': '))
            new = re.sub(r'(<script type="application/ld\+json" data-guide-schema="">)(.*?)(</script>)',
                         lambda m: m.group(1) + data + m.group(3), html, count=1, flags=re.S)
            assert new != html or data in html, (path, 'schema block missing')
            new = tag_store_links(new, ORIGIN + prefix + route(f), lang)
            check(BeautifulSoup(new, 'html.parser'), f, prefix, lang, problems)
            if new != path.read_text():
                changed.append(str(path.relative_to(ROOT)))
                if not checking:
                    path.write_text(new)
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    site = ET.parse(ROOT / 'sitemap.xml')
    tree = site.getroot()
    existing = {n.find('{' + ns + '}loc').text: n for n in tree}
    before = ET.tostring(tree)
    for f in TOPICS:
        for _, prefix in LOCALES:
            url = ORIGIN + prefix + route(f)
            n = existing.get(url)
            if n is None:
                n = ET.SubElement(tree, '{' + ns + '}url')
                ET.SubElement(n, '{' + ns + '}loc').text = url
                ET.SubElement(n, '{' + ns + '}lastmod')
            n.find('{' + ns + '}lastmod').text = PAGE_MODIFIED.get(f, MODIFIED)
    ET.indent(tree, space='  ')
    if ET.tostring(tree) != before:
        changed.append('sitemap.xml')
        if not checking:
            site.write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    if problems:
        raise SystemExit('Guide checks failed:\n' + '\n'.join(problems))
    if checking and changed:
        raise SystemExit('Generated output out of date: ' + ', '.join(changed))
    print(f'{len(TOPICS) * len(LOCALES)} guide pages: schema from visible text, canonical, hreflang, '
          f'local links and images passed; {"no changes" if not changed else "updated " + ", ".join(changed)}')


if __name__ == '__main__':
    main()
