export type CrimeCategory = 'Cybercrime' | 'Robbery' | 'Homicide' | 'Narcotics' | 'Financial Fraud' | 'Vehicle Theft' | 'Public Order';
export type CrimeSeverity = 'Low' | 'Medium' | 'High' | 'Critical';
export type DistrictName = 'Bengaluru Urban' | 'Mysuru' | 'Mangaluru' | 'Hubballi-Dharwad' | 'Belagavi' | 'Kalaburagi' | 'Shivamogga';
export type UserRole = 'Inspector General' | 'Senior Analyst' | 'District Superintendent' | 'Field Investigator' | 'Super Admin';

export interface StatMetric {
  id: string;
  title: string;
  value: string | number;
  change: string;
  isPositive: boolean;
  timeframe: string;
  iconName: string;
}

export interface RecentAlert {
  id: string;
  firNumber: string;
  title: string;
  district: DistrictName;
  category: CrimeCategory;
  severity: CrimeSeverity;
  timestamp: string;
  status: 'Investigating' | 'Active Search' | 'Apprehended' | 'Closed';
  summary: string;
}

export interface CrimeTrendData {
  month: string;
  cybercrime: number;
  robbery: number;
  narcotics: number;
  fraud: number;
  homicide: number;
}

export interface DistrictCrimeStat {
  district: DistrictName;
  totalCases: number;
  highSeverity: number;
  solvedRate: number; // Percentage
  riskScore: number; // 0 - 100
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
  structuredData?: {
    summaryMetrics?: { label: string; value: string; color?: string }[];
    evidenceTable?: { key: string; detail: string }[];
    locationPreview?: { district: string; coordinates: [number, number]; riskLevel: string };
    chartData?: { name: string; value: number }[];
  };
}

export interface ChatThread {
  id: string;
  title: string;
  lastUpdated: string;
  previewText: string;
  category: string;
}

export interface CrimeIncidentMapMarker {
  id: string;
  firNumber: string;
  title: string;
  category: CrimeCategory;
  severity: CrimeSeverity;
  coordinates: [number, number]; // [lat, lng]
  district: DistrictName;
  timestamp: string;
  description: string;
  suspectsInvolved: number;
}

export interface CriminalNode {
  id: string;
  name: string;
  alias: string;
  role: string;
  riskScore: number;
  avatar: string;
  primaryDistrict: DistrictName;
  status: 'Warrant Issued' | 'Under Surveillance' | 'In Custody' | 'Absconding';
  chargesCount: number;
  gangAffiliation: string;
  connections: string[]; // Node IDs
}

export interface CriminalLink {
  source: string;
  target: string;
  relationship: 'Co-accused' | 'Financial Transfer' | 'Associate' | 'Gang Leader' | 'Communication';
  strength: number; // 1 - 5
}

export interface IntelligenceReport {
  id: string;
  reportCode: string;
  title: string;
  category: string;
  author: string;
  dateGenerated: string;
  classification: 'TOP SECRET' | 'CONFIDENTIAL' | 'RESTRICTED';
  district: DistrictName;
  fileSize: string;
  status: 'Verified' | 'Draft' | 'Archived';
  summary: string;
}

export interface UserProfile {
  id: string;
  name: string;
  badgeNumber: string;
  rank: UserRole;
  department: string;
  district: DistrictName;
  email: string;
  phone: string;
  clearanceLevel: 'LEVEL 5 - TOP SECRET' | 'LEVEL 4 - RESTRICTED';
  lastLogin: string;
  activeSessionIp: string;
}
