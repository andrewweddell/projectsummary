# Stakeholder Register & RACI Matrix
## Global Underwriting Appsure Implementation

### Stakeholder Register

| Name/Role | Organization | Role in Project | Interest/Influence | Contact Method | Key Concerns |
|-----------|--------------|-----------------|-------------------|----------------|--------------|
| **Kim Brew** | Global Underwriting | Project Sponsor | High/High | Email, Phone | Delivery timeline, system capabilities |
| **Managing Principal** | Global Underwriting | Executive Sponsor | High/High | Monthly briefing | ROI, business continuity |
| **Mark Hutson** | Appsure | CEO/Managing Director | High/Medium | Escalation only | Contract delivery, client satisfaction |
| **[PM Name]** | Appsure | Project Manager | High/High | Daily | On-time delivery, resource management |
| **System Owner** | Global Underwriting | Business Lead | High/High | Daily | Requirements, UAT sign-off |
| **Underwriters Team** | Global Underwriting | End Users | High/Medium | Weekly updates | System usability, training |
| **Finance Team** | Global Underwriting | End Users | High/Medium | Weekly updates | Financial accuracy, reporting |
| **IT Team** | Global Underwriting | Technical Support | Medium/High | As needed | Integration, security |
| **Brokers** | External | End Users | Medium/Low | Portal updates | Ease of use, system availability |
| **Technical BA** | Appsure | Implementation Lead | High/High | Daily | Configuration accuracy |
| **Solution Architect** | Appsure | Technical Lead | High/High | Daily | Architecture, performance |
| **Developers** | Appsure | Technical Team | Medium/High | Daily | Code quality, timelines |

### RACI Matrix

**R** = Responsible (Does the work)  
**A** = Accountable (Final approval)  
**C** = Consulted (Provides input)  
**I** = Informed (Kept updated)

| Activity | GU Sponsor | GU System Owner | GU Underwriters | GU Finance | GU IT | Appsure PM | Appsure BA | Appsure Dev | Appsure Architect |
|----------|------------|-----------------|-----------------|------------|-------|------------|------------|-------------|-------------------|
| **Project Initiation** |
| Project Charter | A | C | I | I | I | R | C | I | C |
| Kick-off Meeting | A | R | C | C | C | R | C | C | C |
| Project Plan | A | C | I | I | I | R | C | C | C |
| **Requirements Phase** |
| Business Requirements | A | R | C | C | I | C | R | I | I |
| Product Specifications | I | A | R | C | I | C | R | I | I |
| Technical Design | I | C | I | I | C | A | R | C | R |
| Integration Design | I | C | I | C | R | A | R | C | R |
| **Configuration Phase** |
| Platform Setup | I | I | I | I | C | A | C | R | R |
| Product Configuration | I | A | C | I | I | C | R | C | C |
| Rating Engine | I | A | R | I | I | C | R | R | C |
| Document Templates | I | A | R | C | I | C | R | C | I |
| **Integration Phase** |
| Back-office Integration | I | C | I | R | C | A | R | R | C |
| Bank Import Setup | I | C | I | R | C | A | R | R | C |
| Reporting Setup | I | A | C | R | I | C | R | R | I |
| **Testing Phase** |
| Unit Testing | I | I | I | I | I | A | R | R | C |
| Integration Testing | I | C | I | C | C | A | R | R | C |
| UAT Test Cases | I | A | R | R | I | C | C | I | I |
| UAT Execution | I | A | R | R | C | I | C | I | I |
| Defect Resolution | I | C | C | C | I | A | R | R | C |
| **Training Phase** |
| Training Materials | I | A | C | C | I | C | R | I | I |
| Underwriter Training | I | C | R | I | I | I | R | I | I |
| Finance Training | I | C | I | R | I | I | R | I | I |
| Broker Training | I | A | C | I | I | C | R | I | I |
| **Go-Live Phase** |
| Go-Live Decision | A | R | C | C | C | R | C | C | C |
| Production Deployment | I | I | I | I | C | A | C | R | R |
| Cutover Activities | A | R | C | C | C | R | C | C | C |
| Go-Live Support | I | C | C | C | C | A | R | R | R |
| **Post Go-Live** |
| Hypercare Support | I | C | C | C | C | A | R | R | C |
| Performance Monitoring | I | I | I | I | C | C | C | C | R |
| Post-Implementation Review | A | R | C | C | C | R | C | I | C |
| Handover to BAU | A | R | C | C | R | R | C | I | C |

### Stakeholder Engagement Plan

#### High Power, High Interest (Manage Closely)
- **Kim Brew & System Owner**
  - Daily communication during sprints
  - Weekly status reports
  - Immediate escalation of risks/issues
  - Involvement in all key decisions

#### High Power, Low Interest (Keep Satisfied)
- **Managing Principal**
  - Monthly executive briefings
  - Highlight reports on milestones
  - Focus on business benefits and ROI

#### Low Power, High Interest (Keep Informed)
- **Underwriters & Finance Teams**
  - Weekly project updates
  - Regular training sessions
  - UAT participation
  - Feedback mechanisms

#### Low Power, Low Interest (Monitor)
- **Brokers**
  - Portal availability updates
  - Training announcements
  - Go-live communications

### Communication Protocols

1. **Escalation Path:**
   - Level 1: Project Managers (both sides)
   - Level 2: System Owner / Appsure BA Lead
   - Level 3: Kim Brew / Appsure PM Director
   - Level 4: Managing Principal / Mark Hutson

2. **Meeting Cadence:**
   - Daily stand-ups (Project team)
   - Weekly status meetings (Stakeholders)
   - Fortnightly steering committee
   - Monthly executive briefing

3. **Reporting:**
   - Weekly status reports (Email)
   - Risk and issue logs (Jira)
   - Sprint burndown charts (Jira)
   - Milestone reports (Confluence)

### Stakeholder Success Criteria

| Stakeholder | Success Criteria |
|-------------|------------------|
| Kim Brew | On-time delivery, within budget, meets requirements |
| System Owner | Smooth transition, minimal business disruption |
| Underwriters | Easy to use system, faster processing |
| Finance Team | Accurate financial processing, comprehensive reporting |
| IT Team | Stable system, secure, maintainable |
| Brokers | Intuitive portal, quick quote turnaround |
| Appsure PM | Successful delivery, client satisfaction |

### Change Impact Assessment

| Stakeholder Group | Current State | Future State | Change Impact | Support Needed |
|-------------------|---------------|--------------|---------------|----------------|
| Underwriters | Manual JAVLN process | Automated Appsure | High | Extensive training, change champions |
| Finance | Manual reconciliation | Automated allocation | Medium | Process training, documentation |
| Brokers | Email/phone quotes | Online portal | Medium | Portal training, user guides |
| IT | Limited integration | API-based integration | Low | Technical documentation |