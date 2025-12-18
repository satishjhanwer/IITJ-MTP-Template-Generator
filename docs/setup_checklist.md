# Repository Setup Checklist

Complete this checklist to set up and deploy your Academic Report Generator repository.

## ✅ Pre-Push Checklist

### 1. Local Testing

- [ ] Install dependencies: `pip install -r scripts/requirements.txt`
- [ ] Test proposal generation:

  ```bash
  python scripts/generate.py --config examples/sample-proposal/config.yaml --output output/test-proposal
  ```

- [ ] Test major project generation:

  ```bash
  python scripts/generate.py --config examples/sample-major-project/config.yaml --output output/test-major
  ```

- [ ] Test zero-dependency version:

  ```bash
  python scripts/generate_simple.py
  ```

- [ ] (Optional) Test LaTeX compilation if you have LaTeX installed:

  ```bash
  cd output/test-proposal
  pdflatex proposal.tex
  bibtex proposal
  pdflatex proposal.tex
  pdflatex proposal.tex
  ```

### 2. Repository Initialization

- [ ] Initialize git repository:

  ```bash
  git init
  ```

- [ ] Add all files:

  ```bash
  git add .
  ```

- [ ] Create initial commit:

  ```bash
  git commit -m "Initial commit: Academic Report Generator"
  ```

### 3. GitHub Repository Setup

- [ ] Create repository on GitHub: `IITJ-MTP-Template-Generator`
- [ ] Add remote:

  ```bash
  git remote add origin https://github.com/satishjhanwer/IITJ-MTP-Template-Generator.git
  ```

- [ ] Push to GitHub:

  ```bash
  git branch -M main
  git push -u origin main
  ```

## 🚀 Post-Push Configuration

### 4. Enable GitHub Pages

- [ ] Go to repository Settings → Pages
- [ ] Source: Deploy from a branch
- [ ] Branch: `main` (or `master`)
- [ ] Folder: `/docs`
- [ ] Click Save
- [ ] Wait 1-2 minutes for deployment
- [ ] Visit: `https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/`

### 5. Configure Repository Settings

- [ ] Add repository description: "Generate professional LaTeX academic reports with ease"
- [ ] Add topics/tags: `latex`, `academic`, `report-generator`, `python`, `thesis`, `proposal`
- [ ] Enable Issues
- [ ] Enable Discussions (optional)
- [ ] Add repository website: `https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/`

### 6. GitHub Actions

- [ ] Go to Actions tab
- [ ] Verify workflows are enabled
- [ ] Check that "Test Generator" workflow runs successfully
- [ ] Check that "Deploy Documentation" workflow runs successfully

### 7. Create First Release

- [ ] Go to Releases → Create a new release
- [ ] Tag version: `v1.0.0`
- [ ] Release title: `v1.0.0 - Initial Release`
- [ ] Description:

  ```markdown
  # Academic Report Generator v1.0.0
  
  First stable release of the Academic Report Generator!
  
  ## Features
  - ✅ Proposal report template
  - ✅ Major project report template
  - ✅ Interactive CLI
  - ✅ YAML configuration support
  - ✅ Zero-dependency fallback
  - ✅ Comprehensive documentation
  
  ## Installation
  See the [Quick Start Guide](https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/quickstart)
  ```

- [ ] Publish release

## 📝 Optional Enhancements

### 8. Add Repository Badges

Add to README.md after the title:

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/)
[![Test Status](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/workflows/Test%20Generator/badge.svg)](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/actions)
```

### 9. Create Issue Templates

- [ ] Create `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] Create `.github/ISSUE_TEMPLATE/feature_request.md`

### 10. Add Pull Request Template

- [ ] Create `.github/PULL_REQUEST_TEMPLATE.md`

### 11. Community Files

- [ ] Verify `CONTRIBUTING.md` is in place
- [ ] Add `CODE_OF_CONDUCT.md` (optional)
- [ ] Add `SECURITY.md` (optional)

## 🎯 Verification

After completing the setup:

- [ ] Visit repository page - looks professional
- [ ] Visit GitHub Pages site - documentation loads correctly
- [ ] Clone repository fresh and test generator
- [ ] Check that Actions workflows pass
- [ ] Verify all links work in documentation

## 📢 Promotion (Optional)

- [ ] Share on social media
- [ ] Post in relevant communities (Reddit, Discord, etc.)
- [ ] Add to awesome lists
- [ ] Submit to package indexes (PyPI - future consideration)

---

**Congratulations! Your repository is ready for users! 🎉**
