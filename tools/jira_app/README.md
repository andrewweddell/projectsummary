# Global Underwriting Jira Manager

A simple web application and CLI tools for managing Jira tickets for the Global Underwriting Appsure implementation project.

## Features

### Web Interface
- 📊 **Dashboard** - View project statistics and ticket overview
- 🔍 **Search** - Real-time ticket search functionality
- 📝 **Ticket Management** - View and edit individual tickets
- 🔄 **Sync** - Pull tickets from Jira and push updates back
- 📚 **Confluence Integration** - Browse and export pages from GLO space
- 📥 **Page Export** - Download Confluence pages to versioned folders
- ⚙️ **Configuration** - Easy setup of Jira and Confluence connections

### Command Line Tools
- 🧪 **Connection Testing** - Verify Jira connectivity
- 📥 **Bulk Sync** - Sync all tickets from Jira
- 🚀 **Bulk Creation** - Create all 117 project tickets at once
- 📋 **Ticket Listing** - View tickets in terminal
- ✏️ **Ticket Updates** - Update tickets via CLI

## Quick Start

### 1. Prerequisites
- Python 3.7+
- Jira account with API access
- Project permissions in Jira

### 2. Installation
```bash
cd jira_app
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration
1. Copy the example config:
```bash
cp config.example.json config.json
```

2. Edit `config.json` with your details:
```json
{
  "jira_url": "https://appsure.atlassian.net",
  "jira_username": "your.email@company.com", 
  "jira_api_token": "your_api_token_here",
  "project_key": "GLO",
  "confluence_url": "https://appsure.atlassian.net/wiki",
  "confluence_username": "your.email@company.com",
  "confluence_api_token": "your_api_token_here"
}
```

3. Get your API token from [Atlassian](https://id.atlassian.com/manage-profile/security/api-tokens)

### 4. Test Connection
```bash
source venv/bin/activate
python standalone_scripts.py test
```

### 5. Start Web App
```bash
source venv/bin/activate
python app.py
```

Visit http://localhost:5001

## Usage

### Web Interface

#### Initial Setup
1. Go to **Configuration** page
2. Enter your Jira details
3. Click **Test Connection**
4. Save configuration

#### Managing Tickets
1. **Sync from Jira**: Pull all existing tickets
2. **Create All Tickets**: Bulk create the 117 project tickets
3. **View/Edit**: Click on any ticket to view or edit
4. **Search**: Use the sidebar search box

#### Confluence Integration
1. **Navigate to Confluence**: Click "Confluence" in the sidebar
2. **Browse Pages**: View all pages from the GLO space
3. **Select Pages**: Check the pages you want to export
4. **Process Pages**: Click "Process Selected Pages" to download
5. **Access Exports**: Find exported pages in `confluence_exports/` folder with timestamps

### Command Line Interface

#### Available Commands
```bash
# Activate virtual environment first
source venv/bin/activate

# Test Jira connection
python standalone_scripts.py test

# Sync all tickets from Jira  
python standalone_scripts.py sync

# Create all 117 project tickets
python standalone_scripts.py create

# List all tickets
python standalone_scripts.py list

# Update a specific ticket
python standalone_scripts.py update
```

#### Examples
```bash
# Activate virtual environment
source venv/bin/activate

# Quick connection test
python standalone_scripts.py test

# Sync and list tickets
python standalone_scripts.py sync
python standalone_scripts.py list

# Create all project tickets (one-time setup)
python standalone_scripts.py create
```

## Project Structure

```
jira_app/
├── app.py                 # Flask web application
├── jira_client.py         # Jira REST API client
├── confluence_client.py   # Confluence REST API client
├── ticket_manager.py      # Ticket management logic
├── standalone_scripts.py  # CLI tools
├── requirements.txt       # Python dependencies
├── config.example.json    # Configuration template
├── config.json           # Your configuration (create this)
├── ticket_cache.json     # Local ticket cache (auto-generated)
├── confluence_exports/    # Exported Confluence pages (auto-created)
└── templates/            # Web interface templates
    ├── base.html
    ├── index.html
    ├── config.html
    ├── confluence.html
    ├── ticket_detail.html
    └── edit_ticket.html
```

## Ticket Structure

The app manages 117 tickets for the Global Underwriting project using a **two-level hierarchy**:

### Structure: Epics + Stories Only
- **1 Epic (GLO-1)**: Overall project container
- **116 Stories (GLO-2 to GLO-117)**: Individual work items

### Distribution:
- **GLO-1**: Epic - Global Underwriting Appsure Platform Implementation
- **GLO-2 to GLO-43**: Sprint 1-2 - Foundation, Planning & Core Configuration
- **GLO-44 to GLO-87**: Sprint 3-4 - Product Implementation & Testing
- **GLO-88 to GLO-117**: Sprint 5-6 - Training, Go-Live & NFRs

**Why this structure?** 
- ✅ Simple hierarchy (Epic → Stories)
- ✅ Each story is a meaningful, independent work unit
- ✅ Perfect granularity for project tracking
- ✅ Easy to assign, track, and report on
- ✅ No complex parent-child relationships

## API Endpoints

The web app provides REST API endpoints:

- `GET /api/tickets` - Get all tickets as JSON
- `GET /search?q=term` - Search tickets
- `POST /create_all_tickets` - Create all project tickets

## Configuration Details

### Required Jira Permissions
Your Jira account needs:
- Browse Projects
- Create Issues (Stories and Epics)
- Edit Issues
- Manage Project (for Epic creation)

### Custom Fields
Some Jira instances use different field IDs. You may need to adjust:
- Epic Link: `customfield_10014` (in `jira_client.py`)
- Epic Name: `customfield_10011` (in `jira_client.py`)

### Security
- API tokens are stored in `config.json` - keep this file secure
- Don't commit `config.json` to version control
- Use environment variables for production deployments

## Troubleshooting

### Connection Issues
1. Verify Jira URL is correct (include https://)
2. Check username is your email address
3. Ensure API token is valid and not expired
4. Confirm project key exists and you have access

### Permission Errors
- Make sure you can create/edit issues in the project
- Epic creation requires project management permissions
- Some custom fields may need admin access

### Sync Issues
- Run `python standalone_scripts.py sync` to refresh cache
- Check Jira query limits (default: 1000 issues)
- Large projects may need pagination (not implemented)

## Development

### Adding New Features
1. Backend: Extend `jira_client.py` or `ticket_manager.py`
2. Frontend: Add routes to `app.py` and templates
3. CLI: Add commands to `standalone_scripts.py`

### Testing
```bash
# Activate virtual environment
source venv/bin/activate

# Test individual components
python -c "from jira_client import JiraClient; print('Import OK')"
python standalone_scripts.py test
```

## Support

For issues with:
- **Jira API**: Check [Atlassian REST API docs](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)
- **This app**: Check the code comments and error messages
- **Permissions**: Contact your Jira administrator

## License

This is a custom tool for the Global Underwriting project. Use at your own discretion.