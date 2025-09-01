# Global Underwriting Appsure Implementation Project

## 🏗️ Project Overview
This repository contains all documentation, tools, and resources for the Global Underwriting Appsure implementation project. The project involves comprehensive system integration with Jira-based project management and automated reporting.

## 📁 Repository Structure

```
/globalunderwriting/
├── docs/                           # Project documentation
│   ├── business/                   # Business documentation
│   │   ├── contracts/             # Legal agreements and contracts
│   │   └── confluence_project_overview.md  # Executive project summary
│   ├── project_management/        # Project management artifacts
│   │   ├── implementation_timeline.md      # Sprint timeline and milestones
│   │   ├── project_summary.md             # Master project index
│   │   ├── PROJECT_STRUCTURE_RATIONALE.md # Project approach justification
│   │   ├── risk_register_dependencies.md  # Risk management framework
│   │   └── stakeholder_register_raci.md   # Stakeholder management and RACI
│   ├── technical/                 # Technical documentation
│   │   ├── EPIC_IMPLEMENTATION_SUMMARY.md # Epic structure overview
│   │   ├── jira_project_structure.md      # Complete Jira setup guide
│   │   └── jira_sync_workflow.md          # Critical workflow procedures
│   └── templates/                 # Templates and standards
│       └── information_gathering_templates.md  # Requirements collection
├── tools/                         # Development tools and utilities
│   └── jira_app/                 # Jira integration application
│       ├── app.py                # Main Flask application
│       ├── README.md             # Jira app documentation
│       ├── config.example.json   # Configuration template
│       ├── requirements.txt      # Python dependencies
│       └── project_status_report_latest.md  # Live project status (103 tickets)
└── README.md                     # This file
```

## 🎯 Key Project Components

### Project Management (103 Jira Tickets)
- **Total Epics:** 7
- **Total Stories:** 95
- **Live Status Tracking:** `tools/jira_app/project_status_report_latest.md`

### Documentation Categories
1. **Business Documentation** - Executive summaries, contracts, requirements
2. **Project Management** - Timelines, stakeholders, risks, processes
3. **Technical Documentation** - Jira structure, workflows, implementation guides
4. **Templates** - Standardized forms and collection templates

### Integration Tools
- **Jira Integration App** - Python Flask application for project synchronization
- **Automated Reporting** - Live status updates and project tracking
- **Configuration Management** - Environment setup and deployment tools

## 🚀 Quick Start

### Jira Application
```bash
cd tools/jira_app/
pip install -r requirements.txt
cp config.example.json config.json
# Configure your settings in config.json
python app.py
```

### Project Status
- Current status: **Active Development**
- Last updated: **2025-08-25**
- View live status: `tools/jira_app/project_status_report_latest.md`

## 📋 Documentation Migration

### Priority Files for Confluence Migration:
1. `docs/business/confluence_project_overview.md` → Project Overview
2. `docs/project_management/implementation_timeline.md` → Timeline & Milestones
3. `docs/project_management/stakeholder_register_raci.md` → Stakeholder Management
4. `docs/project_management/risk_register_dependencies.md` → Risk Register
5. `docs/templates/information_gathering_templates.md` → Requirements Templates

### Keep Local (Operational):
- `docs/technical/jira_sync_workflow.md` - Critical operational procedures
- `tools/jira_app/` - All technical implementation files
- `tools/jira_app/project_status_report_latest.md` - Auto-generated status reports

## 🔧 Maintenance

- **Jira Sync:** Automated via `tools/jira_app/`
- **Status Reports:** Auto-generated and updated in real-time
- **Documentation:** Keep Confluence and local docs synchronized

## 📞 Support & Contact

For questions about this project structure or documentation:
- Review project summary: `docs/project_management/project_summary.md`
- Check stakeholder contacts: `docs/project_management/stakeholder_register_raci.md`
- Technical issues: See `tools/jira_app/README.md`