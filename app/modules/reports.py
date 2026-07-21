import sqlite3
import pandas as pd
from datetime import datetime
from app.modules.insights import generate_analytical_insights
from app.modules.predictive import calculate_district_risk_scores

DB_PATH = "D:/Datathon - Cyber Nexus/crime_records.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def generate_html_report() -> str:
    """
    Generates a beautifully formatted, printable HTML report summarizing state crime analytics.
    """
    insights = generate_analytical_insights()
    risk_scores = calculate_district_risk_scores()
    
    # Render categories table
    cats_html = ""
    for cat in insights["categories"]:
        cats_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{cat['crime_head']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">{cat['count']}</td>
        </tr>
        """
        
    # Render district risks table
    risks_html = ""
    for score in risk_scores:
        badge_color = "red" if score["risk_level"] == "Critical" else "orange" if score["risk_level"] == "High" else "yellow"
        risks_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{score['district']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">{score['risk_score']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: center;">
                <span style="background-color: {badge_color}; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">
                    {score['risk_level']}
                </span>
            </td>
        </tr>
        """

    # Complete print-ready page
    report_template = f"""
    <html>
    <head>
        <title>CyberNexus Crime Intelligence Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; margin: 40px; }}
            .header {{ text-align: center; border-bottom: 3px solid #22d3ee; padding-bottom: 20px; margin-bottom: 30px; }}
            .header h1 {{ margin: 0; color: #0891b2; font-size: 26px; }}
            .header p {{ margin: 5px 0 0 0; color: #666; font-size: 14px; }}
            .grid {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
            .card {{ flex: 1; background: #f9f9f9; border: 1px solid #eee; padding: 15px; border-radius: 8px; text-align: center; margin: 0 10px; }}
            .card h3 {{ margin: 0; font-size: 12px; color: #666; text-transform: uppercase; }}
            .card p {{ margin: 10px 0 0 0; font-size: 24px; font-weight: bold; color: #0891b2; }}
            .section {{ margin-bottom: 30px; }}
            .section h2 {{ font-size: 18px; border-bottom: 1px solid #eee; padding-bottom: 8px; color: #333; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #f2f2f2; text-align: left; padding: 10px; font-size: 13px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>CYBERNEXUS CRIME INTELLIGENCE REPORT</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Karnataka State Police SCRB Database</p>
        </div>
        
        <div class="grid">
            <div class="card" style="margin-left: 0;">
                <h3>Total Crimes</h3>
                <p>{insights['stats']['total_crimes']}</p>
            </div>
            <div class="card">
                <h3>Solved Rate</h3>
                <p>{insights['stats']['solved_percentage']}%</p>
            </div>
            <div class="card">
                <h3>Under Investigation</h3>
                <p>{insights['stats']['pending_count']}</p>
            </div>
            <div class="card" style="margin-right: 0;">
                <h3>Surge Alerts</h3>
                <p>{len(insights['anomalies'])}</p>
            </div>
        </div>

        <div class="section">
            <h2>Executive Analytics Summary</h2>
            <p style="line-height: 1.6; font-size: 14px;">{insights['explanation']}</p>
        </div>

        <div style="display: flex; gap: 20px;">
            <div class="section" style="flex: 1;">
                <h2>Crime Categories Breakdown</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Category</th>
                            <th style="text-align: right;">Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cats_html}
                    </tbody>
                </table>
            </div>
            
            <div class="section" style="flex: 1;">
                <h2>District Risk Rankings</h2>
                <table>
                    <thead>
                        <tr>
                            <th>District</th>
                            <th style="text-align: right;">Risk Rating</th>
                            <th style="text-align: center;">Severity Level</th>
                        </tr>
                    </thead>
                    <tbody>
                        {risks_html}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="section" style="margin-top: 50px; border-top: 1px solid #ddd; padding-top: 20px; font-size: 11px; text-align: center; color: #777;">
            Report compiled by CyberNexus Decision Intelligence System. Classification: Official Law Enforcement Use Only.
        </div>
        <script>
            // Auto trigger browser print dialog
            window.onload = function() {{ window.print(); }}
        </script>
    </body>
    </html>
    """
    return report_template
