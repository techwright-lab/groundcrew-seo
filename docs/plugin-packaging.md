# Plugin packaging

The marketplace and plugin manifests use VERSION in `scripts/generate-adapters.py`.
Run `python3 scripts/generate-adapters.py --check` to check generated metadata.

## Claude Code

```text
/plugin marketplace add techwright-lab/groundcrew-seo
/plugin install groundcrew-seo@groundcrew
```

For a local test, replace the repository name with the absolute checkout path.
Use `CLAUDE_CONFIG_DIR` with a disposable directory to isolate the test settings.
The shell commands `claude plugin marketplace add` and `claude plugin install` perform the same operations.
Run `claude plugin details groundcrew-seo` to list the loaded skills.

## OpenAI Codex

Run `python3 scripts/build-plugin.py` to build `dist/groundcrew-seo-1.1.0.zip`.
The ZIP includes `.codex-plugin/plugin.json`, `skills/`, `shared/`, and `LICENSE`.
The build uses the distribution validator's allowed roots and denied path components.
It rejects MCP configuration, unsafe symlinks, and unsupported file types.
Shared-reference symlinks become regular files in the ZIP.
Files use a fixed timestamp, mode, order, and ZIP_STORED encoding for repeatable output.
The build does not publish the ZIP.

Extract the ZIP into `plugin/` under a disposable marketplace directory.
Create `.agents/plugins/marketplace.json` in that directory:

```json
{
  "name": "groundcrew-local",
  "plugins": [{
    "name": "groundcrew-seo",
    "source": {"source": "local", "path": "./plugin"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Productivity"
  }]
}
```

Use a disposable `CODEX_HOME` directory for these commands:

```sh
codex plugin marketplace add /absolute/path/to/disposable-marketplace --json
codex plugin add groundcrew-seo@groundcrew-local --json
codex plugin list --json
```

## Acceptance output (2026-11-01)

`claude plugin validate .` passed with a missing-icon warning.
The README install guidance remains with TEC-11907 because its owner changes that section.

Claude marketplace installation and component inventory:

```text
Adding marketplace…✔ Successfully added marketplace: groundcrew (declared in user settings)
Installing plugin "groundcrew-seo@groundcrew"...✔ Successfully installed plugin: groundcrew-seo@groundcrew (scope: user)
Groundcrew SEO — TrustGrowth (groundcrew-seo) 1.1.0
  Description: Twenty open SEO and growth skills for AI agents — audit, fix, keywords, competitors, E-E-A-T, AI visibility, evidence-labeled reports, and the grow loop — from TrustGrowth.
  Source: groundcrew-seo@groundcrew

Component inventory
  Skills (20)  ai-visibility, audit-report, authority-report, authority-review, backlink-opportunities, competitor-readout, competitor-watch, content-desk, content-strategy, eeat-review, fix-my-site, geo-report, grow, keyword-report, keyword-scout, score-report, site-audit, standup, trustgrowth, weekly-report
  Agents (0)
  Hooks (0)
  MCP servers (0)
  LSP servers (0)

Projected token cost
  Always-on:   ~1,263 tok   added to every session

Per-component (rounded)
  component               always-on  on-invoke
  ai-visibility                 ~90      ~1.3k
  audit-report                  ~60       ~970
  authority-report              ~60       ~560
  authority-review             ~100       ~920
  backlink-opportunities       ~100        ~1k
  competitor-readout            ~50       ~570
  competitor-watch              ~60       ~570
  content-desk                  ~60       ~580
  content-strategy              ~90      ~1.1k
  eeat-review                   ~50       ~530
  fix-my-site                   ~60      ~1.5k
  geo-report                    ~60       ~540
  grow                          ~50      ~1.1k
  keyword-report                ~60       ~580
  keyword-scout                 ~60       ~690
  score-report                  ~50       ~500
  site-audit                    ~60      ~1.3k
  standup                       ~50       ~480
  trustgrowth                   ~70      ~1.5k
  weekly-report                 ~50       ~590

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

Codex local installation and enabled state:

```json
{
  "marketplaceName": "groundcrew-local",
  "installedRoot": "/tmp/TEC-10704-local-marketplace",
  "alreadyAdded": false
}
{
  "pluginId": "groundcrew-seo@groundcrew-local",
  "name": "groundcrew-seo",
  "marketplaceName": "groundcrew-local",
  "version": "1.1.0",
  "installedPath": "/tmp/TEC-10704-codex-home/plugins/cache/groundcrew-local/groundcrew-seo/1.1.0",
  "authPolicy": "ON_INSTALL"
}
{
  "installed": [
    {
      "pluginId": "groundcrew-seo@groundcrew-local",
      "name": "groundcrew-seo",
      "marketplaceName": "groundcrew-local",
      "version": "1.1.0",
      "installed": true,
      "enabled": true,
      "source": {
        "source": "local",
        "path": "/tmp/TEC-10704-local-marketplace/plugin"
      },
      "marketplaceSource": {
        "sourceType": "local",
        "source": "/tmp/TEC-10704-local-marketplace"
      },
      "installPolicy": "AVAILABLE",
      "authPolicy": "ON_INSTALL"
    }
  ],
  "available": []
}

```

Codex app-server `skills/list` loaded these skills from the installed ZIP.
The response had no skill errors.

```text
groundcrew-seo:ai-visibility
groundcrew-seo:audit-report
groundcrew-seo:authority-report
groundcrew-seo:authority-review
groundcrew-seo:backlink-opportunities
groundcrew-seo:competitor-readout
groundcrew-seo:competitor-watch
groundcrew-seo:content-desk
groundcrew-seo:content-strategy
groundcrew-seo:eeat-review
groundcrew-seo:fix-my-site
groundcrew-seo:geo-report
groundcrew-seo:grow
groundcrew-seo:keyword-report
groundcrew-seo:keyword-scout
groundcrew-seo:score-report
groundcrew-seo:site-audit
groundcrew-seo:standup
groundcrew-seo:trustgrowth
groundcrew-seo:weekly-report
```

ZIP file list (94 files):

```text
.codex-plugin/plugin.json
LICENSE
shared/connectors.md
shared/contract/capabilities.json
shared/contract-pin.json
shared/dataforseo.md
shared/evidence.schema.yaml
shared/provider-selection.md
shared/reporting.md
skills/ai-visibility/SKILL.md
skills/ai-visibility/references/connectors.md
skills/ai-visibility/references/dataforseo.md
skills/ai-visibility/references/provider-selection.md
skills/ai-visibility/references/reporting.md
skills/audit-report/SKILL.md
skills/audit-report/references/connectors.md
skills/audit-report/references/provider-selection.md
skills/audit-report/references/reporting.md
skills/authority-report/SKILL.md
skills/authority-report/references/connectors.md
skills/authority-report/references/provider-selection.md
skills/authority-report/references/reporting.md
skills/authority-review/SKILL.md
skills/authority-review/references/connectors.md
skills/authority-review/references/provider-selection.md
skills/authority-review/references/reporting.md
skills/backlink-opportunities/SKILL.md
skills/backlink-opportunities/references/connectors.md
skills/backlink-opportunities/references/dataforseo.md
skills/backlink-opportunities/references/provider-selection.md
skills/backlink-opportunities/references/reporting.md
skills/competitor-readout/SKILL.md
skills/competitor-readout/references/connectors.md
skills/competitor-readout/references/provider-selection.md
skills/competitor-readout/references/reporting.md
skills/competitor-watch/SKILL.md
skills/competitor-watch/references/connectors.md
skills/competitor-watch/references/dataforseo.md
skills/competitor-watch/references/provider-selection.md
skills/competitor-watch/references/reporting.md
skills/content-desk/SKILL.md
skills/content-desk/references/connectors.md
skills/content-desk/references/provider-selection.md
skills/content-desk/references/reporting.md
skills/content-strategy/SKILL.md
skills/content-strategy/references/connectors.md
skills/content-strategy/references/provider-selection.md
skills/content-strategy/references/reporting.md
skills/eeat-review/SKILL.md
skills/eeat-review/references/connectors.md
skills/eeat-review/references/provider-selection.md
skills/eeat-review/references/reporting.md
skills/fix-my-site/SKILL.md
skills/fix-my-site/references/connectors.md
skills/fix-my-site/references/provider-selection.md
skills/fix-my-site/references/reporting.md
skills/geo-report/SKILL.md
skills/geo-report/references/connectors.md
skills/geo-report/references/provider-selection.md
skills/geo-report/references/reporting.md
skills/grow/SKILL.md
skills/grow/references/connectors.md
skills/grow/references/provider-selection.md
skills/grow/references/reporting.md
skills/keyword-report/SKILL.md
skills/keyword-report/references/connectors.md
skills/keyword-report/references/provider-selection.md
skills/keyword-report/references/reporting.md
skills/keyword-scout/SKILL.md
skills/keyword-scout/references/connectors.md
skills/keyword-scout/references/dataforseo.md
skills/keyword-scout/references/provider-selection.md
skills/keyword-scout/references/reporting.md
skills/score-report/SKILL.md
skills/score-report/references/connectors.md
skills/score-report/references/provider-selection.md
skills/score-report/references/reporting.md
skills/site-audit/SKILL.md
skills/site-audit/references/connectors.md
skills/site-audit/references/provider-selection.md
skills/site-audit/references/reporting.md
skills/standup/SKILL.md
skills/standup/references/connectors.md
skills/standup/references/provider-selection.md
skills/standup/references/reporting.md
skills/trustgrowth/SKILL.md
skills/trustgrowth/references/connectors.md
skills/trustgrowth/references/contract.md
skills/trustgrowth/references/provider-selection.md
skills/trustgrowth/references/reporting.md
skills/weekly-report/SKILL.md
skills/weekly-report/references/connectors.md
skills/weekly-report/references/provider-selection.md
skills/weekly-report/references/reporting.md
```
