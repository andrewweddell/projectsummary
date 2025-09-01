# Risk Register, Dependencies & Assumptions
## Global Underwriting Appsure Implementation

### Risk Register

| Risk ID | Risk Description | Category | Probability | Impact | Risk Score | Mitigation Strategy | Owner | Status |
|---------|------------------|----------|-------------|--------|------------|-------------------|-------|--------|
| **R001** | Product specifications incomplete or change during implementation | Scope | High | High | 16 | Lock down requirements in Sprint 1, formal change control process | GU System Owner | Open |
| **R003** | UAT resources unavailable during testing window | Resource | Medium | High | 12 | Early scheduling, backup testers identified | GU System Owner | Open |
| **R004** | Integration with back-office systems delayed | Technical | Medium | Medium | 9 | Early integration specs, parallel development tracks | Appsure Architect | Open |
| **R006** | Azure infrastructure provisioning delays | Technical | Low | High | 8 | Early infrastructure request, backup plan | Appsure Architect | Open |
| **R007** | Change resistance from underwriters | People | Medium | Medium | 9 | Change champions, comprehensive training | GU System Owner | Open |
| **R008** | Regulatory compliance requirements change | Compliance | Low | High | 8 | Regular compliance reviews, flexible configuration | GU Compliance | Open |
| **R009** | Performance issues with rating engine | Technical | Low | Medium | 6 | Performance testing, optimization sprints | Appsure Dev | Open |
| **R010** | Bank statement import format changes | External | Low | Medium | 6 | Flexible import configuration, Macquarie engagement | Appsure BA | Open |
| **R005** | Broker adoption lower than expected | Business | Medium | Low | 6 | Broker engagement plan, intuitive UX design | GU System Owner | Open |
| **R012** | Project timeline aggressive (2-3 months) | Schedule | High | High | 16 | Parallel workstreams, additional resources if needed | Appsure PM | Open |
| **R013** | Key project resources leave during implementation | Resource | Low | High | 8 | Knowledge transfer, backup resources identified | Both PMs | Open |
| **R014** | Production go-live issues | Technical | Medium | High | 12 | Comprehensive testing, rollback plan, hypercare support | Appsure Team | Open |

**Risk Scoring Matrix:**
- Probability: Low (1), Medium (3), High (5)
- Impact: Low (1), Medium (3), High (5)
- Risk Score = Probability × Impact

### Dependencies Register

| Dep ID | Dependency Description | Type | Provider | Required By | Impact if Delayed | Status |
|--------|------------------------|------|----------|-------------|-------------------|--------|
| **D001** | Completed product specifications (Fire, GL, PI) | Document | Global Underwriting | Sprint 2 start | Configuration delays | Pending |
| **D002** | Policy wordings and endorsements finalized | Document | Global Underwriting | Sprint 2 | Document template delays | Pending |
| **D003** | Rating models and calculation logic | Business | Global Underwriting | Sprint 2 | Rating engine delays | Pending |
| **D004** | Azure infrastructure provisioned | Technical | Appsure | Sprint 1 end | Entire project delay | Pending |
| **D005** | Back-office system integration specs | Technical | Global Underwriting IT | Sprint 3 | Integration delays | Pending |
| **D006** | Bank account details and format (Macquarie) | External | GU Finance/Macquarie | Sprint 3 | Import process delays | Pending |
| **D007** | UAT resources availability | Resource | Global Underwriting | Sprint 4 | Testing delays | Pending |
| **D008** | Broker list and commission structures | Business | Global Underwriting | Sprint 3 | Portal setup delays | Pending |
| **D010** | Management KPI definitions | Business | GU Finance | Sprint 3 | Reporting delays | Pending |
| **D011** | User roles and permissions matrix | Business | Global Underwriting | Sprint 1 | Security setup delays | Pending |
| **D012** | Training environment availability | Technical | Appsure | Sprint 4 | Training delays | Pending |
| **D013** | Go-live approval from stakeholders | Decision | GU Management | Sprint 4 end | Go-live delays | Pending |
| **D015** | Compliance sign-off | Regulatory | GU Compliance | Before go-live | Go-live delays | Pending |

### Assumptions Log

| ID | Assumption | Category | Impact if False | Validation Method | Owner |
|----|------------|----------|-----------------|-------------------|-------|
| **A001** | Product specifications are complete and signed off | Requirements | Major delays, rework | Document review in Sprint 1 | GU System Owner |
| **A002** | No integration with Sunrise or SCTP in Phase 1 | Scope | Scope increase, timeline impact | Confirmed in project charter | Both PMs |
| **A003** | 4-6 sprints sufficient for implementation | Schedule | Timeline extension needed | Sprint velocity tracking | Appsure PM |
| **A004** | Global Underwriting manages regulatory compliance | Compliance | Appsure scope increase | Compliance workshop | GU Compliance |
| **A005** | No data migration - policies transition at renewal | Scope | N/A - Confirmed excluded | Confirmed in updated scope | GU System Owner |
| **A006** | Standard Appsure platform meets all requirements | Technical | Customization needed | Requirements analysis | Appsure BA |
| **A007** | Macquarie bank format is standard | Integration | Custom development needed | Technical review | Appsure Architect |
| **A008** | UAT can be completed in one sprint | Schedule | Extended testing period | Test case estimation | GU System Owner |
| **A009** | ISO 27001:2022 certification sufficient | Compliance | Additional security measures | Compliance review | GU IT |
| **A010** | Hypercare support for 4 weeks is adequate | Support | Extended support needed | Go-live planning | Both PMs |
| **A011** | Training can be delivered remotely | Logistics | On-site training needed | Training plan review | GU System Owner |
| **A012** | Current Fire, GL, PI products are standard | Product | Complex configuration needed | Product review | Appsure BA |

### Issue Log Template

| Issue ID | Date Raised | Description | Severity | Assigned To | Target Resolution | Status | Resolution |
|----------|-------------|-------------|----------|-------------|-------------------|--------|------------|
| I001 | [Date] | [Issue description] | [Critical/High/Medium/Low] | [Name] | [Date] | [Open/In Progress/Closed] | [Resolution details] |

### Risk Mitigation Strategies

#### High-Priority Risks (Score ≥ 12)

1. **R001 - Incomplete Product Specifications**
   - Conduct detailed requirements workshop Week 1
   - Document all assumptions
   - Get formal sign-off before configuration
   - Implement strict change control


3. **R012 - Aggressive Timeline**
   - Run parallel workstreams where possible
   - Identify critical path activities
   - Have backup resources available
   - Consider MVP approach for initial go-live

4. **R014 - Production Go-Live Issues**
   - Comprehensive test coverage
   - Production-like test environment
   - Detailed go-live runbook
   - Rollback plan prepared
   - 24/7 support during cutover

### Contingency Plans

| Risk Event | Contingency Plan | Trigger Point |
|------------|------------------|---------------|
| Timeline slippage | Add resources or reduce scope | 20% behind schedule |
| Resource unavailability | Engage contractors or Appsure backup team | Key resource absent >3 days |
| Major defects in UAT | Extended testing sprint | >10 critical defects |
| Integration failure | Manual workarounds initially | Integration not ready by Sprint 4 |

### Monthly Risk Review Process

1. Review all open risks
2. Update probability and impact scores
3. Identify new risks
4. Review mitigation effectiveness
5. Update contingency plans
6. Escalate high-priority risks to steering committee
7. Close resolved risks
8. Document lessons learned