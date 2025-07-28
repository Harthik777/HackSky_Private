import React from 'react';
import { Shield, Zap, AlertTriangle, Activity } from 'lucide-react';

const StatisticsCards: React.FC = () => {
  const stats = [
    {
      title: 'Systems Monitored',
      value: '12',
      icon: Shield,
      color: 'text-cyber-400',
      bgColor: 'bg-cyber-900',
      change: '+2',
      changeType: 'positive'
    },
    {
      title: 'Power Consumption',
      value: '847.2 kW',
      icon: Zap,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-900',
      change: '-3.2%',
      changeType: 'positive'
    },
    {
      title: 'Active Alerts',
      value: '3',
      icon: AlertTriangle,
      color: 'text-red-400',
      bgColor: 'bg-red-900',
      change: '+1',
      changeType: 'negative'
    },
    {
      title: 'Detection Accuracy',
      value: '94.7%',
      icon: Activity,
      color: 'text-green-400',
      bgColor: 'bg-green-900',
      change: '+1.2%',
      changeType: 'positive'
    }
  ];

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