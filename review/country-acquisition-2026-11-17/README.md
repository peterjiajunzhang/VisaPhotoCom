# Country site acquisition update · 2026-11-17

The five affected iPhone apps each use one website campaign. Root homepages, matching root guides and the country sites use the same corresponding URL. App IDs come from the five AppStoreAppleID values in VisaPhotoApps. The provider token comes from the US campaign previously generated in this developer account, recorded in the app repository at `docs/marketing/evidence/search-2026-11-04/asc-campaign-links.json`. Apple documents that the token is account-wide and that Analytics requires at least five individual first-time downloads per campaign before showing it. Tagged store URLs were opened to confirm their listing and campaign/provider query parameters after the Apple redirect. No installs were used as test traffic. [Apple campaign links](https://developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links/)

| App | Website campaign | Pages |
| --- | --- | --- |
| Canada | `canada-website-20261117` | Canada homepage and seven root homepages |
| China | `china-website-20261117` | China homepage, seven root homepages and two root China troubleshooting guides |
| India | `india-website-20261117` | India homepage, seven root homepages and two root India e-Visa guides |
| Japan | `japan-website-20261117` | Japan homepage and seven root homepages |
| Schengen | `schengen-website-20261117` | Schengen homepage, six English and Simplified Chinese country pages, seven root homepages and two root comparison guides |

Clean entity URLs remain in structured data. US home and guide campaigns and Google Play referrers retain their original destinations. Public Google Play badge coverage remains the US product only. Original App Store badge art is used at the updated country CTAs.

## Published guidance

- Canada distinguishes the app’s 420×540 JPEG and automatic background replacement from the visitor-visa photo rules and the separate PR photo route. [IRCC TRV specifications](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides/temporary-resident-visa-application-photograph-specifications.html) · [IRCC permanent resident photos](https://www.canada.ca/en/immigration-refugees-citizenship/services/permanent-residents/card/photos.html)
- China describes the app’s 420×560 JPEG and links back to the existing troubleshooting article. The article covers the application’s own upload and check flow. [Chinese Embassy application guide](https://us.china-embassy.gov.cn/eng./lsfw/zj/qz2021/202509/t20250920_11712388.htm)
- India distinguishes the portal’s square JPEG range of 10 KB to 1 MB and sample upload minimum of 350×350 pixels from the app’s up-to-1000×1000 px and 10–300 KB target. Free preview precedes the single export purchase. [India e-Visa instructions](https://indianvisaonline.gov.in/visa/tvoa.html) · [Government sample form](https://indianvisaonline.gov.in/evisa/images/SampleForm.pdf)
- Japan links to the two-size comparison and identifies the San Francisco instructions by visa type. [MOFA visa application form](https://www.mofa.go.jp/mofaj/files/000124525.pdf) · [San Francisco work and long-term visa instructions](https://www.sf.us.emb-japan.go.jp/itpr_en/e_m02_01_03.html)
- Schengen distinguishes the 29 Schengen countries from the app’s separate Cyprus and generic selections. Its country pages keep their paired canonical and language links. [European Commission member list](https://home-affairs.ec.europa.eu/policies/schengen/schengen-area_en)

## Regression coverage

The 24 edited pages are checked for campaign and product ID, official badge, supported platform, canonical, language and structured-data links. Responsive checks include mobile, tablet and desktop, and the Japan, Canada and Schengen navigation paths. The withdrawn US JPEG inspector is checked across all seven homepage and guide routes, its historical `#file-check` fragment, the older Chinese redirect and its former CSS/JavaScript asset URLs. Existing published DS-160 text guides remain usable.

Run `python scripts/build_locales.py`, `python scripts/build_guides.py --check` and `python scripts/check_growth.py .` to regenerate and verify the root locale and guide contracts.
