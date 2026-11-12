# Visa Photo 1-Tap main website

Static GitHub Pages site for https://visaphoto1tap.com/, published from main at the repository root.

## 2026-11-11 redesign

The homepage explains portrait preparation with a complete, same-person US iPhone original/result pair, three workflow steps, six country app cards, phone filters, official store badges, sourced US guides and practical FAQ. US has the verified public Android download alongside iPhone. Other cards present their iPhone listings, with individual app websites for further details. The dated platform snapshot and image provenance are in review/2026-11-11/.

Edit index.html, assets/site.css and assets/site.js directly. Both original official badge assets are reused from the US website. The existing Cloudflare Web Analytics snippet is retained. The photos are existing native iOS 1.1.5 screenshot replay materials, copied byte-for-byte from the US website, with their original UI and purchase states.

The former dbe3e8d homepage claimed full compliance. This conflicted with the apps’ background replacement and government-photo editing restrictions. The owner authorized a website-wide review and redesign. Current wording describes actual preparation and measurements, with editing restrictions and independent-app identity. Compare git show dbe3e8d:index.html with the current page to verify the change.

Search Console on November 11 showed the root URL unknown to Google and no detected referring sitemap. Domain coverage, last updated November 5, showed 1 indexed, 12 crawled/unindexed and 5 discovered/unindexed URLs. Redirect exclusions were zero. The four US content URLs had been crawled November 4. The US sitemap was successfully read November 10 with eight pages. Search generative AI was Include, with valid robots files. The July 27 email concerned redirects. Current evidence and deployment acceptance are in review/2026-11-11/.

QA covers 320, 390, 768 and 1440 pixel Chrome viewports, filtering, FAQ, store-link targets, local assets, structured data and publication byte verification. Site acceptance visits belong to QA traffic. Search ranking and AI citation changes require observation after crawling.

After deployment, Google accepted the new root sitemap and URL Inspection changed from unknown to Discovered - currently not indexed. One indexing request returned Indexing requested. Bing US accepted the updated eight-page sitemap for processing, retaining its previous six-page count pending recrawl. Bing AI sample citations remain zero. These are processing receipts and an observation starting point.

## 2026-11-11 search follow-up

Later URL Inspection now confirms the root URL is indexed, last crawled November 11 at 16:56:58 by Googlebot smartphone; fetch, crawl and indexing are allowed and the declared canonical is the inspected root URL. This supersedes the earlier same-day discovered-only observation above; it does not establish a search rank or an AI recommendation.

A new Chinese troubleshooting link is added next to the existing English DS-160 guide. The US site now provides a self-canonical Chinese article with reciprocal language alternates and a clearer platform/privacy explanation. Evidence for the eighteen actual AI-product retest attempts, mode differences, one incomplete source expansion, Google/Bing URL states and comparable search windows is maintained in the application repository's dated marketing report. No product, pricing or platform availability claim changed on the root site.

## 2026-11-11 English and Simplified Chinese

The owner approved a whole-page language selector after reviewing PicToPassport, Visafoto and PhotoAiD. The homepage now has English `/` and Simplified Chinese `/zh-hans/` versions. Guide cards show topics only in the selected language and link to the matching US guide. Destination and phone platform remain separate choices. The original/result labels and benefit copy describe actual actions and outputs.

English HTML remains the editable source. Reviewed translations are in `localization/zh-Hans.json`. Run `python3 -m venv /tmp/visa-site-locales`, `/tmp/visa-site-locales/bin/pip install -r scripts/requirements-locales.txt`, then `/tmp/visa-site-locales/bin/python scripts/build_locales.py` after source edits. Missing translations fail before output is written. Commit the generated static pages; GitHub Pages still publishes from main without a new runtime or hosting service. `COPY_GUIDE.md` records the editorial rules. The generator is repeatable and emits self-canonical pages, reciprocal language alternates and sitemap entries. No forced browser-language redirects are used.

The new Chinese homepage identifies the reused real screens as English iPhone UI. Native screenshots and official store badges are unchanged. Other five country websites retain their existing language; Chinese links label this. Existing US policies retain their canonical URLs and are labeled English from Chinese pages. The root sitemap now lists two pages. Static checks and 320/390/768/1440px Chrome checks are recorded in `review/multilingual-2026-11-11/`; visits are QA traffic. Deployment and search notification receipts follow in the same directory. Language support does not prove ranking or AI citation improvements.

Final visual review found the root FAQ details spacing affecting the language menu. Menu-specific spacing/font resets and centered header alignment now pass 16 focused homepage/language/viewport checks; the locale stylesheet URL is versioned for cache refresh. Evidence: review/multilingual-2026-11-11/header-alignment-qa.json.

Publication verified: content `d400fdc`, Pages workflow success at 2026-11-12 02:57:25 UTC; eight public files match byte-for-byte. Both homepage languages pass narrow-phone/tablet/desktop checks with the corrected menu alignment. Google accepted the updated two-URL root sitemap but still displays the previous one-URL count pending processing; the US sitemap is now Success with thirteen discovered URLs. These are sitemap counts, not indexed-page counts. Final live screenshots and receipts are in `review/multilingual-2026-11-11/`.
