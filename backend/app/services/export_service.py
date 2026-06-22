from textwrap import wrap

from app.models.entities import Decision


def build_decision_pdf(decision: Decision) -> bytes:
    lines = [
        "FutureYou Decision Simulation",
        f"Title: {decision.title}",
        f"Goal: {decision.goal}",
        f"Location: {decision.country_location}",
        f"Risk tolerance: {decision.risk_tolerance}",
        "",
        "Scenarios",
    ]
    for scenario in decision.scenarios:
        lines.extend(
            [
                f"{scenario.option.label} - {scenario.scenario_type}: {scenario.title}",
                f"Probability: {scenario.probability:.0%}",
                scenario.narrative,
                "Next actions: " + "; ".join(scenario.action_path[:3]),
                "",
            ]
        )
    return _simple_pdf(lines)


def _simple_pdf(lines: list[str]) -> bytes:
    y = 780
    commands = ["BT", "/F1 11 Tf", "50 800 Td", "14 TL"]
    for raw_line in lines:
        for line in wrap(raw_line, width=86) or [""]:
            if y < 60:
                break
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands.append(f"({escaped}) Tj")
            commands.append("T*")
            y -= 14
    commands.append("ET")
    stream = "\n".join(commands).encode("latin-1", errors="replace")
    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj",
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
        b"5 0 obj << /Length "
        + str(len(stream)).encode()
        + b" >> stream\n"
        + stream
        + b"\nendstream endobj",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj + b"\n")
    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(
        f"trailer << /Root 1 0 R /Size {len(objects) + 1} >>\n"
        f"startxref\n{xref_offset}\n%%EOF".encode()
    )
    return bytes(pdf)
