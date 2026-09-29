from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

DARK_NAVY = RGBColor(15, 23, 42)
ACCENT_BLUE = RGBColor(14, 116, 144)
TEXT_DARK = RGBColor(30, 41, 59)

slides = [
    {
        "title": "Global Weather & Disaster Intelligence System",
        "sub": "Real-Time Telemetry, 11-Year Empirical Analysis (2015–2026) & Lunar Syzygy Forecasting",
        "bullets": [
            "Domain: Python Web Frameworks, Environmental Data Pipelines & Astrometric Modeling",
            "Core Objective: Predictive binary rain advisories & pattern-based disaster window forecasting",
            "Data Coverage: 2015 to 2026 global flood deluges & industrial chemical fire incidents",
            "Presented By: College Project Evaluation"
        ]
    },
    {
        "title": "Problem Statement & Critical Need",
        "sub": "Why standalone atmospheric dashboards fail during compound catastrophes",
        "bullets": [
            "Binary Advisory Void: Most tools provide raw numeric telemetry without deterministic 'Rain: YES/NO' advisories.",
            "Gravitational Syzygy Ignored: Conventional flood alerts overlook ocean Spring Tides caused by Full and New Moons.",
            "Estuary Backwater Blockage: Sea levels surge up to 2.5m during Syzygy, trapping swollen rivers and submerging urban centers.",
            "Industrial Fire Seasonality: High summer heatwaves drastically increase chemical solvent vapor explosions in factory zones."
        ]
    },
    {
        "title": "System Architecture & Core Modules",
        "sub": "Decoupled 3-layer execution pipeline",
        "bullets": [
            "Layer 1 - Live Telemetry & Rain Engine: Fetches OpenWeatherMap API metrics; parses 3-hour PoP values (>0.20 threshold).",
            "Layer 2 - Empirical Knowledge Base: 11-year dataset (2015–2026) mapping exact start/end dates, duration, and lunar alignments.",
            "Layer 3 - Autonomous Predictive Engine: Scans upcoming 365 calendar days to identify risk windows without manual date picking.",
            "Export Pipeline: Built-in CSV generation for empirical faculty review and audit compliance."
        ]
    },
    {
        "title": "Scientific Basis: Lunar Phases vs Flood Hazards",
        "sub": "Understanding the gravitational mechanics of coastal inundation",
        "bullets": [
            "Full Moon & New Moon (Syzygy / Spring Tides):",
            "  • Sun, Earth, and Moon align linearly, exerting maximum gravitational attraction.",
            "  • High astronomical ocean tides physically block river estuaries (e.g., Chennai 2015, Kerala 2018, Vardah 2016).",
            "Half Moon (Quadrature / Neap Tides):",
            "  • Gravitational vectors offset at 90-degree right angles, minimizing tidal ranges.",
            "  • Storm runoff discharges rapidly into oceans with low backwater risk."
        ]
    },
    {
        "title": "11-Year Empirical Dataset (2015–2026)",
        "sub": "Natural deluges and industrial factory fire coverage",
        "bullets": [
            "Natural Deluges: Chennai Floods (2015, 2023), Kerala Inundations (2018, 2019, 2024, 2026), Assam Basin (2022, 2026).",
            "Global Events: Noto Japan Tsunami (2024), Dubai Flash Deluges (2024), California Wildfires (2025), Turkey Quake (2023).",
            "Industrial Fire Incidents: SIDCO Kakkalur (2024), Gummidipoondi Boiler Explosion (2024), Red Hills Warehouse (2026), Manali Pipeline (2026).",
            "Root Causes: Summer thermal expansions (March–June) accelerate industrial chemical detonations."
        ]
    },
    {
        "title": "Autonomous Pattern-Driven Forecasting",
        "sub": "Machine intelligence replacing manual date inputs",
        "bullets": [
            "No Manual Date Picker: User enters only the location (e.g., Chennai, Kerala, Salem).",
            "Historical Pattern Matching: Identifies regional vulnerability windows (Northeast Monsoon, Southwest Monsoon, Summer Fire).",
            "Chronological Scanning: Scans forward horizons and pinpoints the next Full/New Moon Syzygy alignment automatically.",
            "Output Delivery: Delivers exact Start-to-End Date spans, active durations, and physical trigger mechanics."
        ]
    },
    {
        "title": "Faculty Verification & Deliverables",
        "sub": "Transparent, auditable engineering prototype",
        "bullets": [
            "Live Working Prototype: Streamlit tabbed UI featuring instant metric cards and expandable incident details.",
            "Auditable CSV Database: One-click export of verified historical records covering 2015–2026.",
            "Clean Layout: Zero text truncation (...) utilizing custom CSS responsive cards.",
            "Future Roadmap: Cloud deployment on Streamlit Community Cloud and supervised ML model training."
        ]
    }
]

blank_layout = prs.slide_layouts[6]

for slide_data in slides:
    slide = prs.slides.add_slide(blank_layout)
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.3))
    tf_header = header_box.text_frame
    tf_header.word_wrap = True
    
    p_title = tf_header.paragraphs[0]
    p_title.text = slide_data["title"]
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = DARK_NAVY
    
    p_sub = tf_header.add_paragraph()
    p_sub.text = slide_data["sub"]
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = ACCENT_BLUE
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.7), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    for idx, bullet in enumerate(slide_data["bullets"]):
        p_body = tf_body.paragraphs[0] if idx == 0 else tf_body.add_paragraph()
        p_body.text = bullet
        p_body.font.size = Pt(16)
        p_body.font.color.rgb = TEXT_DARK
        p_body.space_after = Pt(10)

output_ppt = "Global_Weather_and_Disaster_Project_Presentation.pptx"
prs.save(output_ppt)
print(f"Presentation PPTX successfully generated: {output_ppt}")