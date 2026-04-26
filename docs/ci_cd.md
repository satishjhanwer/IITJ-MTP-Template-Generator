# CI/CD Auto-Compilation Guide

## Overview

The IITJ MTP Template Generator includes automatic LaTeX compilation through GitHub Actions. When you push `.tex` files to your repository, they are automatically compiled to PDF and made available as downloadable artifacts.

## How It Works

### Manual Compilation

The workflow is triggered manually from the GitHub Actions tab (it does not run automatically on push). This keeps your free Actions minutes available for when you actually need a compiled PDF.

### Supported Report Types

All three report types are automatically detected and compiled:

- **Proposal Reports** (`proposal.tex`)
- **Major Project Reports** (`main.tex`)
- **Presentation Slides** (`slides.tex`)

## Using the Workflow

### Setup (One-Time)

1. **Fork or clone** this repository to your GitHub account

2. **Generate your report** using the generator:

   ```bash
   python scripts/generate.py --config my-config.yaml
   ```

3. **Commit and push** the generated files:

   ```bash
   git add output/
   git commit -m "Add my project report"
   git push origin main
   ```

4. **Trigger compilation** manually from the Actions tab (see [Triggering the Workflow](#triggering-the-workflow))

### Downloading Compiled PDFs

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Click on the latest **"Compile LaTeX to PDF"** workflow run
4. Scroll down to **Artifacts**
5. Download `compiled-pdfs-{number}.zip`
6. Extract the ZIP file to get your PDFs

## Triggering the Workflow

To run compilation:

1. Go to **Actions** tab in your repository
2. Click **"Compile LaTeX to PDF"** in the left sidebar
3. Click **"Run workflow"** button
4. Select the branch
5. Click **"Run workflow"**

## Workflow Details

### Compilation Process

For each LaTeX file found, the workflow:

1. **First Pass**: `pdflatex -interaction=nonstopmode file.tex`
2. **Bibliography**: `bibtex file` (if `.bib` files exist)
3. **Second Pass**: `pdflatex -interaction=nonstopmode file.tex`
4. **Third Pass**: `pdflatex -interaction=nonstopmode file.tex` (for references/TOC)

### Artifact Retention

- **Retention Period**: 30 days
- **Artifact Name**: `compiled-pdfs-{run-number}`
- **Contents**: All PDF files from `output/` directory

## Troubleshooting

### No PDFs Generated

**Check the workflow logs:**

1. Go to Actions tab
2. Click on the failed workflow run
3. Expand the "Find and compile LaTeX files" step
4. Look for compilation errors

**Common issues:**

- LaTeX syntax errors in your `.tex` files
- Missing packages or dependencies
- Bibliography errors (missing `.bib` file or citations)

### Compilation Warnings

Warnings are normal and don't prevent PDF generation. The workflow uses `-interaction=nonstopmode` to continue compilation even with warnings.

### Workflow Not Appearing

**Verify:**

- You are on the correct repository page in GitHub
- Workflow file exists at `.github/workflows/compile-latex.yml`
- The workflow has `workflow_dispatch:` in its `on:` section

## Advanced Configuration

### Customizing the Workflow

You can modify `.github/workflows/compile-latex.yml` to:

- Change artifact retention period (line with `retention-days`)
- Add additional LaTeX packages to install
- Modify compilation commands
- Add post-processing steps

### Example: Adding Custom Packages

Edit the "Install LaTeX" step:

```yaml
- name: Install LaTeX
  run: |
    sudo apt-get update
    sudo apt-get install -y \
      texlive-latex-base \
      texlive-latex-extra \
      texlive-bibtex-extra \
      texlive-fonts-extra \    # Add this
      texlive-science \        # Add this
      biber
```

## Status Badge

Add the compilation status badge to your README:

```markdown
[![Compile LaTeX](https://github.com/YOUR-USERNAME/YOUR-REPO/workflows/Compile%20LaTeX%20to%20PDF/badge.svg)](https://github.com/YOUR-USERNAME/YOUR-REPO/actions)
```

Replace `YOUR-USERNAME` and `YOUR-REPO` with your GitHub username and repository name.

## Benefits

- [x] **Automatic PDF Generation** - No need to install LaTeX locally  
- [x] **Version Control** - Every commit gets compiled  
- [x] **Collaboration** - Team members can download PDFs without LaTeX  
- [x] **Consistent Environment** - Same LaTeX version for everyone  
- [x] **Free** - GitHub Actions provides free minutes for public repositories

## Limitations

- **Build Time**: Compilation takes 2-5 minutes depending on document complexity
- **Free Tier**: GitHub provides 2,000 minutes/month for free (public repos)
- **File Size**: Artifacts are limited to 2GB per repository
- **Retention**: Artifacts are deleted after 30 days (configurable)

## FAQ

**Q: Can I compile locally instead?**  
A: Yes! The workflow doesn't replace local compilation. See the main README for local compilation instructions.

**Q: How do I disable auto-compilation?**  
A: Delete or rename `.github/workflows/compile-latex.yml`

**Q: Can I compile on pull requests?**  
A: Yes, modify the workflow's `on:` section to include `pull_request`

**Q: What if compilation fails?**  
A: Check the workflow logs for errors. The workflow continues even if one file fails, so other PDFs may still be generated.

---

**Need Help?** Open an issue on [GitHub](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/issues)

---
