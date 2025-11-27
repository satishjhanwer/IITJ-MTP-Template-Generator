# IITJ MTP Template Generator

Generate professional LaTeX academic reports (proposals, major projects, presentations) with dynamic user inputs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/)
[![Test Status](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/workflows/Test%20Generator/badge.svg)](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/actions)

## 🎯 Features

- **Interactive CLI** - Easy-to-use command-line interface for collecting inputs
- **YAML Configuration** - Use config files for reproducible report generation
- **Multiple Report Types** - Proposal reports and major project reports (presentations coming in Phase 2)
- **Professional Templates** - IEEE-style LaTeX templates with proper formatting
- **Customizable** - Modify templates to match your university's requirements
- **Well-Documented** - Comprehensive guides and examples included

## 📋 Supported Report Types

### Phase 1 (Available Now)

- ✅ **Proposal Report** (MTP1/Research Proposal)
- ✅ **Major Project Report** (Full Thesis/Dissertation)

### Phase 2 (Coming Soon)

- ⏳ **Presentation Slides** (Beamer)

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

```bash
cd output/your-project-name
pdflatex proposal.tex  # or main.tex for major projects
bibtex proposal        # or main
pdflatex proposal.tex
pdflatex proposal.tex
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
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
│   └── major-project/           # Major project template
├── examples/
│   ├── sample-proposal/         # Example proposal config
│   └── sample-major-project/    # Example major project config
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

- [x] Phase 1: Core generator and templates
- [x] Proposal report template
- [x] Major project report template
- [ ] Phase 2: Presentation slides (Beamer)
- [ ] Phase 3: Web-based configuration generator
- [ ] Phase 4: Multiple university templates
- [ ] Phase 5: CI/CD for auto-compilation

---

-- **Made with ❤️ for students and researchers** --
