# Farsi-only content, RTL-first layout, no i18n framework

We considered a bilingual Farsi/English site, which would mean Django's i18n framework, locale-prefixed URLs (`/fa/`, `/en/`), and a translation workflow the Content Editor would have to maintain on every future edit. We decided to build Farsi-only instead: pages render right-to-left by default, with embedded English/Latin terms (drug names, measurements) explicitly marked left-to-right so mixed sentences stay readable. The patient base is Persian-speaking, and the site's primary job (Q1: credibility for patients who already have the doctor's name) doesn't need an English audience, so bilingual support would add ongoing translation overhead for a non-technical editor without a corresponding benefit.

**Consequences**: adding English later means retrofitting Django's i18n framework and translating all existing content, not just flipping a setting.
