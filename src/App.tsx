import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, Activity, Zap, Settings, Bell, TrendingUp, X } from 'lucide-react';
import PowerMonitorChart from './components/PowerMonitorChart';
import SystemStatus from './components/SystemStatus';
import AnomalyAlerts from './components/AnomalyAlerts';
import AttackDetectionPanel from './components/AttackDetectionPanel';
import StatisticsCards from './components/StatisticsCards';

interface Alert {
  id: number;
  type: 'critical' | 'warning' | 'info';
  message: string;
  timestamp: Date;
  system: string;
}

function App() {
  const [alerts, setAlerts] = useState<Alert[]>([
    {
      id: 1,
      type: 'critical' as const,
      message: 'Unusual power spike detected on Motor Controller #3',
      timestamp: new Date(),
      system: 'Motor Control Unit'
    },
    {
      id: 2,
      type: 'warning' as const,
      message: 'Network latency increased on PLC-001',
      timestamp: new Date(Date.now() - 300000),
      system: 'PLC Network'
    }
  ]);

  const [systemHealth, setSystemHealth] = useState({
    overall: 'good',
    components: {
      nilm: 'online',
      ml_models: 'online',
      data_collection: 'warning',
      alert_system: 'online'
    }
  });

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Shield className="w-8 h-8 text-cyber-400" />
            <div>
              <h1 className="text-2xl font-bold text-white">0verr1de ICS Security</h1>
              <p className="text-gray-400 text-sm">Non-Intrusive Load Monitoring System</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg">
              <Settings className="w-5 h-5" />
            </button>
            <button 
              onClick={() => {
                setAlerts([]);
                // Add a subtle feedback for demo purposes
                console.log('🔔 Alerts cleared!');
              }}
              className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg relative transition-colors"
              title={alerts.length > 0 ? 'Clear all alerts' : 'No new alerts'}
            >
              <Bell className="w-5 h-5" />
              {alerts.length > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
                  {alerts.length}
                </span>
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-6 space-y-6">
        {/* Statistics Cards */}
        <StatisticsCards />

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Power Monitoring Chart - Takes 2 columns */}
          <div className="lg:col-span-2">
            <PowerMonitorChart />
          </div>

          {/* System Status */}
          <div>
            <SystemStatus systemHealth={systemHealth} />
          </div>
        </div>

        {/* Secondary Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Anomaly Alerts */}
          <AnomalyAlerts alerts={alerts} setAlerts={setAlerts} />

          {/* Attack Detection Panel */}
          <AttackDetectionPanel />
        </div>

        {/* Team Info Footer */}
        <div className="card mt-8">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-cyber-400 mb-2">Team 0verr1de</h3>
            <p className="text-gray-300 mb-2">
              Paranjay Chaudhary & Harthik MV - Manipal Institute of Technology
            </p>
            <p className="text-gray-500 text-sm">
              Advanced ICS Cybersecurity Solution using Non-Intrusive Load Monitoring (NILM)
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
