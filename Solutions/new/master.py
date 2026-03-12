def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers, no_top_border_columns=[]):
    from reportlab.lib import colors
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle

    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Define shared paragraph styles
    white_text_style = ParagraphStyle(
        name="WhiteHeaderStyle",
        parent=custom_style,
        textColor=colors.white,
        alignment=1,
    )

    black_text_style = ParagraphStyle(
        name="BlackHeaderStyle",
        parent=custom_style,
        textColor=colors.black,
        alignment=1,
    )

    for level in range(num_levels):
        row = []
        styles = []
        col_idx = 0

        while col_idx < num_columns:
            header = multi_headers[level][col_idx]
            span_count = 1
            row.append("")

            while (
                col_idx + span_count < num_columns and
                multi_headers[level][col_idx + span_count] == header
            ):
                span_count += 1
                row.append("")

            if level == 0 and header == "":
                row[col_idx] = ""
            else:
                style = white_text_style if level == 0 else black_text_style
                row[col_idx] = Paragraph(f"<b>{header}</b>", style)

                bg_color = "#1372be" if level == 0 else "#d5dafb"
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
                header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))
                header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
                header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))

            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

    # Merge vertically those with empty top-level headers (like BM LT Vol, 1D Stdev)
    if num_levels == 2:
        for col_idx in range(num_columns):
            if multi_headers[0][col_idx] == '' and multi_headers[1][col_idx] != '':
                header_styles.append(('SPAN', (col_idx, 0), (col_idx, 1)))

    # Apply solid dark borders to the entire table area
    header_styles.append(('GRID', (0, 0), (-1, num_levels - 1), 1, colors.black))
    header_styles.append(('BOX', (0, 0), (-1, num_levels - 1), 1.5, colors.black))

    # If legacy config for top border removal is still passed
    for col_idx in no_top_border_columns:
        header_styles.append(('LINEABOVE', (col_idx, 0), (col_idx, 0), 0, colors.white))
        header_styles.append(('LINEBEFORE', (col_idx, 0), (col_idx, -1), 0, colors.white))
        header_styles.append(('LINEAFTER', (col_idx, 0), (col_idx, -1), 0, colors.white))
        header_styles.append(('BACKGROUND', (col_idx, 0), (col_idx, 0), colors.white))

    return table_data, header_styles
1) ShadowOps – Self‑Learning Workflow Agent
Use Case Title
ShadowOps – Self‑Learning Workflow Agent

Problem Statement
Across the firm, teams manually resolve thousands of recurring breaks, reconciliations, and workflow interruptions every day. The know‑how to fix these issues lives inside individual analysts’ heads and case histories, not in scalable systems, so the same patterns are re‑executed manually, slowing resolution and consuming highly skilled staff time.

Potential Solution
Introduce ShadowOps, a self‑learning workflow agent that observes how analysts resolve exceptions across systems during real work. Instead of requiring manual process mapping, it learns repeatable patterns directly from user actions, converts them into compliant, auditable workflows, and then starts executing the repetitive steps autonomously while escalating edge cases to humans.

Expected Outcomes / Benefits

Reduced manual effort on high‑volume, repeatable exceptions

Faster and more consistent turnaround time for breaks and reconciliations

Analysts freed to focus on complex, high‑value cases and risk management

An expanding library of automated workflows that compounds efficiency over time

Type of Use Case
AI (including Gen & Agentic AI), Automation, Process Optimization

2) AskMS / KnowBuddy – Instant Team Knowledge Agent
(You can pick the name you like more; I’ll use AskMS here, but KnowBuddy also works.)

Use Case Title
AskMS – Instant Team Knowledge Agent

Problem Statement
Team knowledge is scattered across wikis, runbooks, dashboards, code repositories, chat threads, and incident tickets. Finding a simple answer such as “who owns this job?” or “where is this validation implemented?” often requires searching multiple tools or interrupting colleagues, which slows onboarding, troubleshooting, and day‑to‑day delivery.

Potential Solution
Introduce AskMS, a plug‑and‑play knowledge agent that teams can connect to their existing documentation, repositories, and operational logs in minutes. Colleagues can ask natural‑language questions and receive precise answers with links, owners, and relevant context drawn from their team’s real artifacts, kept up to date as the sources change.

Expected Outcomes / Benefits

Faster onboarding for engineers and analysts joining new teams

Less time spent hunting for internal documentation or “who knows this?”

Better knowledge sharing and fewer single‑point‑of‑failure experts

Quicker troubleshooting and incident resolution across time zones

Type of Use Case
AI (including Gen & Agentic AI), Day to Day Assistant, Business Enablement

3) CodeAtlas – Enterprise Code Discovery Agent
Use Case Title
CodeAtlas – Enterprise Code Discovery Agent

Problem Statement
In a large codebase, similar utilities, libraries, and business logic often get re‑implemented because developers don’t know an equivalent solution already exists. This leads to duplicated engineering effort, inconsistent implementations of the same concept, and more code to maintain and support.

Potential Solution
Introduce CodeAtlas, an enterprise code discovery agent that indexes internal repositories and understands code logic across languages. Developers can describe what they need in plain language or sample code, and CodeAtlas surfaces existing implementations, reusable libraries, shared patterns, and related design docs anywhere in the firm.

Expected Outcomes / Benefits

Reduced duplication of utilities and core business logic

Faster development by reusing proven internal components

More consistent implementations of cross‑cutting concerns (logging, security, calculations, etc.)

Better visibility into “what already exists” for architects and tech leads

Type of Use Case
AI (including Gen & Agentic AI), Technology Enablement (SDLC, DevOps, SRE)

4) LivingDocs – Self‑Maintaining System Documentation
Use Case Title
LivingDocs – Self‑Maintaining System Documentation

Problem Statement
System documentation quickly becomes stale because it relies on manual updates. Engineers often depend on tribal knowledge and reverse‑engineering to understand architecture, dependencies, and operational procedures, which slows onboarding and incident response and increases operational risk.

Potential Solution
Introduce LivingDocs, a platform that continuously analyzes code repositories, pipelines, infrastructure definitions, and logs to automatically generate and refresh system documentation. It keeps architecture diagrams, dependency maps, API descriptions, and key runbooks current as systems evolve, without relying on manual editing.

Expected Outcomes / Benefits

Always‑up‑to‑date technical documentation for services and jobs

Faster onboarding and handover between teams and regions

Quicker and more accurate troubleshooting during incidents and change windows

Reduced reliance on a few experts for “how this really works” knowledge

Type of Use Case
Technology Enablement (SDLC, DevOps, SRE), Process Optimization

5) OneClick Compliance – Automated Project Compliance Setup
Use Case Title
OneClick Compliance – Automated Project Compliance Setup

Problem Statement
Every project must adhere to firm‑wide standards for CI/CD, security checks, monitoring, scheduling, and release processes. Today, teams configure these controls manually, which takes time, introduces variation between implementations, and often triggers lengthy review cycles when standards are not fully met.

Potential Solution
Introduce OneClick Compliance, a system that, when a project or repository is registered, automatically provisions required enterprise controls. It generates standard CI/CD pipelines, security and quality gates, monitoring and alerting, scheduler jobs, and basic compliance documentation based on the project type and environment.

Expected Outcomes / Benefits

Much faster and more consistent setup of new projects and services

Higher and more uniform adherence to enterprise engineering standards

Reduced manual configuration and fewer back‑and‑forth review cycles

Stronger operational reliability and cleaner compliance evidence for audits

Type of Use Case
Technology Enablement (SDLC, DevOps, SRE), Automation, Infrastructure, Hygiene and RTB