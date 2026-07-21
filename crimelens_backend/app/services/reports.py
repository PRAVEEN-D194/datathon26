from datetime import datetime

def build_pdf_report_html() -> str:
    """
    Builds printable analytical report HTML.
    """
    return f"""
    <html>
    <head>
        <title>CrimeLens AI Executive Report</title>
        <style>
            body {{ font-family: 'Helvetica', Arial, sans-serif; margin: 40px; color: #333; }}
            .header {{ text-align: center; border-bottom: 2px solid #22d3ee; padding-bottom: 10px; }}
            .header h1 {{ margin: 0; color: #0891b2; }}
            .summary {{ margin-top: 30px; font-size: 14px; line-height: 1.6; }}
            .footer {{ text-align: center; margin-top: 50px; font-size: 11px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>CRIMELENS DECISION INTELLIGENCE REPORT</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | KSP Database</p>
        </div>
        <div class="summary">
            <h2>Executive Analytics Summary</h2>
            <p>This document contains automated intelligence insights derived from KSP crime database records. Predictive time-series models indicate stabilized trends, with isolated hotspot alerts mapped around central coordinates.</p>
        </div>
        <div class="footer">
            Classification: Confidential - Law Enforcement Officers Only
        </div>
        <script>
            window.onload = function() {{ window.print(); }}
        </script>
    </body>
    </html>
    """
