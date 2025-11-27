---
layout: default
title: Input Schema Reference
---

## Input Schema Reference

Complete reference for all configuration options.

[View Full Documentation](INPUT_SCHEMA.md)

## Quick Reference

### Required Fields

```yaml
project:
  title: "Your Project Title"
  type: "proposal"  # or "major-project"

author:
  name: "Full Name"
  roll_number: "Student ID"

academic:
  supervisor: "Dr. Supervisor Name"
  department: "Department Name"
  university: "University Name"
  degree: "Degree Name"
  session: "2024-25"

dates:
  submission_date: "November 2024"
```

### Optional Fields

```yaml
formatting:
  font_size: 12
  line_spacing: 1.5
  bibliography_style: "IEEE"

content:
  include_declaration: true
  include_certificate: true

assets:
  logo_path: "./path/to/logo.png"
```

---

[← Back to Home](index.md)
