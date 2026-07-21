import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { FloatingAIButton } from './components/FloatingAIButton';

// Page Imports
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { AIAssistantPage } from './pages/AIAssistantPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { CrimeMapPage } from './pages/CrimeMapPage';
import { CriminalNetworkPage } from './pages/CriminalNetworkPage';
import { ReportsPage } from './pages/ReportsPage';
import { ProfileSettingsPage } from './pages/ProfileSettingsPage';

const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#081229]">
      <Sidebar collapsed={sidebarCollapsed} setCollapsed={setSidebarCollapsed} />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-y-auto px-6 py-6 scroll-smooth">
          {children}
        </main>
      </div>
      <FloatingAIButton />
    </div>
  );
};

export function App() {
  return (
    <Router>
      <Routes>
        {/* Auth Route */}
        <Route path="/login" element={<LoginPage />} />

        {/* Dashboard & Enterprise App Routes */}
        <Route
          path="/dashboard"
          element={
            <AppLayout>
              <DashboardPage />
            </AppLayout>
          }
        />
        <Route
          path="/ai-assistant"
          element={
            <AppLayout>
              <AIAssistantPage />
            </AppLayout>
          }
        />
        <Route
          path="/analytics"
          element={
            <AppLayout>
              <AnalyticsPage />
            </AppLayout>
          }
        />
        <Route
          path="/crime-map"
          element={
            <AppLayout>
              <CrimeMapPage />
            </AppLayout>
          }
        />
        <Route
          path="/criminal-network"
          element={
            <AppLayout>
              <CriminalNetworkPage />
            </AppLayout>
          }
        />
        <Route
          path="/reports"
          element={
            <AppLayout>
              <ReportsPage />
            </AppLayout>
          }
        />
        <Route
          path="/settings"
          element={
            <AppLayout>
              <ProfileSettingsPage />
            </AppLayout>
          }
        />

        {/* Fallback to Dashboard */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
