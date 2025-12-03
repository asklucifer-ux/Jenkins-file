#!/usr/bin/env python3
"""
Simple converter: Trivy JSON -> HTML table list
Usage: python generate_trivy_html_report.py trivy-report.json trivy-report.html
"""
import json
import sys
import datetime
from html import escape

def make_row(cols):
    return "<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in cols) + "</tr>\n"

def generate(json_file, html_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = []
    html.append("<!doctype html><html><head><meta charset='utf-8'><title>Trivy Vulnerability Scan Report</title>")
    html.append("<style>table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:6px}th{background:#0b6fa6;color:white}</style>")
    html.append("</head><body>")
    html.append(f"<h1>Trivy Vulnerability Scan Report</h1>")
    html.append(f"<p>Generated On: {datetime.datetime.now().isoformat()}</p>")

    # Trivy JSON top-level can contain Results (array)
    results = data.get("Results", [])
    # Build a single table of vulnerabilities across targets
    html.append("<table>")
    html.append("<thead><tr><th>Target</th><th>Vulnerability ID</th><th>Pkg</th><th>Installed</th><th>Severity</th><th>Title</th><th>Description</th></tr></thead><tbody>")

    for result in results:
        target = result.get("Target", "N/A")
        vulns = result.get("Vulnerabilities") or []
        for v in vulns:
            vid = v.get("VulnerabilityID", "")
            pkg = v.get("PkgName", "")
            inst = v.get("InstalledVersion", "")
            sev = v.get("Severity", "")
            title = v.get("Title", "")
            desc = v.get("Description", "")
            html.append(make_row([target, vid, pkg, inst, sev, title, (desc[:400] + '...') if desc and len(desc)>400 else desc]))

    html.append("</tbody></table>")
    html.append("</body></html>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print("HTML report written to", html_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_trivy_html_report.py input.json output.html")
        sys.exit(2)
    generate(sys.argv[1], sys.argv[2])
