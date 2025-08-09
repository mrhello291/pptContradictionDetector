"""
AI-powered inconsistency detection using Google Gemini.
"""
import json
import logging
import re
import io
from typing import List, Dict, Any, Optional
from PIL import Image
import google.generativeai as genai

from utils.config import Config
from utils.models import SlideContent, Inconsistency, InconsistencyType, SeverityLevel

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI-powered analyzer for detecting inconsistencies in presentations."""
    
    def __init__(self):
        """Initialize the AI analyzer with Gemini configuration."""
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            generation_config=genai.types.GenerationConfig(
                temperature=Config.TEMPERATURE,
                max_output_tokens=Config.MAX_TOKENS,
            )
        )
        
        logger.info(f"Initialized AI analyzer with model: {Config.GEMINI_MODEL}")
    
    def analyze_inconsistencies(self, slides: List[SlideContent]) -> List[Inconsistency]:
        """Analyze slides for inconsistencies using AI."""
        logger.info(f"Analyzing {len(slides)} slides for inconsistencies")
        
        # Prepare content for analysis
        presentation_content = self._prepare_content_for_analysis(slides)
        
        # Generate analysis prompt
        prompt = self._create_analysis_prompt(presentation_content)
        
        try:
            # Get AI analysis
            response = self.model.generate_content(prompt)
            
            # Parse the response
            inconsistencies = self._parse_ai_response(response.text, slides)
            
            logger.info(f"Found {len(inconsistencies)} potential inconsistencies")
            return inconsistencies
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            raise
    
    
    def _prepare_content_for_analysis(self, slides: List[SlideContent]) -> List[Any]:
        """Prepare slide content for AI analysis."""
        content_parts = []
        
        for slide in slides:
            # Step 1: Add raw text and metadata
            content_parts.append(f"\n--- SLIDE {slide.slide_number} ---")
            if slide.title:
                content_parts.append(f"Title: {slide.title}")
            content_parts.append(f"Content: {slide.raw_content}")
            if slide.numerical_data:
                content_parts.append(f"Numerical Data: {json.dumps(slide.numerical_data, indent=2)}")

            # Step 2: Add all images (full-slide and individual)
            if slide.images_data:
                content_parts.append(f"Images from slide {slide.slide_number}:")
                for image_bytes in slide.images_data:
                    try:
                        content_parts.append(Image.open(io.BytesIO(image_bytes)))
                    except Exception as e:
                        logger.warning(f"Failed to open image bytes for analysis: {e}")
                        
        return content_parts

    
    def _create_analysis_prompt(self, content: str) -> str:
        """Create a comprehensive prompt for inconsistency detection."""
        return f"""
You are an expert analyst tasked with finding factual and logical inconsistencies in a PowerPoint presentation. 

Analyze the following presentation content, which includes text and images (charts, graphs, diagrams), and identify ANY inconsistencies, contradictions, or logical errors across slides.

When analyzing images, pay special attention to:
- **Graph and Chart data:** Read axes, data points, labels, and trends.
- **Colors and labels:** Note how they are used to represent different data series.
- **Diagrams and flowcharts:** Understand the relationships and logic they depict.
- **Numbers and text:** Look for any numbers or text embedded within the images.


TYPES OF INCONSISTENCIES TO DETECT:
1. **Numerical Conflicts**: Conflicting revenue figures, percentages that don't add up, mismatched statistics
2. **Textual Contradictions**: Contradictory claims or statements (e.g., "highly competitive market" vs "few competitors")  
3. **Timeline Mismatches**: Conflicting dates, inconsistent forecasts, temporal contradictions
4. **Logical Inconsistencies**: Claims that contradict each other logically
5. **Data Mismatches**: Charts/tables with conflicting information
6. **Percentage Errors**: Percentages that don't sum to 100% when they should
7. **Factual Contradictions**: Any factual claims that contradict each other

PRESENTATION CONTENT:
{content}

INSTRUCTIONS:
- Be thorough and meticulous in your analysis
- Look for both obvious and subtle inconsistencies
- Compare information across ALL slides (both text and visual content)
- Pay special attention to numerical data, dates, percentages, and factual claims
- Consider context and domain knowledge
- Only flag genuine inconsistencies, not minor variations in phrasing

RESPONSE FORMAT:
Return your analysis as a JSON array of inconsistencies. Each inconsistency should have this structure:

{{
  "type": "one of: numerical_conflict, textual_contradiction, timeline_mismatch, logical_inconsistency, data_mismatch, percentage_error, factual_contradiction",
  "severity": "one of: low, medium, high, critical",
  "description": "Brief description of the inconsistency",
  "affected_slides": [list of slide numbers],
  "evidence": {{
    "slide_X": "relevant content from slide X",
    "slide_Y": "conflicting content from slide Y"
  }},
  "confidence_score": float between 0.0 and 1.0,
  "explanation": "Detailed explanation of why this is an inconsistency"
}}

Example:
[
  {{
    "type": "numerical_conflict",
    "severity": "high", 
    "description": "Revenue figures don't match between slides",
    "affected_slides": [2, 5],
    "evidence": {{
      "slide_2": "Q1 Revenue: $1.2M",
      "slide_5": "Q1 Revenue: $1.5M"
    }},
    "confidence_score": 0.95,
    "explanation": "Slide 2 shows Q1 revenue as $1.2M while slide 5 shows it as $1.5M - these should be consistent."
  }}
]

IMPORTANT: Return ONLY the JSON array, no additional text or formatting.
"""
    
    def _parse_ai_response(self, response_text: str, slides: List[SlideContent]) -> List[Inconsistency]:
        """Parse AI response and convert to Inconsistency objects."""
        inconsistencies = []
        
        try:
            # Clean up the response text
            cleaned_response = self._clean_response_text(response_text)
            
            # Parse JSON
            response_data = json.loads(cleaned_response)
            
            if not isinstance(response_data, list):
                logger.warning("AI response is not a list, attempting to extract inconsistencies")
                return []
            
            # Convert to Inconsistency objects
            for item in response_data:
                try:
                    inconsistency = self._create_inconsistency_from_dict(item)
                    if inconsistency:
                        inconsistencies.append(inconsistency)
                except Exception as e:
                    logger.warning(f"Error parsing inconsistency: {e}")
                    continue
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.debug(f"Raw response: {response_text}")
            
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', response_text, re.DOTALL)
            if json_match:
                try:
                    response_data = json.loads(json_match.group(1))
                    for item in response_data:
                        inconsistency = self._create_inconsistency_from_dict(item)
                        if inconsistency:
                            inconsistencies.append(inconsistency)
                except Exception as e:
                    logger.error(f"Failed to parse extracted JSON: {e}")
        
        return inconsistencies
    
    def _clean_response_text(self, text: str) -> str:
        """Clean up AI response text for JSON parsing."""
        # Remove markdown code blocks
        text = re.sub(r'```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```', '', text)
        
        # Remove any text before the first '[' and after the last ']'
        start_idx = text.find('[')
        end_idx = text.rfind(']')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            text = text[start_idx:end_idx + 1]
        
        return text.strip()
    
    def _create_inconsistency_from_dict(self, data: Dict[str, Any]) -> Optional[Inconsistency]:
        """Create an Inconsistency object from dictionary data."""
        try:
            # Map string values to enums
            inconsistency_type = InconsistencyType(data.get('type', 'logical_inconsistency'))
            severity = SeverityLevel(data.get('severity', 'medium'))
            
            return Inconsistency(
                type=inconsistency_type,
                severity=severity,
                description=data.get('description', ''),
                affected_slides=data.get('affected_slides', []),
                evidence=data.get('evidence', {}),
                confidence_score=float(data.get('confidence_score', 0.0)),
                explanation=data.get('explanation', '')
            )
        except (ValueError, KeyError, TypeError) as e:
            logger.warning(f"Error creating inconsistency from data {data}: {e}")
            return None
    
    def generate_summary(self, inconsistencies: List[Inconsistency], total_slides: int) -> str:
        """Generate a summary of the analysis results."""
        if not inconsistencies:
            return f"No inconsistencies detected across {total_slides} slides."
        
        severity_counts = {}
        type_counts = {}
        
        for inc in inconsistencies:
            severity_counts[inc.severity.value] = severity_counts.get(inc.severity.value, 0) + 1
            type_counts[inc.type.value] = type_counts.get(inc.type.value, 0) + 1
        
        summary_parts = [
            f"Analysis completed for {total_slides} slides.",
            f"Found {len(inconsistencies)} inconsistencies:"
        ]
        
        # Add severity breakdown
        if severity_counts:
            summary_parts.append("Severity breakdown:")
            for severity, count in severity_counts.items():
                summary_parts.append(f"  - {severity.title()}: {count}")
        
        # Add type breakdown
        if type_counts:
            summary_parts.append("Type breakdown:")
            for inc_type, count in type_counts.items():
                summary_parts.append(f"  - {inc_type.replace('_', ' ').title()}: {count}")
        
        return '\n'.join(summary_parts) 