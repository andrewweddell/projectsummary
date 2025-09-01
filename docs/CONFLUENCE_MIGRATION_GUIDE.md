# Confluence Migration Guide - Global Underwriting Project

## 📋 Migration Overview

This guide provides step-by-step instructions for migrating project documentation from the local repository to Confluence, following the recommended space structure.

## 🎯 Confluence Space Setup

### Space Configuration
- **Space Key:** `GUAIP` (Global Underwriting Appsure Implementation Project)
- **Space Name:** Global Underwriting Appsure Implementation
- **Template:** Project management template with custom macros
- **Permissions:** Restricted to project team and stakeholders

## 📁 Confluence Space Structure

```
🏠 Global Underwriting Appsure Implementation
├── 📋 Project Overview
├── 📅 Planning & Timeline
├── 👥 Stakeholder Management
├── ⚠️ Risk & Issue Management
├── 📊 Status & Reporting
├── 📋 Requirements & Design
├── 🧪 Testing & Quality
├── 🎓 Training & Change Management
├── 📚 Document Library
└── ⚙️ Project Tools & Process
```

## 🚀 High Priority Files for Migration

### Phase 1 - Foundation Pages (Week 1)

| **Local File** | **Confluence Location** | **Status** | **Notes** |
|---|---|---|---|
| `docs/business/confluence_project_overview.md` | `📋 Project Overview` | 🔴 Pending | Executive summary, business objectives |
| `docs/project_management/implementation_timeline.md` | `📅 Planning & Timeline → Implementation Timeline` | 🔴 Pending | Sprint timeline and milestones |
| `docs/project_management/stakeholder_register_raci.md` | `👥 Stakeholder Management → Stakeholder Register` | 🔴 Pending | RACI matrix and contacts |
| `docs/project_management/risk_register_dependencies.md` | `⚠️ Risk & Issue Management → Risk Register` | 🔴 Pending | Risk framework and dependencies |

### Phase 2 - Content Migration (Week 2)

| **Local File** | **Confluence Location** | **Status** | **Notes** |
|---|---|---|---|
| `docs/templates/information_gathering_templates.md` | `📋 Requirements & Design → Templates` | 🔴 Pending | Requirements collection templates |
| `tools/jira_app/project_status_report_latest.md` | `📊 Status & Reporting → Project Dashboard` | 🔴 Pending | Live project status (103 tickets) |
| `docs/technical/jira_project_structure.md` | `⚙️ Project Tools & Process → Jira Setup Guide` | 🔴 Pending | Complete Jira configuration |
| `docs/business/contracts/` | `📚 Document Library → Contracts` | 🔴 Pending | Reference only, upload PDFs |

## 📝 Migration Steps

### Step 1: Create Confluence Space
1. Create new space with key `GUAIP`
2. Set up permissions for project team
3. Configure project management template
4. Create main page structure (see structure above)

### Step 2: Migrate Foundation Content
1. **Project Overview Page**
   - Copy content from `docs/business/confluence_project_overview.md`
   - Add executive summary section
   - Include project scope and objectives
   - Add success criteria and KPIs

2. **Implementation Timeline Page**
   - Copy content from `docs/project_management/implementation_timeline.md`
   - Add timeline macro for visual representation
   - Include sprint planning details
   - Link to Jira milestones

3. **Stakeholder Register Page**
   - Copy content from `docs/project_management/stakeholder_register_raci.md`
   - Format RACI matrix as Confluence table
   - Add contact information
   - Include communication preferences

4. **Risk Register Page**
   - Copy content from `docs/project_management/risk_register_dependencies.md`
   - Create risk tracking table with status
   - Add dependency visualization
   - Include mitigation strategies

### Step 3: Set Up Live Reporting
1. **Project Dashboard**
   - Create automated status page
   - Link to `tools/jira_app/project_status_report_latest.md`
   - Add Jira macros for live ticket status
   - Include project health indicators

2. **Jira Integration**
   - Install Jira macro for Confluence
   - Configure live ticket displays
   - Set up automated updates
   - Test synchronization

### Step 4: Content Organization
1. **Templates Section**
   - Copy `docs/templates/information_gathering_templates.md`
   - Create form templates in Confluence
   - Add collection workflows
   - Include approval processes

2. **Document Library**
   - Upload contract PDFs as attachments
   - Create reference links
   - Set up version control
   - Add metadata and tags

## 🔧 Confluence Configuration

### Page Templates
Create custom page templates for:
- Status reports
- Meeting notes  
- Requirements documentation
- Risk assessments
- Timeline updates

### Macros to Enable
- **Jira Issues Macro** - Live ticket integration
- **Timeline Macro** - Project milestones
- **Status Macro** - Visual project health
- **Table of Contents** - Navigation
- **Calendar Macro** - Event tracking

### Automation Rules
Set up automation for:
- Daily status updates from Jira
- Weekly project reports
- Risk register notifications
- Timeline milestone alerts

## ✅ Migration Checklist

### Pre-Migration Setup
- [ ] Create Confluence space with correct permissions
- [ ] Install required macros and apps
- [ ] Set up page templates
- [ ] Configure Jira integration

### Content Migration Phase 1
- [ ] Project Overview page created
- [ ] Timeline page migrated with visual timeline
- [ ] Stakeholder register formatted as tables
- [ ] Risk register with tracking status
- [ ] Live reporting dashboard configured

### Content Migration Phase 2
- [ ] Requirements templates migrated
- [ ] Document library set up
- [ ] Jira integration guide created
- [ ] Automation rules configured
- [ ] User training materials added

### Post-Migration Validation
- [ ] All links working correctly
- [ ] Jira macros displaying live data
- [ ] Permissions set correctly for all stakeholders
- [ ] Search functionality working
- [ ] Mobile accessibility verified

## 🚫 Files to Keep Local Only

**Operational Files (Do NOT migrate):**
- `docs/technical/jira_sync_workflow.md` - Critical operational procedures
- `tools/jira_app/` - All technical implementation files
- `tools/jira_app/README.md` - Technical documentation
- `tools/jira_app/config.example.json` - Configuration files
- Development and testing artifacts

## 🔄 Ongoing Maintenance

### Daily
- Automated Jira status updates
- Live project dashboard refresh

### Weekly  
- Status report generation
- Risk register review
- Timeline milestone updates

### Monthly
- Content review and cleanup
- User access audit
- Template updates as needed

## 📞 Support

For Confluence migration support:
- Technical setup: See `tools/jira_app/README.md`
- Content questions: Review local documentation first
- Access issues: Contact project administrator
- Training needs: Schedule team training session

---

**Migration Timeline:** 3 weeks total
**Priority:** High - Critical for stakeholder communication
**Dependencies:** Confluence space creation, Jira integration setup
**Success Criteria:** All high-priority content accessible in Confluence with live Jira integration