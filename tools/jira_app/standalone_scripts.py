#!/usr/bin/env python3
"""
Standalone scripts for Jira operations
Can be run independently without the web interface
"""

import json
import sys
import argparse
from jira_client import JiraClient
from ticket_manager import TicketManager

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found. Please create it first.")
        print("You can use config.example.json as a template.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in config.json")
        sys.exit(1)

def test_connection():
    """Test Jira connection"""
    print("🔌 Testing Jira connection...")
    config = load_config()
    
    client = JiraClient(
        url=config['jira_url'],
        username=config['jira_username'],
        api_token=config['jira_api_token'],
        project_key=config['project_key']
    )
    
    if client.test_connection():
        print("✅ Connection successful!")
        
        # Get project info
        project_info = client.get_project_info()
        if project_info:
            print(f"📋 Project: {project_info.get('name', 'Unknown')} ({project_info.get('key', 'Unknown')})")
            print(f"📝 Description: {project_info.get('description', 'No description')}")
        return True
    else:
        print("❌ Connection failed!")
        return False

def sync_tickets():
    """Sync all tickets from Jira"""
    print("🔄 Syncing tickets from Jira...")
    config = load_config()
    
    client = JiraClient(
        url=config['jira_url'],
        username=config['jira_username'],
        api_token=config['jira_api_token'],
        project_key=config['project_key']
    )
    
    if not client.test_connection():
        print("❌ Cannot connect to Jira")
        return False
        
    ticket_manager = TicketManager(client)
    tickets = ticket_manager.sync_from_jira()
    
    print(f"✅ Synced {len(tickets)} tickets")
    
    # Show summary
    epics = len([t for t in tickets if t['issue_type'] == 'Epic'])
    stories = len([t for t in tickets if t['issue_type'] == 'Story'])
    tasks = 0  # No tasks or sub-tasks - using Epic → Story structure only
    
    print(f"📊 Summary: {epics} Epics, {stories} Stories, {tasks} Tasks")
    return True

def create_all_tickets():
    """Create all project tickets in Jira"""
    print("🚀 Creating all project tickets in Jira...")
    print("This will create 117 tickets (1 Epic, 20+ Stories, 90+ Tasks)")
    
    confirm = input("Continue? (y/N): ").lower().strip()
    if confirm != 'y':
        print("Operation cancelled.")
        return False
    
    config = load_config()
    
    client = JiraClient(
        url=config['jira_url'],
        username=config['jira_username'],
        api_token=config['jira_api_token'],
        project_key=config['project_key']
    )
    
    if not client.test_connection():
        print("❌ Cannot connect to Jira")
        return False
        
    ticket_manager = TicketManager(client)
    
    try:
        created_tickets = ticket_manager.create_all_project_tickets()
        print(f"✅ Successfully created {len(created_tickets)} tickets!")
        
        # Show first few created tickets
        for ticket_id, jira_key in list(created_tickets.items())[:10]:
            print(f"  {ticket_id} → {jira_key}")
        
        if len(created_tickets) > 10:
            print(f"  ... and {len(created_tickets) - 10} more tickets")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating tickets: {e}")
        return False

def list_tickets():
    """List all tickets from cache"""
    print("📋 Listing all tickets...")
    config = load_config()
    
    client = JiraClient(
        url=config['jira_url'],
        username=config['jira_username'],
        api_token=config['jira_api_token'],
        project_key=config['project_key']
    )
    
    ticket_manager = TicketManager(client)
    tickets = ticket_manager.get_all_tickets()
    
    if not tickets:
        print("No tickets found. Run 'sync' first.")
        return
    
    print(f"Found {len(tickets)} tickets:\n")
    
    # Group by type
    epics = [t for t in tickets if t['issue_type'] == 'Epic']
    stories = [t for t in tickets if t['issue_type'] == 'Story']
    tasks = []  # No tasks or sub-tasks - using Epic → Story structure only
    
    def print_tickets(ticket_list, title):
        if ticket_list:
            print(f"📌 {title} ({len(ticket_list)}):")
            for ticket in ticket_list[:5]:  # Show first 5
                status_emoji = "✅" if "done" in ticket['status'].lower() else "🔄" if "progress" in ticket['status'].lower() else "📝"
                print(f"  {status_emoji} {ticket['key']}: {ticket['summary'][:60]}...")
            if len(ticket_list) > 5:
                print(f"  ... and {len(ticket_list) - 5} more")
            print()
    
    print_tickets(epics, "Epics")
    print_tickets(stories, "Stories")  
    print_tickets(tasks, "Tasks")

def update_ticket():
    """Update a specific ticket"""
    ticket_key = input("Enter ticket key (e.g., GLO-1): ").strip().upper()
    if not ticket_key:
        print("❌ Ticket key is required")
        return False
    
    config = load_config()
    client = JiraClient(
        url=config['jira_url'],
        username=config['jira_username'],
        api_token=config['jira_api_token'],
        project_key=config['project_key']
    )
    
    ticket_manager = TicketManager(client)
    ticket = ticket_manager.get_ticket_by_key(ticket_key)
    
    if not ticket:
        print(f"❌ Ticket {ticket_key} not found. Run 'sync' first.")
        return False
    
    print(f"📋 Current ticket: {ticket['key']}")
    print(f"   Summary: {ticket['summary']}")
    print(f"   Status: {ticket['status']}")
    print(f"   Type: {ticket['issue_type']}")
    print()
    
    # Get updates
    new_summary = input(f"New summary (press Enter to keep current): ").strip()
    new_description = input(f"New description (press Enter to keep current): ").strip()
    
    print("\nAvailable statuses: To Do, In Progress, Done, Blocked")
    new_status = input(f"New status (press Enter to keep current): ").strip()
    
    if not new_summary and not new_description and not new_status:
        print("No changes specified.")
        return False
    
    # Update ticket
    try:
        success = ticket_manager.update_ticket(
            ticket_key,
            summary=new_summary if new_summary else None,
            description=new_description if new_description else None,
            status=new_status if new_status else None
        )
        
        if success:
            print(f"✅ Successfully updated {ticket_key}")
        else:
            print(f"❌ Failed to update {ticket_key}")
            
        return success
        
    except Exception as e:
        print(f"❌ Error updating ticket: {e}")
        return False

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Jira Ticket Manager - Standalone Scripts')
    parser.add_argument('command', choices=['test', 'sync', 'create', 'list', 'update'], 
                       help='Command to execute')
    
    args = parser.parse_args()
    
    print("🎯 Global Underwriting - Jira Ticket Manager")
    print("=" * 50)
    
    if args.command == 'test':
        success = test_connection()
    elif args.command == 'sync':
        success = sync_tickets()
    elif args.command == 'create':
        success = create_all_tickets()
    elif args.command == 'list':
        list_tickets()
        success = True
    elif args.command == 'update':
        success = update_ticket()
    else:
        print(f"❌ Unknown command: {args.command}")
        success = False
    
    if success:
        print("\n✅ Operation completed successfully!")
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()