"""Content extraction from LaTeX reports for presentations.

This module extracts relevant content from proposal and major project
reports to automatically populate presentation slides.
"""

import os
from typing import Dict, List, Optional, Any
from .latex_parser import (
    extract_section, extract_subsection, extract_environment,
    extract_itemize_list, extract_first_paragraph, extract_chapter,
    clean_latex
)


class ContentExtractor:
    """Extract content from LaTeX reports for presentations."""

    def __init__(self, report_path: str):
        """Initialize with path to LaTeX report.

        Args:
            report_path: Path to main LaTeX file (proposal.tex or main.tex)

        Raises:
            FileNotFoundError: If report file doesn't exist
        """
        if not os.path.exists(report_path):
            raise FileNotFoundError(f"Report not found: {report_path}")

        with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.content = f.read()

        self.report_path = report_path
        self.report_dir = os.path.dirname(report_path)

    def extract_for_presentation(self) -> Dict[str, Any]:
        """Extract all relevant content for presentation.

        Returns:
            Dictionary with extracted content for each section
        """
        return {
            'introduction': self.extract_introduction(),
            'objectives': self.extract_objectives(),
            'methodology': self.extract_methodology(),
            'results': self.extract_results(),
            'conclusion': self.extract_conclusion(),
        }

    def extract_introduction(self) -> Dict[str, str]:
        """Extract introduction content.

        Returns:
            Dictionary with motivation and problem statement
        """
        intro_content = extract_section(self.content, 'Introduction')
        if not intro_content:
            intro_content = extract_chapter(self.content, 'Introduction')

        if not intro_content:
            abstract = extract_environment(self.content, 'abstract')
            if abstract:
                return {
                    'motivation': clean_latex(abstract),
                    'problem_statement': '',
                }
            return {}

        motivation = extract_subsection(intro_content, 'Motivation')
        if not motivation:
            motivation = extract_first_paragraph(intro_content, max_length=400)
        else:
            motivation = extract_first_paragraph(motivation, max_length=400)

        problem = extract_subsection(intro_content, 'Problem Statement')
        if not problem:
            problem = extract_subsection(intro_content, 'Problem')

        if problem:
            problem = extract_first_paragraph(problem, max_length=300)

        return {
            'motivation': motivation,
            'problem_statement': problem or '',
        }

    def extract_objectives(self) -> List[str]:
        """Extract objectives list.

        Returns:
            List of objective strings
        """
        obj_content = extract_section(self.content, 'Objectives')
        if not obj_content:
            obj_content = extract_subsection(self.content, 'Objectives')

        if not obj_content:
            for name in ['Research Objectives', 'Project Objectives', 'Goals']:
                obj_content = extract_section(self.content, name)
                if obj_content:
                    break

        if obj_content:
            objectives = extract_itemize_list(obj_content)
            return objectives[:5]  # limit to 5 for presentation slides

        return []

    def extract_methodology(self) -> Dict[str, Any]:
        """Extract methodology content.

        Returns:
            Dictionary with methodology overview and key points
        """
        method_content = extract_section(self.content, 'Methodology')
        if not method_content:
            method_content = extract_chapter(self.content, 'Methodology')

        if not method_content:
            for name in ['Proposed Solution', 'Approach', 'Design', 'Implementation']:
                method_content = extract_section(self.content, name)
                if method_content:
                    break

        if not method_content:
            return {}

        overview = extract_first_paragraph(method_content, max_length=400)

        approaches = []
        approach_section = extract_subsection(method_content, 'Approach')
        if approach_section:
            approaches = extract_itemize_list(approach_section)[:3]

        technologies = []
        tech_section = extract_subsection(method_content, 'Technologies')
        if not tech_section:
            tech_section = extract_subsection(method_content, 'Tools')

        if tech_section:
            technologies = extract_itemize_list(tech_section)[:5]

        return {
            'overview': overview,
            'approaches': approaches,
            'technologies': technologies,
        }

    def extract_results(self) -> Dict[str, Any]:
        """Extract results content (for major projects).

        Returns:
            Dictionary with implementation and evaluation content
        """
        results_content = extract_section(self.content, 'Results')
        if not results_content:
            results_content = extract_chapter(self.content, 'Results')

        if not results_content:
            for name in ['Implementation', 'Evaluation', 'Experiments']:
                results_content = extract_section(self.content, name)
                if results_content:
                    break

        if not results_content:
            return {}

        impl_section = extract_subsection(results_content, 'Implementation')
        if impl_section:
            implementation = extract_itemize_list(impl_section)[:4]
        else:
            implementation = []

        eval_section = extract_subsection(results_content, 'Evaluation')
        if eval_section:
            evaluation = extract_first_paragraph(eval_section, max_length=300)
        else:
            evaluation = extract_first_paragraph(results_content, max_length=300)

        return {
            'implementation': implementation,
            'evaluation': evaluation,
        }

    def extract_conclusion(self) -> Dict[str, Any]:
        """Extract conclusion content.

        Returns:
            Dictionary with summary and future work
        """
        concl_content = extract_section(self.content, 'Conclusion')
        if not concl_content:
            concl_content = extract_chapter(self.content, 'Conclusion')

        if not concl_content:
            return {}

        summary = extract_first_paragraph(concl_content, max_length=400)

        future_work = []
        future_section = extract_subsection(concl_content, 'Future Work')
        if not future_section:
            future_section = extract_subsection(concl_content, 'Future Scope')

        if future_section:
            future_work = extract_itemize_list(future_section)[:4]

        return {
            'summary': summary,
            'future_work': future_work,
        }


def extract_content_from_report(report_path: str) -> Optional[Dict[str, Any]]:
    """Extract content from a LaTeX report.

    Convenience function for extracting content.

    Args:
        report_path: Path to LaTeX report file

    Returns:
        Extracted content dictionary or None if extraction fails
    """
    try:
        extractor = ContentExtractor(report_path)
        return extractor.extract_for_presentation()
    except Exception as e:
        print(f"[WARNING] Content extraction failed: {e}")
        return None
