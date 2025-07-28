import React from 'react';
import { AlertTriangle, X, Clock, MapPin } from 'lucide-react';

interface Alert {
  id: number;
  type: 'critical' | 'warning' | 'info';
  message: string;
  timestamp: Date;
  system: string;
}

interface AnomalyAlertsProps {
  alerts: Alert[];
  setAlerts: React.Dispatch<React.SetStateAction<Alert[]>>;
}

const AnomalyAlerts: React.FC<AnomalyAlertsProps> = ({ alerts, setAlerts }) => {
  const getAlertStyle = (type: string) => {
    switch (type) {
      case 'critical':
        return 'border-red-500 bg-red-900/20';
      case 'warning':
        return 'border-yellow-500 bg-yellow-900/20';
      case 'info':
        return 'border-blue-500 bg-blue-900/20';
      default:
        return 'border-gray-500 bg-gray-900/20';
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5 text-red-400" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-400" />;
      case 'info':
        return <AlertTriangle className="w-5 h-5 text-blue-400" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-gray-400" />;
    }
  };

  const dismissAlert = (alertId: number) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
  };

  const formatTimeAgo = (timestamp: Date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - timestamp.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `${diffInHours}h ago`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    return `${diffInDays}d ago`;
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <AlertTriangle className="w-6 h-6 text-yellow-400" />
          <h3 className="text-lg font-semibold text-white">Security Alerts</h3>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-gray-400 text-sm">
            {alerts.length} active
          </span>
        </div>
      </div>

      <div className="space-y-3 max-h-80 overflow-y-auto">
        {alerts.length === 0 ? (
          <div className="text-center py-8">
            <AlertTriangle className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-400">No active alerts</p>
            <p className="text-gray-500 text-sm">System is operating normally</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} className={`p-4 rounded-lg border-l-4 ${getAlertStyle(alert.type)}`}>
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <div className="mt-0.5">
                    {getAlertIcon(alert.type)}
                  </div>
                  <div className="flex-1">
                    <p className="text-white font-medium">{alert.message}</p>
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-400">
                      <div className="flex items-center space-x-1">
                        <MapPin className="w-4 h-4" />
                        <span>{alert.system}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{formatTimeAgo(alert.timestamp)}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => dismissAlert(alert.id)}
                  className="p-1 text-gray-400 hover:text-white hover:bg-gray-700 rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {alerts.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">
              Critical: {alerts.filter(a => a.type === 'critical').length} | 
              Warning: {alerts.filter(a => a.type === 'warning').length}
            </span>
            <button
              onClick={() => setAlerts([])}
              className="text-cyber-400 hover:text-cyber-300 font-medium"
            >
              Clear All
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnomalyAlerts; 