# Skills Index

Complete catalog of all OpenClaw skills in this workspace.

## Core Skills (4)

### 1. qqbot-cron
- **Description**: QQ Bot intelligent reminders with scheduling
- **Features**: One-time reminders, recurring tasks, auto-fallback
- **Status**: ✅ Active
- **Documentation**: `~/.openclaw/extensions/qqbot/skills/qqbot-cron/SKILL.md`

### 2. qqbot-media
- **Description**: QQ Bot media sending (images, files)
- **Features**: Image upload, file sharing, multimedia support
- **Status**: ✅ Active
- **Documentation**: `~/.openclaw/extensions/qqbot/skills/qqbot-media/SKILL.md`

### 3. clawhub
- **Description**: ClawHub CLI for skill management
- **Features**: Search, install, update, publish skills
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/clawhub/SKILL.md`

### 4. github
- **Description**: GitHub CLI integration
- **Features**: Issues, PRs, CI runs, API queries
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/github/SKILL.md`

## Professional Skills (18)

### 1. page-agent
- **Description**: Alibaba's GUI agent for web automation
- **Features**: Natural language web control, DOM analysis, multi-LLM support
- **Version**: v1.5.7
- **Status**: ✅ Complete (100%)
- **Documentation**: `/root/.openclaw/workspace/skills/page-agent/SKILL.md`
- **Examples**: 8 usage examples in `skills/page-agent/examples/`

### 2. glm-4.6v-test
- **Description**: GLM-4.6V model testing and validation
- **Features**: API connection, dialogue, math, code generation tests
- **Provider**: glmcode (智谱AI)
- **Status**: ✅ Complete (100%)
- **Documentation**: `/root/.openclaw/workspace/skills/glm-4.6v-test/`

### 3. adspirer-ads-agent
- **Description**: AI-powered advertising and performance marketing agent
- **Features**: Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads
- **Capabilities**: 100+ tools for paid media, keyword research, budget optimization
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/adspirer-ads-agent/SKILL.md`

### 4. agent-browser
- **Description**: Fast Rust-based headless browser automation
- **Features**: Navigate, click, type, snapshot pages via structured commands
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/agent-browser/SKILL.md`

### 5. code-security-auditor
- **Description**: Comprehensive code security audit with AI-powered vulnerability detection
- **Features**: OWASP Top 10, dependency scanning, secret detection, SAST
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/code-security-auditor/SKILL.md`

### 6. contract-reviewer
- **Description**: Review business contracts for risks and compliance gaps
- **Features**: NDA review, MSA analysis, SaaS agreements, vendor contracts
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/contract-reviewer/SKILL.md`

### 7. find-skills
- **Description**: Help users discover and install agent skills
- **Features**: Skill search, capability matching, installation guidance
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/find-skills/SKILL.md`

### 8. notion
- **Description**: Notion API for pages, databases, and blocks management
- **Features**: CRUD operations, database queries, block management
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/notion/SKILL.md`

### 9. obsidian
- **Description**: Work with Obsidian vaults and automation
- **Features**: Plain Markdown notes, obsidian-cli integration
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/obsidian/SKILL.md`

### 10. session-monitor
- **Description**: Auto-monitor and display session status
- **Features**: Token consumption, model info, function status monitoring
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/session-monitor/SKILL.md`

### 11. stock-monitor-skill
- **Description**: Full-featured intelligent stock monitoring and alert system
- **Features**: Cost percentage, MA crossover, RSI, volume anomaly, gap analysis
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/stock-monitor-skill/SKILL.md`

### 12. summarize
- **Description**: Summarize URLs or files with summarize CLI
- **Features**: Web pages, PDFs, images, audio, YouTube summarization
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/summarize/SKILL.md`

### 13. tavily-search
- **Description**: AI-optimized web search via Tavily API
- **Features**: Concise, relevant results for AI agents
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/tavily-search/SKILL.md`

### 14. tdd-ecc
- **Description**: Test-driven development with red-green-refactor loop
- **Features**: TDD workflow, integration tests, de-sloppify pattern
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/tdd-ecc/SKILL.md`

### 15. test-effort-estimator
- **Description**: Estimate test effort based on product requirements
- **Features**: Task breakdown, effort estimation, Excel export
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/test-effort-estimator/SKILL.md`

### 16. weather
- **Description**: Get current weather and forecasts (no API key required)
- **Features**: Current conditions, forecasts, multiple locations
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/weather/SKILL.md`

### 17. ai-security-scanner
- **Description**: AI security vulnerability scanning
- **Features**: AI model security checks, vulnerability detection
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/ai-security-scanner/SKILL.md`

### 18. meta-ads
- **Description**: Meta Ads (Facebook & Instagram) management
- **Features**: Campaign creation, performance analysis, ad optimization
- **Status**: ✅ Active
- **Documentation**: `/root/.openclaw/workspace/skills/meta-ads/SKILL.md`

## Skill Management

### Installation Policy
1. Try `skillhub` (domestic registry) first
2. Fallback to `clawhub` (public registry) if unavailable
3. Summarize source, version, and risk signals before installation

### Usage Examples

#### Page Agent
```javascript
import { PageAgent } from 'page-agent';

const agent = new PageAgent({
  apiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-4'
});

await agent.navigate('https://example.com');
await agent.chat('Click the login button');
```

#### GLM-4.6V
```python
from openclaw import Model

model = Model('glm-4.6v')
response = model.chat('Hello, GLM-4.6V!')
```

## Statistics

- **Total Skills**: 22
- **Active Skills**: 22
- **Core Skills**: 4
- **Professional Skills**: 18
- **Integration Status**: 100%
- **Test Coverage**: 83.3%

## Maintenance

Regular updates are performed to keep skills up-to-date:
- Dependency checks every 2 days
- Security scans every 3 days
- Documentation reviews weekly

---

**Last Updated**: 2026-03-15 01:08
**Maintained by**: Echo-2 (Agentic AI)
