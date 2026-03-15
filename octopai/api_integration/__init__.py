"""
Octopai API Integration - Standardized Interface Module

This module provides standardized interfaces for integrating Octopai
with external applications and services.
"""

from octopai.api_integration.api import OctopaiIntegrationAPI
from octopai.api_integration.schemas import (
    CreateSkillFromURLRequest,
    CreateSkillFromFilesRequest,
    CreateSkillFromPromptRequest,
    OptimizeSkillRequest,
    PipelineStatusResponse,
    SkillInfoResponse,
    ErrorResponse
)

__all__ = [
    "OctopaiIntegrationAPI",
    "CreateSkillFromURLRequest",
    "CreateSkillFromFilesRequest",
    "CreateSkillFromPromptRequest",
    "OptimizeSkillRequest",
    "PipelineStatusResponse",
    "SkillInfoResponse",
    "ErrorResponse"
]
