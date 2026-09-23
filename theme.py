# theme.py
# need to change color of spinner (not working)
"""
Injects custom CSS into Streamlit app
"""

import streamlit as st

DISPLAY_FONT = "'Fraunces', serif"
BODY_FONT = "'Source Serif 4', serif"

COLORS = {"bg": "#14171c",
          "panel": "#1b1f26",
          "panel_raised": "#20242c",
          "rule": "#383e48",
          "text": "#e7e1d2",
          "text_muted": "#97917f",
          "accent": "#c1502e",
          "accent_soft": "#c1502e33",
          "fate": "#6f9089",
          "fate_soft": "#6f908933"}

STAT_LABELS = {"health": "Health",
               "renown": "Renown",
               "morale": "Morale",
               "warband_loyalty": "Warband Loyalty",
               "favor_of_fate": "Favor of Fate"}


def render_stat_bar(state) -> str:
    """Creates the game stats bar"""
    cells = []
    for stat_key, label in STAT_LABELS.items():
        value = getattr(state, stat_key)
        value_text = f"{value:+d}" if stat_key == "favor_of_fate" else str(value)
        css_class = "rag-stat fate" if stat_key == "favor_of_fate" else "rag-stat"
        cells.append(
            f'<div class="{css_class}">'
            f'<div class="rag-label">{label}</div>'
            f'<div class="rag-value">{value_text}</div>'
            f"</div>"
        )
    return f'<div class="rag-statbar">{"".join(cells)}</div>'


def apply_theme() -> None:
    """Injects custom theme"""
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">

        <style>

        :root {{
            --bg: {COLORS["bg"]};
            --panel: {COLORS["panel"]};
            --panel-raised: {COLORS["panel_raised"]};
            --rule: {COLORS["rule"]};
            --text: {COLORS["text"]};
            --text-muted: {COLORS["text_muted"]};
            --accent: {COLORS["accent"]};
            --accent-soft: {COLORS["accent_soft"]};
            --fate: {COLORS["fate"]};
            --fate-soft: {COLORS["fate_soft"]};
        }}

        
        /* ---------- App shell ---------- */

        /* App width */
        .block-container,
        [data-testid="stAppViewContainer"] .main .block-container {{
            max-width: 900px;
        }}

        /* Background */
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        .main {{
            background-color: var(--bg);
            color: var(--text);
        }}

        # /* Spinner */
        # [data-testid="stSpinnerIcon"] {{
        # color: red !important;
        # }}
        
        
        /* ------- Main Typography -------- */

        /* Header font family and color */
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4,
        [data-testid="stMarkdownContainer"] h5,
        [data-testid="stAppViewContainer"] h1 *,
        [data-testid="stAppViewContainer"] h2 *,
        [data-testid="stAppViewContainer"] h3 *,
        [data-testid="stAppViewContainer"] h4 *, 
        [data-testid="stAppViewContainer"] h5 * {{
            font-family: {DISPLAY_FONT} !important;
            font-weight: 500 !important;
            color: var(--text) !important;
            letter-spacing: 0.01em;
        }}

        /* Header alignment */
        h1, h2, h4 {{
            text-align: center !important;
        }}

        h2 {{
            font-size: 30px !important;
        }}
        
        h4 {{
            font-size: 16px !important;
        }}

        /* Caption (st.caption) */
        [data-testid="stCaptionContainer"] {{
            font-family: {DISPLAY_FONT} !important;
            text-align: center !important;
            color: var(--text) !important;
        }}

        /* Remaining text (st.markdown/st.write) */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            font-family: {BODY_FONT} !important;
            color: var(--text);
            font-size: 17px;
            line-height: 1.7;
        }}

        
        /* ---------- Sidebar ---------- */
        /* Sidebar expand/collapse icon */
        [data-testid="stIconMaterial"] {{
            color: var(--accent) !important;
        }}

        /* Sidebar background and border */
        [data-testid="stSidebar"] {{
            background-color: var(--panel);
            border-right: 1px solid var(--rule);
        }}

        /* Stats Glossary size */
        [data-testid="stSidebar"] h3 {{
            font-size: 18px !important;
        }}

        /* Sidebar text*/
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p *,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li * {{
            font-size: 13px !important;
            color: var(--text-muted) !important;
        }}
        
        /* Stats */
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong {{
            color: var(--text) !important;
        }}

        /* Sidebar horizontal line */
        hr {{
            border-top: 1px solid var(--rule) !important;
        }}

        
        /* ---------- Buttons (choices, actions) ---------- */

        /* Button background */
        div.stButton > button {{
            font-family: {BODY_FONT};
            background-color: var(--panel-raised);
            color: var(--text);
            border: 1px solid var(--rule);
            border-radius: 3px;
            padding: 12px 18px;
            text-align: left !important;
            transition: border-color .15s ease, background-color .15s ease;
        }}

        /* Button hover */
        div.stButton > button:hover:not(:disabled) {{
            border-color: var(--accent);
            background-color: var(--accent-soft);
            color: var(--text);
        }}

        /* Button disabled */
        div.stButton > button:disabled {{
            opacity: 0.55;
        }}

        /* Button type primary are center aligned */
        [data-testid="stBaseButton-primary"] > div {{
            justify-content: center !important;
        }}

        /* Button type secondary are left aligned */
        [data-testid="stBaseButton-secondary"] > div {{
            justify-content: flex-start !important;
        }}

        /* Primary button background */
        [data-testid="stBaseButton-primary"] {{
            background-color: var(--accent) !important;
            border: none !important;
            text-align: center !important;
            padding: 10px 28px !important;
            width: auto !important;
            display: block !important;
            margin: 0 auto !important;
        }}

        /* Primary button font and color */
        [data-testid="stBaseButton-primary"] p,
        [data-testid="stBaseButton-primary"] span {{
            font-family: {DISPLAY_FONT} !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            color: var(--text) !important;
        }}

        /* Primary button hover */
        [data-testid="stBaseButton-primary"]:hover {{
            filter: brightness(1.25);
        }}

        /* Sidebar primary button alignment*/
        [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {{
            width: auto !important;
            margin: 0 !important;
        }}

        /* Sidebar primary button font color*/
        [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p {{
            color: var(--text) !important;
        }}


        /* ---------- Stats header (custom HTML, not st.metric) ---------- */
        .rag-statbar {{
            display: flex;
            justify-content: space-between;
            gap: 6px;
            padding: 14px 10px;
            background-color: var(--panel);
            border-top: 1px solid var(--rule);
            border-bottom: 1px solid var(--rule);
            margin-bottom: 24px;
        }}
        .rag-stat {{
            flex: 1;
            text-align: center;
        }}
        .rag-stat .rag-label {{
            font-family: {BODY_FONT};
            font-size: 10.5px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }}
        .rag-stat .rag-value {{
            font-family: {DISPLAY_FONT};
            font-weight: 500;
            font-size: 17px;
            color: var(--text);
        }}

        </style>
        """,
        unsafe_allow_html = True,
    )