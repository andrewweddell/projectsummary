"""
Ticket Management System for Global Underwriting Project
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from jira_client import JiraClient
import logging

logger = logging.getLogger(__name__)

class MarkdownReportGenerator:
    """Generates project management friendly markdown reports from Jira tickets"""
    
    @staticmethod
    def format_date(date_str):
        """Format ISO date string to readable format"""
        if not date_str:
            return "Not set"
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return date_str
    
    @staticmethod
    def get_status_emoji(status):
        """Get emoji representation for ticket status"""
        status_lower = status.lower()
        if 'done' in status_lower or 'closed' in status_lower or 'resolved' in status_lower:
            return "✅"
        elif 'progress' in status_lower or 'review' in status_lower:
            return "🔄"
        elif 'blocked' in status_lower:
            return "🚫"
        else:
            return "📋"
    
    @staticmethod
    def get_priority_emoji(priority):
        """Get emoji representation for ticket priority"""
        if not priority:
            return "⚪"
        priority_lower = priority.lower()
        if 'highest' in priority_lower or 'critical' in priority_lower:
            return "🔴"
        elif 'high' in priority_lower:
            return "🟠"
        elif 'medium' in priority_lower:
            return "🟡"
        elif 'low' in priority_lower:
            return "🟢"
        else:
            return "⚪"
    
    @classmethod
    def generate_project_summary(cls, tickets):
        """Generate project summary statistics"""
        total = len(tickets)
        epics = len([t for t in tickets if t['issue_type'] == 'Epic'])
        stories = len([t for t in tickets if t['issue_type'] == 'Story'])
        
        status_counts = {}
        priority_counts = {}
        assignee_counts = {}
        
        for ticket in tickets:
            # Status counts
            status = ticket['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Priority counts
            priority = ticket.get('priority', 'No Priority')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # Assignee counts
            assignee = ticket.get('assignee', 'Unassigned')
            assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1
        
        return {
            'total': total,
            'epics': epics,
            'stories': stories,
            'status_counts': status_counts,
            'priority_counts': priority_counts,
            'assignee_counts': assignee_counts
        }
    
    @classmethod
    def generate_markdown_report(cls, tickets, project_name="Global Underwriting"):
        """Generate comprehensive markdown report for project managers"""
        
        summary = cls.generate_project_summary(tickets)
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a lookup map for ticket keys to summaries for better parent/epic display
        ticket_lookup = {ticket['key']: ticket['summary'] for ticket in tickets}
        
        # Start building the markdown content
        md = []
        md.append(f"# {project_name} - Project Status Report")
        md.append(f"**Generated:** {report_date}")
        md.append("")
        
        # Project Summary
        md.append("## 📊 Project Summary")
        md.append("")
        md.append(f"- **Total Tickets:** {summary['total']}")
        md.append(f"- **Epics:** {summary['epics']}")
        md.append(f"- **Stories:** {summary['stories']}")
        md.append("")
        
        # Status Distribution
        md.append("### Status Distribution")
        md.append("")
        for status, count in sorted(summary['status_counts'].items()):
            emoji = cls.get_status_emoji(status)
            md.append(f"- {emoji} **{status}:** {count} tickets")
        md.append("")
        
        # Priority Distribution
        md.append("### Priority Distribution")
        md.append("")
        for priority, count in sorted(summary['priority_counts'].items()):
            emoji = cls.get_priority_emoji(priority)
            md.append(f"- {emoji} **{priority}:** {count} tickets")
        md.append("")
        
        # Team Workload
        md.append("### Team Workload")
        md.append("")
        for assignee, count in sorted(summary['assignee_counts'].items()):
            md.append(f"- **{assignee}:** {count} tickets")
        md.append("")
        
        # Epics Overview
        epics = [t for t in tickets if t['issue_type'] == 'Epic']
        if epics:
            md.append("## 🎯 Epics Overview")
            md.append("")
            for epic in sorted(epics, key=lambda x: x['key']):
                status_emoji = cls.get_status_emoji(epic['status'])
                priority_emoji = cls.get_priority_emoji(epic.get('priority'))
                
                md.append(f"### {status_emoji} [{epic['key']}] {epic['summary']}")
                md.append(f"**Status:** {epic['status']} | **Priority:** {epic.get('priority', 'Not set')} {priority_emoji}")
                md.append(f"**Assignee:** {epic.get('assignee', 'Unassigned')}")
                md.append(f"**Created:** {cls.format_date(epic['created'])}")
                md.append(f"**Updated:** {cls.format_date(epic['updated'])}")
                if epic.get('due_date'):
                    md.append(f"**Due Date:** {cls.format_date(epic['due_date'])}")
                if epic.get('description'):
                    md.append(f"**Description:** {epic['description']}")
                md.append("")
        
        # All Tickets Table
        md.append("## 📋 All Tickets")
        md.append("")
        md.append("| Key | Summary | Status | Priority | Assignee | Type | Epic/Parent | Created | Updated | Due Date |")
        md.append("|-----|---------|---------|----------|----------|------|---------|---------|---------|----------|")
        
        for ticket in sorted(tickets, key=lambda x: x['key']):
            status_emoji = cls.get_status_emoji(ticket['status'])
            priority_emoji = cls.get_priority_emoji(ticket.get('priority'))
            
            key = ticket['key']
            summary = ticket['summary'][:50] + "..." if len(ticket['summary']) > 50 else ticket['summary']
            status = f"{status_emoji} {ticket['status']}"
            priority = f"{priority_emoji} {ticket.get('priority', 'Not set')}"
            assignee = ticket.get('assignee', 'Unassigned')
            issue_type = ticket['issue_type']
            
            # Determine Epic/Parent display - prioritize epic_link over parent
            epic_parent = "-"
            if ticket.get('epic_link'):
                epic_key = ticket['epic_link']
                epic_name = ticket_lookup.get(epic_key)
                if epic_name:
                    # Truncate long epic names for table display
                    epic_name_short = epic_name[:30] + "..." if len(epic_name) > 30 else epic_name
                    epic_parent = f"{epic_key}: {epic_name_short}"
                else:
                    epic_parent = epic_key
            elif ticket.get('parent'):
                parent_key = ticket['parent']
                parent_name = ticket_lookup.get(parent_key)
                if parent_name:
                    # Truncate long parent names for table display
                    parent_name_short = parent_name[:30] + "..." if len(parent_name) > 30 else parent_name
                    epic_parent = f"{parent_key}: {parent_name_short}"
                else:
                    epic_parent = parent_key
                
            created = cls.format_date(ticket['created']).split(' ')[0]  # Date only
            updated = cls.format_date(ticket['updated']).split(' ')[0]  # Date only
            due_date = cls.format_date(ticket.get('due_date')).split(' ')[0] if ticket.get('due_date') else "-"
            
            # Escape pipe characters in content
            summary = summary.replace('|', '\\|')
            assignee = assignee.replace('|', '\\|')
            epic_parent = epic_parent.replace('|', '\\|') if epic_parent != "-" else epic_parent
            
            md.append(f"| {key} | {summary} | {status} | {priority} | {assignee} | {issue_type} | {epic_parent} | {created} | {updated} | {due_date} |")
        
        md.append("")
        
        # Detailed Ticket Information
        md.append("## 📝 Detailed Ticket Information")
        md.append("")
        
        # Group by status for better organization
        status_groups = {}
        for ticket in tickets:
            status = ticket['status']
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(ticket)
        
        for status, status_tickets in sorted(status_groups.items()):
            status_emoji = cls.get_status_emoji(status)
            md.append(f"### {status_emoji} {status} ({len(status_tickets)} tickets)")
            md.append("")
            
            for ticket in sorted(status_tickets, key=lambda x: x['key']):
                priority_emoji = cls.get_priority_emoji(ticket.get('priority'))
                
                md.append(f"#### [{ticket['key']}] {ticket['summary']}")
                md.append("")
                
                # Basic Information Table
                md.append("| Field | Value |")
                md.append("|-------|-------|")
                md.append(f"| **Type** | {ticket['issue_type']} |")
                md.append(f"| **Status** | {ticket['status']} |")
                md.append(f"| **Priority** | {priority_emoji} {ticket.get('priority', 'Not set')} |")
                md.append(f"| **Assignee** | {ticket.get('assignee', 'Unassigned')} |")
                md.append(f"| **Reporter** | {ticket.get('reporter', 'Not set')} |")
                md.append(f"| **Created** | {cls.format_date(ticket['created'])} |")
                md.append(f"| **Updated** | {cls.format_date(ticket['updated'])} |")
                
                if ticket.get('due_date'):
                    md.append(f"| **Due Date** | {cls.format_date(ticket['due_date'])} |")
                if ticket.get('parent'):
                    md.append(f"| **Parent** | {ticket['parent']} |")
                if ticket.get('epic_link'):
                    md.append(f"| **Epic** | {ticket['epic_link']} |")
                if ticket.get('labels'):
                    md.append(f"| **Labels** | {', '.join(ticket['labels'])} |")
                if ticket.get('components'):
                    md.append(f"| **Components** | {', '.join(ticket['components'])} |")
                if ticket.get('fix_versions'):
                    md.append(f"| **Fix Versions** | {', '.join(ticket['fix_versions'])} |")
                
                md.append("")
                
                if ticket.get('description'):
                    md.append("**Description:**")
                    md.append("")
                    # Clean up description formatting
                    desc = ticket['description'].strip()
                    if desc:
                        md.append(desc)
                    else:
                        md.append("*No description provided*")
                    md.append("")
                
                md.append("---")
                md.append("")
        
        # Footer
        md.append("## 📋 Report Information")
        md.append("")
        md.append(f"- **Report Generated:** {report_date}")
        md.append(f"- **Total Tickets Analyzed:** {len(tickets)}")
        md.append("- **Generated by:** Global Underwriting Jira Integration Application")
        md.append("")
        
        return "\n".join(md)

class TicketManager:
    def __init__(self, jira_client: JiraClient, cache_file: str = "ticket_cache.json"):
        self.jira = jira_client
        self.cache_file = cache_file
        self.ticket_cache = self.load_cache()
    
    @staticmethod
    def _extract_epic_link(fields, epic_link_field):
        """Extract epic link from Jira fields using the proper field identifier"""
        try:
            # Try the dynamically identified field first
            if epic_link_field in fields:
                epic_data = fields[epic_link_field]
                if isinstance(epic_data, dict) and 'key' in epic_data:
                    return epic_data['key']
                elif isinstance(epic_data, str):
                    return epic_data
            
            # Fallback to common field names
            if fields.get("epic", {}).get("key"):
                return fields["epic"]["key"]
            
            # Check for custom fields that might contain epic links
            for field_key, field_value in fields.items():
                if field_key.startswith('customfield_') and field_value:
                    if isinstance(field_value, dict) and 'key' in field_value:
                        # This might be an epic link
                        return field_value['key']
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting epic link: {e}")
            return None
        
    def load_cache(self) -> Dict:
        """Load ticket cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache: {e}")
        return {"tickets": {}, "last_sync": None}
        
    def save_cache(self):
        """Save ticket cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.ticket_cache, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
            
    def sync_from_jira(self, progress_callback=None, operation_id=None) -> List[Dict]:
        """Pull all tickets from Jira and update cache"""
        logger.info("Syncing tickets from Jira...")
        
        if progress_callback:
            progress_callback(5, "Fetching tickets from Jira API...")
        
        # Get epic field mapping for proper epic link extraction
        epic_fields = self.jira.identify_epic_fields()
        epic_link_field = epic_fields.get('epic_link', 'epic')
        
        issues = self.jira.get_all_project_issues()
        synced_tickets = []
        total_issues = len(issues)
        
        if progress_callback:
            progress_callback(15, f"Processing {total_issues} tickets from Jira...", {"total_tickets": total_issues})
        
        # Clear existing ticket cache to remove any tickets that no longer exist in Jira
        old_ticket_count = len(self.ticket_cache["tickets"])
        self.ticket_cache["tickets"] = {}
        
        if progress_callback and old_ticket_count > 0:
            progress_callback(
                18, 
                f"Cleared {old_ticket_count} old tickets from cache...", 
                {"cleared_tickets": old_ticket_count}
            )
        
        for i, issue in enumerate(issues):
            fields = issue["fields"]
            ticket_data = {
                "key": issue["key"],
                "summary": fields["summary"],
                "description": fields.get("description", ""),
                "status": fields["status"]["name"],
                "issue_type": fields["issuetype"]["name"],
                "assignee": fields["assignee"]["displayName"] if fields["assignee"] else None,
                "created": fields["created"],
                "updated": fields["updated"],
                "parent": fields["parent"]["key"] if fields.get("parent") else None,
                "priority": fields["priority"]["name"] if fields.get("priority") else None,
                "due_date": fields.get("duedate"),
                "fix_versions": [v["name"] for v in fields.get("fixVersions", [])],
                "components": [c["name"] for c in fields.get("components", [])],
                "labels": fields.get("labels", []),
                "reporter": fields["reporter"]["displayName"] if fields.get("reporter") else None,
                "epic_link": self._extract_epic_link(fields, epic_link_field)
            }
            
            self.ticket_cache["tickets"][issue["key"]] = ticket_data
            synced_tickets.append(ticket_data)
            
            # Update progress
            if progress_callback and total_issues > 0:
                # Progress from 20% to 80% for processing tickets (adjusted for cache clearing)
                progress_percentage = 20 + int((i + 1) / total_issues * 60)
                progress_callback(
                    progress_percentage, 
                    f"Processed ticket {issue['key']} ({i + 1}/{total_issues})...",
                    {"processed_tickets": i + 1, "current_ticket": issue["key"]}
                )
            
        if progress_callback:
            progress_callback(85, "Saving ticket cache...")
            
        self.ticket_cache["last_sync"] = datetime.now().isoformat()
        self.save_cache()
        
        if progress_callback:
            progress_callback(90, "Generating project status report...")
        
        # Auto-export markdown report for project managers
        try:
            self.auto_export_after_sync()
            logger.info("Project status report automatically generated")
        except Exception as e:
            logger.warning(f"Failed to auto-generate project report: {e}")
        
        if progress_callback:
            progress_callback(100, f"Successfully synced {len(synced_tickets)} tickets from Jira")
        
        logger.info(f"Synced {len(synced_tickets)} tickets from Jira")
        return synced_tickets
        
    def get_all_tickets(self) -> List[Dict]:
        """Get all tickets from cache"""
        return list(self.ticket_cache["tickets"].values())
        
    def get_ticket_by_key(self, key: str) -> Optional[Dict]:
        """Get specific ticket by key"""
        return self.ticket_cache["tickets"].get(key)
        
    def update_ticket(self, key: str, summary: str = None, description: str = None, 
                     status: str = None) -> bool:
        """Update ticket in Jira and cache"""
        logger.info(f"Updating ticket {key}")
        
        # Update in Jira
        success = self.jira.update_issue(key, summary, description, status)
        
        if success and key in self.ticket_cache["tickets"]:
            # Update cache
            if summary:
                self.ticket_cache["tickets"][key]["summary"] = summary
            if description:
                self.ticket_cache["tickets"][key]["description"] = description
            if status:
                self.ticket_cache["tickets"][key]["status"] = status
            
            self.ticket_cache["tickets"][key]["updated"] = datetime.now().isoformat()
            self.save_cache()
            
        return success
        
    def create_all_project_tickets(self, progress_callback=None, operation_id=None) -> Dict[str, str]:
        """Create all tickets from the project structure"""
        logger.info("Creating all project tickets...")
        
        if progress_callback:
            progress_callback(5, "Loading project structure...")
        
        # Define the ticket structure
        ticket_structure = self.get_project_structure()
        created_tickets = {}
        
        if progress_callback:
            progress_callback(10, "Creating Epic tickets...")
        
        # First, check for existing epics and create mapping for them
        existing_tickets = self.get_all_tickets()
        existing_epics = [t for t in existing_tickets if t['issue_type'] == 'Epic']
        epic_mapping = {}
        
        # Create mapping for existing epics based on their summaries
        for existing_epic in existing_epics:
            summary = existing_epic['summary']
            if 'Foundation & Planning' in summary:
                epic_mapping['GLO-E1'] = existing_epic['key']
            elif 'Core Platform Configuration' in summary:
                epic_mapping['GLO-E2'] = existing_epic['key']
            elif 'Product Implementation' in summary:
                epic_mapping['GLO-E3'] = existing_epic['key']
            elif 'Integration & Testing' in summary:
                epic_mapping['GLO-E4'] = existing_epic['key']
            elif 'Training & Go-Live' in summary:
                epic_mapping['GLO-E5'] = existing_epic['key']
            elif 'Compliance & Operations' in summary:
                epic_mapping['GLO-E6'] = existing_epic['key']
        
        logger.info(f"Found existing epic mapping: {epic_mapping}")
        
        # Create any missing epics
        epics = ticket_structure.get("epics", [])
        total_epics = len(epics)
        
        for i, epic_data in enumerate(epics):
            # Skip if epic already exists
            if epic_data["key"] in epic_mapping:
                logger.info(f"Epic {epic_data['key']} already exists as {epic_mapping[epic_data['key']]}")
                created_tickets[epic_data["key"]] = epic_mapping[epic_data["key"]]
                if progress_callback:
                    progress_percentage = 10 + int((i + 1) / total_epics * 15)
                    progress_callback(progress_percentage, f"Epic {epic_data['key']} already exists: {epic_mapping[epic_data['key']]}", {"epic_key": epic_mapping[epic_data['key']]})
                continue
            
            # Create new epic
            epic_key = self.jira.create_epic(
                epic_data["summary"],
                epic_data["description"]
            )
            
            if epic_key:
                epic_mapping[epic_data["key"]] = epic_key
                created_tickets[epic_data["key"]] = epic_key
                logger.info(f"Created Epic: {epic_data['key']} -> {epic_key}")
                
                if progress_callback:
                    progress_percentage = 10 + int((i + 1) / total_epics * 15)
                    progress_callback(progress_percentage, f"Created epic {epic_data['key']}: {epic_key}", {"epic_key": epic_key})
            else:
                logger.error(f"Failed to create epic {epic_data['key']} - this will cause story linking issues!")
        
        # Log the complete epic mapping for debugging
        logger.info(f"Final epic mapping: {epic_mapping}")
        
        # Create Stories and link to appropriate epics
        stories = ticket_structure.get("stories", [])
        
        # Skip existing tickets
        existing_tickets = ["GLO-1", "GLO-2", "GLO-3"]  # Skip existing tickets
        
        stories_to_create = [story for story in stories 
                           if story["ticket_id"] not in existing_tickets]
        total_stories = len(stories_to_create)
        
        if progress_callback:
            progress_callback(
                25, 
                f"Creating {total_stories} story tickets...", 
                {"total_stories": total_stories}
            )
        
        for i, story_data in enumerate(stories_to_create):
            # Determine which epic this story belongs to based on story number
            epic_key_to_link = None
            story_number = int(story_data["ticket_id"].split("-")[1])
            
            # Map story numbers to epics based on the project structure
            # Use the actual Jira epic keys that were created, not the planned keys
            if 255 <= story_number <= 279:
                epic_key_to_link = epic_mapping.get("GLO-E1")  # This maps to actual key like GLO-260
            elif 280 <= story_number <= 296:
                epic_key_to_link = epic_mapping.get("GLO-E2")
            elif 297 <= story_number <= 311:
                epic_key_to_link = epic_mapping.get("GLO-E3")
            elif 312 <= story_number <= 326:
                epic_key_to_link = epic_mapping.get("GLO-E4")
            elif 327 <= story_number <= 341:
                epic_key_to_link = epic_mapping.get("GLO-E5")
            elif 342 <= story_number <= 351:
                epic_key_to_link = epic_mapping.get("GLO-E6")
            
            # Log the epic mapping for debugging
            if epic_key_to_link:
                logger.info(f"Story {story_data['ticket_id']} (number {story_number}) will be linked to epic {epic_key_to_link}")
            else:
                logger.warning(f"No epic mapping found for story {story_data['ticket_id']} (number {story_number})")
            
            try:
                story_key = self.jira.create_story(
                    story_data["summary"],
                    story_data["description"],
                    epic_key_to_link
                )
                
                if story_key:
                    created_tickets[story_data["ticket_id"]] = story_key
                    if epic_key_to_link:
                        logger.info(f"Created Story: {story_data['ticket_id']} -> {story_key} (linked to epic {epic_key_to_link})")
                    else:
                        logger.info(f"Created Story: {story_data['ticket_id']} -> {story_key} (no epic link)")
                    
                    # Update progress for story creation (25% to 75%)
                    if progress_callback and total_stories > 0:
                        progress_percentage = 25 + int((i + 1) / total_stories * 50)
                        progress_callback(
                            progress_percentage,
                            f"Created story {story_data['ticket_id']}: {story_key} ({i + 1}/{total_stories})",
                            {
                                "created_stories": i + 1,
                                "current_story": story_data["ticket_id"],
                                "story_key": story_key
                            }
                        )
                else:
                    logger.error(f"Failed to create story {story_data['ticket_id']}")
                    if progress_callback and total_stories > 0:
                        progress_percentage = 25 + int((i + 1) / total_stories * 50)
                        progress_callback(
                            progress_percentage,
                            f"Failed to create story {story_data['ticket_id']} ({i + 1}/{total_stories})",
                            {
                                "created_stories": len([k for k, v in created_tickets.items() if k.startswith("GLO-") and int(k.split("-")[1]) > 254]),
                                "failed_story": story_data["ticket_id"]
                            }
                        )
            except Exception as e:
                logger.error(f"Error creating story {story_data['ticket_id']}: {e}")
                if progress_callback and total_stories > 0:
                    progress_percentage = 25 + int((i + 1) / total_stories * 50)
                    progress_callback(
                        progress_percentage,
                        f"Error creating story {story_data['ticket_id']}: {str(e)} ({i + 1}/{total_stories})",
                        {
                            "created_stories": len([k for k, v in created_tickets.items() if k.startswith("GLO-") and int(k.split("-")[1]) > 254]),
                            "error_story": story_data["ticket_id"]
                        }
                    )
        
        # Handle existing tickets in progress reporting
        for ticket_id in existing_tickets:
            if progress_callback:
                progress_callback(
                    None,  # Don't update percentage
                    f"Skipped existing ticket: {ticket_id}",
                    {"skipped_ticket": ticket_id}
                )
                    
        if progress_callback:
            progress_callback(80, "Syncing created tickets back from Jira...")
                            
        # Sync back from Jira to update cache
        self.sync_from_jira(progress_callback=lambda step, msg, details=None: 
                           progress_callback(80 + int(step * 0.2), msg, details) if progress_callback else None)
        
        if progress_callback:
            progress_callback(100, f"Successfully created {len(created_tickets)} tickets")
        
        return created_tickets
        
    def parse_markdown_project_structure(self) -> Dict:
        """Parse project structure from markdown file"""
        import re
        import os
        
        markdown_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'technical', 'jira_project_structure.md')
        
        if not os.path.exists(markdown_path):
            logger.warning(f"Markdown file not found at {markdown_path}, using fallback structure")
            return self.get_fallback_structure()
        
        try:
            with open(markdown_path, 'r') as f:
                content = f.read()
                
            # Extract all epics from the markdown
            epics = []
            epic_pattern = r'### EPIC:\s*(GLO-E\d+)\s*-\s*(.+?)\n.*?\*\*Epic Description:\*\*\s*(.+?)(?=\n|$)'
            epic_matches = re.findall(epic_pattern, content, re.MULTILINE | re.DOTALL)
            
            for epic_match in epic_matches:
                epic_key = epic_match[0].strip()
                epic_title = epic_match[1].strip()
                epic_desc = epic_match[2].strip()
                
                epics.append({
                    "key": epic_key,
                    "summary": epic_title,
                    "description": epic_desc
                })
            
            # Extract all stories from the markdown
            stories = []
            story_pattern = r'### STORY:\s*(GLO-\d+)\s*-\s*(.+?)\n\*\*Description:\*\*\s*(.+?)(?=\n(?:\*\*|###)|$)'
            story_matches = re.findall(story_pattern, content, re.MULTILINE | re.DOTALL)
            
            for story_match in story_matches:
                story_id = story_match[0].strip()
                story_title = story_match[1].strip()
                story_desc = story_match[2].strip()
                
                stories.append({
                    "ticket_id": story_id,
                    "summary": story_title,
                    "description": story_desc
                })
            
            return {
                "epics": epics,
                "stories": stories
            }
            
        except Exception as e:
            logger.error(f"Error parsing markdown file: {e}")
            return self.get_fallback_structure()
    
    def get_fallback_structure(self) -> Dict:
        """Fallback structure if markdown parsing fails"""
        return {
            "epics": [
                {
                    "key": "GLO-E1",
                    "summary": "Foundation & Planning",
                    "description": "Set up project governance, Azure infrastructure, and complete business requirements analysis"
                }
            ],
            "stories": [
                {"ticket_id": "GLO-255", "summary": "Project Setup & Governance", "description": "Establish project foundation and governance structures"},
                {"ticket_id": "GLO-256", "summary": "Requirements Analysis", "description": "Analyze and document all business requirements"},
                {"ticket_id": "GLO-257", "summary": "Technical Design", "description": "Create technical design and architecture documentation"}
            ]
        }

    def get_project_structure(self) -> Dict:
        """Get project structure from markdown files"""
        return self.parse_markdown_project_structure()
        
    def get_tickets_by_status(self, status: str) -> List[Dict]:
        """Get all tickets with specific status"""
        return [ticket for ticket in self.get_all_tickets() 
                if ticket["status"].lower() == status.lower()]
        
    def get_tickets_by_type(self, issue_type: str) -> List[Dict]:
        """Get all tickets of specific type"""
        return [ticket for ticket in self.get_all_tickets() 
                if ticket["issue_type"].lower() == issue_type.lower()]
        
    def search_tickets(self, search_term: str) -> List[Dict]:
        """Search tickets by summary or description"""
        search_term = search_term.lower()
        return [ticket for ticket in self.get_all_tickets() 
                if search_term in ticket["summary"].lower() or 
                   search_term in (ticket.get("description") or "").lower()]
    
    def export_to_markdown(self, file_path: str = None, project_name: str = "Global Underwriting") -> str:
        """Export all tickets to markdown format for project managers"""
        logger.info("Generating markdown report for project managers...")
        
        tickets = self.get_all_tickets()
        
        if not tickets:
            logger.warning("No tickets found to export")
            return ""
        
        # Generate the markdown content
        markdown_content = MarkdownReportGenerator.generate_markdown_report(tickets, project_name)
        
        # Determine file path
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"project_status_report_{timestamp}.md"
        
        # Write to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"Project status report exported to: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error writing markdown file: {e}")
            raise
    
    def auto_export_after_sync(self, project_name: str = "Global Underwriting") -> str:
        """Automatically export markdown report after ticket sync"""
        return self.export_to_markdown(
            file_path="project_status_report_latest.md", 
            project_name=project_name
        )