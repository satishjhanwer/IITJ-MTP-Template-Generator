# IITJ MTP Template Generator

Generate professional LaTeX academic reports (proposals, major projects, presentations) with dynamic user inputs.

[![GitHub Actions](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/workflows/Compile%20LaTeX/badge.svg)](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/actions)
[![Tests](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/workflows/Run%20Tests/badge.svg)](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![LaTeX](https://img.shields.io/badge/LaTeX-TeX%20Live-green.svg)](https://www.latex-project.org/get/)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/actions)
[![Status](https://img.shields.io/badge/status-production--ready-success.svg)](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/actions)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/)

A comprehensive, production-ready Python-based template generator for creating professional LaTeX academic reports for IIT Jodhpur's Major Technical Project (MTP). Supports proposal reports, major project reports, and presentation slides with automated CI/CD compilation, content extraction, and performance optimizations.

## ✨ Features

### Core Features

- **Three Report Types**: Proposal, Major Project, and Presentation (Beamer slides)
- **Interactive CLI**: Easy-to-use command-line interface for collecting inputs
- **YAML Configuration**: Use config files for reproducible report generation
- **Professional Templates**: IEEE-style LaTeX templates with proper formatting
- **Customizable**: Modify templates to match your university's requirements
- **Zero Dependencies Option**: Fallback generator without external dependencies
- **Comprehensive Documentation**: Detailed guides and examples
- **CI/CD Auto-Compilation**: Automatic PDF generation via GitHub Actions
- **Content Extraction**: Auto-populate presentation slides from existing reports
- **GitHub Pages**: Professional documentation site

### Quality & Performance

- **93% Test Coverage**: 60+ unit tests across all utilities
- **66% Faster Generation**: Optimized with template caching and parallel I/O
- **Error Handling**: Helpful error messages with suggestions and documentation links
- **Progress Tracking**: Visual progress bars and spinners for better UX
- **Cross-Platform**: Tested on Windows, macOS, and Linux with Python 3.9-3.12

## 📋 Supported Report Types

- ✅ **Proposal Report** (MTP1/Research Proposal)
- ✅ **Major Project Report** (Full Thesis/Dissertation)
- ✅ **Presentation Slides** (Beamer)

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)

### Installation

- Clone this repository:

```bash
git clone https://github.com/satishjhanwer/IITJ-MTP-Template-Generator.git
cd IITJ-MTP-Template-Generator
```

- Install Python dependencies:

```bash
pip install -r scripts/requirements.txt
```

#### Interactive Mode

```bash
python scripts/generate.py
```

Follow the prompts to enter your project details.

#### Using a Config File

```bash
python scripts/generate.py --config examples/sample-proposal/config.yaml
```

### Compile the Generated Report

#### Option 1: Automatic Compilation (Recommended)

If you're using GitHub, push your generated files and let GitHub Actions compile them automatically:

```bash
git add output/
git commit -m "Add my project report"
git push origin main
```

Then download the compiled PDF from the **Actions** tab → **Artifacts**. See [CI/CD Guide](docs/CI_CD.md) for details.

#### Option 2: Local Compilation

```bash
cd output/your-project-name
pdflatex proposal.tex  # or main.tex for major projects, slides.tex for presentations
bibtex proposal        # or main (skip for presentations)
pdflatex proposal.tex
pdflatex proposal.tex
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- [CI/CD Auto-Compilation](docs/CI_CD.md) - Automatic PDF generation with GitHub Actions
- [Input Schema](docs/INPUT_SCHEMA.md) - Complete configuration reference
- [Customization Guide](docs/CUSTOMIZATION.md) - Customize templates and formatting
- [FAQ](docs/FAQ.md) - Frequently asked questions

## 📁 Project Structure

```bash
IITJ-MTP-Template-Generator/
├── scripts/
│   ├── generate.py              # Main generator script
│   ├── generate_simple.py       # Zero-dependency fallback
│   ├── requirements.txt         # Python dependencies
│   └── utils/                   # Utility modules
├── templates/
│   ├── proposal/                # Proposal report template
│   ├── major-project/           # Major project template
│   └── presentation/            # Presentation slides template
├── examples/
│   ├── sample-proposal/         # Example proposal config
│   ├── sample-major-project/    # Example major project config
│   └── sample-presentation/     # Example presentation config
├── docs/                        # Documentation
└── README.md                    # This file
```

## 🎨 Customization

### Using Custom Logo

```bash
python scripts/generate.py --config config.yaml --logo path/to/logo.png
```

Or specify in your `config.yaml`:

```yaml
assets:
  logo_path: "./path/to/logo.png"
```

### Formatting Options

Customize formatting in your config file:

```yaml
formatting:
  font_size: 12           # 10, 11, or 12
  line_spacing: 1.5       # 1.0, 1.5, or 2.0
  bibliography_style: IEEE # IEEE, APA, or ACM
```

See [Customization Guide](docs/CUSTOMIZATION.md) for more options.

## 📖 Example Usage

### Proposal Report

```yaml
project:
  title: "Web Accessibility Analyzer"
  type: "proposal"

author:
  name: "John Doe"
  roll_number: "2021CS001"
  email: "john.doe@university.edu"

academic:
  supervisor: "Dr. Jane Smith"
  department: "Department of Computer Science"
  university: "Your University Name"
  degree: "Bachelor of Technology"
  session: "2024-25"

dates:
  submission_date: "November 2024"
```

### Major Project Report

Same as proposal, but set `type: "major-project"` and add supervisor details:

```yaml
academic:
  supervisor_designation: "Professor"
  supervisor_department: "Department of Computer Science"
```

## 🛠️ Tech Stack

- **Python 3.9+** - Core generator
- **Jinja2** - Template rendering
- **PyYAML** - Configuration parsing
- **LaTeX** - Document generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas where you can contribute:

- New university templates
- Additional report types
- Bug fixes
- Documentation improvements
- Translations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- IEEE for the bibliography style
- LaTeX community for excellent documentation
- All contributors and users of this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/discussions)
- **Documentation**: [docs/](docs/)

## 🗺️ Roadmap

### ✅ Completed

- [x] Proposal report template
- [x] Major project report template
- [x] Presentation slides (Beamer)
- [x] Interactive CLI generator
- [x] YAML configuration support
- [x] Zero-dependency fallback script
- [x] Comprehensive documentation
- [x] GitHub Pages deployment
- [x] CI/CD auto-compilation
- [x] Content extraction from reports
- [x] Unit testing framework (93% coverage)
- [x] Performance optimizations (66% faster)
- [x] Error handling with helpful messages
- [x] Progress tracking and UX improvements

### 🚧 In Progress / Planned

- [ ] Web-based configuration generator
- [ ] Multiple university templates (IIT Delhi, IISc, etc.)
- [ ] Template customization UI
- [ ] Multi-language support
- [ ] PyPI package distribution
- [ ] VS Code extension

See [PENDING_ITEMS.md](PENDING_ITEMS.md) for detailed feature roadmap.

---

-- **Made with ❤️ for students and researchers** --
