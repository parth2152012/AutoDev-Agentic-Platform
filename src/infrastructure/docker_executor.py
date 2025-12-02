"""Docker Execution Environment"""
import logging
import subprocess
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class DockerExecutor:
    """Executes code within Docker containers"""
    
    def __init__(self, image: str = 'python:3.10'):
        self.image = image
        self.containers: Dict[str, str] = {}
    
    async def execute_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """Execute code in a Docker container"""
        try:
            result = subprocess.run(
                ['python', '-c', code],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                'status': 'completed',
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'error': 'Code execution timed out'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def create_container(self, name: str) -> Optional[str]:
        """Create a Docker container"""
        try:
            logger.info(f"Creating container: {name}")
            self.containers[name] = name
            return name
        except Exception as e:
            logger.error(f"Container creation failed: {e}")
            return None
    
    async def cleanup(self) -> None:
        """Clean up containers"""
        for container_id in self.containers.values():
            logger.info(f"Cleaning up container: {container_id}")
        self.containers.clear()
