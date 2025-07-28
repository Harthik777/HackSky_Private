import React from 'react';
import { Server, Brain, Database, AlertCircle } from 'lucide-react';

interface SystemHealthProps {
  systemHealth: {
    overall: string;
    components: {
      nilm: string;
      ml_models: string;
      data_collection: string;
      alert_system: string;
    };
  };
}

const SystemStatus: React.FC<SystemHealthProps> = ({ systemHealth }) => {
  const components = [
    {
      name: 'NILM Sensors',
      status: systemHealth.components.nilm,
      icon: Server,
      description: 'Non-intrusive load monitoring'
    },
    {
      name: 'ML Models',
      status: systemHealth.components.ml_models,
      icon: Brain,
      description: '1D CNN/LSTM detection models'
    },
    {
      name: 'Data Collection',
      status: systemHealth.components.data_collection,
      icon: Database,
      description: 'Power trace acquisition'
    },
    {
      name: 'Alert System',
      status: systemHealth.components.alert_system,
      icon: AlertCircle,
      description: 'Anomaly notification service'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'text-green-400';
      case 'warning':
        return 'text-yellow-400';
      case 'offline':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'online':
        return 'bg-green-900';
      case 'warning':
        return 'bg-yellow-900';
      case 'offline':
        return 'bg-red-900';
      default:
        return 'bg-gray-900';
    }
  };

  const getOverallStatus = () => {
    const statuses = Object.values(systemHealth.components);
    if (statuses.includes('offline')) return { status: 'Critical', color: 'text-red-400', bg: 'bg-red-900' };
    if (statuses.includes('warning')) return { status: 'Warning', color: 'text-yellow-400', bg: 'bg-yellow-900' };
    return { status: 'Operational', color: 'text-green-400', bg: 'bg-green-900' };
  };

  const overallStatus = getOverallStatus();

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">System Status</h3>
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${overallStatus.bg} ${overallStatus.color}`}>
          {overallStatus.status}
        </div>
      </div>

      <div className="space-y-4">
        {components.map((component, index) => (
          <div key={index} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg border border-gray-600">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-lg ${getStatusBg(component.status)}`}>
                <component.icon className={`w-5 h-5 ${getStatusColor(component.status)}`} />
              </div>
              <div>
                <p className="text-white font-medium">{component.name}</p>
                <p className="text-gray-400 text-sm">{component.description}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className={`status-indicator ${
                component.status === 'online' ? 'status-online' :
                component.status === 'warning' ? 'status-warning' : 'status-offline'
              }`}></div>
              <span className={`text-sm font-medium capitalize ${getStatusColor(component.status)}`}>
                {component.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t border-gray-700">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Last Updated</span>
          <span className="text-gray-300">{new Date().toLocaleTimeString()}</span>
        </div>
        <div className="flex items-center justify-between text-sm mt-2">
          <span className="text-gray-400">Uptime</span>
          <span className="text-green-400">99.7% (7d avg)</span>
        </div>
      </div>
    </div>
  );
};

export default SystemStatus; 