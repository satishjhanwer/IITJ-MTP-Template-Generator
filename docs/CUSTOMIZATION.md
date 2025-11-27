# Customization Guide

Learn how to customize the IITJ MTP Template Generator templates to match your needs.

## Table of Contents

1. [Formatting Options](#formatting-options)
2. [Modifying Templates](#modifying-templates)
3. [Custom Logos](#custom-logos)
4. [Adding Custom Sections](#adding-custom-sections)
5. [Bibliography Styles](#bibliography-styles)
6. [Advanced Customization](#advanced-customization)

## Formatting Options

### Font Size

Change the base font size in your config:

```yaml
formatting:
  font_size: 12  # Options: 10, 11, 12
```

Or modify the template directly in `proposal.tex` or `main.tex`:

```latex
\documentclass[12pt]{article}  % Change 12pt to 10pt or 11pt
```

### Line Spacing

Adjust line spacing in your config:

```yaml
formatting:
  line_spacing: 1.5  # Options: 1.0, 1.5, 2.0
```

Or in the template:

```latex
\setstretch{1.5}  % Change to 1.0 or 2.0
```

### Page Margins

Modify margins in the template:

```latex
\geometry{
    paper=a4paper,
    inner=1in,        % Left margin
    outer=1in,        % Right margin
    top=0.75in,       % Top margin
    bottom=0.75in     % Bottom margin
}
```

### Colors

For Beamer presentations (Phase 2), you can customize colors:

```latex
\usecolortheme{default}  % blue
\usecolortheme{crane}    % orange
\usecolortheme{beaver}   % red
```

For reports, add custom colors:

```latex
\usepackage{xcolor}
\definecolor{primarycolor}{RGB}{0, 102, 204}
```

## Modifying Templates

### Directory Structure

Templates are located in:

- `templates/proposal/` - Proposal report templates
- `templates/major-project/` - Major project templates

### Jinja2 Syntax

Templates use Jinja2 syntax with LaTeX-friendly delimiters:

- Variables: `\VAR{VARIABLE_NAME}`
- Blocks: `\BLOCK{if condition}...\BLOCK{endif}`
- Comments: `\#{comment}`

### Example: Adding a Custom Variable

1. In your config file:

```yaml
custom:
  project_code: "CS-2024-001"
```

1. In `scripts/utils/template_engine.py`, add to `prepare_context()`:

```python
'PROJECT_CODE': config.get('custom', {}).get('project_code', ''),
```

1. In your template:

```latex
Project Code: \VAR{PROJECT_CODE}
```

## Custom Logos

### Using Your University Logo

1. **Via Config File**:

```yaml
assets:
  logo_path: "./path/to/logo.png"
```

1. **Via Command Line**:

```bash
python scripts/generate.py --config config.yaml --logo path/to/logo.png
```

### Logo Requirements

- **Format**: PNG, JPG, or PDF
- **Size**: Minimum 300x300 pixels
- **Aspect Ratio**: Square (1:1) recommended
- **Quality**: High resolution for print

### Adjusting Logo Size

In `titlePage.tex`:

```latex
\includegraphics[width=0.3\textwidth]{logo.png}  % Change 0.3 to adjust size
```

## Adding Custom Sections

### For Proposal Reports

1. Create a new section file in `templates/proposal/sections/`:

```bash
touch templates/proposal/sections/my_section.tex
```

1. Add content to `my_section.tex`:

```latex
% TODO: Add your custom section content here

\subsection{Custom Subsection}
Content goes here...
```

1. Include it in `proposal.tex`:

```latex
\section{My Custom Section}
\input{sections/my_section.tex}
```

### For Major Project Reports

Same process, but use `templates/major-project/chapters/` directory.

## Bibliography Styles

### Using IEEE Style (Default)

```latex
\bibliographystyle{IEEEtran}
\bibliography{refs}
```

### Using APA Style

1. Download `apa.bst` from CTAN
2. Place it in your template directory
3. Update the template:

```latex
\bibliographystyle{apa}
\bibliography{refs}
```

### Using ACM Style

1. Download `ACM-Reference-Format.bst`
2. Place it in your template directory
3. Update the template:

```latex
\bibliographystyle{ACM-Reference-Format}
\bibliography{refs}
```

### Custom Bibliography Format

Modify the `.bst` file or create your own using `makebst` tool.

## Advanced Customization

### Custom Chapter Formatting

Modify chapter headings using `titlesec`:

```latex
\usepackage{titlesec}

\titleformat{\section}
  {\normalfont\Large\bfseries\centering}  % Format
  {\thesection}                            % Label
  {1em}                                    % Sep
  {}                                       % Before code

\titleformat{\subsection}
  {\normalfont\large\bfseries}
  {\thesubsection}
  {1em}
  {}
```

### Custom Headers and Footers

Add page headers and footers:

```latex
\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\fancyfoot[C]{Your University Name}
```

### Custom Title Page Layout

Modify `titlePage.tex` to change the layout:

```latex
% Change from right-aligned to centered
\begin{center}
\Huge{\textbf{\ttitle}}
\end{center}
```

### Adding a Table of Abbreviations

1. Create `abbreviations.tex`:

```latex
\section*{List of Abbreviations}
\begin{tabular}{ll}
API & Application Programming Interface \\
HTML & HyperText Markup Language \\
WCAG & Web Content Accessibility Guidelines \\
\end{tabular}
```

1. Include it in main file:

```latex
\newpage
\input{abbreviations.tex}
```

### Custom Figure and Table Numbering

Change numbering style:

```latex
% Chapter.Section.Number format
\counterwithin{figure}{section}
\counterwithin{table}{section}

% Continuous numbering
\counterwithout{figure}{section}
\counterwithout{table}{section}
```

### Adding Appendices

```latex
\appendix

\section{Appendix A: Additional Data}
\input{appendices/appendix_a.tex}

\section{Appendix B: Code Listings}
\input{appendices/appendix_b.tex}
```

## Template Inheritance

### Creating a University-Specific Template

1. Copy the base template:

```bash
cp -r templates/proposal templates/proposal-myuni
```

1. Modify the copied template
1. Update generator to support new template type

### Sharing Custom Templates

1. Fork the repository
2. Add your custom template
3. Submit a pull request
4. Document your customizations

## Tips and Best Practices

1. **Test Changes**: Always test template modifications by generating a sample report
2. **Version Control**: Keep your customizations in version control
3. **Document Changes**: Add comments explaining custom modifications
4. **Backup Originals**: Keep a copy of original templates before modifying
5. **Validate LaTeX**: Use a LaTeX editor with syntax checking
6. **Incremental Changes**: Make small changes and test frequently

## Common Customizations

### Remove List of Figures/Tables

In `main.tex` or `proposal.tex`, comment out:

```latex
% \listoffigures
% \listoftables
```

### Change Date Format

```latex
\usepackage{datetime}
\newdateformat{mydate}{\THEDAY\ \monthname[\THEMONTH] \THEYEAR}
\mydate\today
```

### Add Line Numbers (for Review)

```latex
\usepackage{lineno}
\linenumbers
```

### Two-Column Layout

```latex
\documentclass[12pt,twocolumn]{article}
```

## Getting Help

- Check existing templates for examples
- Consult [LaTeX documentation](https://www.overleaf.com/learn)
- Ask in [GitHub Discussions](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/discussions)
- See [FAQ](faq) for common issues

---

**Need more customization options? Open an issue on GitHub!**
