import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { Activity, TrendingUp } from 'lucide-react';

const PowerMonitorChart: React.FC = () => {
  const [data, setData] = useState([
    { time: '10:00', power: 820, normal: 850, anomaly: null },
    { time: '10:05', power: 832, normal: 855, anomaly: null },
    { time: '10:10', power: 845, normal: 860, anomaly: null },
    { time: '10:15', power: 867, normal: 862, anomaly: null },
    { time: '10:20', power: 923, normal: 865, anomaly: 923 }, // Anomaly detected
    { time: '10:25', power: 889, normal: 868, anomaly: null },
    { time: '10:30', power: 851, normal: 870, anomaly: null },
    { time: '10:35', power: 847, normal: 872, anomaly: null },
    { time: '10:40', power: 863, normal: 875, anomaly: null },
    { time: '10:45', power: 871, normal: 878, anomaly: null },
  ]);

  const [currentPower, setCurrentPower] = useState(871);

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      const newPower = 850 + Math.random() * 50 + (Math.random() > 0.9 ? 80 : 0); // Occasional spike
      setCurrentPower(Math.round(newPower));
      
      setData(prevData => {
        const newTime = new Date();
        const timeString = `${newTime.getHours()}:${newTime.getMinutes().toString().padStart(2, '0')}`;
        
        const newDataPoint = {
          time: timeString,
          power: Math.round(newPower),
          normal: 880,
          anomaly: newPower > 920 ? Math.round(newPower) : null
        };
        
        return [...prevData.slice(1), newDataPoint];
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-800 border border-gray-600 rounded-lg p-3 shadow-lg">
          <p className="text-gray-300">{`Time: ${label}`}</p>
          <p className="text-cyber-400">{`Power: ${payload[0].value} kW`}</p>
          {payload[0].payload.anomaly && (
            <p className="text-red-400 font-semibold">⚠️ Anomaly Detected</p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Activity className="w-6 h-6 text-cyber-400" />
          <div>
            <h3 className="text-lg font-semibold text-white">Real-Time Power Monitoring</h3>
            <p className="text-gray-400 text-sm">NILM-based system monitoring</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-white">{currentPower} kW</p>
          <p className="text-gray-400 text-sm">Current Load</p>
        </div>
      </div>

      <div style={{ width: '100%', height: '300px' }}>
        <ResponsiveContainer>
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="time" 
              stroke="#9CA3AF"
              fontSize={12}
            />
            <YAxis 
              stroke="#9CA3AF"
              fontSize={12}
              domain={['dataMin - 20', 'dataMax + 20']}
            />
            <Tooltip content={<CustomTooltip />} />
            
            {/* Normal operating range */}
            <Area
              type="monotone"
              dataKey="normal"
              stroke="#6B7280"
              fill="#6B7280"
              fillOpacity={0.1}
              strokeDasharray="5 5"
            />
            
            {/* Actual power consumption */}
            <Area
              type="monotone"
              dataKey="power"
              stroke="#0EA5E9"
              fill="#0EA5E9"
              fillOpacity={0.2}
              strokeWidth={2}
            />
            
            {/* Anomaly points */}
            <Line
              type="monotone"
              dataKey="anomaly"
              stroke="#EF4444"
              strokeWidth={3}
              dot={{ fill: '#EF4444', strokeWidth: 2, r: 4 }}
              connectNulls={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-700">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-cyber-400 rounded-full"></div>
            <span className="text-gray-300 text-sm">Actual Power</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-gray-500 rounded-full"></div>
            <span className="text-gray-300 text-sm">Normal Range</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span className="text-gray-300 text-sm">Anomalies</span>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-green-400">
          <TrendingUp className="w-4 h-4" />
          <span className="text-sm">System Operating Normally</span>
        </div>
      </div>
    </div>
  );
};

export default PowerMonitorChart; 