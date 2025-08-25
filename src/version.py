"""
Version and build information module.
"""
import os
from datetime import datetime

class BuildInfo:
    """Container for build and version information."""
    
    def __init__(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def __str__(self):
        return f"Version: {self.version}, Build: {self.build_date}, Commit: {self.git_commit}"
    
    def to_dict(self):
        return {
            'version': self.version,
            'build_date': self.build_date,
            'git_commit': self.git_commit
        }

# Global instance
build_info = BuildInfo()

def get_version_info():
    """Get formatted version information string."""
    return str(build_info)

def get_version_dict():
    """Get version information as dictionary."""
    return build_info.to_dict()
