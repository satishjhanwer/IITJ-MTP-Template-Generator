# IITJ MTP Template Generator

Generate professional LaTeX academic reports with ease

[Get Started](quickstart){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What is IITJ MTP Template Generator?

A Python-based tool that generates professional LaTeX academic reports from simple configuration files. Perfect for students and researchers who need to create:

- 📄 **Proposal Reports** (MTP1/Research Proposals)
- 📚 **Major Project Reports** (Full Thesis/Dissertation)
- 🎤 **Presentation Slides** (Coming in Phase 2)

## Key Features

✅ **Easy to Use** - Interactive CLI or YAML configuration  
✅ **Professional Templates** - IEEE-style formatting  
✅ **Fully Customizable** - Modify templates to match your needs  
✅ **Well Documented** - Comprehensive guides and examples  
✅ **Zero Dependencies Option** - Works without pip  

## Quick Example

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
- Automatic table of contents, figures, and tables
- IEEE-style citations

## Getting Started

1. [Quick Start Guide](quickstart) - Get up and running in 5 minutes
2. [CI/CD Auto-Compilation](ci-cd) - Automatic PDF generation with GitHub Actions
3. [Input Schema](input-schema) - Learn about configuration options
4. [Customization Guide](customization) - Personalize your templates
5. [FAQ](faq) - Common questions and troubleshooting

## Example Output

The generator creates a complete LaTeX project with:

- All necessary `.tex` files
- Bibliography with example entries
- TODO markers for easy content addition
- Compilation instructions
- Template-specific README

## Requirements

- Python 3.8+
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Optional: Jinja2 and PyYAML (or use zero-dependency version)

## License

MIT License - Free to use for academic and commercial purposes

---

**Ready to create your academic report?** [Get Started →](quickstart)
