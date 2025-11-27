# Proposal Report Template

This directory contains your generated proposal report. Follow the instructions below to complete and compile your report.

## 📁 File Structure

```bash
.
├── proposal.tex              # Main LaTeX file
├── titlePage.tex             # Title page
├── sections/                 # Content sections
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── literature_review.tex
│   ├── methodology.tex
│   └── timeline.tex
├── proposal_refs.bib         # Bibliography
├── IEEEtran.bst             # IEEE bibliography style
└── logo.png                  # University logo
```

## ✏️ Editing Your Report

1. **Abstract** (`sections/abstract.tex`): Write a 150-300 word summary of your project
2. **Introduction** (`sections/introduction.tex`): Complete the motivation, problem statement, and objectives
3. **Literature Review** (`sections/literature_review.tex`): Add related work and gap analysis
4. **Methodology** (`sections/methodology.tex`): Describe your system architecture and approach
5. **Timeline** (`sections/timeline.tex`): Update the project milestones and deliverables
6. **References** (`proposal_refs.bib`): Add your bibliography entries

## 🔧 Compiling the Report

### Using pdflatex (Recommended)

```bash
pdflatex proposal.tex
bibtex proposal
pdflatex proposal.tex
pdflatex proposal.tex
```

### Using latexmk (If available)

```bash
latexmk -pdf proposal.tex
```

### Clean auxiliary files

```bash
# Windows
del *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot

# Linux/Mac
rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
```

## 📝 Tips

- Search for `[TODO]` markers in the .tex files to find sections that need completion
- Use `\cite{reference_key}` to cite references from `proposal_refs.bib`
- Add figures to a `figures/` directory and include them with `\includegraphics{figures/filename.png}`
- Keep paragraphs concise and use subsections to organize content

## 🆘 Common Issues

**Issue**: Bibliography not showing

- **Solution**: Make sure you've cited at least one reference using `\cite{key}` and run bibtex

**Issue**: Figures not displaying

- **Solution**: Check that image files exist and paths are correct

**Issue**: Compilation errors

- **Solution**: Check for special characters that need escaping: `& % $ # _ { } ~ ^`

## 📚 Resources

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
- [Overleaf Documentation](https://www.overleaf.com/learn)
- [IEEE Citation Guide](https://ieee-dataport.org/sites/default/files/analysis/27/IEEE%20Citation%20Guidelines.pdf)
