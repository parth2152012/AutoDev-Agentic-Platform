"""Input validation utilities for the AutoDev platform"""

from typing import Any, Dict, List
from src.utils.errors import ValidationError

def validate_input(value: Any, expected_type: type, allow_none: bool = False) -> bool:
    """Validate input value against expected type"""
    if allow_none and value is None:
        return True
    
    if not isinstance(value, expected_type):
        raise ValidationError(
            f"Expected {expected_type.__name__}, got {type(value).__name__}"
        )
    
    return True

def validate_config(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """Validate configuration dictionary has all required keys"""
    missing_keys = [key for key in required_keys if key not in config]
    
    if missing_keys:
        raise ValidationError(
            f"Missing required configuration keys: {', '.join(missing_keys)}"
        )
    
    return True

def validate_non_empty_string(value: str, field_name: str = "value") -> bool:
    """Validate string is not empty"""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")
    return True

def validate_positive_number(value: float, field_name: str = "value") -> bool:
    """Validate number is positive"""
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValidationError(f"{field_name} must be a positive number")
    return True
