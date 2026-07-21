import random

def generate_recommendations(district: str, crime_type: str, severity: str = "Medium") -> list:
    """
    Generates intelligent, actionable policing recommendation logs based on crime analytics.
    """
    recommendations = []
    
    # 1. Base recommendations by Crime Type
    if crime_type == "Cyber Crime":
        recommendations.extend([
            {
                "title": "Establish Cyber Fraud Awareness Campaigns",
                "desc": f"Conduct digital literacy and security workshops in schools/colleges in {district}.",
                "priority": "High" if severity == "High Surge Alert" else "Medium"
            },
            {
                "title": "Establish ISP/Bank Coordination Desk",
                "desc": "Partner with nodal bank contacts to shorten transaction freeze turnaround time below 1 hour.",
                "priority": "Critical" if severity == "High Surge Alert" else "High"
            },
            {
                "title": "Enhance Digital Evidence Training",
                "desc": f"Conduct advanced forensic and IP logging analysis courses for investigating officers in {district}.",
                "priority": "Medium"
            }
        ])
    elif crime_type == "Narcotics":
        recommendations.extend([
            {
                "title": "Intensify Entry-Point Checkpoints",
                "desc": f"Deploy drug sniffer squads at district highway borders and courier terminals in {district}.",
                "priority": "Critical"
            },
            {
                "title": "Establish Campus Surveillance Programs",
                "desc": "Coordinate plainclothes patrols and local intelligence gatherers near educational institutions.",
                "priority": "High"
            }
        ])
    elif crime_type == "Theft":
        recommendations.extend([
            {
                "title": "Deploy Random Night Patrol Vectors",
                "desc": f"Increase visibility of patrol beats between 11 PM and 5 AM in residential sectors of {district}.",
                "priority": "High" if severity == "High Surge Alert" else "Medium"
            },
            {
                "title": "CCTV Infrastructure Audit",
                "desc": "Inspect public cameras around transport junctions and commercial hubs; replace dead feeds.",
                "priority": "Medium"
            }
        ])
    elif crime_type == "Crimes Against Women":
        recommendations.extend([
            {
                "title": "Deploy 'Pink Patrol' Units",
                "desc": f"Establish specialized response vehicles at transit depots, parks, and colleges in {district}.",
                "priority": "High"
            },
            {
                "title": "Install Dedicated Helpline Outposts",
                "desc": "Setup localized safety reporting terminals linked directly to KSP Command Center.",
                "priority": "Medium"
            }
        ])
    else:  # General / Assault
        recommendations.extend([
            {
                "title": "Community Policing & Peace Committee Meetings",
                "desc": f"Engage community leaders in {district} to resolve local disputes proactively.",
                "priority": "Medium"
            },
            {
                "title": "Map Alcohol/Licensing Violations",
                "desc": "Monitor bar operating hours and patrol areas with histories of public nuisance complaints.",
                "priority": "High"
            }
        ])

    return recommendations
