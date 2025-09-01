"""
Jira API Client for Global Underwriting Project
"""
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JiraClient:
    def __init__(self, url: str, username: str, api_token: str, project_key: str = "GLO"):
        """
        Initialize Jira client
        
        Args:
            url: Jira instance URL (e.g., https://yourcompany.atlassian.net)
            username: Your Jira username/email
            api_token: API token from Jira
            project_key: Project key (default: GLO)
        """
        self.base_url = url.rstrip('/')
        self.auth = (username, api_token)
        self.project_key = project_key
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def test_connection(self) -> bool:
        """Test connection to Jira"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/2/myself")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
            
    def get_project_info(self) -> Dict:
        """Get project information"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/2/project/{self.project_key}")
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            logger.error(f"Failed to get project info: {e}")
            return {}
            
    def identify_epic_fields(self) -> Dict[str, str]:
        """Identify epic-related custom field IDs for this Jira instance"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/2/field")
            if response.status_code != 200:
                logger.error(f"Failed to get fields: {response.text}")
                return {}
                
            fields = response.json()
            epic_fields = {}
            
            for field in fields:
                field_name = field.get('name', '').lower()
                field_id = field.get('id', '')
                
                # Common patterns for epic fields
                if 'epic name' in field_name or field_name == 'epic name':
                    epic_fields['epic_name'] = field_id
                elif 'epic link' in field_name or field_name == 'epic link':
                    epic_fields['epic_link'] = field_id
                elif 'story points' in field_name or field_name == 'story points':
                    epic_fields['story_points'] = field_id
                elif field_id.startswith('customfield_') and 'epic' in field_name:
                    # Generic epic field detection
                    if 'name' in field_name:
                        epic_fields['epic_name'] = field_id
                    elif 'link' in field_name:
                        epic_fields['epic_link'] = field_id
                        
            logger.info(f"Identified epic fields: {epic_fields}")
            return epic_fields
            
        except Exception as e:
            logger.error(f"Error identifying epic fields: {e}")
            return {}
            
    def create_epic(self, summary: str, description: str = "", sprint_info: Dict = None, story_points: int = None) -> Optional[str]:
        """Create epic with comprehensive metadata"""
        try:
            # First, create epic without custom fields
            payload = {
                "fields": {
                    "project": {"key": self.project_key},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": "Epic"}
                }
            }
            
            # Add sprint and label information
            if sprint_info:
                labels = payload["fields"].get("labels", [])
                labels.append(f"Sprint-{sprint_info.get('number', '')}")
                payload["fields"]["labels"] = labels
            
            response = self.session.post(
                f"{self.base_url}/rest/api/2/issue",
                data=json.dumps(payload)
            )
            
            if response.status_code == 201:
                epic_key = response.json()["key"]
                logger.info(f"Created epic: {epic_key}")
                
                # Now try to update with custom fields if needed
                try:
                    epic_fields = self.identify_epic_fields()
                    update_payload = {"fields": {}}
                    
                    # Add epic name if field identified
                    if 'epic_name' in epic_fields:
                        update_payload["fields"][epic_fields['epic_name']] = summary
                        logger.info(f"Adding epic name field: {epic_fields['epic_name']}")
                    
                    # Add story points if provided and field identified
                    if story_points and 'story_points' in epic_fields:
                        update_payload["fields"][epic_fields['story_points']] = story_points
                        logger.info(f"Adding story points field: {epic_fields['story_points']}")
                    
                    # Only update if we have fields to update
                    if update_payload["fields"]:
                        update_response = self.session.put(
                            f"{self.base_url}/rest/api/2/issue/{epic_key}",
                            data=json.dumps(update_payload)
                        )
                        
                        if update_response.status_code == 204:
                            logger.info(f"Updated epic {epic_key} with custom fields")
                        else:
                            logger.warning(f"Failed to update epic custom fields: {update_response.text}")
                            
                except Exception as e:
                    logger.warning(f"Error updating epic custom fields (epic still created): {e}")
                
                return epic_key
            else:
                logger.error(f"Failed to create epic: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating epic: {e}")
            return None
            
    def create_story(self, summary: str, description: str = "", epic_key: str = None, story_points: int = None, priority: str = None, sprint: int = None) -> Optional[str]:
        """Create story without epic linking initially - epic linking will be done separately"""
        try:
            # Create story with basic fields first (no epic link during creation)
            payload = {
                "fields": {
                    "project": {"key": self.project_key},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": "Story"}
                }
            }
            
            # Add priority if provided
            if priority:
                payload["fields"]["priority"] = {"name": priority}
                
            # Add sprint label if provided
            if sprint:
                labels = payload["fields"].get("labels", [])
                labels.append(f"Sprint-{sprint}")
                payload["fields"]["labels"] = labels
                
            response = self.session.post(
                f"{self.base_url}/rest/api/2/issue",
                data=json.dumps(payload)
            )
            
            if response.status_code == 201:
                story_key = response.json()["key"]
                logger.info(f"Created story: {story_key}")
                
                # Now try to link to epic if provided (separate operation)
                if epic_key:
                    success = self.link_story_to_epic(story_key, epic_key)
                    if success:
                        logger.info(f"Successfully linked story {story_key} to epic {epic_key}")
                    else:
                        logger.warning(f"Story {story_key} created but failed to link to epic {epic_key}")
                
                # Try to add story points if provided (separate operation)
                if story_points:
                    success = self.add_story_points(story_key, story_points)
                    if success:
                        logger.info(f"Successfully added {story_points} story points to {story_key}")
                    else:
                        logger.warning(f"Story {story_key} created but failed to add story points")
                        
                return story_key
            else:
                logger.error(f"Failed to create story: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating story: {e}")
            return None
    
    def link_story_to_epic(self, story_key: str, epic_key: str) -> bool:
        """Link a story to an epic after creation - try multiple approaches"""
        try:
            # Approach 1: Try using issue link (Epic-Story relationship)
            logger.info(f"Attempting to link story {story_key} to epic {epic_key} using issue link...")
            
            link_payload = {
                "type": {
                    "name": "Epic-Story Link"
                },
                "inwardIssue": {
                    "key": story_key
                },
                "outwardIssue": {
                    "key": epic_key
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/rest/api/2/issueLink",
                data=json.dumps(link_payload)
            )
            
            if response.status_code == 201:
                logger.info(f"Successfully linked story {story_key} to epic {epic_key} using issue link")
                return True
            else:
                logger.warning(f"Issue link approach failed: {response.text}")
            
            # Approach 2: Try using parent relationship (if supported)
            logger.info(f"Attempting to link using parent relationship...")
            
            parent_payload = {
                "fields": {
                    "parent": {
                        "key": epic_key
                    }
                }
            }
            
            response = self.session.put(
                f"{self.base_url}/rest/api/2/issue/{story_key}",
                data=json.dumps(parent_payload)
            )
            
            if response.status_code == 204:
                logger.info(f"Successfully linked story {story_key} to epic {epic_key} using parent relationship")
                return True
            else:
                logger.warning(f"Parent relationship approach failed: {response.text}")
            
            # Approach 3: Try using epic link field (original approach)
            logger.info(f"Attempting to link using epic link custom field...")
            epic_fields = self.identify_epic_fields()
            
            if 'epic_link' not in epic_fields:
                logger.warning("Epic link field not identified")
                return False
                
            payload = {
                "fields": {
                    epic_fields['epic_link']: epic_key
                }
            }
            
            response = self.session.put(
                f"{self.base_url}/rest/api/2/issue/{story_key}",
                data=json.dumps(payload)
            )
            
            if response.status_code == 204:
                logger.info(f"Successfully linked story {story_key} to epic {epic_key} using epic link field")
                return True
            else:
                logger.warning(f"Epic link field approach failed: {response.text}")
                
            # All approaches failed
            logger.error(f"All linking approaches failed for story {story_key} to epic {epic_key}")
            return False
                
        except Exception as e:
            logger.error(f"Error linking story {story_key} to epic {epic_key}: {e}")
            return False
    
    def add_story_points(self, story_key: str, story_points: int) -> bool:
        """Add story points to a story after creation"""
        try:
            epic_fields = self.identify_epic_fields()
            
            if 'story_points' not in epic_fields:
                logger.warning("Story points field not identified - cannot add story points")
                return False
                
            payload = {
                "fields": {
                    epic_fields['story_points']: story_points
                }
            }
            
            response = self.session.put(
                f"{self.base_url}/rest/api/2/issue/{story_key}",
                data=json.dumps(payload)
            )
            
            if response.status_code == 204:
                logger.info(f"Successfully added {story_points} story points to {story_key}")
                return True
            else:
                logger.error(f"Failed to add story points: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding story points to {story_key}: {e}")
            return False
            
    # Task/subtask creation removed - using Epics and Stories only
            
    def get_all_project_issues(self) -> List[Dict]:
        """Get all issues in the project"""
        try:
            # Get epic field mapping first
            epic_fields = self.identify_epic_fields()
            fields_list = [
                "summary", "description", "status", "issuetype", "parent", 
                "assignee", "created", "updated", "priority", "duedate", 
                "fixVersions", "components", "labels", "reporter"
            ]
            
            # Add epic link field if identified
            if 'epic_link' in epic_fields:
                fields_list.append(epic_fields['epic_link'])
                
            jql = f"project = {self.project_key} ORDER BY key ASC"
            response = self.session.get(
                f"{self.base_url}/rest/api/2/search",
                params={
                    "jql": jql,
                    "maxResults": 1000,
                    "fields": ",".join(fields_list)
                }
            )
            
            if response.status_code == 200:
                return response.json().get("issues", [])
            else:
                logger.error(f"Failed to get issues: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting issues: {e}")
            return []
            
    def get_epic_progress_summary(self) -> Dict[str, Dict]:
        """Get progress summary for each epic with linked stories"""
        try:
            issues = self.get_all_project_issues()
            epic_fields = self.identify_epic_fields()
            
            # Separate epics and stories
            epics = {}
            stories = []
            
            for issue in issues:
                issue_type = issue.get('fields', {}).get('issuetype', {}).get('name', '')
                if issue_type == 'Epic':
                    epics[issue['key']] = {
                        'key': issue['key'],
                        'summary': issue.get('fields', {}).get('summary', ''),
                        'status': issue.get('fields', {}).get('status', {}).get('name', ''),
                        'linked_stories': []
                    }
                elif issue_type == 'Story':
                    # Get epic link from the story
                    epic_link = None
                    if 'epic_link' in epic_fields:
                        epic_link = issue.get('fields', {}).get(epic_fields['epic_link'])
                    
                    stories.append({
                        'key': issue['key'],
                        'summary': issue.get('fields', {}).get('summary', ''),
                        'status': issue.get('fields', {}).get('status', {}).get('name', ''),
                        'epic_link': epic_link
                    })
            
            # Link stories to epics
            for story in stories:
                if story['epic_link'] and story['epic_link'] in epics:
                    epics[story['epic_link']]['linked_stories'].append(story)
                    
            # Calculate progress for each epic
            epic_progress = {}
            for epic_key, epic_data in epics.items():
                linked_stories = epic_data['linked_stories']
                total_stories = len(linked_stories)
                
                if total_stories > 0:
                    completed_stories = len([s for s in linked_stories 
                                           if s['status'].lower() in ['done', 'closed', 'resolved']])
                    in_progress_stories = len([s for s in linked_stories 
                                             if 'progress' in s['status'].lower() or 'development' in s['status'].lower()])
                    progress_percentage = (completed_stories / total_stories) * 100
                else:
                    completed_stories = 0
                    in_progress_stories = 0  
                    progress_percentage = 0
                
                epic_progress[epic_key] = {
                    'epic_summary': epic_data['summary'],
                    'epic_status': epic_data['status'],
                    'total_stories': total_stories,
                    'completed_stories': completed_stories,
                    'in_progress_stories': in_progress_stories,
                    'pending_stories': total_stories - completed_stories - in_progress_stories,
                    'progress_percentage': round(progress_percentage, 1),
                    'story_details': linked_stories
                }
            
            return epic_progress
            
        except Exception as e:
            logger.error(f"Error getting epic progress: {e}")
            return {}
            
    def get_project_overview(self) -> Dict:
        """Get high-level project overview with epic progress"""
        try:
            epic_progress = self.get_epic_progress_summary()
            
            # Calculate overall project metrics
            total_epics = len(epic_progress)
            total_stories = sum(ep['total_stories'] for ep in epic_progress.values())
            total_completed = sum(ep['completed_stories'] for ep in epic_progress.values())
            total_in_progress = sum(ep['in_progress_stories'] for ep in epic_progress.values())
            
            overall_progress = (total_completed / total_stories * 100) if total_stories > 0 else 0
            
            completed_epics = len([ep for ep in epic_progress.values() 
                                 if ep['progress_percentage'] == 100])
            
            return {
                'project_key': self.project_key,
                'total_epics': total_epics,
                'completed_epics': completed_epics,
                'total_stories': total_stories,
                'completed_stories': total_completed,
                'in_progress_stories': total_in_progress,
                'pending_stories': total_stories - total_completed - total_in_progress,
                'overall_progress_percentage': round(overall_progress, 1),
                'epic_breakdown': epic_progress,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting project overview: {e}")
            return {}
            
    def update_issue(self, issue_key: str, summary: str = None, description: str = None, 
                    status: str = None) -> bool:
        """Update an existing issue"""
        try:
            update_fields = {}
            if summary:
                update_fields["summary"] = summary
            if description:
                update_fields["description"] = description
                
            payload = {"fields": update_fields}
            
            # Handle status transition separately
            if status:
                transitions = self.get_available_transitions(issue_key)
                transition_id = None
                for trans in transitions:
                    if trans["to"]["name"].lower() == status.lower():
                        transition_id = trans["id"]
                        break
                        
                if transition_id:
                    transition_payload = {
                        "transition": {"id": transition_id}
                    }
                    self.session.post(
                        f"{self.base_url}/rest/api/2/issue/{issue_key}/transitions",
                        data=json.dumps(transition_payload)
                    )
            
            if update_fields:
                response = self.session.put(
                    f"{self.base_url}/rest/api/2/issue/{issue_key}",
                    data=json.dumps(payload)
                )
                return response.status_code == 204
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating issue {issue_key}: {e}")
            return False
            
    def get_available_transitions(self, issue_key: str) -> List[Dict]:
        """Get available transitions for an issue"""
        try:
            response = self.session.get(
                f"{self.base_url}/rest/api/2/issue/{issue_key}/transitions"
            )
            if response.status_code == 200:
                return response.json().get("transitions", [])
            return []
        except Exception as e:
            logger.error(f"Error getting transitions for {issue_key}: {e}")
            return []
            
    def delete_issue(self, issue_key: str) -> bool:
        """Delete an issue"""
        try:
            response = self.session.delete(
                f"{self.base_url}/rest/api/2/issue/{issue_key}"
            )
            return response.status_code == 204
        except Exception as e:
            logger.error(f"Error deleting issue {issue_key}: {e}")
            return False
            
    def create_epics_from_structure(self) -> Dict[str, str]:
        """
        Create the 6 epics based on the new project structure
        Returns mapping of epic keys to Jira keys
        """
        epic_mapping = {}
        
        epics_data = [
            {
                "key": "GLO-E1",
                "summary": "Foundation & Planning",
                "description": "Set up project governance, Azure infrastructure, and complete business requirements analysis",
                "sprint_info": {"number": 1},
                "story_count": 25
            },
            {
                "key": "GLO-E2", 
                "summary": "Core Platform Configuration",
                "description": "Establish core Appsure platform with user roles, workflows, and billing processes",
                "sprint_info": {"number": 2},
                "story_count": 17
            },
            {
                "key": "GLO-E3",
                "summary": "Product Implementation", 
                "description": "Configure both GL/Fire and PI products with rating engines, broker portal, and workflows",
                "sprint_info": {"number": 3},
                "story_count": 15
            },
            {
                "key": "GLO-E4",
                "summary": "Integration & Testing",
                "description": "Implement back-office integrations, execute UAT, and complete all testing phases",
                "sprint_info": {"number": 4}, 
                "story_count": 15
            },
            {
                "key": "GLO-E5",
                "summary": "Training & Go-Live",
                "description": "Conduct user training, finalize production environment, and execute go-live",
                "sprint_info": {"number": 5},
                "story_count": 15
            },
            {
                "key": "GLO-E6",
                "summary": "Compliance & Operations", 
                "description": "Implement APRA compliance, security controls, and operational monitoring",
                "sprint_info": {"number": 0},  # Cross-cutting
                "story_count": 10
            }
        ]
        
        for epic_data in epics_data:
            epic_key = self.create_epic(
                summary=epic_data["summary"],
                description=epic_data["description"],
                sprint_info=epic_data["sprint_info"],
                story_points=epic_data["story_count"]
            )
            
            if epic_key:
                epic_mapping[epic_data["key"]] = epic_key
                logger.info(f"Created epic {epic_data['key']} -> {epic_key}")
            else:
                logger.error(f"Failed to create epic {epic_data['key']}")
                
        return epic_mapping

    def bulk_create_from_structure(self, structure_file: str) -> Dict[str, str]:
        """
        Create all tickets from the project structure
        Returns mapping of ticket numbers to Jira keys
        """
        # Load the project structure
        with open(structure_file, 'r') as f:
            content = f.read()
            
        # Parse the structure and create tickets
        ticket_mapping = {}
        
        # Create epics first
        epic_mapping = self.create_epics_from_structure()
        ticket_mapping.update(epic_mapping)
        
        # TODO: Parse stories from markdown and create with epic links
        # This would involve parsing the markdown to extract story information
        # and linking them to the appropriate epics based on the sprint/epic mapping
        
        return ticket_mapping