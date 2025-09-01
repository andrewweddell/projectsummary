"""
Confluence Client for connecting to Atlassian Confluence API
"""
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from datetime import datetime
import logging
import time
from typing import List, Dict, Optional
import re

logger = logging.getLogger(__name__)

class ConfluenceClient:
    """Client for interacting with Confluence API"""
    
    def __init__(self, url: str, username: str, api_token: str):
        """
        Initialize Confluence client
        
        Args:
            url: Confluence base URL (e.g., https://appsure.atlassian.net/wiki)
            username: User email for authentication
            api_token: API token for authentication
        """
        self.base_url = url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.auth = HTTPBasicAuth(username, api_token)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def test_connection(self) -> bool:
        """Test the connection to Confluence"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/space")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_space(self, space_key: str) -> Optional[Dict]:
        """
        Get space information
        
        Args:
            space_key: The space key (e.g., 'GLO')
            
        Returns:
            Space information dict or None if not found
        """
        try:
            response = self.session.get(
                f"{self.base_url}/rest/api/space/{space_key}",
                params={'expand': 'description.plain,homepage'}
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get space: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting space: {e}")
            return None
    
    def get_pages_from_space(self, space_key: str, limit: int = 100, start: int = 0) -> List[Dict]:
        """
        Get all pages from a space with pagination
        
        Args:
            space_key: The space key (e.g., 'GLO')
            limit: Number of pages per request
            start: Starting index for pagination
            
        Returns:
            List of page dictionaries
        """
        all_pages = []
        
        while True:
            try:
                response = self.session.get(
                    f"{self.base_url}/rest/api/content",
                    params={
                        'spaceKey': space_key,
                        'type': 'page',
                        'status': 'current',
                        'expand': 'version,history,ancestors,space',
                        'limit': limit,
                        'start': start
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Failed to get pages: {response.status_code} - {response.text}")
                    break
                    
                data = response.json()
                pages = data.get('results', [])
                
                if not pages:
                    break
                    
                all_pages.extend(pages)
                
                # Check if there are more pages
                if len(pages) < limit:
                    break
                    
                start += limit
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching pages: {e}")
                break
                
        return all_pages
    
    def get_page_content(self, page_id: str, expand_body: bool = True) -> Optional[Dict]:
        """
        Get detailed page content
        
        Args:
            page_id: The page ID
            expand_body: Whether to include the page body content
            
        Returns:
            Page content dict or None if not found
        """
        try:
            expand_params = 'version,history,ancestors,space'
            if expand_body:
                expand_params += ',body.storage,body.view'
                
            response = self.session.get(
                f"{self.base_url}/rest/api/content/{page_id}",
                params={'expand': expand_params}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get page content: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting page content: {e}")
            return None
    
    def get_page_attachments(self, page_id: str) -> List[Dict]:
        """
        Get attachments for a page
        
        Args:
            page_id: The page ID
            
        Returns:
            List of attachment dictionaries
        """
        try:
            response = self.session.get(
                f"{self.base_url}/rest/api/content/{page_id}/child/attachment",
                params={'expand': 'version,container'}
            )
            
            if response.status_code == 200:
                return response.json().get('results', [])
            else:
                logger.error(f"Failed to get attachments: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting attachments: {e}")
            return []
    
    def download_attachment(self, download_url: str) -> Optional[bytes]:
        """
        Download an attachment
        
        Args:
            download_url: The attachment download URL
            
        Returns:
            Attachment content as bytes or None
        """
        try:
            # Ensure URL is absolute
            if not download_url.startswith('http'):
                download_url = self.base_url + download_url
                
            response = self.session.get(download_url)
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"Failed to download attachment: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error downloading attachment: {e}")
            return None
    
    def export_page_as_pdf(self, page_id: str) -> Optional[bytes]:
        """
        Export a page as PDF
        
        Args:
            page_id: The page ID
            
        Returns:
            PDF content as bytes or None
        """
        try:
            # Confluence PDF export endpoint
            pdf_url = f"{self.base_url}/spaces/flyingpdf/pdfpageexport.action?pageId={page_id}"
            
            response = self.session.get(pdf_url)
            
            if response.status_code == 200:
                return response.content
            else:
                logger.warning(f"PDF export not available, falling back to HTML export")
                return None
                
        except Exception as e:
            logger.error(f"Error exporting page as PDF: {e}")
            return None
    
    def search_pages(self, cql: str, limit: int = 50) -> List[Dict]:
        """
        Search pages using CQL (Confluence Query Language)
        
        Args:
            cql: CQL query string
            limit: Maximum number of results
            
        Returns:
            List of matching pages
        """
        try:
            response = self.session.get(
                f"{self.base_url}/rest/api/content/search",
                params={
                    'cql': cql,
                    'limit': limit,
                    'expand': 'version,history,space'
                }
            )
            
            if response.status_code == 200:
                return response.json().get('results', [])
            else:
                logger.error(f"Search failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching pages: {e}")
            return []
    
    def format_page_info(self, page: Dict) -> Dict:
        """
        Format page information for display
        
        Args:
            page: Raw page data from API
            
        Returns:
            Formatted page information
        """
        formatted = {
            'id': page.get('id'),
            'title': page.get('title'),
            'type': page.get('type', 'page'),
            'space': page.get('space', {}).get('key'),
            'space_name': page.get('space', {}).get('name'),
            'created_date': None,
            'created_by': None,
            'last_modified': None,
            'modified_by': None,
            'version': None,
            'url': None,
            'ancestors': []
        }
        
        # Extract history information
        if 'history' in page:
            history = page['history']
            formatted['created_date'] = history.get('createdDate')
            formatted['created_by'] = history.get('createdBy', {}).get('displayName')
            
        # Extract version information
        if 'version' in page:
            version = page['version']
            formatted['version'] = version.get('number')
            formatted['last_modified'] = version.get('when')
            formatted['modified_by'] = version.get('by', {}).get('displayName')
            
        # Build URL
        if '_links' in page:
            formatted['url'] = self.base_url + page['_links'].get('webui', '')
            
        # Extract ancestors (parent pages)
        if 'ancestors' in page:
            formatted['ancestors'] = [
                {'id': a['id'], 'title': a['title']} 
                for a in page['ancestors']
            ]
            
        return formatted
    
    def clean_html_content(self, html_content: str) -> str:
        """
        Clean HTML content from Confluence storage format
        
        Args:
            html_content: Raw HTML from Confluence
            
        Returns:
            Cleaned text content
        """
        # Remove Confluence-specific tags
        cleaned = re.sub(r'<ac:[^>]+>', '', html_content)
        cleaned = re.sub(r'</ac:[^>]+>', '', cleaned)
        cleaned = re.sub(r'<ri:[^>]+/>', '', cleaned)
        
        # Remove HTML tags but keep content
        cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
        
        # Clean up whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned.strip()