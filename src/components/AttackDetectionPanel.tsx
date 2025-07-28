import React, { useState, useEffect } from 'react';
import { Shield, Brain, Target, TrendingDown } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

const AttackDetectionPanel: React.FC = () => {
  const [threatLevel, setThreatLevel] = useState('Low');
  const [confidenceScore, setConfidenceScore] = useState(94.7);

  const threatData = [
    { name: 'Normal', value: 87, color: '#10B981' },
    { name: 'Suspicious', value: 10, color: '#F59E0B' },
    { name: 'Malicious', value: 3, color: '#EF4444' }
  ];

  const attackTypes = [
    { type: 'DoS Attack', probability: 15, detected: 2 },
    { type: 'Data Injection', probability: 8, detected: 0 },
    { type: 'Command Injection', probability: 12, detected: 1 },
    { type: 'Replay Attack', probability: 5, detected: 0 },
    { type: 'Man-in-Middle', probability: 3, detected: 0 }
  ];

  const modelMetrics = {
    accuracy: 94.7,
    precision: 92.3,
    recall: 89.6,
    f1Score: 90.9
  };

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setConfidenceScore(prev => Math.max(85, Math.min(99, prev + (Math.random() - 0.5) * 2)));
      
      // Occasionally change threat level
      if (Math.random() > 0.95) {
        const levels = ['Low', 'Medium', 'High'];
        setThreatLevel(levels[Math.floor(Math.random() * levels.length)]);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'Low':
        return 'text-green-400 bg-green-900';
      case 'Medium':
        return 'text-yellow-400 bg-yellow-900';
      case 'High':
        return 'text-red-400 bg-red-900';
      default:
        return 'text-gray-400 bg-gray-900';
    }
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-800 border border-gray-600 rounded-lg p-3 shadow-lg">
          <p className="text-gray-300">{`${payload[0].payload.type}`}</p>
          <p className="text-cyber-400">{`Probability: ${payload[0].value}%`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Shield className="w-6 h-6 text-red-400" />
          <div>
            <h3 className="text-lg font-semibold text-white">Attack Detection</h3>
            <p className="text-gray-400 text-sm">ML-powered threat analysis</p>
          </div>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${getThreatLevelColor(threatLevel)}`}>
          {threatLevel} Risk
        </div>
      </div>

      {/* Threat Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div>
          <h4 className="text-white font-medium mb-3">Activity Classification</h4>
          <div style={{ width: '100%', height: '150px' }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={threatData}
                  cx="50%"
                  cy="50%"
                  innerRadius={30}
                  outerRadius={60}
                  dataKey="value"
                >
                  {threatData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value) => [`${value}%`, 'Percentage']}
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div>
          <h4 className="text-white font-medium mb-3">Model Performance</h4>
          <div className="space-y-2">
            {Object.entries(modelMetrics).map(([key, value]) => (
              <div key={key} className="flex items-center justify-between">
                <span className="text-gray-400 text-sm capitalize">
                  {key.replace(/([A-Z])/g, ' $1')}
                </span>
                <div className="flex items-center space-x-2">
                  <div className="w-16 bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-cyber-400 h-2 rounded-full" 
                      style={{ width: `${value}%` }}
                    ></div>
                  </div>
                  <span className="text-white text-sm font-medium">{value}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Attack Types */}
      <div className="mb-6">
        <h4 className="text-white font-medium mb-3">Attack Vector Analysis</h4>
        <div style={{ width: '100%', height: '200px' }}>
          <ResponsiveContainer>
            <BarChart data={attackTypes} layout="horizontal">
              <XAxis type="number" stroke="#9CA3AF" fontSize={12} />
              <YAxis 
                type="category" 
                dataKey="type" 
                stroke="#9CA3AF" 
                fontSize={12}
                width={100}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="probability" fill="#0EA5E9" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Current Status */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-700">
        <div className="text-center">
          <div className="flex items-center justify-center space-x-1 mb-1">
            <Brain className="w-4 h-4 text-cyber-400" />
            <p className="text-gray-400 text-sm">Confidence</p>
          </div>
          <p className="text-lg font-bold text-white">{confidenceScore.toFixed(1)}%</p>
        </div>
        <div className="text-center">
          <div className="flex items-center justify-center space-x-1 mb-1">
            <Target className="w-4 h-4 text-green-400" />
            <p className="text-gray-400 text-sm">Detected</p>
          </div>
          <p className="text-lg font-bold text-white">
            {attackTypes.reduce((sum, attack) => sum + attack.detected, 0)}
          </p>
        </div>
        <div className="text-center">
          <div className="flex items-center justify-center space-x-1 mb-1">
            <TrendingDown className="w-4 h-4 text-yellow-400" />
            <p className="text-gray-400 text-sm">Blocked</p>
          </div>
          <p className="text-lg font-bold text-white">3</p>
        </div>
      </div>
    </div>
  );
};

export default AttackDetectionPanel; 