/**
 * Web config generator — builds config.yaml and validates client-side
 * using the same rules as scripts/utils/validators.py where applicable.
 */

const EMAIL_RE = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const DATE_RE = /^[A-Z][a-z]+\s+\d{4}$/;
const VALID_TYPES = ["proposal", "major-project", "presentation"];

/** Double-quote YAML string with minimal escaping. */
function yamlQuote(str) {
  return `"${String(str).replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
}

function validateEmail(email) {
  if (!email || !String(email).trim()) return true;
  return EMAIL_RE.test(String(email).trim());
}

function validateDateFormat(dateStr) {
  if (!dateStr || !String(dateStr).trim()) return false;
  return DATE_RE.test(String(dateStr).trim());
}

function getTrimmed(value) {
  return value == null ? "" : String(value).trim();
}

function collectConfig() {
  const type = document.getElementById("project-type").value;
  const dept = getTrimmed(document.getElementById("academic-dept").value);
  let supervisorDept = getTrimmed(document.getElementById("supervisor-dept").value);
  if (type === "major-project" && !supervisorDept) {
    supervisorDept = dept;
  }

  const config = {
    project: {
      title: getTrimmed(document.getElementById("project-title").value),
      type,
    },
    author: {
      name: getTrimmed(document.getElementById("author-name").value),
      roll_number: getTrimmed(document.getElementById("author-roll").value),
      email: getTrimmed(document.getElementById("author-email").value),
    },
    academic: {
      supervisor: getTrimmed(document.getElementById("academic-supervisor").value),
      co_supervisor: getTrimmed(document.getElementById("academic-co").value),
      department: dept,
      university: getTrimmed(document.getElementById("academic-uni").value),
      degree: getTrimmed(document.getElementById("academic-degree").value),
      session: getTrimmed(document.getElementById("academic-session").value),
    },
    dates: {
      submission_date: getTrimmed(document.getElementById("submission-date").value),
    },
    formatting: {
      color_scheme: document.getElementById("fmt-color").value,
      font_size: parseInt(document.getElementById("fmt-size").value, 10),
      line_spacing: parseFloat(document.getElementById("fmt-spacing").value),
      bibliography_style: document.getElementById("fmt-bib").value,
    },
    content: {
      include_declaration: document.querySelector('input[name="content.include_declaration"]').checked,
      include_certificate: document.querySelector('input[name="content.include_certificate"]').checked,
      include_acknowledgments: document.querySelector('input[name="content.include_acknowledgments"]').checked,
      include_abstract: document.querySelector('input[name="content.include_abstract"]').checked,
    },
  };

  if (type === "major-project") {
    config.academic.supervisor_designation = getTrimmed(
      document.getElementById("supervisor-designation").value
    );
    config.academic.supervisor_department = supervisorDept;
  }

  const logo = getTrimmed(document.getElementById("logo-path").value);
  if (logo) {
    config.assets = { logo_path: logo };
  }

  if (type === "presentation") {
    const presDate = getTrimmed(document.getElementById("pres-date").value);
    config.presentation = {
      theme: getTrimmed(document.getElementById("pres-theme").value) || "Madrid",
      color_scheme: getTrimmed(document.getElementById("pres-color").value) || "default",
      aspect_ratio: document.getElementById("pres-aspect").value,
      presentation_date: presDate,
      extract_from_report: document.getElementById("pres-extract").checked,
      report_path: getTrimmed(document.getElementById("pres-report-path").value),
    };
  }

  return config;
}

/**
 * Mirrors scripts/utils/validators.validate_config plus session, submission date,
 * and major-project supervisor lines expected by templates.
 */
function validateConfig(config) {
  const errors = [];

  const required = [
    "project.title",
    "project.type",
    "author.name",
    "author.roll_number",
    "academic.supervisor",
    "academic.department",
    "academic.university",
    "academic.degree",
    "academic.session",
  ];

  for (const path of required) {
    const parts = path.split(".");
    let cur = config;
    let ok = true;
    for (const p of parts) {
      if (!cur || typeof cur !== "object" || !(p in cur) || !String(cur[p]).trim()) {
        ok = false;
        break;
      }
      cur = cur[p];
    }
    if (!ok) errors.push(`Missing or empty: ${path}`);
  }

  if (config.project && config.project.type && !VALID_TYPES.includes(config.project.type)) {
    errors.push(`Invalid project type: must be one of ${VALID_TYPES.join(", ")}`);
  }

  if (config.author && config.author.email && !validateEmail(config.author.email)) {
    errors.push(`Invalid email format: ${config.author.email}`);
  }

  if (config.dates && !validateDateFormat(config.dates.submission_date)) {
    errors.push('Submission date must look like "Month YYYY" (e.g. November 2024).');
  }

  if (config.project && config.project.type === "major-project") {
    if (!getTrimmed(config.academic.supervisor_designation)) {
      errors.push("Supervisor designation is required for major project reports.");
    }
    if (!getTrimmed(config.academic.supervisor_department)) {
      errors.push("Supervisor department is required for major project reports.");
    }
  }

  const fs = config.formatting && config.formatting.font_size;
  if (fs != null && ![10, 11, 12].includes(fs)) {
    errors.push("Font size must be 10, 11, or 12.");
  }

  const ls = config.formatting && config.formatting.line_spacing;
  if (ls != null && ![1.0, 1.5, 2.0].includes(ls)) {
    errors.push("Line spacing must be 1.0, 1.5, or 2.0.");
  }

  return errors;
}

function buildYaml(config) {
  const lines = [];
  lines.push("# Generated by IITJ MTP Web config generator");
  lines.push("# docs/input_schema.md — full schema reference");
  lines.push("");

  lines.push("project:");
  lines.push(`  title: ${yamlQuote(config.project.title)}`);
  lines.push(`  type: ${yamlQuote(config.project.type)}`);
  lines.push("");

  lines.push("author:");
  lines.push(`  name: ${yamlQuote(config.author.name)}`);
  lines.push(`  roll_number: ${yamlQuote(config.author.roll_number)}`);
  lines.push(`  email: ${yamlQuote(config.author.email)}`);
  lines.push("");

  lines.push("academic:");
  lines.push(`  supervisor: ${yamlQuote(config.academic.supervisor)}`);
  lines.push(`  co_supervisor: ${yamlQuote(config.academic.co_supervisor)}`);
  if (config.project.type === "major-project") {
    lines.push(`  supervisor_designation: ${yamlQuote(config.academic.supervisor_designation)}`);
    lines.push(`  supervisor_department: ${yamlQuote(config.academic.supervisor_department)}`);
  }
  lines.push(`  department: ${yamlQuote(config.academic.department)}`);
  lines.push(`  university: ${yamlQuote(config.academic.university)}`);
  lines.push(`  degree: ${yamlQuote(config.academic.degree)}`);
  lines.push(`  session: ${yamlQuote(config.academic.session)}`);
  lines.push("");

  lines.push("dates:");
  lines.push(`  submission_date: ${yamlQuote(config.dates.submission_date)}`);
  lines.push("");

  if (config.project.type === "presentation") {
    const p = config.presentation;
    lines.push("presentation:");
    lines.push(`  theme: ${yamlQuote(p.theme)}`);
    lines.push(`  color_scheme: ${yamlQuote(p.color_scheme)}`);
    lines.push(`  aspect_ratio: ${yamlQuote(p.aspect_ratio)}`);
    lines.push(`  presentation_date: ${yamlQuote(p.presentation_date)}`);
    lines.push(`  extract_from_report: ${p.extract_from_report ? "true" : "false"}`);
    lines.push(`  report_path: ${yamlQuote(p.report_path)}`);
    lines.push("");
  }

  lines.push("formatting:");
  lines.push(`  color_scheme: ${yamlQuote(config.formatting.color_scheme)}`);
  lines.push(`  font_size: ${config.formatting.font_size}`);
  lines.push(`  line_spacing: ${config.formatting.line_spacing}`);
  lines.push(`  bibliography_style: ${yamlQuote(config.formatting.bibliography_style)}`);
  lines.push("");

  lines.push("content:");
  lines.push(`  include_declaration: ${config.content.include_declaration}`);
  lines.push(`  include_certificate: ${config.content.include_certificate}`);
  lines.push(`  include_acknowledgments: ${config.content.include_acknowledgments}`);
  lines.push(`  include_abstract: ${config.content.include_abstract}`);
  lines.push("");

  if (config.assets && config.assets.logo_path) {
    lines.push("assets:");
    lines.push(`  logo_path: ${yamlQuote(config.assets.logo_path)}`);
    lines.push("");
  }

  return lines.join("\n");
}

function updateVisibility() {
  const type = document.getElementById("project-type").value;
  document.getElementById("presentation-block").classList.toggle("hidden", type !== "presentation");
  document.getElementById("major-supervisor-fields").classList.toggle("hidden", type !== "major-project");

  const designationInput = document.getElementById("supervisor-designation");
  const deptInput = document.getElementById("supervisor-dept");
  if (type === "major-project") {
    designationInput.required = true;
    deptInput.required = true;
  } else {
    designationInput.required = false;
    deptInput.required = false;
  }
}

/** Only when report type changes — not on every form input. */
function applyTypeContentDefaults() {
  const type = document.getElementById("project-type").value;
  const boxes = document.querySelectorAll('#content-checkboxes input[type="checkbox"]');
  if (type === "presentation") {
    boxes.forEach((cb) => {
      cb.checked = false;
    });
  } else {
    boxes.forEach((cb) => {
      cb.checked = true;
    });
  }

  if (type === "major-project") {
    const supDept = document.getElementById("supervisor-dept");
    if (!getTrimmed(supDept.value)) {
      supDept.value = getTrimmed(document.getElementById("academic-dept").value);
    }
  }
}

function renderStatus(errors) {
  const el = document.getElementById("validation-status");
  const download = document.getElementById("btn-download");
  const copy = document.getElementById("btn-copy");

  if (!errors.length) {
    el.className = "status ok";
    el.innerHTML = "<strong>Valid.</strong> You can download or copy the YAML.";
    el.classList.remove("hidden");
    download.disabled = false;
    copy.disabled = false;
    return;
  }

  el.className = "status err";
  el.innerHTML = `<strong>Fix the following:</strong><ul>${errors.map((e) => `<li>${escapeHtml(e)}</li>`).join("")}</ul>`;
  el.classList.remove("hidden");
  download.disabled = true;
  copy.disabled = true;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function refresh() {
  updateVisibility();
  const config = collectConfig();
  const errors = validateConfig(config);

  document.getElementById("yaml-preview").textContent = buildYaml(config);
  renderStatus(errors);

  const hint = document.getElementById("preview-hint");
  hint.textContent = errors.length
    ? "Preview updates as you type; fix validation errors to enable download."
    : "YAML matches the form and passes validation.";
}

function downloadYaml() {
  const config = collectConfig();
  const errors = validateConfig(config);
  if (errors.length) return;

  const yaml = buildYaml(config);
  const blob = new Blob([yaml], { type: "text/yaml;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "config.yaml";
  a.click();
  URL.revokeObjectURL(a.href);
}

async function copyYaml() {
  const config = collectConfig();
  const errors = validateConfig(config);
  if (errors.length) return;

  const yaml = buildYaml(config);
  try {
    await navigator.clipboard.writeText(yaml);
    const hint = document.getElementById("preview-hint");
    const prev = hint.textContent;
    hint.textContent = "Copied to clipboard.";
    setTimeout(() => {
      hint.textContent = prev;
    }, 2000);
  } catch {
    document.getElementById("preview-hint").textContent =
      "Clipboard unavailable — select text in the preview or use Download.";
  }
}

function init() {
  document.getElementById("project-type").addEventListener("change", () => {
    applyTypeContentDefaults();
    refresh();
  });
  document.getElementById("config-form").addEventListener("input", refresh);
  document.getElementById("config-form").addEventListener("change", (e) => {
    if (e.target && e.target.id === "project-type") return;
    refresh();
  });
  document.getElementById("btn-download").addEventListener("click", downloadYaml);
  document.getElementById("btn-copy").addEventListener("click", copyYaml);

  const deptEl = document.getElementById("academic-dept");
  const supDeptEl = document.getElementById("supervisor-dept");
  deptEl.addEventListener("input", () => {
    if (document.getElementById("project-type").value === "major-project" && !getTrimmed(supDeptEl.value)) {
      supDeptEl.placeholder = deptEl.value || "Same as department";
    }
  });

  updateVisibility();
  refresh();
}

init();
