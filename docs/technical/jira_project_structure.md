# Global Underwriting - Appsure Implementation
## Jira Project Structure

### EPIC: GLO-E1 - Foundation & Planning
**Epic Key:** GLO-E1
**Objective:** Establish project charter, infrastructure, and detailed planning
**Target:** Sprint 1 (Weeks 1-2)
**Story Count:** 25 stories (GLO-255 through GLO-279)
**Epic Description:** Set up project governance, Azure infrastructure, and complete business requirements analysis

### EPIC: GLO-E2 - Core Platform Configuration  
**Epic Key:** GLO-E2
**Objective:** Configure base Appsure instance and workflow engine
**Target:** Sprint 2 (Weeks 3-4) 
**Story Count:** 17 stories (GLO-280 through GLO-296)
**Epic Description:** Establish core Appsure platform with user roles, workflows, and billing processes

### EPIC: GLO-E3 - Product Implementation
**Epic Key:** GLO-E3
**Objective:** Implement GL/Fire and PI product configurations
**Target:** Sprint 3 (Weeks 5-6)
**Story Count:** 15 stories (GLO-297 through GLO-311)
**Epic Description:** Configure both GL/Fire and PI products with rating engines, broker portal, and workflows

### EPIC: GLO-E4 - Integration & Testing
**Epic Key:** GLO-E4
**Objective:** Complete system integrations and comprehensive testing
**Target:** Sprint 4 (Weeks 7-8)
**Story Count:** 15 stories (GLO-312 through GLO-326)
**Epic Description:** Implement back-office integrations, execute UAT, and complete all testing phases

### EPIC: GLO-E5 - Training & Go-Live  
**Epic Key:** GLO-E5
**Objective:** Deliver training and execute production deployment
**Target:** Sprint 5-6 (Weeks 9-12)
**Story Count:** 15 stories (GLO-327 through GLO-341)
**Epic Description:** Conduct user training, finalize production environment, and execute go-live

### EPIC: GLO-E6 - Compliance & Operations
**Epic Key:** GLO-E6
**Objective:** Ensure regulatory compliance and operational readiness  
**Target:** Throughout project
**Story Count:** 10 stories (GLO-342 through GLO-351)
**Epic Description:** Implement APRA compliance, security controls, and operational monitoring

---

## Sprint 1 - Foundation & Planning (Weeks 1-2)

### STORY: GLO-255 - Establish project charter and RACI matrix
**Description:** Define project scope, objectives, and responsibility matrix for all stakeholders
**Epic:** GLO-E1 (Foundation & Planning)
**Sprint:** 1
**Story Points:** 3
**Priority:** High

### STORY: GLO-256 - Set up project tracking in Jira
**Description:** Configure Jira project for tracking all Global Underwriting implementation work
**Epic:** GLO-E1 (Foundation & Planning)
**Sprint:** 1
**Story Points:** 2
**Priority:** High

### STORY: GLO-257 - Configure Confluence space
**Description:** Set up documentation space for project artifacts and knowledge sharing
**Epic:** GLO-E1 (Foundation & Planning)
**Sprint:** 1
**Story Points:** 2
**Priority:** Medium

### STORY: GLO-258 - Schedule kickoff meeting with stakeholders
**Description:** Organize and conduct project kickoff with all key stakeholders
**Epic:** GLO-E1 (Foundation & Planning)
**Sprint:** 1
**Story Points:** 1
**Priority:** High

### STORY: GLO-259 - Define communication plan and cadence
**Description:** Establish regular communication rhythm and reporting structure
**Epic:** GLO-E1 (Foundation & Planning)
**Sprint:** 1
**Story Points:** 2
**Priority:** Medium

### STORY: GLO-260 - Review and validate product specifications (GL including Fire, PI)
**Description:** Analyze current product specifications for General Liability (including Fire) and Professional Indemnity products

### STORY: GLO-261 - Document business operating processes
**Description:** Map and document current business processes for underwriting workflow

### STORY: GLO-262 - Confirm rating models and pricing logic
**Description:** Validate existing rating models and pricing algorithms for migration to Appsure

### STORY: GLO-263 - Review policy wordings and endorsements
**Description:** Audit current policy wordings and endorsements for compatibility

### STORY: GLO-264 - Validate quotation questions and lookup lists
**Description:** Review and confirm all quotation questions and reference data

### STORY: GLO-265 - Produce technical design for product configuration
**Description:** Create detailed technical specifications for Appsure product setup

### STORY: GLO-266 - Design system architecture and integrations
**Description:** Plan system architecture and integration points with existing systems

### STORY: GLO-267 - Document transition approach for existing policies
**Description:** Define strategy for migrating existing policies to new system

### STORY: GLO-268 - Design user roles and permissions structure
**Description:** Define user access levels and permission matrix for different roles

### STORY: GLO-269 - Define automated and manual testing approach
**Description:** Establish testing strategy including automated and manual test procedures

### STORY: GLO-270 - Document back-office system integration specs
**Description:** Define requirements for integrating with existing back-office systems

### STORY: GLO-271 - Design bank statement import process (Macquarie)
**Description:** Create specifications for automated bank statement processing

### STORY: GLO-272 - Define extract formats for financial systems
**Description:** Specify data formats for financial system integrations

### STORY: GLO-273 - Document bordereaux reporting requirements
**Description:** Define bordereaux reporting formats and frequencies

### STORY: GLO-274 - Confirm reporting requirements for GL product
**Description:** Validate all reporting requirements for General Liability product

### STORY: GLO-275 - Provision Azure Australia East infrastructure
**Description:** Set up Azure cloud infrastructure in Australia East region

### STORY: GLO-276 - Establish development/test environment
**Description:** Configure non-production environments for development and testing

### STORY: GLO-277 - Configure production environment
**Description:** Set up secure production environment with proper controls

### STORY: GLO-278 - Set up security and access controls
**Description:** Implement security measures and user access controls

### STORY: GLO-279 - Implement backup and disaster recovery
**Description:** Configure backup processes and disaster recovery procedures

---

## Sprint 2 - Core Configuration (Weeks 3-4)

### STORY: GLO-280 - Configure base Appsure instance
**Description:** Set up the core Appsure platform with basic configuration
**Epic:** GLO-E2 (Core Platform Configuration)
**Sprint:** 2
**Story Points:** 8
**Priority:** High

### STORY: GLO-281 - Set up user roles and permissions
**Description:** Configure user access levels and permission matrix for different roles

### STORY: GLO-282 - Configure workflow engine
**Description:** Set up workflow processes for underwriting and policy management

### STORY: GLO-283 - Set up document templates
**Description:** Configure policy documents and certificate templates

### STORY: GLO-284 - Configure communication templates
**Description:** Set up email and notification templates

### STORY: GLO-285 - Configure GL product structure with Fire coverage
**Description:** Set up General Liability product including Fire coverage options

### STORY: GLO-286 - Implement GL/Fire rating engine
**Description:** Configure rating algorithms and pricing logic for GL and Fire products

### STORY: GLO-287 - Set up GL/Fire quotation flow
**Description:** Configure quotation process and workflow for GL/Fire products

### STORY: GLO-288 - Configure GL/Fire policy documents
**Description:** Set up policy document generation for GL and Fire products

### STORY: GLO-289 - Set up GL/Fire endorsements
**Description:** Configure endorsement options and processing for GL/Fire products

### STORY: GLO-290 - Set up occupation-based rules
**Description:** Configure occupation-specific underwriting rules and pricing

### STORY: GLO-291 - Configure coverage limits
**Description:** Set up coverage limit options and validation rules

### STORY: GLO-292 - Configure billing processes
**Description:** Set up invoicing, payment processing, and billing workflows

### STORY: GLO-293 - Set up stamp duty calculations
**Description:** Configure stamp duty calculations for different states/territories

### STORY: GLO-294 - Configure withholding tax
**Description:** Set up withholding tax calculations and processing

### STORY: GLO-295 - Implement cash allocation rules
**Description:** Configure automatic cash allocation and reconciliation processes

### STORY: GLO-296 - Set up debtor management
**Description:** Configure overdue payment tracking and collection processes

---

## Sprint 3 - Product Implementation (Weeks 5-6)

### STORY: GLO-297 - Configure PI product structure
**Description:** Set up Professional Indemnity product structure and configuration in Appsure

### STORY: GLO-298 - Implement PI rating engine
**Description:** Configure rating algorithms and pricing logic for Professional Indemnity product

### STORY: GLO-299 - Set up PI quotation flow
**Description:** Configure quotation process and workflow for Professional Indemnity product

### STORY: GLO-300 - Configure PI policy documents
**Description:** Set up policy document generation for Professional Indemnity product

### STORY: GLO-301 - Set up PI endorsements
**Description:** Configure endorsement options and processing for Professional Indemnity product

### STORY: GLO-302 - Configure broker portal access
**Description:** Set up broker portal access controls and authentication

### STORY: GLO-303 - Set up broker user management
**Description:** Configure broker user accounts and role-based access controls

### STORY: GLO-304 - Implement quote and apply workflows
**Description:** Configure broker portal quotation and application workflows

### STORY: GLO-305 - Configure broker commission structures
**Description:** Set up commission calculation and payment structures for brokers

### STORY: GLO-306 - Set up broker reporting
**Description:** Configure reporting capabilities for broker portal users

### STORY: GLO-307 - Configure document templates for both products
**Description:** Set up document templates for GL/Fire and PI products

### STORY: GLO-308 - Set up automated workflows
**Description:** Configure automated business process workflows in Appsure

### STORY: GLO-309 - Configure referral rules
**Description:** Set up automated referral rules and escalation processes

### STORY: GLO-310 - Set up approval hierarchies
**Description:** Configure approval workflows and authorization levels

### STORY: GLO-311 - Configure notification settings
**Description:** Set up automated notification and alert systems

---

## Sprint 4 - Integration & Testing (Weeks 7-8)

### STORY: GLO-312 - Implement back-office system extracts
**Description:** Develop and configure data extracts for back-office system integration

### STORY: GLO-313 - Configure bank statement import
**Description:** Set up automated bank statement import process from Macquarie

### STORY: GLO-314 - Set up management reporting (KPIs)
**Description:** Configure management dashboards and KPI reporting

### STORY: GLO-315 - Implement bordereaux reporting
**Description:** Set up bordereaux reporting for reinsurance requirements

### STORY: GLO-316 - Test all integration points
**Description:** Conduct comprehensive testing of all system integrations

### STORY: GLO-317 - Execute unit tests for all products
**Description:** Perform unit testing for GL/Fire and PI product configurations

### STORY: GLO-318 - Perform integration testing
**Description:** Execute end-to-end integration testing across all systems

### STORY: GLO-319 - Conduct workflow testing
**Description:** Test all configured business process workflows

### STORY: GLO-320 - Test document generation
**Description:** Validate policy document and certificate generation

### STORY: GLO-321 - Validate financial calculations
**Description:** Test rating engines, billing, and financial processes

### STORY: GLO-322 - Prepare UAT scenarios
**Description:** Develop comprehensive user acceptance test scenarios

### STORY: GLO-323 - Train UAT participants
**Description:** Conduct training sessions for UAT team members

### STORY: GLO-324 - Execute UAT test cases
**Description:** Run user acceptance testing with business stakeholders

### STORY: GLO-325 - Track and resolve defects
**Description:** Manage defect resolution process during UAT

### STORY: GLO-326 - Obtain UAT sign-off
**Description:** Secure formal UAT approval from business stakeholders

---

## Sprint 5-6 - Training & Go-Live (Weeks 9-12) *If Required*

### STORY: GLO-327 - Develop training materials
**Description:** Create comprehensive training materials for all user groups

### STORY: GLO-328 - Conduct underwriter training
**Description:** Train underwriting staff on Appsure system functionality

### STORY: GLO-329 - Train finance team
**Description:** Provide training to finance team on billing and reporting features

### STORY: GLO-330 - Train broker support team
**Description:** Train broker support staff on portal functionality and troubleshooting

### STORY: GLO-331 - Create user documentation
**Description:** Develop user guides and system documentation

### STORY: GLO-332 - Finalize production environment
**Description:** Complete production environment setup and validation

### STORY: GLO-333 - Complete security audit
**Description:** Conduct final security assessment and remediate findings

### STORY: GLO-334 - Perform final smoke testing
**Description:** Execute final system validation before go-live

### STORY: GLO-335 - Create go-live runsheet
**Description:** Develop detailed go-live execution plan and runsheet

### STORY: GLO-336 - Implement cutover plan
**Description:** Execute system cutover and data migration processes

### STORY: GLO-337 - Monitor system performance
**Description:** Continuously monitor system performance post go-live

### STORY: GLO-338 - Provide hypercare support
**Description:** Deliver intensive support during initial production period

### STORY: GLO-339 - Address production issues
**Description:** Resolve any production issues and system defects

### STORY: GLO-340 - Conduct post-implementation review
**Description:** Perform project retrospective and lessons learned session

### STORY: GLO-341 - Transition to BAU support
**Description:** Handover system to business-as-usual support team

---

## Non-Functional Requirements (NFRs)

### STORY: GLO-342 - Ensure APRA compliance
**Description:** Implement and validate APRA compliance requirements

### STORY: GLO-343 - Implement data privacy controls
**Description:** Configure data privacy and protection controls

### STORY: GLO-344 - Configure audit logging
**Description:** Set up comprehensive audit trail and logging

### STORY: GLO-345 - Set up security monitoring
**Description:** Implement security monitoring and threat detection

### STORY: GLO-346 - Document compliance measures
**Description:** Create compliance documentation and evidence

### STORY: GLO-347 - Configure performance monitoring
**Description:** Set up system performance monitoring and dashboards

### STORY: GLO-348 - Set up alerting thresholds
**Description:** Configure automated alerts for system issues

### STORY: GLO-349 - Implement disaster recovery
**Description:** Set up disaster recovery and business continuity processes

### STORY: GLO-350 - Test failover procedures
**Description:** Validate disaster recovery and failover procedures

### STORY: GLO-351 - Document SLAs
**Description:** Create service level agreements and operational documentation

---

## Definition of Done
- [ ] Code/configuration completed and peer reviewed
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Documentation updated
- [ ] Security requirements met
- [ ] Performance criteria satisfied
- [ ] UAT sign-off obtained
- [ ] Deployed to production

---

## Ticket Summary

**Total Tickets:** 103
- **Epics:** 6 (GLO-E1 through GLO-E6)
- **Stories:** 97 (GLO-255 through GLO-351)
- **Tasks:** 0 (eliminated - all converted to stories)

**Epic Distribution:**
- GLO-E1 (Foundation & Planning): 25 stories (GLO-255 to GLO-279)
- GLO-E2 (Core Platform Configuration): 17 stories (GLO-280 to GLO-296)
- GLO-E3 (Product Implementation): 15 stories (GLO-297 to GLO-311)
- GLO-E4 (Integration & Testing): 15 stories (GLO-312 to GLO-326)
- GLO-E5 (Training & Go-Live): 15 stories (GLO-327 to GLO-341)
- GLO-E6 (Compliance & Operations): 10 stories (GLO-342 to GLO-351)

**Sprint Distribution:**
- Sprint 1: 25 stories (GLO-255 to GLO-279) → Epic GLO-E1
- Sprint 2: 17 stories (GLO-280 to GLO-296) → Epic GLO-E2  
- Sprint 3: 15 stories (GLO-297 to GLO-311) → Epic GLO-E3
- Sprint 4: 15 stories (GLO-312 to GLO-326) → Epic GLO-E4
- Sprint 5-6: 15 stories (GLO-327 to GLO-341) → Epic GLO-E5
- Cross-cutting: 10 stories (GLO-342 to GLO-351) → Epic GLO-E6

**Note:** Ticket numbering now starts from GLO-255 to align with Jira project sequence