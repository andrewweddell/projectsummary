# Information Gathering Templates
## Global Underwriting Appsure Implementation

### 1. Client Contact Information Template

| Role | Name | Email | Phone | Time Zone | Preferred Contact Method | Escalation Level |
|------|------|-------|-------|-----------|-------------------------|------------------|
| Project Sponsor | Kim Brew | | | AEST | | Level 3 |
| System Owner | [TBD] | | | | | Level 2 |
| Lead Underwriter | | | | | | Level 1 |
| Finance Lead | | | | | | Level 1 |
| IT Lead | | | | | | Level 1 |
| Compliance Officer | | | | | | Level 2 |
| Training Coordinator | | | | | | Level 1 |
| UAT Lead | | | | | | Level 1 |
| Broker Liaison | | | | | | Level 1 |

### 2. Current System & Process Assessment

#### 2.1 JAVLN System Details
| Aspect | Details | Notes |
|--------|---------|-------|
| Version | | |
| Number of Users | | |
| Data Volume (policies) | | |
| Average Daily Transactions | | |
| Key Pain Points | | |
| Retention Requirements | | |
| Decommission Timeline | | |

#### 2.2 Current Business Processes
| Process | Current State | Desired Future State | Priority |
|---------|---------------|---------------------|----------|
| Quote Generation | | | |
| Policy Issuance | | | |
| Endorsement Processing | | | |
| Renewal Management | | | |
| Cancellation Handling | | | |
| Billing & Invoicing | | | |
| Cash Allocation | | | |
| Commission Calculation | | | |
| Reporting | | | |
| Document Generation | | | |

### 3. Product Configuration Requirements


#### 3.1 General Liability Product (including Fire Coverage)
| Element | Requirement | Business Rules | Notes |
|---------|-------------|----------------|-------|
| Coverage Types | | | |
| Policy Limits | | | |
| Deductibles | | | |
| Rating Factors | | | |
| Occupancy Classes | | | |
| Fire Protection Elements | | | |
| Exclusions | | | |
| Document Templates | | | |

#### 3.2 Professional Indemnity Product
| Element | Requirement | Business Rules | Notes |
|---------|-------------|----------------|-------|
| Coverage Types | | | |
| Policy Limits | | | |
| Deductibles | | | |
| Professional Classes | | | |
| Rating Factors | | | |
| Retroactive Dates | | | |
| Claims Made Rules | | | |
| Document Templates | | | |

### 4. Integration Requirements Checklist

#### 4.1 System Integrations
| System | Purpose | Data Flow | Frequency | Format | Contact Person |
|--------|---------|-----------|-----------|--------|----------------|
| Back-office Financial | | Outbound | | | |
| Macquarie Bank | Bank statements | Inbound | Daily | | |
| Bordereaux System | Reporting | Outbound | Monthly | | |
| Email System | Notifications | Outbound | Real-time | | |
| Document Storage | Archive | Outbound | Real-time | | |
| Future: Sunrise | TBD | | | | |
| Future: SCTP | TBD | | | | |

#### 4.2 Data Elements for Integration
| Data Type | Source | Target | Transformation Required | Validation Rules |
|-----------|--------|--------|------------------------|------------------|
| Policy Data | | | | |
| Premium Info | | | | |
| Claims Data | | | | |
| Commission | | | | |
| Tax Data | | | | |
| Broker Info | | | | |

### 5. ~~Data Migration Assessment~~ [REMOVED - No Migration Required]

**Note:** Data migration has been excluded from scope. Existing policies will transition to Appsure at renewal.

### 6. Compliance & Security Requirements

| Requirement | Description | Current State | Required State | Owner |
|-------------|-------------|---------------|----------------|-------|
| APRA Compliance | | | | |
| Privacy Act | | | | |
| Data Retention | | | | |
| Audit Logging | | | | |
| Access Controls | | | | |
| Encryption | | | | |
| Backup Requirements | | | | |
| Disaster Recovery | | | | |

### 7. User Access & Training Needs

#### 7.1 User Groups
| User Group | Number of Users | Access Level | Training Needs | Training Format |
|------------|-----------------|--------------|----------------|-----------------|
| Underwriters | | Full | | |
| Finance Team | | Financial modules | | |
| Brokers | | Portal only | | |
| Management | | Read-only/Reports | | |
| IT Support | | Admin | | |
| Compliance | | Audit/Reports | | |

#### 7.2 Training Requirements
| Topic | Audience | Duration | Prerequisites | Materials Needed |
|-------|----------|----------|---------------|------------------|
| System Overview | All | | | |
| Quote & Bind | Underwriters | | | |
| Policy Admin | Underwriters | | | |
| Financial Processing | Finance | | | |
| Broker Portal | Brokers | | | |
| Reporting | Management | | | |
| System Admin | IT | | | |

### 8. Testing Scenarios Template

| Scenario ID | Description | Test Data Required | Expected Result | Actual Result | Pass/Fail |
|-------------|-------------|-------------------|-----------------|---------------|-----------|
| TS-001 | | | | | |
| TS-002 | | | | | |
| TS-003 | | | | | |

### 9. Go-Live Readiness Checklist

#### 9.1 Business Readiness
- [ ] All products configured and tested
- [ ] Business processes documented
- [ ] Users trained
- [ ] Broker communications sent
- [ ] Contingency plans in place
- [ ] Support structure defined

#### 9.2 Technical Readiness
- [ ] Production environment ready
- [ ] All integrations tested
- [ ] Data migration completed (if applicable)
- [ ] Performance testing passed
- [ ] Security audit completed
- [ ] Backup and recovery tested

#### 9.3 Operational Readiness
- [ ] Support team trained
- [ ] Escalation process defined
- [ ] Monitoring configured
- [ ] Documentation complete
- [ ] Change management process defined
- [ ] Hypercare plan approved

### 10. Key Performance Indicators (KPIs)

| KPI | Current Baseline | Target | Measurement Method | Frequency |
|-----|------------------|--------|-------------------|-----------|
| Quote Turnaround Time | | | | |
| Policy Issuance Time | | | | |
| Quote Conversion Rate | | | | |
| System Availability | | 99.5% | | |
| User Satisfaction | | >80% | | |
| Error Rate | | <2% | | |
| Cash Allocation Time | | | | |
| Report Generation Time | | | | |

### 11. ~~Syndicate Information~~ [REMOVED - Not Required]

**Note:** Syndicate logic has been excluded from scope.

### 12. Document Templates Required

| Document Type | Current Template Available | Modifications Needed | Approval Required From |
|---------------|---------------------------|---------------------|----------------------|
| Quote Letter | □ Yes □ No | | |
| Policy Schedule | □ Yes □ No | | |
| Policy Wording | □ Yes □ No | | |
| Invoice | □ Yes □ No | | |
| Renewal Notice | □ Yes □ No | | |
| Cancellation Notice | □ Yes □ No | | |
| Endorsement | □ Yes □ No | | |
| Certificate of Currency | □ Yes □ No | | |

### 13. Reporting Requirements

| Report Name | Purpose | Frequency | Recipients | Format | Data Elements |
|-------------|---------|-----------|------------|--------|---------------|
| Daily Production | | Daily | | | |
| Monthly Bordereaux | | Monthly | | | |
| Commission Statement | | Monthly | | | |
| Financial Summary | | Monthly | | | |
| Renewal Pipeline | | Weekly | | | |
| Claims Summary | | Monthly | | | |

### Information Collection Schedule

| Week | Information Required | From | To | Status |
|------|---------------------|------|-----|--------|
| Week 1 | Contact details, current state | GU Team | Appsure PM | |
| Week 1 | Product specifications | GU Underwriting | Appsure BA | |
| Week 2 | Integration requirements | GU IT | Appsure Architect | |
| Week 2 | Compliance requirements | GU Compliance | Appsure PM | |
| Week 3 | User access matrix | GU System Owner | Appsure BA | |
| Week 3 | Training needs | GU HR | Appsure PM | |
| Week 4 | Test scenarios | GU Underwriting | Appsure QA | |
| Week 5 | Training requirements finalized | GU HR | Appsure PM | |