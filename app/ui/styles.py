import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
          :root {
            --assist-bg: #080d12;
            --assist-panel: #111820;
            --assist-panel-2: #17212b;
            --assist-text: #f8fafc;
            --assist-muted: #b7c0cb;
            --assist-green: #55e6a5;
            --assist-gold: #f5c866;
            --assist-line: rgba(255,255,255,0.13);
          }

          .stApp {
            background: var(--assist-bg);
            color: var(--assist-text);
          }

          header[data-testid="stHeader"],
          [data-testid="stToolbar"],
          [data-testid="stDecoration"],
          footer {
            visibility: hidden;
            height: 0;
          }

          .block-container {
            max-width: 450px;
            padding: 20px 14px 28px;
            background: linear-gradient(180deg, #111a23 0%, #0c1218 100%);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 24px;
            box-shadow: 0 24px 64px rgba(0,0,0,0.34);
            min-height: 92vh;
          }

          h1, h2, h3, p, label, span, div {
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          }

          h1 {
            font-size: 2.15rem;
            line-height: 1.08;
            letter-spacing: 0;
            margin: 0 0 12px;
          }

          h2 {
            font-size: 1.22rem;
            margin-top: 0;
          }

          .app-logo {
            width: 44px;
            height: 44px;
            border-radius: 8px;
            display: grid;
            place-items: center;
            color: #061019;
            background: var(--assist-green);
            font-weight: 900;
          }

          .assist-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 16px 8px;
          }

          .assist-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            min-height: 34px;
            padding: 7px 11px;
            border-radius: 999px;
            color: var(--assist-green);
            background: rgba(85, 230, 165, 0.1);
            border: 1px solid rgba(85, 230, 165, 0.24);
            font-size: 0.84rem;
            font-weight: 700;
          }

          .assist-section {
            padding: 18px 16px;
            border-top: 1px solid var(--assist-line);
          }

          .hero {
            padding: 34px 18px 28px;
          }

          .hero h1 {
            margin-top: 0;
          }

          .hero-copy {
            color: var(--assist-muted);
            font-size: 1.02rem;
            line-height: 1.52;
            margin-bottom: 22px;
            max-width: 34rem;
          }

          .quiet-card,
          .status-card {
            border: 1px solid var(--assist-line);
            border-radius: 8px;
            padding: 16px;
            background: var(--assist-panel);
          }

          .quiet-card p {
            color: var(--assist-muted);
            line-height: 1.5;
            margin: 0;
          }

          .section-heading h2 {
            margin-bottom: 5px;
          }

          .section-heading p {
            color: var(--assist-muted);
            line-height: 1.45;
            margin: 0;
          }

          .signal-strip {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 24px;
          }

          .signal {
            min-height: 66px;
            border-radius: 8px;
            padding: 12px;
            background: #131d27;
            border: 1px solid var(--assist-line);
            color: var(--assist-muted);
            font-size: 0.82rem;
            font-weight: 750;
          }

          .signal strong {
            display: block;
            color: var(--assist-text);
            font-size: 0.94rem;
            margin-bottom: 2px;
          }

          .result-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
            margin: 14px 0 12px;
          }

          .metric {
            min-height: 82px;
            border-radius: 8px;
            padding: 14px 15px;
            background: #131d27;
            border: 1px solid var(--assist-line);
          }

          .metric-value {
            font-size: 1.72rem;
            line-height: 1;
            font-weight: 850;
            color: var(--assist-text);
            margin-top: 10px;
          }

          .metric-note {
            font-size: 1.35rem;
            line-height: 1.15;
          }

          .metric-label {
            color: var(--assist-muted);
            font-size: 0.86rem;
            font-weight: 700;
          }

          .mini-list {
            border: 1px solid var(--assist-line);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 10px;
          }

          .mini-row {
            display: flex;
            justify-content: space-between;
            gap: 14px;
            padding: 12px 14px;
            border-bottom: 1px solid var(--assist-line);
            background: rgba(255,255,255,0.035);
          }

          .mini-row:last-child {
            border-bottom: 0;
          }

          .mini-row strong {
            color: var(--assist-green);
            font-weight: 800;
          }

          .retry {
            border: 1px solid rgba(245, 200, 102, 0.32);
            background: rgba(245, 200, 102, 0.1);
            padding: 15px 16px;
            border-radius: 8px;
            color: #fff5d8;
            font-weight: 700;
            line-height: 1.45;
          }

          div[data-testid="stButton"] > button {
            width: 100%;
            min-height: 60px;
            border-radius: 12px;
            border: 0;
            color: #061019;
            background: var(--assist-green);
            font-size: 1.03rem;
            font-weight: 850;
            box-shadow: 0 12px 28px rgba(85, 230, 165, 0.16);
            margin-top: 8px;
          }

          div[data-testid="stButton"] > button:hover {
            color: #061019;
            border: 0;
            transform: translateY(-1px);
          }

          [data-testid="stFileUploader"] {
            border: 1px dashed rgba(247,251,255,0.32);
            border-radius: 8px;
            padding: 12px;
            background: rgba(255,255,255,0.045);
          }

          [data-testid="stFileUploader"] section {
            background: transparent;
            border: 0;
          }

          [data-testid="stSidebar"] {
            background: #0a131d;
          }

          [data-testid="stCameraInput"] {
            border: 1px solid var(--assist-line);
            border-radius: 8px;
            padding: 10px;
            background: #0f1821;
          }

          [data-testid="stCameraInput"] video,
          [data-testid="stCameraInput"] img {
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.08);
          }

          .backup-section {
            border-top: 0;
            padding-top: 8px;
          }

          .streamlit-expanderHeader {
            color: var(--assist-text);
            font-weight: 750;
          }

          img {
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.09);
          }

          @media (min-width: 720px) {
            .block-container {
              padding-top: 22px;
            }

            .result-grid {
              grid-template-columns: 1fr 1fr;
            }

            .result-grid .metric:first-child {
              grid-column: span 2;
            }
          }

          @media (max-width: 380px) {
            .signal-strip {
              grid-template-columns: 1fr;
            }

            h1 {
              font-size: 1.95rem;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
