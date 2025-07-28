# 📊 **REAL DATA INTEGRATION GUIDE**
## **Replace Fake Data with Your Actual NILM Data**

---

## 🎯 **QUICK START** (For Hackathon Demo)

### **Option 1: CSV File Integration (EASIEST)**

1. **Create data folder:**
```bash
mkdir data/
```

2. **Add your CSV file:**
```bash
# Copy your data file to: data/power_consumption.csv
# Required format (see sample):
timestamp,device_id,power_consumption,voltage,current
2024-01-28 10:00:00,motor_01,125.5,220.1,0.57
2024-01-28 10:05:00,motor_01,130.2,219.8,0.59
```

3. **Install dependencies:**
```bash
cd backend/
pip install pandas numpy scikit-learn
```

4. **Restart server:**
```bash
python server.py
```

✅ **Your dashboard will now use REAL data!**

---

## 📊 **DATA FORMAT REQUIREMENTS**

### **CSV Format:**
```csv
timestamp,device_id,power_consumption,voltage,current
2024-01-28 10:00:00,motor_controller_1,125.5,220.1,0.57
2024-01-28 10:05:00,motor_controller_1,130.2,219.8,0.59
2024-01-28 10:10:00,plc_001,85.3,24.1,3.54
```

### **Required Columns:**
- `timestamp` - Date/time in YYYY-MM-DD HH:MM:SS format
- `device_id` - Unique identifier for each ICS device
- `power_consumption` - Power reading in kW or W
- `voltage` (optional) - Voltage measurement
- `current` (optional) - Current measurement

---

## 🔧 **ADVANCED INTEGRATION OPTIONS**

### **Option 2: Real-time Modbus Integration**

1. **Install Modbus library:**
```bash
pip install pymodbus
```

2. **Set environment variables:**
```bash
# Windows
set MODBUS_HOST=192.168.1.100
set MODBUS_PORT=502

# Linux/Mac
export MODBUS_HOST=192.168.1.100
export MODBUS_PORT=502
```

3. **Modify `data_integration.py`:**
```python
# Update convert_raw_to_power() for your sensor specs
def convert_raw_to_power(self, raw_value):
    scale_factor = 0.1  # Your sensor's scale factor
    offset = 0          # Your sensor's offset
    return (raw_value * scale_factor) + offset
```

### **Option 3: Machine Learning Model Integration**

1. **Save your trained model:**
```python
import joblib
# After training your 1D CNN/LSTM model:
joblib.dump(your_model, 'models/anomaly_detector.pkl')
```

2. **Update model loading:**
```python
# In data_integration.py __init__():
try:
    self.ml_model = joblib.load('models/anomaly_detector.pkl')
except:
    print("ML model not found, using statistical detection")
```

---

## 🚀 **DEPLOYMENT WITH REAL DATA**

### **Vercel Deployment:**
1. Include your data files in the repo:
```bash
git add data/power_consumption.csv
git add models/your_model.pkl
git commit -m "Add real data and ML model"
git push origin main
```

2. Set environment variables in Vercel:
- Go to Vercel Dashboard → Project → Settings → Environment Variables
- Add: `MODBUS_HOST`, `MODBUS_PORT` (if using Modbus)

### **Local Testing:**
```bash
# Check data source status
curl http://localhost:5000/api/data-source

# Expected response:
{
  "using_real_data": true,
  "real_data_module_available": true
}
```

---

## 🎯 **HACKATHON DEMO CHECKLIST**

### **Before Presentation:**
- [ ] Real data CSV file added to `data/power_consumption.csv`
- [ ] Backend server shows "✅ Real data connector initialized"
- [ ] Dashboard displays actual power readings from your data
- [ ] Anomaly detection working on your data
- [ ] Deployment successful with real data

### **During Demo:**
1. **Show data source:** Visit `/api/data-source` to prove real data usage
2. **Explain NILM:** Point out how power signatures detect anomalies
3. **Live dashboard:** Show real-time updates from your actual data
4. **ML integration:** Highlight anomaly detection on actual readings

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues:**

**"Using simulated data only"**
```bash
# Solution: Install pandas
pip install pandas numpy

# Check data file exists
ls data/power_consumption.csv
```

**"Error loading CSV data"**
```bash
# Check CSV format (first few lines):
head -5 data/power_consumption.csv

# Ensure timestamp format is correct:
# GOOD: 2024-01-28 10:00:00
# BAD:  28/01/2024 10:00
```

**"No recent data found"**
```bash
# Update timestamps to recent dates
# Or modify hours_back parameter in server.py
```

### **Testing Your Integration:**
```bash
# 1. Check server logs
python backend/server.py
# Look for: "📊 Using real power data"

# 2. Test API endpoint
curl http://localhost:5000/api/power-data
# Should return your actual data points

# 3. Check dashboard
# Open http://localhost:5173
# Power chart should show your actual readings
```

---

## 📈 **PRESENTATION TIPS**

### **Data Story for Judges:**
1. **"We collected real power consumption data from [your source]"**
2. **"Our NILM system processes actual industrial readings"**
3. **"The ML model detected X anomalies in our dataset"**
4. **"This dashboard monitors real ICS infrastructure"**

### **Technical Highlights:**
- Real-time data processing
- NILM-based anomaly detection
- Machine learning integration
- Industrial protocol support (Modbus)
- Scalable cloud deployment

---

**🏆 Good luck with your hackathon presentation!** 