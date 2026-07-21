import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import { PageHeader } from '../components/PageHeader';
import { mockMapMarkers } from '../data/mockData';
import { SearchBar } from '../components/SearchBar';
import { MapPin, ShieldAlert, Layers, Filter, Eye } from 'lucide-react';
import { CrimeCategory, DistrictName } from '../types';

// Custom Leaflet Pin Icon Builder
const createCustomIcon = (category: CrimeCategory, severity: string) => {
  const color = severity === 'Critical' ? '#EF4444' : '#F59E0B';
  const svgHtml = `
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="16" cy="16" r="14" fill="${color}" fill-opacity="0.25" stroke="${color}" stroke-width="2"/>
      <circle cx="16" cy="16" r="6" fill="${color}"/>
    </svg>
  `;
  return L.divIcon({
    html: svgHtml,
    className: 'custom-map-pin',
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  });
};

export const CrimeMapPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('All');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [showHeatmap, setShowHeatmap] = useState<boolean>(true);

  // Karnataka center coordinates
  const karnatakaCenter: [number, number] = [13.2500, 76.5000];

  const filteredMarkers = mockMapMarkers.filter((m) => {
    const matchesSearch =
      m.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.firNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.district.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDistrict = selectedDistrict === 'All' || m.district === selectedDistrict;
    const matchesCategory = selectedCategory === 'All' || m.category === selectedCategory;
    return matchesSearch && matchesDistrict && matchesCategory;
  });

  return (
    <div className="space-y-4 pb-8 h-[calc(100vh-100px)] flex flex-col">
      <PageHeader
        title="Interactive Crime Incident & Geofence Map"
        subtitle="Geospatial analysis of active FIRs, patrol geofences, and crime hotspots across Karnataka."
        badge="GPS MESH LIVE"
      />

      {/* Main Map Container Area */}
      <div className="relative flex-1 rounded-2xl overflow-hidden border border-blue-500/20 shadow-2xl">
        {/* Floating Top Control Panel */}
        <div className="absolute top-4 left-4 right-4 z-20 flex flex-col md:flex-row items-center gap-3">
          <div className="flex-1 w-full md:w-auto">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              placeholder="Search Incident Map by FIR #, Location or Crime Keywords..."
              showFilterToggle={false}
            />
          </div>

          <div className="flex items-center space-x-2 w-full md:w-auto overflow-x-auto">
            {/* District Selector */}
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="py-2 px-3 bg-slate-900/90 border border-blue-500/30 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500 backdrop-blur-md"
            >
              <option value="All">All Districts</option>
              <option value="Bengaluru Urban">Bengaluru Urban</option>
              <option value="Mysuru">Mysuru</option>
              <option value="Mangaluru">Mangaluru</option>
              <option value="Hubballi-Dharwad">Hubballi-Dharwad</option>
            </select>

            {/* Crime Category Selector */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="py-2 px-3 bg-slate-900/90 border border-blue-500/30 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500 backdrop-blur-md"
            >
              <option value="All">All Categories</option>
              <option value="Financial Fraud">Financial Fraud</option>
              <option value="Vehicle Theft">Vehicle Theft</option>
              <option value="Narcotics">Narcotics</option>
              <option value="Cybercrime">Cybercrime</option>
              <option value="Robbery">Robbery</option>
            </select>

            {/* Heatmap Toggle */}
            <button
              onClick={() => setShowHeatmap(!showHeatmap)}
              className={`py-2 px-3 rounded-xl text-xs font-bold flex items-center space-x-1.5 transition-all backdrop-blur-md border ${
                showHeatmap
                  ? 'bg-blue-600/80 text-white border-blue-400 shadow-glow-sm'
                  : 'bg-slate-900/90 text-slate-300 border-blue-500/30 hover:text-white'
              }`}
            >
              <Layers size={14} />
              <span>{showHeatmap ? 'Heatmap Active' : 'Show Heatmap'}</span>
            </button>
          </div>
        </div>

        {/* Leaflet React Map */}
        <MapContainer center={karnatakaCenter} zoom={7} scrollWheelZoom={true} className="w-full h-full z-10">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Render Heatmap Hotspot Radius Rings if toggled */}
          {showHeatmap &&
            filteredMarkers.map((marker) => (
              <Circle
                key={`circle-${marker.id}`}
                center={marker.coordinates}
                radius={marker.severity === 'Critical' ? 18000 : 10000}
                pathOptions={{
                  color: marker.severity === 'Critical' ? '#EF4444' : '#F59E0B',
                  fillColor: marker.severity === 'Critical' ? '#EF4444' : '#F59E0B',
                  fillOpacity: 0.15,
                  weight: 1.5
                }}
              />
            ))}

          {/* Incident Markers */}
          {filteredMarkers.map((marker) => (
            <Marker
              key={marker.id}
              position={marker.coordinates}
              icon={createCustomIcon(marker.category, marker.severity)}
            >
              <Popup>
                <div className="p-1 max-w-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-bold text-cyan-400">{marker.firNumber}</span>
                    <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                      marker.severity === 'Critical' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
                    }`}>
                      {marker.severity}
                    </span>
                  </div>

                  <h4 className="text-xs font-bold text-white mt-1">{marker.title}</h4>
                  <p className="text-[11px] text-slate-300 mt-1 leading-snug">{marker.description}</p>

                  <div className="mt-2 pt-2 border-t border-slate-700/60 flex items-center justify-between text-[10px] text-slate-400">
                    <span>{marker.district}</span>
                    <span className="font-semibold text-cyan-300">{marker.suspectsInvolved} Suspects Mapped</span>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>

        {/* Floating Bottom Legend */}
        <div className="absolute bottom-4 right-4 z-20 bg-slate-900/90 border border-blue-500/30 p-3 rounded-2xl backdrop-blur-md text-xs space-y-1.5 shadow-xl">
          <div className="font-bold text-white uppercase tracking-wider text-[10px] mb-1">Incident Risk Index</div>
          <div className="flex items-center space-x-2 text-[11px] text-slate-300">
            <span className="w-3 h-3 rounded-full bg-red-500 border border-white/20" />
            <span>Critical Severity (Immediate Response)</span>
          </div>
          <div className="flex items-center space-x-2 text-[11px] text-slate-300">
            <span className="w-3 h-3 rounded-full bg-amber-500 border border-white/20" />
            <span>High Severity (Active Investigation)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
