# Host on Runflare (Iran-based PaaS)

The patient base and both content editors are in Iran, where international clouds (AWS, Heroku, Render, etc.) are often slow, filtered, or impractical to pay for from inside the country. We decided to deploy to Runflare, an Iran-based cloud/PaaS, instead of a global provider. Reachability and payment feasibility for the actual users outweigh the more mature tooling and documentation of the international clouds.

**Consequences**: deployment follows Runflare's own CLI-based deploy flow rather than the more common Heroku/Render-style buildpack conventions, and there's a smaller community/doc base to lean on when something goes wrong.
