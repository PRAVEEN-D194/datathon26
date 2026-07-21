import sqlite3
import pandas as pd
import numpy as np

DB_PATH = "D:/Datathon - Cyber Nexus/crime_records.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def generate_analytical_insights():
    """
    Computes high-level crime dashboard indicators:
    - Total Crimes, Solved Ratio, Pending Investigation
    - Trends and Anomaly Surges
    - Station Performance rankings
    """
    conn = get_db_connection()
    
    # 1. Base Stats
    query_stats = """
        SELECT 
            count(*) as total_crimes,
            sum(case when status = 'Solved' then 1 else 0 end) as solved_count,
            sum(case when status = 'Under Investigation' then 1 else 0 end) as pending_count,
            sum(case when status = 'Chargesheeted' then 1 else 0 end) as chargesheet_count
        FROM crime_incidents
    """
    stats_df = pd.read_sql_query(query_stats, conn)
    base_stats = stats_df.iloc[0].to_dict()
    solved_ratio = round((base_stats['solved_count'] / base_stats['total_crimes']) * 100, 2) if base_stats['total_crimes'] > 0 else 0
    base_stats['solved_percentage'] = solved_ratio

    # 2. Crime Categories Distribution
    query_cats = """
        SELECT crime_head, count(*) as count
        FROM crime_incidents
        GROUP BY crime_head
        ORDER BY count DESC
    """
    cats_df = pd.read_sql_query(query_cats, conn)
    categories = cats_df.to_dict(orient="records")

    # 3. Monthly Trend Growth
    query_trends = """
        SELECT strftime('%Y-%m', date_occurrence) as month, count(*) as count
        FROM crime_incidents
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    """
    trends_df = pd.read_sql_query(query_trends, conn)
    # Reverse to chronological order
    trends_df = trends_df.iloc[::-1]
    
    # Calculate MoM growth rate
    trends = trends_df.to_dict(orient="records")
    mom_growth = 0.0
    if len(trends) > 1:
        prev = trends[-2]["count"]
        curr = trends[-1]["count"]
        mom_growth = round(((curr - prev) / prev) * 100, 2) if prev > 0 else 0.0

    # 4. Anomaly Detection (Surges)
    # Detect if any district-crime_head combination in the last 30 days is higher 
    # than mean + 2*std of past 12 months.
    query_anomaly = """
        SELECT district, crime_head, count(*) as count, strftime('%Y-%m', date_occurrence) as month
        FROM crime_incidents
        GROUP BY district, crime_head, month
    """
    all_data = pd.read_sql_query(query_anomaly, conn)
    conn.close()

    anomalies = []
    if not all_data.empty:
        # Group to find average monthly cases for each district + crime type combination
        stats = all_data.groupby(['district', 'crime_head'])['count'].agg(['mean', 'std']).reset_index()
        stats['std'] = stats['std'].fillna(0.0)
        
        # Get latest month counts
        latest_month = all_data['month'].max()
        latest_data = all_data[all_data['month'] == latest_month]
        
        merged = pd.merge(latest_data, stats, on=['district', 'crime_head'])
        # Anomaly condition: count > mean + 1.8 * std AND count > 5 (to avoid small count anomalies)
        merged['is_anomaly'] = merged['count'] > (merged['mean'] + 1.8 * merged['std'])
        merged_anom = merged[(merged['is_anomaly'] == True) & (merged['count'] > 5)]
        
        for _, row in merged_anom.iterrows():
            anomalies.append({
                "district": row["district"],
                "crime_type": row["crime_head"],
                "current_count": int(row["count"]),
                "historical_mean": round(row["mean"], 2),
                "severity": "High Surge Alert"
            })

    # Summary Text
    anomaly_text = f"Detected {len(anomalies)} sudden crime surges in the state." if anomalies else "No major crime volume anomalies detected."
    explanation = f"State crime records report a solved rate of {solved_ratio}%. MoM count changed by {mom_growth}%. {anomaly_text}"

    return {
        "stats": base_stats,
        "categories": categories,
        "trends": trends,
        "mom_growth": mom_growth,
        "anomalies": anomalies,
        "explanation": explanation
    }

if __name__ == "__main__":
    print("Testing Analytical Insights...")
    insights = generate_analytical_insights()
    print("Explanation:", insights["explanation"])
    print("Top Categories:", insights["categories"][:3])
    print("Anomalies:", insights["anomalies"])
