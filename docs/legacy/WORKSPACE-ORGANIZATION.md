# Workspace Organization Plan

## Current State Analysis

### Directory Structure
```
/root/.openclaw/workspace/
├── Core Configuration Files (9)
├── Memory & Documentation (15)
├── Skills Directory (22 skills)
├── Project Directories (6)
├── Python Scripts & Automation (18)
├── Backup & Temporary Files (3)
└── System Files (5)
```

### Issues Identified
1. **Mixed content types**: Workspace root contains both config files and project code
2. **Python scripts scattered**: 18 standalone scripts without proper organization
3. **Backup files**: ad-platform-backup-*.tar.gz (72MB) should be archived
4. **Deprecated projects**: oceanengine-ads, stocks_analysis, LemClaw appear inactive
5. **Skill management inconsistency**: Some skills have minimal content (40 bytes)
6. **Missing documentation**: Many Python scripts lack README or usage docs
7. **Git ignore gaps**: Large files and temporary files not properly ignored

## Organization Strategy

### Phase 1: Archive & Cleanup
**Goal**: Remove unnecessary files and archive old projects

**Actions**:
1. Move backup files to archives/
2. Move deprecated projects to archived/
3. Delete __pycache__ directories
4. Clean up node_modules (add to .gitignore)
5. Remove empty or minimal skill directories

**Files to Archive**:
- ad-platform-backup-20260302-160134.tar.gz → archives/backups/
- oceanengine-ads/ → archived/deprecated/
- stocks_analysis/ → archived/deprecated/
- LemClaw/ → archived/deprecated/

### Phase 2: Reorganize Skills
**Goal**: Ensure all skills have proper structure and documentation

**Actions**:
1. Audit each skill directory
2. Remove empty or incomplete skills
3. Standardize skill structure (SKILL.md, README.md, examples/)
4. Create skills/index.md for catalog

**Skills to Review**:
- adspirer-ads-agent (57 bytes - likely incomplete)
- agent-browser (63 bytes - incomplete)
- ai-security-scanner (74 bytes - incomplete)
- contract-reviewer (40 bytes - incomplete)
- find-skills (40 bytes - incomplete)
- github (40 bytes - incomplete)
- meta-ads (40 bytes - incomplete)
- notion (40 bytes - incomplete)
- obsidian (40 bytes - incomplete)
- stock-monitor-skill (74 bytes - incomplete)
- summarize (40 bytes - incomplete)
- weather (40 bytes - incomplete)

### Phase 3: Organize Python Scripts
**Goal**: Create logical directories for scripts

**Actions**:
1. Create scripts/ directory
2. Move Python scripts to subdirectories:
   - scripts/automation/ (web automation, captcha)
   - scripts/analysis/ (stock analysis, contract analysis)
   - scripts/integration/ (openclaw integration)
   - scripts/utils/ (utility scripts)
3. Add README.md to each subdirectory
4. Update imports and references

**Script Categories**:
- **Automation** (8 scripts):
  - enhanced_login.py
  - enhanced_website_login.py
  - fixed_web_automation.py
  - website_login.py
  - google_captcha_solver.py
  - web_data_collector.py
  - web_search_integration.py
  - local_web_search.py

- **Analysis** (5 scripts):
  - stock_analyzer.py
  - stock_cli.py
  - baidu_news_search.py
  - contract-analysis-*.md (documentation)
  - captcha-model-risk-analysis.md

- **Integration** (5 scripts):
  - echo2_swarm.py
  - multi_user_permission.py
  - openclaw_system.py
  - openclaw-with-openviking.py
  - openclaw_memory_integration.py

- **Utils** (5 scripts):
  - simple_openclaw.py
  - test_integration.py
  - test-memory-service.py
  - web_search_demo.py
  - web_search_test.py

### Phase 4: Improve Documentation
**Goal**: Create comprehensive documentation

**Actions**:
1. Update README.md with current project overview
2. Create PROJECTS.md cataloging all projects
3. Create SCRIPTS.md documenting all Python scripts
4. Update MEMORY.md with organization changes
5. Create .gitignore improvements

**Documentation Structure**:
```
docs/
├── README.md (main docs index)
├── projects.md (project catalog)
├── scripts.md (script documentation)
└── api/ (API documentation)
```

### Phase 5: Git Management
**Goal**: Clean up git repository

**Actions**:
1. Update .gitignore
2. Run git prune
3. Archive old commits if needed
4. Create proper commit messages

## Target Directory Structure

```
/root/.openclaw/workspace/
├── .git/
├── .gitignore (updated)
├── .openclaw/
├── .env
│
├── Core Files (9)
│   ├── AGENTS.md
│   ├── BOOTSTRAP.md
│   ├── HEARTBEAT.md
│   ├── IDENTITY.md
│   ├── MEMORY.md
│   ├── README.md (updated)
│   ├── SOUL.md
│   ├── TOOLS.md
│   └── USER.md
│
├── Documentation (organized)
│   ├── docs/
│   │   ├── README.md
│   │   ├── projects.md
│   │   ├── scripts.md
│   │   └── api/
│   ├── memory/
│   │   ├── YYYY-MM-DD.md (daily logs)
│   │   └── heartbeat-state.json
│   └── *.md (analysis docs, contracts)
│
├── Skills (22 - quality controlled)
│   └── skills/
│       ├── index.md (skill catalog)
│       ├── adspirer-ads-agent/
│       ├── agent-browser/
│       ├── code-security-auditor/
│       ├── contract-reviewer/
│       ├── find-skills/
│       ├── github/
│       ├── glm-4.6v-test/
│       ├── notion/
│       ├── obsidian/
│       ├── page-agent/
│       ├── session-monitor/
│       ├── stock-monitor-skill/
│       ├── summarize/
│       ├── tavily-search/
│       ├── tdd-ecc/
│       ├── test-effort-estimator/
│       └── weather/
│
├── Active Projects (3)
│   ├── ad-platform/
│   ├── page-agent/
│   └── permissions-system/
│
├── Scripts (organized)
│   └── scripts/
│       ├── automation/
│       │   ├── README.md
│       │   ├── enhanced_login.py
│       │   ├── enhanced_website_login.py
│       │   ├── fixed_web_automation.py
│       │   ├── website_login.py
│       │   ├── google_captcha_solver.py
│       │   ├── web_data_collector.py
│       │   └── web_search_integration.py
│       ├── analysis/
│       │   ├── README.md
│       │   ├── stock_analyzer.py
│       │   ├── stock_cli.py
│       │   └── baidu_news_search.py
│       ├── integration/
│       │   ├── README.md
│       │   ├── echo2_swarm.py
│       │   ├── multi_user_permission.py
│       │   ├── openclaw_system.py
│       │   └── openclaw_memory_integration.py
│       └── utils/
│           ├── README.md
│           ├── simple_openclaw.py
│           ├── test_integration.py
│           ├── test-memory-service.py
│           ├── web_search_demo.py
│           └── web_search_test.py
│
└── Archives
    ├── archived/
    │   ├── deprecated/
    │   │   ├── oceanengine-ads/
    │   │   ├── stocks_analysis/
    │   │   └── LemClaw/
    │   └── backups/
    │       └── ad-platform-backup-20260302-160134.tar.gz
    ├── openclaw-permission-config/
    ├── openclaw-permission-manager/
    └── superclaw.backup/
```

## Execution Order

1. **Phase 1: Archive & Cleanup** (15 min)
2. **Phase 2: Reorganize Skills** (20 min)
3. **Phase 3: Organize Python Scripts** (25 min)
4. **Phase 4: Improve Documentation** (15 min)
5. **Phase 5: Git Management** (10 min)

**Total Estimated Time**: 85 minutes

## Success Criteria

✅ All files properly categorized and organized
✅ No duplicate or empty directories
✅ Comprehensive documentation for all projects and scripts
✅ Git repository clean and properly managed
✅ .gitignore properly configured
✅ All broken references fixed
