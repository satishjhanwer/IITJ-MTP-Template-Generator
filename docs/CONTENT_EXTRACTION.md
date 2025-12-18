# Content Extraction from Reports

## Overview

The IITJ MTP Template Generator can automatically extract content from existing LaTeX reports (proposal or major project) to populate presentation slides. This feature saves time and ensures consistency between your report and presentation.

## How It Works

The content extractor:

1. Parses your existing LaTeX report
2. Extracts content from key sections
3. Cleans LaTeX commands and formatting
4. Populates presentation slides with extracted content
5. Falls back to TODO placeholders if extraction fails

## Configuration

### Enable Content Extraction

Add to your `config.yaml`:

```yaml
presentation:
  theme: "Madrid"
  color_scheme: "default"
  aspect_ratio: "16:9"
  
  # Content extraction
  extract_from_report: true
  report_path: "./output/my-project/main.tex"  # Path to your report
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `extract_from_report` | Enable/disable extraction | `false` |
| `report_path` | Path to LaTeX report file | `""` |

## Content Mapping

The extractor maps report sections to presentation slides:

| Report Section | Presentation Slide | What's Extracted |
|----------------|-------------------|------------------|
| Abstract | Introduction overview | First 2-3 sentences |
| Introduction | Motivation slide | First paragraph or Motivation subsection |
| Problem Statement | Problem slide | Problem Statement subsection |
| Objectives | Objectives slide | Itemized list of objectives (max 5) |
| Methodology | Methodology overview | First paragraph |
| Technologies | Technologies slide | List of tools/frameworks |
| Results | Results slides | Implementation highlights, evaluation summary |
| Conclusion | Summary slide | First paragraph |
| Future Work | Future Work slide | Itemized list (max 4) |

## Usage Example

### Step 1: Generate Your Report

```bash
python scripts/generate.py --config my-report-config.yaml
```

### Step 2: Create Presentation Config

Create `presentation-config.yaml`:

```yaml
project:
  title: "My Project Title"
  type: "presentation"

author:
  name: "Your Name"
  roll_number: "2021CS001"

academic:
  supervisor: "Dr. Supervisor Name"
  department: "Department of Computer Science"
  university: "Your University"
  degree: "Bachelor of Technology"
  session: "2024-25"

dates:
  submission_date: "December 2024"

presentation:
  theme: "Madrid"
  color_scheme: "default"
  aspect_ratio: "16:9"
  presentation_date: "December 2024"
  
  # Enable extraction
  extract_from_report: true
  report_path: "./output/my-project/main.tex"
```

### Step 3: Generate Presentation

```bash
python scripts/generate.py --config presentation-config.yaml
```

Output:

```txt
📄 Extracting content from: ./output/my-project/main.tex
✅ Content extracted successfully
📁 Output directory: output/my-project-presentation
✅ Report generated successfully!
```

## What Gets Extracted

### Introduction Section

**From Report:**

```latex
\section{Introduction}
This project addresses the growing need for accessible web applications.
Web accessibility ensures that people with disabilities can use websites...

\subsection{Motivation}
According to WHO, over 1 billion people live with some form of disability...
```

**To Presentation:**

```latex
\begin{frame}{Motivation}
According to WHO, over 1 billion people live with some form of disability...
\end{frame}
```

### Objectives Section

**From Report:**

```latex
\section{Objectives}
\begin{itemize}
    \item Develop an automated accessibility testing tool
    \item Implement WCAG 2.1 compliance checking
    \item Create detailed accessibility reports
\end{itemize}
```

**To Presentation:**

```latex
\begin{frame}{Objectives}
\begin{enumerate}
    \item Develop an automated accessibility testing tool
    \item Implement WCAG 2.1 compliance checking
    \item Create detailed accessibility reports
\end{enumerate}
\end{frame}
```

## Limitations

### What Works Well

✅ Standard LaTeX section structures  
✅ Itemize/enumerate lists  
✅ Simple text paragraphs  
✅ Common LaTeX commands  

### What May Need Manual Review

⚠️ Complex nested structures  
⚠️ Mathematical equations  
⚠️ Tables and figures  
⚠️ Custom LaTeX commands  
⚠️ Non-standard section names  

## Best Practices

### 1. Review Extracted Content

Always review the generated slides. The extraction is "best effort" and may need refinement.

### 2. Use Standard Section Names

For best results, use standard section names in your report:

- Introduction
- Objectives
- Methodology
- Results
- Conclusion
- Future Work

### 3. Keep Lists Simple

Simple itemize/enumerate lists extract better than complex nested structures.

### 4. Provide Fallback

If extraction fails, the generator falls back to TODO placeholders, so you can still generate the presentation.

## Troubleshooting

### No Content Extracted

**Problem:** Extraction completes but slides are empty

**Solutions:**

- Check that report uses standard section names
- Verify report file path is correct
- Check report file is valid LaTeX

### Extraction Fails

**Problem:** Error message during extraction

**Solutions:**

- Verify report file exists at specified path
- Check file is readable
- Try with absolute path instead of relative

### Partial Extraction

**Problem:** Some sections extracted, others missing

**Solutions:**

- Check section names in your report
- Verify sections contain extractable content
- Review extraction logs for warnings

## Advanced Usage

### Custom Section Names

If your report uses non-standard section names, you can:

1. Temporarily rename sections in a copy
2. Extract content
3. Manually copy content for non-standard sections

### Combining Manual and Extracted Content

You can:

1. Enable extraction to get base content
2. Edit generated slides to add/refine content
3. Add figures, diagrams manually

## Technical Details

### LaTeX Parsing

The extractor uses regex-based parsing:

- Matches `\section{}` and `\subsection{}` patterns
- Extracts environment content (`\begin{}...\end{}`)
- Parses `\item` entries from lists
- Cleans common LaTeX commands

### Content Cleaning

Automatically removes:

- Citations (`\cite{}`, `\citep{}`)
- References (`\ref{}`, `\label{}`)
- Formatting commands (`\textbf{}`, `\textit{}`)
- Comments (`%...`)
- Figure/table environments

### Error Handling

- Graceful degradation on parse errors
- Continues if one section fails
- Falls back to TODO placeholders
- Logs warnings for debugging

## FAQ

**Q: Can I extract from PDF files?**  
A: No, extraction only works with LaTeX (.tex) source files.

**Q: Will it preserve my custom formatting?**  
A: Basic formatting is preserved, but complex LaTeX may be simplified.

**Q: Can I extract from multiple files?**  
A: Specify the main file; `\input{}` statements are not followed.

**Q: Does it work with Overleaf projects?**  
A: Yes, download your project and extract from the main .tex file.

**Q: Can I customize what gets extracted?**  
A: Currently no, but you can edit the generated slides after extraction.

---

**Need Help?** Open an issue on [GitHub](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/issues)
