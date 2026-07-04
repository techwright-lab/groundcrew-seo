# Groundcrew

**The open skills that put your AI on TrustGrowth's growth team.**

[TrustGrowth](https://trustgrowth.ai) runs a growth, SEO, and content team for your site — agents that audit, research, strategize, and measure on schedule, server-side, with human approval gates. Groundcrew is how *your* AI joins that team: a set of plain-Markdown skills that any LLM agent can read, plus connect instructions for the TrustGrowth API and MCP server.

Everyone else gives your AI data. TrustGrowth puts a growth team to work — and Groundcrew gives your AI a seat at the table.

## What your agent can do with Groundcrew

| Skill | What it does |
|---|---|
| [`trustgrowth`](skills/trustgrowth/SKILL.md) | Core: connect, authenticate, discover the API, run safe smoke tests. Start here. |
| [`standup`](skills/standup/SKILL.md) | Morning standup with your growth team: score delta, what changed, what needs you. |
| [`site-audit`](skills/site-audit/SKILL.md) | Read audit results, interpret issues by severity, trigger manual audits where your plan allows. |
| [`fix-my-site`](skills/fix-my-site/SKILL.md) | **Flagship.** TrustGrowth finds the issues; your coding agent fixes them in your repo; the next audit verifies. |
| [`keyword-scout`](skills/keyword-scout/SKILL.md) | Turn keyword opportunities (yours + competitor gaps) into a prioritized content plan. |
| [`competitor-watch`](skills/competitor-watch/SKILL.md) | Track competitor movement and interpret what changed. |
| [`eeat-review`](skills/eeat-review/SKILL.md) | E-E-A-T pillar scores and recommendations → a concrete improvement checklist. |
| [`score-report`](skills/score-report/SKILL.md) | Assemble a shareable, claim-safe weekly report from your score history and evidence. |
| [`content-desk`](skills/content-desk/SKILL.md) | 🔜 **Coming soon.** Operate the content pipeline: calendar, briefs, drafts, publication records. |

## Install

**One-liner (Claude Code, OpenClaw, Hermes, or any agent with a skills directory):**

```bash
curl -fsSL https://raw.githubusercontent.com/techwright-lab/groundcrew/main/install.sh | bash
```

**Manual:**

```bash
git clone https://github.com/techwright-lab/groundcrew.git
cp -r groundcrew/skills/* ~/.claude/skills/   # or your agent's skills directory
```

**Claude plugin:** this repo ships a plugin manifest — add it from the Claude Code plugin marketplace or point Claude Code at this repo.

## Connect

You need a TrustGrowth account (Hobby plan or higher) and an API key from **Settings → API Keys**.

```bash
export TRUSTGROWTH_API_BASE="https://trustgrowth.ai"
export TRUSTGROWTH_API_KEY="tg_live_..."
```

**MCP** — connect TrustGrowth as a native tool server:

```json
{
  "mcpServers": {
    "trustgrowth": {
      "type": "http",
      "url": "https://trustgrowth.ai/mcp",
      "headers": { "Authorization": "Bearer tg_live_..." }
    }
  }
}
```

**REST** — everything is also a documented HTTP endpoint: live OpenAPI reference at [trustgrowth.ai/developers](https://trustgrowth.ai/developers).

## Compatibility

| Environment | Skills | MCP | Notes |
|---|---|---|---|
| Claude Code | ✅ | ✅ | Full experience incl. `fix-my-site` against your local repo |
| Cursor | ✅ (rules/context) | ✅ | `fix-my-site` works against your open workspace |
| Hermes | ✅ | ✅ | Install skills into your Hermes skills directory |
| OpenClaw | ✅ | ✅ | Import skills; MCP via HTTP connector |
| claude.ai (web) | ⚠️ paste-in | 🔜 | OAuth connector coming; until then use paste-in workflows |
| ChatGPT | ⚠️ paste-in | 🔜 | Connector support arrives with OAuth |
| Any LLM agent | ✅ | depends | Skills are plain Markdown + curl; if your agent can read files and run HTTP, it works |

⚠️ = degraded but usable: skills are readable instructions, so you can paste the relevant workflow into a chat and supply API responses manually. 🔜 = ships shortly after launch.

## How this relates to the product

TrustGrowth's own team keeps working whether or not your agent shows up — audits run on schedule, research refreshes, the score updates daily. Groundcrew doesn't replace that team; it lets your AI collaborate with it: read the same evidence, act on the same queue, and (with `fix-my-site`) close the loop no dashboard can — actually fixing your site.

These skills only use documented, versioned API surface. If a skill and the live API disagree, trust the live [OpenAPI](https://trustgrowth.ai/developers/openapi.yml) and [open an issue](https://github.com/techwright-lab/groundcrew/issues).

## Dogfood note

TechWright (the company behind TrustGrowth) runs its own growth through this exact surface — our internal agents operate the same API and MCP endpoints these skills document. See the public [proof pages](https://trustgrowth.ai/proofs) for the receipts.

## License

MIT
