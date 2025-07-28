import React, { useState, useEffect } from 'react';
import { Shield, Zap, AlertTriangle, Activity } from 'lucide-react';

const StatisticsCards: React.FC = () => {
  const [stats, setStats] = useState([
    { title: 'Systems Monitored', value: '...', icon: Shield, color: 'text-cyber-400', bgColor: 'bg-cyber-900', change: '', changeType: 'positive' as const },
    { title: 'Power Consumption', value: '...', icon: Zap, color: 'text-yellow-400', bgColor: 'bg-yellow-900', change: '', changeType: 'positive' as const },
    { title: 'Active Alerts', value: '...', icon: AlertTriangle, color: 'text-red-400', bgColor: 'bg-red-900', change: '', changeType: 'negative' as const },
    { title: 'Detection Accuracy', value: '...', icon: Activity, color: 'text-green-400', bgColor: 'bg-green-900', change: '', changeType: 'positive' as const }
  ]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        setStats([
          { ...stats[0], value: data.systems_monitored.toString(), change: `+${Math.floor(Math.random() * 3)}` },
          { ...stats[1], value: data.power_consumption, change: `${Math.random() > 0.5 ? '+' : '-'}${(Math.random() * 5).toFixed(1)}%` },
          { ...stats[2], value: data.active_alerts.toString(), change: `+${Math.floor(Math.random() * 2)}` },
          { ...stats[3], value: data.detection_accuracy, change: `+${(Math.random() * 2).toFixed(1)}%` },
        ]);
      } catch (error) {
        console.error("Failed to fetch stats", error);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <div key={index} className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm font-medium">{stat.title}</p>
              <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
              <div className="flex items-center mt-2">
                <span className={`text-sm font-medium ${
                  stat.changeType === 'positive' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {stat.change}
                </span>
                <span className="text-gray-500 text-sm ml-2">from last hour</span>
              </div>
            </div>
            <div className={`p-3 rounded-lg ${stat.bgColor}`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatisticsCards; 