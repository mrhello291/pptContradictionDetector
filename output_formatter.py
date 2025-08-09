"""
Output formatting module for presenting analysis results.
"""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from models import AnalysisResult, Inconsistency, SeverityLevel

logger = logging.getLogger(__name__)

class OutputFormatter:
    """Formats and displays analysis results in various formats."""
    
    def __init__(self):
        self.severity_colors = {
            SeverityLevel.LOW: '\033[32m',      # Green
            SeverityLevel.MEDIUM: '\033[33m',   # Yellow
            SeverityLevel.HIGH: '\033[31m',     # Red
            SeverityLevel.CRITICAL: '\033[35m'  # Magenta
        }
        self.reset_color = '\033[0m'
    
    def print_console_report(self, result: AnalysisResult, use_colors: bool = True) -> None:
        """Print a formatted console report."""
        print("=" * 80)
        print(f"📊 POWERPOINT CONTRADICTION ANALYSIS REPORT")
        print("=" * 80)
        print(f"Presentation: {result.presentation_name}")
        print(f"Total Slides: {result.total_slides}")
        print(f"Processing Time: {result.processing_time:.2f} seconds")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Summary
        print("📋 SUMMARY")
        print("-" * 40)
        print(result.summary)
        print()
        
        if not result.inconsistencies:
            print("✅ No inconsistencies detected! The presentation appears to be consistent.")
            return
        
        # Inconsistencies by severity
        print("⚠️  INCONSISTENCIES FOUND")
        print("-" * 40)
        
        # Group by severity
        severity_groups = {}
        for inconsistency in result.inconsistencies:
            severity = inconsistency.severity
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(inconsistency)
        
        # Display by severity (critical first)
        severity_order = [SeverityLevel.CRITICAL, SeverityLevel.HIGH, SeverityLevel.MEDIUM, SeverityLevel.LOW]
        
        for severity in severity_order:
            if severity in severity_groups:
                color = self.severity_colors[severity] if use_colors else ''
                reset = self.reset_color if use_colors else ''
                
                print(f"\n{color}🔴 {severity.value.upper()} SEVERITY ({len(severity_groups[severity])} issues){reset}")
                print("-" * 60)
                
                for i, inconsistency in enumerate(severity_groups[severity], 1):
                    self._print_inconsistency(inconsistency, i, use_colors)
        
        print("\n" + "=" * 80)
        print("🔍 TIP: Review high and critical severity issues first!")
        print("=" * 80)
    
    def _print_inconsistency(self, inconsistency: Inconsistency, index: int, use_colors: bool) -> None:
        """Print a single inconsistency with formatting."""
        color = self.severity_colors[inconsistency.severity] if use_colors else ''
        reset = self.reset_color if use_colors else ''
        
        print(f"\n{color}#{index} {inconsistency.description}{reset}")
        print(f"   Type: {inconsistency.type.value.replace('_', ' ').title()}")
        print(f"   Affected Slides: {', '.join(map(str, inconsistency.affected_slides))}")
        print(f"   Confidence: {inconsistency.confidence_score:.2f}")
        
        # Evidence
        if inconsistency.evidence:
            print("   Evidence:")
            for slide_ref, content in inconsistency.evidence.items():
                # Truncate long content
                display_content = content[:100] + "..." if len(content) > 100 else content
                print(f"     {slide_ref}: {display_content}")
        
        # Explanation
        if inconsistency.explanation:
            print(f"   Explanation: {inconsistency.explanation}")
    
    def save_json_report(self, result: AnalysisResult, output_path: Path) -> None:
        """Save analysis results as JSON."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON report saved to {output_path}")
            print(f"📄 Detailed JSON report saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving JSON report: {e}")
            print(f"❌ Error saving JSON report: {e}")
    
    def save_markdown_report(self, result: AnalysisResult, output_path: Path) -> None:
        """Save analysis results as Markdown."""
        try:
            markdown_content = self._generate_markdown_report(result)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Markdown report saved to {output_path}")
            print(f"📝 Markdown report saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving Markdown report: {e}")
            print(f"❌ Error saving Markdown report: {e}")
    
    def _generate_markdown_report(self, result: AnalysisResult) -> str:
        """Generate Markdown content for the report."""
        md_lines = [
            "# PowerPoint Contradiction Analysis Report",
            "",
            f"**Presentation:** {result.presentation_name}  ",
            f"**Total Slides:** {result.total_slides}  ",
            f"**Processing Time:** {result.processing_time:.2f} seconds  ",
            f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            "",
            "## Summary",
            "",
            result.summary,
            ""
        ]
        
        if not result.inconsistencies:
            md_lines.extend([
                "## ✅ Results",
                "",
                "No inconsistencies detected! The presentation appears to be consistent.",
                ""
            ])
            return '\n'.join(md_lines)
        
        md_lines.extend([
            "## ⚠️ Inconsistencies Found",
            "",
            f"Total inconsistencies detected: **{len(result.inconsistencies)}**",
            ""
        ])
        
        # Severity breakdown
        severity_breakdown = result._get_severity_breakdown()
        if any(severity_breakdown.values()):
            md_lines.extend([
                "### Severity Breakdown",
                ""
            ])
            
            for severity, count in severity_breakdown.items():
                if count > 0:
                    emoji = self._get_severity_emoji(severity)
                    md_lines.append(f"- {emoji} **{severity.title()}:** {count}")
            
            md_lines.append("")
        
        # Group by severity
        severity_groups = {}
        for inconsistency in result.inconsistencies:
            severity = inconsistency.severity
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(inconsistency)
        
        # Display by severity
        severity_order = [SeverityLevel.CRITICAL, SeverityLevel.HIGH, SeverityLevel.MEDIUM, SeverityLevel.LOW]
        
        for severity in severity_order:
            if severity in severity_groups:
                emoji = self._get_severity_emoji(severity.value)
                md_lines.extend([
                    f"### {emoji} {severity.value.title()} Severity Issues",
                    ""
                ])
                
                for i, inconsistency in enumerate(severity_groups[severity], 1):
                    md_lines.extend(self._format_inconsistency_markdown(inconsistency, i))
                
                md_lines.append("")
        
        md_lines.extend([
            "---",
            "",
            "💡 **Tip:** Focus on addressing critical and high severity issues first for maximum impact.",
            ""
        ])
        
        return '\n'.join(md_lines)
    
    def _format_inconsistency_markdown(self, inconsistency: Inconsistency, index: int) -> List[str]:
        """Format a single inconsistency as Markdown."""
        lines = [
            f"#### {index}. {inconsistency.description}",
            "",
            f"- **Type:** {inconsistency.type.value.replace('_', ' ').title()}",
            f"- **Affected Slides:** {', '.join(map(str, inconsistency.affected_slides))}",
            f"- **Confidence Score:** {inconsistency.confidence_score:.2f}",
            ""
        ]
        
        if inconsistency.evidence:
            lines.append("**Evidence:**")
            for slide_ref, content in inconsistency.evidence.items():
                lines.append(f"- *{slide_ref}:* {content}")
            lines.append("")
        
        if inconsistency.explanation:
            lines.extend([
                "**Explanation:**",
                inconsistency.explanation,
                ""
            ])
        
        return lines
    
    def _get_severity_emoji(self, severity: str) -> str:
        """Get emoji for severity level."""
        emoji_map = {
            'low': '🟢',
            'medium': '🟡', 
            'high': '🔴',
            'critical': '🚨'
        }
        return emoji_map.get(severity.lower(), '⚪')
    
    def print_quick_summary(self, result: AnalysisResult) -> None:
        """Print a quick one-line summary."""
        if not result.inconsistencies:
            print("✅ No inconsistencies found - presentation is consistent!")
        else:
            critical = sum(1 for i in result.inconsistencies if i.severity == SeverityLevel.CRITICAL)
            high = sum(1 for i in result.inconsistencies if i.severity == SeverityLevel.HIGH)
            
            if critical > 0:
                print(f"🚨 {len(result.inconsistencies)} inconsistencies found ({critical} critical, {high} high severity)")
            elif high > 0:
                print(f"⚠️  {len(result.inconsistencies)} inconsistencies found ({high} high severity)")
            else:
                print(f"⚠️  {len(result.inconsistencies)} minor inconsistencies found") 