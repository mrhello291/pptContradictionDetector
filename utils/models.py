"""
Data models for PowerPoint contradiction detection.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, ByteString
from enum import Enum

class InconsistencyType(Enum):
    """Types of inconsistencies that can be detected."""
    NUMERICAL_CONFLICT = "numerical_conflict"
    TEXTUAL_CONTRADICTION = "textual_contradiction"
    TIMELINE_MISMATCH = "timeline_mismatch"
    LOGICAL_INCONSISTENCY = "logical_inconsistency"
    DATA_MISMATCH = "data_mismatch"
    PERCENTAGE_ERROR = "percentage_error"
    FACTUAL_CONTRADICTION = "factual_contradiction"

class SeverityLevel(Enum):
    """Severity levels for inconsistencies."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SlideContent:
    """Represents content extracted from a single slide."""
    slide_number: int
    title: Optional[str]
    text_content: List[str]
    numerical_data: List[Dict[str, Any]]
    images_data: List[ByteString]
    raw_content: str

@dataclass
class Inconsistency:
    """Represents a detected inconsistency."""
    type: InconsistencyType
    severity: SeverityLevel
    description: str
    affected_slides: List[int]
    evidence: Dict[str, str]  # slide_number -> relevant content
    confidence_score: float  # 0.0 to 1.0
    explanation: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type.value,
            "severity": self.severity.value,
            "description": self.description,
            "affected_slides": self.affected_slides,
            "evidence": self.evidence,
            "confidence_score": self.confidence_score,
            "explanation": self.explanation
        }

@dataclass
class AnalysisResult:
    """Complete analysis result for a PowerPoint presentation."""
    presentation_name: str
    total_slides: int
    inconsistencies: List[Inconsistency]
    processing_time: float
    summary: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "presentation_name": self.presentation_name,
            "total_slides": self.total_slides,
            "inconsistencies": [inc.to_dict() for inc in self.inconsistencies],
            "processing_time": self.processing_time,
            "summary": self.summary,
            "total_inconsistencies": len(self.inconsistencies),
            "severity_breakdown": self._get_severity_breakdown()
        }
    
    def _get_severity_breakdown(self) -> Dict[str, int]:
        """Get count of inconsistencies by severity level."""
        breakdown = {level.value: 0 for level in SeverityLevel}
        for inconsistency in self.inconsistencies:
            breakdown[inconsistency.severity.value] += 1
        return breakdown 