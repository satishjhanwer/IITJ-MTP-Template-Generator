# IITJ MTP Template Generator

Generate professional LaTeX academic reports with ease

<div style="margin-bottom: 20px;">
  <a href="beginners_guide" style="display: inline-block; padding: 10px 16px; background-color: #0969da; color: white; text-decoration: none; border-radius: 6px; font-weight: 500; margin-right: 10px;">Simple guide (beginners)</a>
  <a href="quickstart" style="display: inline-block; padding: 10px 16px; background-color: #058e3f; color: white; text-decoration: none; border-radius: 6px; font-weight: 500; margin-right: 10px;">Quick Start</a>
  <a href="https://github.com/satishjhanwer/IITJ-MTP-Template-Generator" style="display: inline-block; padding: 10px 16px; background-color: #6e40aa; color: white; text-decoration: none; border-radius: 6px; font-weight: 500;">View on GitHub</a>
</div>

---

## What is IITJ MTP Template Generator?

A Python-based tool that builds a **structured LaTeX project** from simple configuration files: your title, name, supervisor, and other settings, plus **section shells** you must fill in (abstract, chapters, acknowledgments, and more). It does **not** write your report content for you. Perfect for students and researchers who need to create:

- 📄 **Proposal Reports** (MTP1/Research Proposals)
- 📚 **Major Project Reports** (Full Thesis/Dissertation)
- 🎤 **Presentation Slides** (Beamer)

## Key Features

✅ **Easy to Use** - Interactive CLI or YAML configuration  
✅ **Professional Templates** - IEEE-style formatting  
✅ **Fully Customizable** - Modify templates to match your needs  
✅ **Well Documented** - Comprehensive guides and examples  
✅ **Zero Dependencies Option** - Works without pip  

## Quick Example

### Option 1: Web-based Configuration (Easiest)

No command line needed! Use the **[interactive web generator](/web/config-generator/)** to:

- Fill in your project details visually
- Preview your `config.yaml` in real-time
- Download the config file directly
- Then run `python scripts/generate.py --config config.yaml`

### Option 2: Command Line

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Generate a proposal report
python scripts/generate.py --config examples/sample-proposal/config.yaml

# Compile to PDF
cd output/your-project
pdflatex proposal.tex
```

## What You Get

### Proposal Report Template

- Title page with university branding
- Abstract and table of contents
- Introduction with objectives
- Literature review with comparison tables
- Methodology with architecture diagrams
- Project timeline
- IEEE-style bibliography

### Major Project Report Template

- Complete front matter (declaration, certificate, acknowledgments)
- 7 comprehensive chapters
- Professional formatting
- Automatic table of contents, figures, tables, abbreviations, and symbols
- IEEE-style citations

### Presentation Slides (Beamer)

- Title, introduction, methodology, results, and conclusion sections
- Configurable theme and aspect ratio via YAML
- Optional content extraction from an existing LaTeX report

## Getting Started

1. [Simple guide for beginners](beginners_guide) - Plain language: what you install, what you get, template PDF vs final PDF
2. [Quick Start Guide](quickstart) - Get up and running in 5 minutes
3. [CI/CD Auto-Compilation](ci_cd) - Automatic PDF generation with GitHub Actions
4. [Input Schema](input-schema) - Learn about configuration options
5. [Customization Guide](customization) - Personalize your templates
6. [FAQ](faq) - Common questions and troubleshooting

## Example Output

The generator creates a complete LaTeX project with:

- All necessary `.tex` files
- Bibliography with example entries
- `[TODO]` / `% TODO` markers where **you** add real content
- Compilation instructions
- Template-specific README

**Note:** Building a PDF immediately after generation shows **formatting and layout**; the text is still placeholder until you edit every section. That early PDF is a **preview**, not your final submission.

## Requirements

- Python 3.9+
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Optional: Jinja2 and PyYAML (or use zero-dependency version)

## License

MIT License - Free to use for academic and commercial purposes

---

**Ready to create your academic report?** [Simple guide →](beginners_guide) &nbsp;·&nbsp; [Quick Start →](quickstart)
