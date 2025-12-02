"""Custom exception classes for AutoDev platform"""

class AutoDevException(Exception):
    """Base exception for all AutoDev platform exceptions"""
    pass

class AgentError(AutoDevException):
    """Exception raised when an agent encounters an error"""
    pass

class ValidationError(AutoDevException):
    """Exception raised for validation errors"""
    pass

class ConfigurationError(AutoDevException):
    """Exception raised for configuration errors"""
    pass

class WorkflowError(AutoDevException):
    """Exception raised for workflow execution errors"""
    pass

class DatabaseError(AutoDevException):
    """Exception raised for database operation errors"""
    pass

class RedisError(AutoDevException):
    """Exception raised for Redis operation errors"""
    pass
