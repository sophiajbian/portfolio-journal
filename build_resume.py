"""
Generate resume-engineering.pdf for Sophia Bian.
Run: python3 build_resume.py
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Colours ──────────────────────────────────────────────────────────────────
INK       = colors.HexColor('#1a1a10')
INK_MID   = colors.HexColor('#4a4a38')
INK_MUTED = colors.HexColor('#7a7860')
INK_FAINT = colors.HexColor('#b0aa90')
RULE      = colors.HexColor('#2a2a1e')
RULE_THIN = colors.HexColor('#d0c8b0')

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    name_style = ParagraphStyle('Name',
        fontName='Helvetica-Bold', fontSize=20,
        textColor=INK, leading=24, alignment=TA_CENTER, spaceAfter=2)

    contact_style = ParagraphStyle('Contact',
        fontName='Helvetica', fontSize=8,
        textColor=INK_MUTED, leading=12, alignment=TA_CENTER, spaceAfter=2)

    section_style = ParagraphStyle('Section',
        fontName='Helvetica-Bold', fontSize=8,
        textColor=INK, leading=10, spaceBefore=10, spaceAfter=2,
        letterSpacing=1.2, alignment=TA_LEFT)

    org_style = ParagraphStyle('Org',
        fontName='Helvetica-Bold', fontSize=9.5,
        textColor=INK, leading=13, spaceBefore=6, spaceAfter=0)

    title_style = ParagraphStyle('Title',
        fontName='Helvetica-Oblique', fontSize=8.8,
        textColor=INK_MID, leading=12, spaceAfter=0)

    bullet_style = ParagraphStyle('Bullet',
        fontName='Helvetica', fontSize=8.5,
        textColor=INK_MID, leading=12.5,
        leftIndent=12, firstLineIndent=-8,
        spaceAfter=1.5)

    normal_style = ParagraphStyle('Normal',
        fontName='Helvetica', fontSize=8.5,
        textColor=INK_MID, leading=12.5, spaceAfter=2)

    skills_label_style = ParagraphStyle('SkillsLabel',
        fontName='Helvetica-Bold', fontSize=8.5,
        textColor=INK, leading=12.5, spaceAfter=0)

    return {
        'name': name_style,
        'contact': contact_style,
        'section': section_style,
        'org': org_style,
        'title': title_style,
        'bullet': bullet_style,
        'normal': normal_style,
        'skills_label': skills_label_style,
    }

def rule(thick=False):
    return HRFlowable(
        width='100%',
        thickness=1.5 if thick else 0.5,
        color=RULE if thick else RULE_THIN,
        spaceAfter=3, spaceBefore=3
    )

def section_header(text, s):
    return [
        Spacer(1, 4),
        rule(thick=True),
        Paragraph(text.upper(), s['section']),
    ]

def entry_header(org, right_text, title, right_sub, s):
    """Two-column header: org + date on one line, title + location below."""
    # Row 1: bold org name | date
    row1 = Table(
        [[Paragraph(org, s['org']), Paragraph(right_text, ParagraphStyle(
            'Right', fontName='Helvetica', fontSize=8.5,
            textColor=INK_MUTED, leading=13, alignment=TA_RIGHT))]],
        colWidths=['70%', '30%'],
        hAlign='LEFT'
    )
    row1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    # Row 2: italic title | location
    row2 = Table(
        [[Paragraph(title, s['title']), Paragraph(right_sub, ParagraphStyle(
            'RightSub', fontName='Helvetica', fontSize=8,
            textColor=INK_FAINT, leading=12, alignment=TA_RIGHT))]],
        colWidths=['70%', '30%'],
        hAlign='LEFT'
    )
    row2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    return [row1, row2]

def bullet(text, s):
    return Paragraph(f'•  {text}', s['bullet'])

def skills_row(label, items, s):
    row = Table(
        [[Paragraph(label, s['skills_label']),
          Paragraph(items, s['normal'])]],
        colWidths=[1.1*inch, 5.65*inch],
        hAlign='LEFT'
    )
    row.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    return row

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    out = 'resume-engineering.pdf'
    doc = SimpleDocTemplate(
        out,
        pagesize=letter,
        leftMargin=0.65*inch, rightMargin=0.65*inch,
        topMargin=0.55*inch,  bottomMargin=0.55*inch,
    )
    s = make_styles()
    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(Paragraph('Sophia Bian', s['name']))
    story.append(Paragraph(
        'sophiabian2029@u.northwestern.edu  ·  '
        'linkedin.com/in/bian-sophia  ·  github.com/sophiajbian',
        s['contact']))
    story.append(rule(thick=True))

    # ── Education ─────────────────────────────────────────────────────────────
    story += section_header('Education', s)
    story += entry_header(
        'Northwestern University',
        'Expected June 2029',
        'B.S. Electrical Engineering, Minor in Computer Science',
        'Evanston, IL',
        s)
    story.append(bullet(
        'Engineering Dean’s Honors List (2025, 2026)', s))
    story.append(bullet(
        'Coursework: Computer Engineering Design · Intro to Computer Engineering · '
        'Object-Oriented Programming · Fundamentals of Computer Science · '
        'Linear Algebra · Multi-Variable Calculus', s))
    story.append(Spacer(1, 5))
    story += entry_header(
        'Henry M. Gunn High School',
        'June 2025',
        'High School Diploma',
        'Palo Alto, CA',
        s)

    # ── Experience ────────────────────────────────────────────────────────────
    story += section_header('Experience', s)

    story += entry_header(
        'Northwestern Formula Racing',
        'September 2025 – Present',
        'PCB & Firmware Engineer, DAQ Subteam',
        'Evanston, IL',
        s)
    story.append(bullet(
        'Contributing to a ~25,000-line C++ firmware codebase on a team of 7, '
        'building the driver-facing Dashboard Controller for a Formula SAE race car', s))
    story.append(bullet(
        'Designed V2 and V3 Dashboard Controller PCBs in Altium Designer: polygon pours '
        'for thermal management, high-current trace layout, and differential pair routing '
        'for CAN Bus signal integrity', s))
    story.append(bullet(
        'Implemented driver debugging screens and a Python script for automated screen '
        'asset generation, reducing manual firmware iteration overhead', s))
    story.append(bullet(
        'Maintained CAN Bus communication interfaces between the dashboard and vehicle '
        'subsystems across multiple firmware revisions', s))

    story.append(Spacer(1, 5))
    story += entry_header(
        'Querrey Simpson Institute for Bioelectronics — Rogers Research Group',
        'January 2026 – Present',
        'Undergraduate Research Assistant',
        'Evanston, IL',
        s)
    story.append(bullet(
        'Assisting development of a portable wireless fluorimeter for continuous '
        'fluorescence monitoring in biomedical applications', s))
    story.append(bullet(
        'Assembled flexible PCB prototypes via SMD soldering; performed functional '
        'validation of photodetector sensing, power regulation, and Bluetooth '
        'communication subsystems', s))
    story.append(bullet(
        'Supported iterative hardware debugging and prototype refinement across '
        'multiple build cycles', s))

    # ── Projects ──────────────────────────────────────────────────────────────
    story += section_header('Projects', s)

    story += entry_header(
        'Resonance — Violin Posture Monitoring Wearable',
        '2025 – 2026',
        'Northwestern Design Thinking & Communication',
        '',
        s)
    story.append(bullet(
        'Designed a wearable sensor unit using an Adafruit Feather RP2040 and '
        'LSM6DSOX + LIS3MDL 9-DoF IMU (accel/gyro/magnetometer) streaming at '
        '~100 Hz over USB-C', s))
    story.append(bullet(
        'Modeled and 3D-printed a compact shoulder-mount housing '
        '(2.25 × 1.19 × 0.25 in, 18 g) for the PCB and rechargeable battery', s))
    story.append(bullet(
        'Built a no-install browser companion app using the WebSerial API with '
        'real-time 3D pose visualization, rolling-window posture scoring, and a '
        'post-session analytics dashboard', s))

    story.append(Spacer(1, 5))
    story += entry_header(
        'SPICALIGN — Assistive Medical Device',
        '2025 – 2026',
        'Northwestern Design Thinking & Communication',
        '',
        s)
    story.append(bullet(
        'Designed a car-seat fitting aid for pediatric patients in hip spica casts, '
        'commissioned by Dr. Michelle Macy (Lurie Children’s Hospital)', s))
    story.append(bullet(
        'Integrated foot-pedal-driven linear actuator (12–18 in travel) and '
        'continuous-rotation servo arms for hands-free operation during cast fitting', s))

    story.append(Spacer(1, 5))
    story += entry_header(
        'FIRST Robotics Competition — Team #1868',
        '2022 – 2025',
        'Electrical Subteam Lead',
        'Palo Alto, CA',
        s)
    story.append(bullet(
        'Led wiring, PCB integration, and sensor systems for competition robots; '
        'FIRST World Championship qualifier ×2', s))

    # ── Skills ────────────────────────────────────────────────────────────────
    story += section_header('Skills', s)
    story.append(Spacer(1, 2))
    story.append(skills_row('Languages',  'C++, Python, MATLAB, HTML / CSS / JavaScript', s))
    story.append(skills_row('Hardware',   'Altium Designer, NI Multisim, SMD soldering, PCB layout', s))
    story.append(skills_row('Protocols',  'CAN Bus, Bluetooth, USB Serial / WebSerial, I²C, SPI', s))
    story.append(skills_row('Mechanical', 'SOLIDWORKS, Fusion 360, OnShape', s))
    story.append(skills_row('Tools',      'Git, GitHub', s))

    # ── Awards ────────────────────────────────────────────────────────────────
    story += section_header('Awards & Activities', s)
    story.append(Spacer(1, 2))
    awards = [
        'Engineering Dean’s Honors List — Northwestern University (2025, 2026)',
        'Aerospace & Aviation Sector Innovation Award — Conrad Challenge (2024)',
        'FIRST Robotics Team #1868 — Electrical Subteam Lead; World Championship qualifier ×2 (2022–2025)',
        'San Francisco Symphony Youth Orchestra — Flute & Piccolo (2023–2025); John Philip Sousa Award recipient',
    ]
    for a in awards:
        story.append(bullet(a, s))

    doc.build(story)
    print(f'Written: {out}')

if __name__ == '__main__':
    build()
