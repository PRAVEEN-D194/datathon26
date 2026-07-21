import {
  StatMetric,
  RecentAlert,
  CrimeTrendData,
  DistrictCrimeStat,
  ChatMessage,
  ChatThread,
  CrimeIncidentMapMarker,
  CriminalNode,
  CriminalLink,
  IntelligenceReport,
  UserProfile
} from '../types';

export const mockUserProfile: UserProfile = {
  id: 'USR-89421',
  name: 'Inspector General Rajesh V. Rao',
  badgeNumber: 'KSP-89421',
  rank: 'Inspector General',
  department: 'Cyber & Special Intelligence Wing',
  district: 'Bengaluru Urban',
  email: 'rajesh.rao@ksp.gov.in',
  phone: '+91 98450 12345',
  clearanceLevel: 'LEVEL 5 - TOP SECRET',
  lastLogin: '2026-07-21 12:45:00 IST',
  activeSessionIp: '10.204.18.92 (KSP Secure Mesh Grid)'
};

export const mockStatMetrics: StatMetric[] = [
  {
    id: 'stat-1',
    title: 'Total Active FIRs',
    value: '14,289',
    change: '+3.2%',
    isPositive: false,
    timeframe: 'vs last month',
    iconName: 'ShieldAlert'
  },
  {
    id: 'stat-2',
    title: 'AI Intelligence Queries',
    value: '98.4%',
    change: '+14.8%',
    isPositive: true,
    timeframe: 'accuracy rate',
    iconName: 'Cpu'
  },
  {
    id: 'stat-3',
    title: 'Critical Threat Suspects',
    value: '342',
    change: '-8.5%',
    isPositive: true,
    timeframe: 'under active tracking',
    iconName: 'Users'
  },
  {
    id: 'stat-4',
    title: 'Hotspot Prediction Index',
    value: '91.2',
    change: '+5.1%',
    isPositive: true,
    timeframe: 'preventative efficacy',
    iconName: 'Activity'
  }
];

export const mockRecentAlerts: RecentAlert[] = [
  {
    id: 'ALT-1092',
    firNumber: 'KA-2026-BLR-00981',
    title: 'High-Value Crypto Laundering Syndicate Detected',
    district: 'Bengaluru Urban',
    category: 'Financial Fraud',
    severity: 'Critical',
    timestamp: '10 mins ago',
    status: 'Active Search',
    summary: 'AI flagged cross-border transactions originating from Koramangala IT hub linked to shell entities.'
  },
  {
    id: 'ALT-1093',
    firNumber: 'KA-2026-MYS-00412',
    title: 'Organized Vehicle Theft Ring Identified in Devaraja',
    district: 'Mysuru',
    category: 'Vehicle Theft',
    severity: 'High',
    timestamp: '32 mins ago',
    status: 'Investigating',
    summary: 'Pattern match confirms 14 stolen SUVs share identical modus operandi via modified ECU software.'
  },
  {
    id: 'ALT-1094',
    firNumber: 'KA-2026-MNG-00298',
    title: 'Darkweb Narcotics Import Intercepted at Port',
    district: 'Mangaluru',
    category: 'Narcotics',
    severity: 'Critical',
    timestamp: '1 hour ago',
    status: 'Apprehended',
    summary: 'Special Crime Cell seized 4.2kg contraband shipment mapped via criminal network link node.'
  },
  {
    id: 'ALT-1095',
    firNumber: 'KA-2026-HUB-00155',
    title: 'Sim Box Ransomware Campaign targeting Regional Co-ops',
    district: 'Hubballi-Dharwad',
    category: 'Cybercrime',
    severity: 'High',
    timestamp: '2 hours ago',
    status: 'Active Search',
    summary: 'IP tracing indicates coordinated phishing campaign targeting 3 district cooperative banks.'
  }
];

export const mockCrimeTrendData: CrimeTrendData[] = [
  { month: 'Jan', cybercrime: 420, robbery: 190, narcotics: 110, fraud: 310, homicide: 24 },
  { month: 'Feb', cybercrime: 480, robbery: 175, narcotics: 135, fraud: 340, homicide: 19 },
  { month: 'Mar', cybercrime: 530, robbery: 160, narcotics: 150, fraud: 380, homicide: 22 },
  { month: 'Apr', cybercrime: 610, robbery: 145, narcotics: 165, fraud: 410, homicide: 18 },
  { month: 'May', cybercrime: 690, robbery: 130, narcotics: 180, fraud: 450, homicide: 15 },
  { month: 'Jun', cybercrime: 740, robbery: 125, narcotics: 195, fraud: 510, homicide: 14 },
  { month: 'Jul', cybercrime: 810, robbery: 110, narcotics: 210, fraud: 570, homicide: 12 }
];

export const mockDistrictCrimeStats: DistrictCrimeStat[] = [
  { district: 'Bengaluru Urban', totalCases: 6420, highSeverity: 480, solvedRate: 78.4, riskScore: 88 },
  { district: 'Mysuru', totalCases: 2150, highSeverity: 120, solvedRate: 84.1, riskScore: 54 },
  { district: 'Mangaluru', totalCases: 1890, highSeverity: 165, solvedRate: 81.2, riskScore: 68 },
  { district: 'Hubballi-Dharwad', totalCases: 1540, highSeverity: 95, solvedRate: 86.5, riskScore: 49 },
  { district: 'Belagavi', totalCases: 1210, highSeverity: 70, solvedRate: 89.0, riskScore: 38 },
  { district: 'Kalaburagi', totalCases: 980, highSeverity: 65, solvedRate: 83.7, riskScore: 42 },
  { district: 'Shivamogga', totalCases: 760, highSeverity: 40, solvedRate: 91.5, riskScore: 29 }
];

export const mockChatThreads: ChatThread[] = [
  {
    id: 'thread-1',
    title: 'Bengaluru Cyber Syndicate Synthesizer',
    lastUpdated: '10m ago',
    previewText: 'Analyzed 45 FIRs linked to Telegram crypto scams.',
    category: 'Cybercrime'
  },
  {
    id: 'thread-2',
    title: 'Mysuru Vehicle Theft MO Matrix',
    lastUpdated: '2h ago',
    previewText: 'Identified 3 key keyless-entry override tools used.',
    category: 'Vehicle Theft'
  },
  {
    id: 'thread-3',
    title: 'Mangaluru Port Narcotics Flow Model',
    lastUpdated: '1d ago',
    previewText: 'Cross-referenced shipping manifests with offender list.',
    category: 'Narcotics'
  },
  {
    id: 'thread-4',
    title: 'Hubballi Sim Box Phishing Cluster',
    lastUpdated: '2d ago',
    previewText: 'Traced tower dump logs across 12 mobile cells.',
    category: 'Financial Fraud'
  }
];

export const mockInitialMessages: ChatMessage[] = [
  {
    id: 'msg-1',
    sender: 'user',
    text: 'Analyze the organized cyber fraud network active in Bengaluru Urban over the past 30 days and list key suspects.',
    timestamp: '14:30'
  },
  {
    id: 'msg-2',
    sender: 'ai',
    text: `### KSP Crime AI Intelligence Synthesis Report

Based on **48 cross-referenced FIRs** and banking anomaly feeds, KSP Intellibot has identified an organized **Telegram-based Investment Fraud Ring** operating across Koramangala and HSR Layout.

#### Executive Intelligence Summary:
- **Total Fraud Value:** ₹4.85 Crores
- **Modus Operandi:** Fake APK distribution + Crypto P2P laundering accounts
- **Primary District Hotspot:** Bengaluru Urban (Electronic City Sector 2)

#### Key Identified Suspects & Risk Profiles:
1. **Vikram "Phantom" Shetty** (Risk Score: 94/100) — *Ring Leader & Wallet Handler*
2. **Karan Nair** (Risk Score: 88/100) — *SIM Mule Supplier*
3. **Ananya Sharma** (Risk Score: 76/100) — *Phishing Portal Developer*`,
    timestamp: '14:31',
    structuredData: {
      summaryMetrics: [
        { label: 'Active FIRs Mapped', value: '48 Cases', color: '#3B82F6' },
        { label: 'Estimated Loss', value: '₹4.85 Cr', color: '#EF4444' },
        { label: 'Network Risk Level', value: 'CRITICAL', color: '#F59E0B' }
      ],
      evidenceTable: [
        { key: 'Lead FIR ID', detail: 'KA-2026-BLR-00981' },
        { key: 'IP Subnet Cluster', detail: '103.145.22.0/24 (VPN Proxied)' },
        { key: 'Mule Accounts Frozen', detail: '34 Accounts across 4 PSU Banks' }
      ],
      locationPreview: {
        district: 'Bengaluru Urban',
        coordinates: [12.9352, 77.6245],
        riskLevel: 'Critical Risk Hotspot'
      }
    }
  }
];

export const mockMapMarkers: CrimeIncidentMapMarker[] = [
  {
    id: 'MAP-1',
    firNumber: 'KA-2026-BLR-00981',
    title: 'Crypto Laundering Hub',
    category: 'Financial Fraud',
    severity: 'Critical',
    coordinates: [12.9352, 77.6245], // Koramangala
    district: 'Bengaluru Urban',
    timestamp: '2026-07-21 11:20 AM',
    description: 'Call center front operation laundering funds via illegal P2P crypto exchanges.',
    suspectsInvolved: 6
  },
  {
    id: 'MAP-2',
    firNumber: 'KA-2026-BLR-01004',
    title: 'High-End Vehicle Theft Incident',
    category: 'Vehicle Theft',
    severity: 'High',
    coordinates: [12.9716, 77.5946], // MG Road
    district: 'Bengaluru Urban',
    timestamp: '2026-07-20 09:45 PM',
    description: 'SUV stolen using signal replay device. Tracked moving towards Hosur highway.',
    suspectsInvolved: 2
  },
  {
    id: 'MAP-3',
    firNumber: 'KA-2026-MYS-00412',
    title: 'Narcotics Storage Raid',
    category: 'Narcotics',
    severity: 'Critical',
    coordinates: [12.3051, 76.6551], // Mysuru Palace Area
    district: 'Mysuru',
    timestamp: '2026-07-21 08:15 AM',
    description: 'Seized synthetic narcotics stash during early morning multi-agency raid.',
    suspectsInvolved: 4
  },
  {
    id: 'MAP-4',
    firNumber: 'KA-2026-MNG-00298',
    title: 'Cyber Heist Ransomware Server',
    category: 'Cybercrime',
    severity: 'High',
    coordinates: [12.9141, 74.8560], // Mangaluru Port Area
    district: 'Mangaluru',
    timestamp: '2026-07-19 04:30 PM',
    description: 'Command & Control server node hosting malware payload targeting regional logistics.',
    suspectsInvolved: 3
  },
  {
    id: 'MAP-5',
    firNumber: 'KA-2026-HUB-00155',
    title: 'Commercial Armed Robbery',
    category: 'Robbery',
    severity: 'High',
    coordinates: [15.3647, 75.1240], // Hubballi Commercial Street
    district: 'Hubballi-Dharwad',
    timestamp: '2026-07-21 02:10 AM',
    description: 'Armed heist at gold loan firm. Alarm triggered, CCTV captured 3 masked suspects.',
    suspectsInvolved: 3
  }
];

export const mockCriminalNodes: CriminalNode[] = [
  {
    id: 'NODE-101',
    name: 'Vikram Shetty',
    alias: 'Phantom',
    role: 'Syndicate Leader & Crypto Handler',
    riskScore: 94,
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    primaryDistrict: 'Bengaluru Urban',
    status: 'Absconding',
    chargesCount: 14,
    gangAffiliation: 'ShadowNet Cyber Syndicate',
    connections: ['NODE-102', 'NODE-103', 'NODE-104']
  },
  {
    id: 'NODE-102',
    name: 'Karan Nair',
    alias: 'Mule Master',
    role: 'Financial Accounts & SIM Provider',
    riskScore: 88,
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80',
    primaryDistrict: 'Bengaluru Urban',
    status: 'Under Surveillance',
    chargesCount: 8,
    gangAffiliation: 'ShadowNet Cyber Syndicate',
    connections: ['NODE-101', 'NODE-105']
  },
  {
    id: 'NODE-103',
    name: 'Ananya Sharma',
    alias: 'ByteCode',
    role: 'Malware Developer',
    riskScore: 76,
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80',
    primaryDistrict: 'Mysuru',
    status: 'Warrant Issued',
    chargesCount: 5,
    gangAffiliation: 'Independent Contractor',
    connections: ['NODE-101']
  },
  {
    id: 'NODE-104',
    name: 'Rahim "Bullet" Khan',
    alias: 'Bullet',
    role: 'Enforcer & Logistics Handler',
    riskScore: 91,
    avatar: 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80',
    primaryDistrict: 'Mangaluru',
    status: 'In Custody',
    chargesCount: 19,
    gangAffiliation: 'Coastline Syndicate',
    connections: ['NODE-101', 'NODE-105']
  },
  {
    id: 'NODE-105',
    name: 'Siddharth Varma',
    alias: 'Banker',
    role: 'Shell Company Director',
    riskScore: 82,
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80',
    primaryDistrict: 'Bengaluru Urban',
    status: 'Under Surveillance',
    chargesCount: 6,
    gangAffiliation: 'ShadowNet Cyber Syndicate',
    connections: ['NODE-102', 'NODE-104']
  }
];

export const mockCriminalLinks: CriminalLink[] = [
  { source: 'NODE-101', target: 'NODE-102', relationship: 'Financial Transfer', strength: 5 },
  { source: 'NODE-101', target: 'NODE-103', relationship: 'Associate', strength: 4 },
  { source: 'NODE-101', target: 'NODE-104', relationship: 'Gang Leader', strength: 5 },
  { source: 'NODE-102', target: 'NODE-105', relationship: 'Co-accused', strength: 3 },
  { source: 'NODE-104', target: 'NODE-105', relationship: 'Communication', strength: 2 }
];

export const mockIntelligenceReports: IntelligenceReport[] = [
  {
    id: 'REP-2026-001',
    reportCode: 'KSP-INT-2026-Q2-CYBER',
    title: 'Comprehensive Cybercrime & Crypto Laundering Threat Matrix',
    category: 'Cybercrime',
    author: 'IG Rajesh V. Rao',
    dateGenerated: '2026-07-18',
    classification: 'TOP SECRET',
    district: 'Bengaluru Urban',
    fileSize: '14.2 MB',
    status: 'Verified',
    summary: 'Deep-dive intelligence synthesis mapping 340 crypto wallets linked to foreign P2P platforms.'
  },
  {
    id: 'REP-2026-002',
    reportCode: 'KSP-INT-2026-MNG-NARCO',
    title: 'Coastal Narcotic Flow & Maritime Import Risk Assessment',
    category: 'Narcotics',
    author: 'SP Mangaluru Cell',
    dateGenerated: '2026-07-15',
    classification: 'CONFIDENTIAL',
    district: 'Mangaluru',
    fileSize: '8.7 MB',
    status: 'Verified',
    summary: 'Predictive analytics on maritime cargo containers utilizing automated image recognition scans.'
  },
  {
    id: 'REP-2026-003',
    reportCode: 'KSP-INT-2026-MYS-AUTO',
    title: 'Mysuru District Organized Vehicle Theft & ECU Tampering Synthesis',
    category: 'Vehicle Theft',
    author: 'DSP Crime Branch',
    dateGenerated: '2026-07-10',
    classification: 'RESTRICTED',
    district: 'Mysuru',
    fileSize: '6.1 MB',
    status: 'Draft',
    summary: 'Modus operandi catalog detailing keyless entry signal replication hardware seized in raids.'
  },
  {
    id: 'REP-2026-004',
    reportCode: 'KSP-INT-2026-HUB-FIN',
    title: 'North Karnataka District Cooperative Phishing & Sim Box Cluster',
    category: 'Financial Fraud',
    author: 'Cyber Crime Unit Hubballi',
    dateGenerated: '2026-07-05',
    classification: 'CONFIDENTIAL',
    district: 'Hubballi-Dharwad',
    fileSize: '11.5 MB',
    status: 'Verified',
    summary: 'Investigation audit detailing 12 SIM box locations deactivated across 3 districts.'
  }
];
