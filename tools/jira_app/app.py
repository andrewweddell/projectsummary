"""
Flask Web App for Jira Ticket Management
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file, Response, stream_template
import os
import json
import time
import queue
from threading import Thread
from jira_client import JiraClient
from ticket_manager import TicketManager
from confluence_client import ConfluenceClient
from progress_tracker import progress_tracker, run_with_progress
import logging
from datetime import datetime
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Global variables for clients
jira_client = None
ticket_manager = None
confluence_client = None

def initialize_clients():
    """Initialize Jira client and ticket manager from config"""
    global jira_client, ticket_manager, confluence_client
    
    try:
        # Load configuration
        config_file = 'config.json'
        if not os.path.exists(config_file):
            logger.warning("No config file found. Please configure Jira connection.")
            return False
            
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        jira_client = JiraClient(
            url=config['jira_url'],
            username=config['jira_username'], 
            api_token=config['jira_api_token'],
            project_key=config['project_key']
        )
        
        # Test connection
        if jira_client.test_connection():
            ticket_manager = TicketManager(jira_client)
            logger.info("Successfully connected to Jira")
            
            # Initialize Confluence client
            # Use Jira credentials as fallback for Confluence
            confluence_url = config.get('confluence_url', config['jira_url'].replace('atlassian.net', 'atlassian.net/wiki'))
            confluence_username = config.get('confluence_username', config['jira_username'])
            confluence_token = config.get('confluence_api_token', config['jira_api_token'])
            
            try:
                confluence_client = ConfluenceClient(
                    url=confluence_url,
                    username=confluence_username,
                    api_token=confluence_token
                )
                if confluence_client.test_connection():
                    logger.info("Successfully connected to Confluence")
                else:
                    logger.warning("Failed to connect to Confluence")
            except Exception as e:
                logger.warning(f"Could not initialize Confluence client: {e}")
            
            return True
        else:
            logger.error("Failed to connect to Jira")
            return False
            
    except Exception as e:
        logger.error(f"Error initializing clients: {e}")
        return False

@app.route('/')
def index():
    """Main dashboard page"""
    if not jira_client:
        return redirect(url_for('config'))
        
    try:
        tickets = ticket_manager.get_all_tickets()
        
        # Get summary stats (Epics + Stories only)
        stats = {
            'total': len(tickets),
            'epics': len([t for t in tickets if t['issue_type'] == 'Epic']),
            'stories': len([t for t in tickets if t['issue_type'] == 'Story']),
            'done': len([t for t in tickets if t['status'].lower() in ['done', 'closed', 'resolved']]),
            'in_progress': len([t for t in tickets if 'progress' in t['status'].lower()]),
            'todo': len([t for t in tickets if t['status'].lower() in ['to do', 'open', 'new']])
        }
        
        return render_template('index.html', tickets=tickets, stats=stats)
        
    except Exception as e:
        flash(f"Error loading tickets: {e}", "error")
        return render_template('index.html', tickets=[], stats={})

@app.route('/config', methods=['GET', 'POST'])
def config():
    """Configuration page for Jira connection"""
    if request.method == 'POST':
        # Load existing config first to preserve other settings
        existing_config = {}
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                existing_config = json.load(f)
        
        config_data = existing_config.copy()
        config_data.update({
            'jira_url': request.form['jira_url'],
            'jira_username': request.form['jira_username'],
            'jira_api_token': request.form['jira_api_token'],
            'project_key': request.form['project_key']
        })
        
        # Save configuration
        try:
            with open('config.json', 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Try to initialize clients
            if initialize_clients():
                flash("Configuration saved and connection successful!", "success")
                return redirect(url_for('index'))
            else:
                flash("Configuration saved but connection failed. Please check your settings.", "error")
                
        except Exception as e:
            flash(f"Error saving configuration: {e}", "error")
    
    # Load existing config if available
    existing_config = {}
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                existing_config = json.load(f)
                # Don't show API tokens for security
                if 'jira_api_token' in existing_config:
                    existing_config['jira_api_token'] = '***'
                if 'confluence_api_token' in existing_config:
                    existing_config['confluence_api_token'] = '***'
        except:
            pass
            
    return render_template('config.html', config=existing_config)

@app.route('/sync', methods=['POST'])
def sync_tickets():
    """Start syncing tickets from Jira with progress tracking"""
    if not ticket_manager:
        return jsonify({"error": "Not connected to Jira"}), 400
    
    # Start the operation first to get operation_id
    operation_id = progress_tracker.start_operation(
        "ticket_sync",
        total_steps=100,
        operation_name="Syncing Tickets from Jira"
    )
        
    def sync_tickets_with_progress(op_id):
        """Background task to sync tickets with progress tracking"""
        try:
            # Add a small delay to ensure the progress modal has time to connect
            time.sleep(0.5)
            
            # Create a progress callback that uses the existing operation_id
            def progress_callback(step, message=None, details=None, total=None):
                if total:
                    progress_tracker.active_operations[op_id].total_steps = total
                progress_tracker.update_progress(op_id, step, message, details)
            
            # Send initial progress update
            progress_tracker.update_progress(op_id, 0, "Starting sync from Jira...")
            
            # Run the sync with our progress callback
            result = ticket_manager.sync_from_jira(
                progress_callback=progress_callback, 
                operation_id=op_id
            )
            
            # Complete the operation
            progress_tracker.complete_operation(
                op_id, 
                True, 
                f"Successfully synced {len(result)} tickets from Jira", 
                {"data": result, "synced_tickets": len(result)}
            )
            
            logger.info(f"Sync operation {op_id} completed successfully with {len(result)} tickets")
            
        except Exception as e:
            logger.exception(f"Error in background ticket sync operation {op_id}")
            progress_tracker.complete_operation(
                op_id, 
                False, 
                f"Sync failed: {str(e)}"
            )
    
    # Start background task with the operation_id
    thread = Thread(target=sync_tickets_with_progress, args=(operation_id,), daemon=True)
    thread.start()
    
    return jsonify({"operation_id": operation_id})

@app.route('/ticket/<ticket_key>')
def view_ticket(ticket_key):
    """View individual ticket details"""
    if not ticket_manager:
        flash("Not connected to Jira", "error")
        return redirect(url_for('config'))
        
    ticket = ticket_manager.get_ticket_by_key(ticket_key)
    if not ticket:
        flash(f"Ticket {ticket_key} not found", "error")
        return redirect(url_for('index'))
        
    return render_template('ticket_detail.html', ticket=ticket)

@app.route('/edit_ticket/<ticket_key>', methods=['GET', 'POST'])
def edit_ticket(ticket_key):
    """Edit ticket details"""
    if not ticket_manager:
        flash("Not connected to Jira", "error")
        return redirect(url_for('config'))
        
    ticket = ticket_manager.get_ticket_by_key(ticket_key)
    if not ticket:
        flash(f"Ticket {ticket_key} not found", "error")
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        summary = request.form.get('summary')
        description = request.form.get('description') 
        status = request.form.get('status')
        
        try:
            success = ticket_manager.update_ticket(ticket_key, summary, description, status)
            if success:
                flash(f"Successfully updated {ticket_key}", "success")
                return redirect(url_for('view_ticket', ticket_key=ticket_key))
            else:
                flash(f"Failed to update {ticket_key}", "error")
        except Exception as e:
            flash(f"Error updating ticket: {e}", "error")
            
    return render_template('edit_ticket.html', ticket=ticket)

@app.route('/create_all_tickets', methods=['POST'])
def create_all_tickets():
    """Start creating all project tickets in Jira with progress tracking"""
    if not ticket_manager:
        return jsonify({"error": "Not connected to Jira"}), 400
    
    # Start the operation first to get operation_id
    operation_id = progress_tracker.start_operation(
        "ticket_creation", 
        total_steps=100, 
        operation_name="Creating All Project Tickets"
    )
        
    def create_tickets_with_progress(op_id):
        """Background task to create tickets with progress tracking"""
        try:
            # Add a small delay to ensure the progress modal has time to connect
            time.sleep(0.5)
            
            # Create a progress callback that uses the existing operation_id
            def progress_callback(step, message=None, details=None, total=None):
                if total:
                    progress_tracker.active_operations[op_id].total_steps = total
                progress_tracker.update_progress(op_id, step, message, details)
            
            # Send initial progress update
            progress_tracker.update_progress(op_id, 0, "Starting ticket creation...")
            
            # Run the ticket creation with our progress callback
            result = ticket_manager.create_all_project_tickets(
                progress_callback=progress_callback, 
                operation_id=op_id
            )
            
            # Complete the operation
            progress_tracker.complete_operation(
                op_id, 
                True, 
                f"Successfully created {len(result)} tickets", 
                {"data": result, "created_tickets": len(result)}
            )
            
            logger.info(f"Ticket creation operation {op_id} completed successfully with {len(result)} tickets")
            
        except Exception as e:
            logger.exception(f"Error in background ticket creation operation {op_id}")
            progress_tracker.complete_operation(
                op_id, 
                False, 
                f"Ticket creation failed: {str(e)}"
            )
    
    # Start background task with the operation_id
    thread = Thread(target=create_tickets_with_progress, args=(operation_id,), daemon=True)
    thread.start()
    
    return jsonify({"operation_id": operation_id})

@app.route('/search')
def search():
    """Search tickets"""
    if not ticket_manager:
        return jsonify({"error": "Not connected to Jira"})
        
    search_term = request.args.get('q', '')
    if not search_term:
        return jsonify([])
        
    try:
        results = ticket_manager.search_tickets(search_term)
        return jsonify([{
            'key': ticket['key'],
            'summary': ticket['summary'],
            'status': ticket['status'],
            'issue_type': ticket['issue_type']
        } for ticket in results])
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/tickets')
def api_tickets():
    """API endpoint to get all tickets as JSON"""
    if not ticket_manager:
        return jsonify({"error": "Not connected to Jira"})
        
    try:
        tickets = ticket_manager.get_all_tickets()
        return jsonify(tickets)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/export/markdown')
def export_markdown():
    """Export tickets to markdown format for project managers"""
    if not ticket_manager:
        flash("Not connected to Jira. Please configure connection first.", "error")
        return redirect(url_for('config'))
        
    try:
        file_path = ticket_manager.export_to_markdown()
        flash(f"Project status report exported successfully to {file_path}", "success")
        return send_file(file_path, as_attachment=True, download_name=file_path)
    except Exception as e:
        flash(f"Error exporting markdown report: {e}", "error")
        return redirect(url_for('index'))

@app.route('/progress/<operation_id>')
def progress_stream(operation_id):
    """Server-Sent Events endpoint for progress updates"""
    def event_stream():
        # Create a queue for this client
        client_queue = queue.Queue()
        progress_tracker.add_listener(operation_id, client_queue)
        
        try:
            # Send initial progress state
            initial_progress = progress_tracker.get_operation_progress(operation_id)
            if initial_progress:
                yield f"data: {json.dumps(initial_progress)}\n\n"
            else:
                # Operation might not be started yet or completed very quickly
                # Wait a moment for it to appear
                for i in range(10):  # Wait up to 1 second
                    time.sleep(0.1)
                    initial_progress = progress_tracker.get_operation_progress(operation_id)
                    if initial_progress:
                        yield f"data: {json.dumps(initial_progress)}\n\n"
                        break
                else:
                    # Still not found, operation likely completed already
                    logger.debug(f"Operation {operation_id} completed before progress stream could connect")
                    yield f"data: {{\"status\": \"completed\", \"percentage\": 100, \"status_message\": \"Operation completed successfully\", \"message\": \"Sync completed\"}}\n\n"
                    return
            
            # Stream progress updates
            while True:
                try:
                    # Wait for progress update with timeout
                    progress_data = client_queue.get(timeout=30)
                    yield f"data: {json.dumps(progress_data)}\n\n"
                    
                    # Stop streaming if operation completed
                    if progress_data.get('status') in ['completed', 'failed']:
                        break
                        
                except queue.Empty:
                    # Send keepalive
                    yield f"data: {{\"keepalive\": true}}\n\n"
                    
        except Exception as e:
            logger.exception("Error in progress stream")
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
        finally:
            # Clean up listener
            progress_tracker.remove_listener(operation_id, client_queue)
    
    return Response(event_stream(), mimetype='text/event-stream', 
                   headers={'Cache-Control': 'no-cache', 
                           'Connection': 'keep-alive',
                           'Access-Control-Allow-Origin': '*'})

@app.route('/api/progress/<operation_id>')
def get_progress_status(operation_id):
    """Get current progress status for an operation"""
    progress = progress_tracker.get_operation_progress(operation_id)
    if not progress:
        return jsonify({"error": "Operation not found"}), 404
    return jsonify(progress)

@app.route('/download/latest_report')
def download_latest_report():
    """Download the latest project status report"""
    report_file = "project_status_report_latest.md"
    
    if not os.path.exists(report_file):
        flash("No project report available. Please sync tickets first.", "warning")
        return redirect(url_for('index'))
    
    try:
        return send_file(report_file, as_attachment=True, download_name=f"Global_Underwriting_Status_Report.md")
    except Exception as e:
        flash(f"Error downloading report: {e}", "error")
        return redirect(url_for('index'))

# Confluence Configuration Route
@app.route('/confluence/config', methods=['POST'])
def confluence_config():
    """Save Confluence configuration"""
    # Load existing config
    existing_config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            existing_config = json.load(f)
    
    # Update with Confluence settings
    existing_config.update({
        'confluence_url': request.form.get('confluence_url', ''),
        'confluence_username': request.form.get('confluence_username', ''),
        'confluence_api_token': request.form.get('confluence_api_token', '')
    })
    
    # Save configuration
    try:
        with open('config.json', 'w') as f:
            json.dump(existing_config, f, indent=2)
        
        # Try to initialize clients
        if initialize_clients():
            flash("Confluence configuration saved successfully!", "success")
        else:
            flash("Configuration saved but connection failed. Please check your settings.", "warning")
    except Exception as e:
        flash(f"Error saving configuration: {e}", "error")
    
    return redirect(url_for('config'))

# Confluence Routes
@app.route('/confluence')
def confluence_pages():
    """Display Confluence pages from GLO space"""
    if not confluence_client:
        flash("Confluence not configured. Please add Confluence credentials in config.", "warning")
        return redirect(url_for('config'))
    
    try:
        # Get pages from GLO space
        pages = confluence_client.get_pages_from_space('GLO')
        
        # Format pages for display
        formatted_pages = []
        for page in pages:
            formatted_page = confluence_client.format_page_info(page)
            formatted_pages.append(formatted_page)
        
        # Sort by last modified date
        formatted_pages.sort(key=lambda x: x.get('last_modified', ''), reverse=True)
        
        return render_template('confluence.html', pages=formatted_pages)
        
    except Exception as e:
        flash(f"Error loading Confluence pages: {e}", "error")
        return render_template('confluence.html', pages=[])

@app.route('/confluence/process', methods=['POST'])
def process_confluence_pages():
    """Process selected Confluence pages and download to versioned folder"""
    if not confluence_client:
        return jsonify({"error": "Confluence not configured"}), 400
    
    try:
        # Get selected page IDs from form
        selected_pages = request.form.getlist('selected_pages')
        
        if not selected_pages:
            return jsonify({"error": "No pages selected"}), 400
        
        # Create versioned folder structure
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_folder = 'confluence_exports'
        version_folder = os.path.join(base_folder, f'GLO_export_{timestamp}')
        
        # Create directories
        os.makedirs(version_folder, exist_ok=True)
        
        # Start progress operation
        operation_id = progress_tracker.start_operation(
            "confluence_export",
            total_steps=len(selected_pages),
            operation_name="Exporting Confluence Pages"
        )
        
        def export_pages_with_progress(op_id, page_ids, folder):
            """Background task to export pages with progress tracking"""
            try:
                # Add a small delay to ensure the progress modal has time to connect
                time.sleep(0.5)
                
                # Send initial progress update
                progress_tracker.update_progress(op_id, 0, f"Starting export of {len(page_ids)} pages...")
                
                exported_files = []
                
                for idx, page_id in enumerate(page_ids):
                    # Update progress
                    progress_tracker.update_progress(
                        op_id,
                        idx + 1,
                        f"Processing page {idx + 1} of {len(page_ids)}",
                        {"current_page": page_id}
                    )
                    
                    # Get full page content
                    page_data = confluence_client.get_page_content(page_id, expand_body=True)
                    
                    if page_data:
                        # Format page info
                        page_info = confluence_client.format_page_info(page_data)
                        
                        # Create safe filename
                        safe_title = "".join(c for c in page_info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        safe_title = safe_title[:100]  # Limit length
                        
                        # Save page content as HTML
                        html_file = os.path.join(folder, f"{safe_title}.html")
                        with open(html_file, 'w', encoding='utf-8') as f:
                            # Write formatted HTML with metadata
                            f.write(f"<!DOCTYPE html>\n<html>\n<head>\n")
                            f.write(f"<title>{page_info['title']}</title>\n")
                            f.write(f"<meta charset='utf-8'>\n")
                            f.write(f"<!-- Confluence Page ID: {page_info['id']} -->\n")
                            f.write(f"<!-- Last Modified: {page_info['last_modified']} -->\n")
                            f.write(f"<!-- Version: {page_info['version']} -->\n")
                            f.write(f"<!-- Modified By: {page_info['modified_by']} -->\n")
                            f.write(f"</head>\n<body>\n")
                            f.write(f"<h1>{page_info['title']}</h1>\n")
                            
                            if 'body' in page_data and 'storage' in page_data['body']:
                                f.write(page_data['body']['storage']['value'])
                            
                            f.write("\n</body>\n</html>")
                        
                        # Also save as markdown/text
                        text_file = os.path.join(folder, f"{safe_title}.txt")
                        with open(text_file, 'w', encoding='utf-8') as f:
                            f.write(f"Title: {page_info['title']}\n")
                            f.write(f"Space: {page_info['space_name']} ({page_info['space']})\n")
                            f.write(f"Last Modified: {page_info['last_modified']}\n")
                            f.write(f"Modified By: {page_info['modified_by']}\n")
                            f.write(f"Version: {page_info['version']}\n")
                            f.write(f"URL: {page_info['url']}\n")
                            f.write("-" * 80 + "\n\n")
                            
                            if 'body' in page_data and 'storage' in page_data['body']:
                                cleaned_content = confluence_client.clean_html_content(
                                    page_data['body']['storage']['value']
                                )
                                f.write(cleaned_content)
                        
                        # Download attachments if any
                        attachments = confluence_client.get_page_attachments(page_id)
                        if attachments:
                            attachment_folder = os.path.join(folder, f"{safe_title}_attachments")
                            os.makedirs(attachment_folder, exist_ok=True)
                            
                            for attachment in attachments:
                                if '_links' in attachment and 'download' in attachment['_links']:
                                    download_url = attachment['_links']['download']
                                    attachment_content = confluence_client.download_attachment(download_url)
                                    
                                    if attachment_content:
                                        attachment_file = os.path.join(
                                            attachment_folder,
                                            attachment.get('title', 'attachment')
                                        )
                                        with open(attachment_file, 'wb') as f:
                                            f.write(attachment_content)
                        
                        exported_files.append({
                            'page_id': page_id,
                            'title': page_info['title'],
                            'html_file': html_file,
                            'text_file': text_file
                        })
                    
                    time.sleep(0.1)  # Rate limiting
                
                # Create index file
                index_file = os.path.join(folder, 'index.html')
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write("<!DOCTYPE html>\n<html>\n<head>\n")
                    f.write("<title>Confluence Export - GLO Space</title>\n")
                    f.write("<style>body { font-family: Arial, sans-serif; } ")
                    f.write("a { text-decoration: none; color: #0052cc; } ")
                    f.write("li { margin: 10px 0; }</style>\n")
                    f.write("</head>\n<body>\n")
                    f.write(f"<h1>Confluence Export - GLO Space</h1>\n")
                    f.write(f"<p>Export Date: {timestamp}</p>\n")
                    f.write(f"<p>Total Pages: {len(exported_files)}</p>\n")
                    f.write("<h2>Exported Pages:</h2>\n<ul>\n")
                    
                    for file_info in exported_files:
                        html_filename = os.path.basename(file_info['html_file'])
                        f.write(f"<li><a href='{html_filename}'>{file_info['title']}</a></li>\n")
                    
                    f.write("</ul>\n</body>\n</html>")
                
                # Complete operation
                progress_tracker.complete_operation(
                    op_id,
                    True,
                    f"Successfully exported {len(exported_files)} pages to {version_folder}",
                    {"exported_files": exported_files, "folder": version_folder}
                )
                
            except Exception as e:
                logger.exception(f"Error exporting Confluence pages: {e}")
                progress_tracker.complete_operation(
                    op_id,
                    False,
                    f"Export failed: {str(e)}"
                )
        
        # Start background task
        thread = Thread(
            target=export_pages_with_progress,
            args=(operation_id, selected_pages, version_folder),
            daemon=True
        )
        thread.start()
        
        return jsonify({
            "operation_id": operation_id,
            "message": f"Starting export of {len(selected_pages)} pages",
            "folder": version_folder
        })
        
    except Exception as e:
        logger.exception(f"Error processing Confluence pages: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/confluence/api/pages')
def api_confluence_pages():
    """API endpoint to get Confluence pages as JSON"""
    if not confluence_client:
        return jsonify({"error": "Confluence not configured"}), 400
    
    try:
        space_key = request.args.get('space', 'GLO')
        pages = confluence_client.get_pages_from_space(space_key)
        
        formatted_pages = []
        for page in pages:
            formatted_pages.append(confluence_client.format_page_info(page))
        
        return jsonify(formatted_pages)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Try to initialize clients on startup
    initialize_clients()
    
    # Run the app with threading support for SSE
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)