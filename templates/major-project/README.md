# Major Project Report Template

This directory contains your generated major project report. Follow the instructions below to complete and compile your report.

## 📁 File Structure

```bash
.
├── main.tex                  # Main LaTeX file
├── titlePage.tex             # Title page
├── declaration.tex           # Declaration page
├── certificate.tex           # Certificate page
├── acknowledgments.tex       # Acknowledgments
├── abstract.tex              # Abstract
├── chapters/                 # Content chapters
│   ├── introduction.tex
│   ├── literature.tex
│   ├── methodology.tex
│   ├── implementation.tex
│   ├── results.tex
│   ├── discussion.tex
│   └── conclusion.tex
├── refs.bib                  # Bibliography
├── IEEEtran.bst             # IEEE bibliography style
└── logo.png                  # University logo
```

## ✏️ Editing Your Report

### Front Matter

1. **Title Page** (`titlePage.tex`): Auto-generated from your inputs
2. **Declaration** (`declaration.tex`): Auto-generated, review and sign
3. **Certificate** (`certificate.tex`): Auto-generated, get supervisor signature
4. **Acknowledgments** (`acknowledgments.tex`): Customize with project-specific acknowledgments
5. **Abstract** (`abstract.tex`): Write a 150-300 word summary

### Main Chapters

1. **Introduction** (`chapters/introduction.tex`): Background, problem, objectives, contributions
2. **Literature Review** (`chapters/literature.tex`): Related work, gap analysis
3. **Methodology** (`chapters/methodology.tex`): System design, architecture, approach
4. **Implementation** (`chapters/implementation.tex`): Development details, features, challenges
5. **Results** (`chapters/results.tex`): Experimental results, evaluation, analysis
6. **Discussion** (`chapters/discussion.tex`): Interpretation, strengths, limitations
7. **Conclusion** (`chapters/conclusion.tex`): Summary, contributions, future work

### References

- **Bibliography** (`refs.bib`): Add all your references in BibTeX format

## 🔧 Compiling the Report

### Using pdflatex (Recommended)

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Using latexmk (If available)

```bash
latexmk -pdf main.tex
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
- Use `\cite{reference_key}` to cite references from `refs.bib`
- Create a `figures/` directory for images and diagrams
- Include figures with `\includegraphics[width=0.8\textwidth]{figures/filename.png}`
- Use tables to present data clearly
- Keep sections focused and well-organized
- Proofread carefully before final submission

## 🆘 Common Issues

**Issue**: Bibliography not showing

- **Solution**: Make sure you've cited at least one reference using `\cite{key}` and run bibtex

**Issue**: Figures not displaying

- **Solution**: Check that image files exist and paths are correct. Use forward slashes in paths.

**Issue**: Table of contents not updating

- **Solution**: Run pdflatex multiple times (usually 2-3 times)

**Issue**: Compilation errors with special characters

- **Solution**: Escape special LaTeX characters: `\& \% \$ \# \_ \{ \} \~ \^`

**Issue**: Page numbers incorrect

- **Solution**: Run pdflatex multiple times to resolve cross-references

## 📚 Resources

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
- [Overleaf Documentation](https://www.overleaf.com/learn)
- [IEEE Citation Guide](https://ieee-dataport.org/sites/default/files/analysis/27/IEEE%20Citation%20Guidelines.pdf)
- [Google Scholar](https://scholar.google.com) - Generate BibTeX entries automatically

## 📐 Formatting Guidelines

- **Font Size**: 12pt (default)
- **Line Spacing**: 1.5 (default)
- **Margins**: 1 inch all around
- **Page Numbers**: Automatic
- **Citation Style**: IEEE (default)
