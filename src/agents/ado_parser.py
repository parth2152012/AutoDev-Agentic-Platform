"""
Azure DevOps Parser Agent

Responsible for:
- Connecting to Azure DevOps
- Fetching user stories
- Parsing and extracting requirements
- Converting ADO requirements into agent tasks
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

try:
    from azure.devops.connection import Connection
    from msrest.authentication import BasicAuthentication
except ImportError:
    Connection = None
    BasicAuthentication = None

logger = logging.getLogger(__name__)


@dataclass
class UserStory:
    """Represents an Azure DevOps user story"""
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    assigned_to: Optional[str] = None
    priority: Optional[int] = None
    state: Optional[str] = None
    tags: List[str] = None
    created_date: Optional[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user story to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'acceptance_criteria': self.acceptance_criteria,
            'assigned_to': self.assigned_to,
            'priority': self.priority,
            'state': self.state,
            'tags': self.tags,
            'created_date': self.created_date
        }


class ADOConnector:
    """Handles connection and communication with Azure DevOps"""
    
    def __init__(self, organization: str, project: str, pat_token: str):
        """
        Initialize ADO connector
        
        Args:
            organization: Azure DevOps organization name
            project: Project name in Azure DevOps
            pat_token: Personal Access Token for authentication
        """
        self.organization = organization
        self.project = project
        self.pat_token = pat_token
        self.connection = None
        self.client = None
        self.connected = False
        
        try:
            self._connect()
        except Exception as e:
            logger.error(f"Failed to connect to Azure DevOps: {e}")
            logger.info("Running in mock mode for development")
    
    def _connect(self):
        """Establish connection to Azure DevOps"""
        if Connection is None:
            logger.warning("Azure DevOps SDK not installed. Install with: pip install azure-devops")
            return
        
        try:
            credentials = BasicAuthentication('', self.pat_token)
            org_url = f'https://dev.azure.com/{self.organization}'
            self.connection = Connection(base_url=org_url, creds=credentials)
            self.client = self.connection.clients.get_work_item_tracking_client()
            self.connected = True
            logger.info(f"Connected to Azure DevOps organization: {self.organization}")
        except Exception as e:
            logger.error(f"ADO Connection error: {e}")
            self.connected = False
    
    def fetch_user_stories(self, query: Optional[str] = None) -> List[UserStory]:
        """
        Fetch user stories from Azure DevOps
        
        Args:
            query: Optional WIQL query to filter stories
            
        Returns:
            List of UserStory objects
        """
        if not self.connected:
            logger.warning("Not connected to ADO. Returning mock data.")
            return self._get_mock_stories()
        
        try:
            if query is None:
                query = f"""
                SELECT [System.Id], [System.Title], [System.State]
                FROM WorkItems
                WHERE [System.ProjectName] = '{self.project}'
                AND [System.WorkItemType] = 'User Story'
                ORDER BY [System.Id]
                """
            
            # Execute query - this is a placeholder for actual ADO API call
            logger.info(f"Executing ADO query: {query}")
            stories = []
            
            # Placeholder for actual API call results
            return stories
        except Exception as e:
            logger.error(f"Error fetching user stories: {e}")
            return self._get_mock_stories()
    
    def _get_mock_stories(self) -> List[UserStory]:
        """Return mock user stories for development"""
        return [
            UserStory(
                id="1",
                title="Create user authentication system",
                description="Implement OAuth2-based authentication with support for Google and GitHub",
                acceptance_criteria=[
                    "Users can sign up with email",
                    "Users can login with OAuth providers",
                    "Session tokens are properly validated",
                    "Password reset functionality works"
                ],
                priority=1,
                state="Active",
                tags=["backend", "security"]
            ),
            UserStory(
                id="2",
                title="Build responsive dashboard UI",
                description="Create a React dashboard with real-time updates for agent monitoring",
                acceptance_criteria=[
                    "Dashboard displays all agents and their status",
                    "Real-time updates work via WebSocket",
                    "Mobile responsive design",
                    "Dark mode support"
                ],
                priority=1,
                state="Active",
                tags=["frontend", "ui"]
            )
        ]
    
    def get_story_details(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific story"""
        if not self.connected:
            logger.warning("Not connected to ADO")
            return None
        
        try:
            # Placeholder for ADO API call
            logger.info(f"Fetching details for story: {story_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching story details: {e}")
            return None


class ADOParser:
    """Agent responsible for parsing ADO user stories into actionable tasks"""
    
    def __init__(self, organization: str = None, project: str = None, pat_token: str = None):
        """
        Initialize ADO Parser Agent
        
        Args:
            organization: Azure DevOps organization (from env if not provided)
            project: Project name (from env if not provided)
            pat_token: Personal Access Token (from env if not provided)
        """
        self.organization = organization or os.getenv('ADO_ORGANIZATION', 'your-org')
        self.project = project or os.getenv('ADO_PROJECT', 'your-project')
        self.pat_token = pat_token or os.getenv('ADO_PAT_TOKEN', '')
        
        self.connector = ADOConnector(self.organization, self.project, self.pat_token)
        self.parsed_stories: List[UserStory] = []
    
    def parse_stories(self) -> List[Dict[str, Any]]:
        """
        Parse all user stories into agent tasks
        
        Returns:
            List of parsed tasks ready for agent orchestration
        """
        logger.info("Starting ADO story parsing...")
        
        try:
            stories = self.connector.fetch_user_stories()
            self.parsed_stories = stories
            
            tasks = []
            for story in stories:
                task = self._convert_story_to_task(story)
                tasks.append(task)
            
            logger.info(f"Successfully parsed {len(tasks)} user stories")
            return tasks
        except Exception as e:
            logger.error(f"Error parsing stories: {e}")
            return []
    
    def _convert_story_to_task(self, story: UserStory) -> Dict[str, Any]:
        """
        Convert a user story into a task for agent orchestration
        
        Args:
            story: UserStory object
            
        Returns:
            Task dictionary for orchestration
        """
        return {
            'id': story.id,
            'title': story.title,
            'description': story.description,
            'requirements': story.acceptance_criteria,
            'priority': story.priority or 2,
            'assigned_agents': self._determine_agents(story),
            'dependencies': [],
            'tags': story.tags,
            'metadata': {
                'ado_id': story.id,
                'state': story.state,
                'created': story.created_date or datetime.now().isoformat()
            }
        }
    
    def _determine_agents(self, story: UserStory) -> List[str]:
        """
        Determine which agents should work on this story
        
        Args:
            story: UserStory object
            
        Returns:
            List of agent names
        """
        agents = []
        
        # Determine agents based on tags and description
        tags_lower = [tag.lower() for tag in story.tags]
        desc_lower = story.description.lower()
        
        if any(tag in tags_lower for tag in ['frontend', 'ui', 'react']):
            agents.append('frontend_agent')
        
        if any(tag in tags_lower for tag in ['backend', 'api', 'server']):
            agents.append('backend_agent')
        
        if any(tag in tags_lower for tag in ['database', 'db', 'data']):
            agents.append('database_agent')
        
        if any(keyword in desc_lower for keyword in ['test', 'validation', 'verify']):
            agents.append('testing_agent')
        
        # Default to full-stack if no specific agents determined
        if not agents:
            agents = ['frontend_agent', 'backend_agent', 'database_agent']
        
        return agents
    
    def get_parsed_stories(self) -> List[UserStory]:
        """Get list of parsed stories"""
        return self.parsed_stories


async def initialize_ado_parser() -> ADOParser:
    """Initialize and return ADO parser agent"""
    parser = ADOParser()
    await parser.parse_stories()
    return parser
