# Global Underwriting Appsure Implementation
## Confluence Project Space

### Project Overview

**Client:** Global Underwriting  
**Project Name:** Appsure Platform Implementation  
**Project Manager:** [To be assigned]  
**Start Date:** 25 August 2025  
**Target Go-Live:** October/November 2025  
**Project Duration:** 2-3 months (4-6 sprints)

### Executive Summary

Global Underwriting is implementing the Appsure platform to replace their existing JAVLN-based manual processes for General Liability (including Fire) and Professional Indemnity (PI) products. This implementation will provide:

- Automated quote and policy generation
- Streamlined broker portal
- Integrated billing and financial management
- Flexible rating and underwriting capabilities
- Comprehensive reporting and analytics

### Business Objectives

1. **Replace Manual Processes:** Eliminate JAVLN-based manual workflows
2. **Improve Efficiency:** Automate quote-to-policy lifecycle
3. **Enable Growth:** Provide scalable platform for future products
4. **Enhance Broker Experience:** Deploy modern online broker portal
5. **Ensure Compliance:** Meet Australian regulatory requirements

### Scope of Work

#### In Scope
- General Liability (GL including Fire coverage) product configuration
- Professional Indemnity (PI) product setup
- Broker portal implementation
- Billing and financial management
- Bank statement import (Macquarie)
- Management reporting and KPIs
- Bordereaux reporting

#### Out of Scope
- Data migration (policies will transition at renewal)
- Integration with Sunrise system
- Integration with SCTP
- Additional products beyond Fire, GL, and PI
- Credit card payment processing (TBC)

### Key Deliverables

1. **Configured Appsure Platform**
   - Stand-alone instance in Azure Australia East
   - Development/Test and Production environments
   - ISO 27001:2022 compliant setup

2. **Product Configurations**
   - General Liability (including Fire) with rating engine
   - Professional Indemnity with underwriting rules

3. **Broker Portal**
   - Online quote and apply functionality
   - Broker user management
   - Commission tracking

4. **Financial Management**
   - Billing processes
   - Stamp duty and withholding tax
   - Cash allocation
   - Bank statement import

5. **Reporting**
   - Management KPI dashboards
   - Bordereaux reports
   - Financial extracts

### Technical Architecture

#### Infrastructure
- **Hosting:** Microsoft Azure Australia East
- **Environment:** Dual environment (Dev/Test + Production)
- **Security:** ISO 27001:2022 certified platform
- **Backup:** Automated daily backups with disaster recovery

#### Integration Points
- Back-office financial systems (Extract)
- Macquarie Bank (Statement import)
- Bordereaux reporting system
- Future: Sunrise and SCTP (separate project)

### Project Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Sprint 1 | Weeks 1-2 | Project setup, requirements analysis, technical design |
| Sprint 2 | Weeks 3-4 | Platform configuration, product implementation |
| Sprint 3 | Weeks 5-6 | Product configuration, integration development |
| Sprint 4 | Weeks 7-8 | System integration, testing, UAT |
| Sprint 5-6 | Weeks 9-12 | Training, go-live preparation, deployment |


### Key Assumptions

1. Product specifications completed and signed off before configuration
2. Business processes and rules defined upfront
3. Initial products are Fire Protection, GL, and PI
4. KPIs aligned with industry standards
5. Global Underwriting manages regulatory compliance
6. Appsure provides disaster recovery plan
7. Banking interface with Macquarie confirmed
8. No Sunrise/SCTP integration in initial phase

### Dependencies

1. **From Global Underwriting:**
   - Completed product specifications
   - Policy wordings and endorsements
   - Rating models and rules
   - Business process documentation
   - UAT resources availability
   - Integration specifications

2. **From Appsure:**
   - Platform provisioning
   - Technical resources
   - Azure infrastructure
   - Support documentation

### Critical Success Factors

1. Clear and complete requirements documentation
2. Active stakeholder engagement
3. Timely decision making
4. Adequate testing coverage
5. Effective change management
6. Comprehensive training program
7. Smooth data migration (if applicable)
8. Post go-live support readiness

### Communication Plan

| Audience | Frequency | Method | Content |
|----------|-----------|--------|---------|
| Steering Committee | Monthly | Meeting | Status, risks, decisions |
| Project Team | Daily | Stand-up | Progress, blockers |
| Stakeholders | Weekly | Email | Status report |
| End Users | As needed | Training | System updates |

### Change Management Process

1. Change request submitted via Jira
2. Impact assessment by project team
3. Cost and timeline evaluation
4. Steering committee approval for major changes
5. Update project documentation
6. Communicate to stakeholders

### Quality Assurance

- Unit testing by Appsure team
- System integration testing
- User acceptance testing by Global Underwriting
- Performance testing
- Security testing
- Production verification testing

### Training Plan

| Audience | Topics | Duration | Method |
|----------|--------|----------|--------|
| Underwriters | Product configuration, rating, quotation | 2 days | Hands-on |
| Finance Team | Billing, cash allocation, reporting | 1 day | Workshop |
| Brokers | Portal usage, quote and apply | Half day | Webinar |
| IT Support | System administration, troubleshooting | 1 day | Technical |

### Post-Implementation Support

- **Hypercare Period:** 4 weeks post go-live
- **Support Model:** Dedicated FTE for first 3-6 months
- **SLA:** Business hours support with escalation path
- **Transition:** Gradual handover to BAU support team

### Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | August 2025 | PM | Initial draft |

### Related Documents

- Client Agreement (Appsure GlobalUnderwriting Jun2025-FireGL-PLv3.pdf)
- Technical Design Document
- Test Plan
- Training Materials
- User Guides