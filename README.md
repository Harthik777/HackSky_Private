# 🛡️ Team 0verr1de - ICS Cybersecurity Dashboard

**Advanced NILM-based Industrial Control System Security**  
**Featuring WADI Water Distribution Dataset Integration**

*Paranjay Chaudhary & Harthik MV - Manipal Institute of Technology*

---

## 🎯 **Hackathon Demo Ready!**

### **🌟 Key Highlights:**
- ✅ **Real WADI Dataset** - Singapore SUTD water distribution data
- ✅ **Actual Cyber Attacks** - Labeled attack scenarios for ML training
- ✅ **NILM Technology** - Non-intrusive load monitoring approach
- ✅ **Production Dashboard** - Real-time monitoring with anomaly detection
- ✅ **One-Click Deploy** - Vercel/Netlify ready for live demos

---

## 🚀 **Quick Start**

### **WADI Dataset Setup (Recommended)**
```bash
# 1. Download WADI from SUTD
# https://itrust.sutd.edu.sg/itrust-labs_datasets/

# 2. Setup data structure
mkdir -p data/wadi/
# Place: WADI_14days.csv, WADI_attackdata.csv

# 3. Install & Run
cd backend/ && pip install -r requirements.txt
python server.py  # Backend

npm install && npm run dev  # Frontend
```

### **Live Demo URLs:**
- **Dashboard:** http://localhost:5173
- **API Health:** http://localhost:5000/api/health  
- **WADI Info:** http://localhost:5000/api/wadi-info

---

## 💧 **WADI Dataset Integration**

### **What is WADI?**
**WADI (Water Distribution)** is a real-world ICS cybersecurity dataset from Singapore University of Technology and Design containing:

- **36+ Industrial Sensors** (flow, pressure, level, quality)
- **Real Cyber Attacks** with ground truth labels
- **14 Days Normal Operation** + attack scenarios
- **Water Distribution System** - critical infrastructure
- **Published Research Dataset** - academically credible

### **Our NILM Approach:**
We convert WADI sensor readings into power consumption patterns:
```python
# Power calculation from WADI sensors
power = flow_sensors * 10 + pump_states * 100 + pressure * 8
# Anomaly detection on power signatures during attacks
```

### **Attack Types Detected:**
- **Flow Manipulation** - Altering flow sensor readings
- **Pressure Attacks** - Manipulating system pressure
- **Pump Control** - Unauthorized pump operations
- **Level Spoofing** - False tank level data
- **Quality Tampering** - Water quality sensor attacks

---

## 🏗️ **Architecture**

### **Frontend (React + TypeScript)**
- **Real-time Power Monitoring** - NILM data visualization
- **System Status Dashboard** - Component health monitoring  
- **Security Alerts Panel** - Attack detection notifications
- **ML Analytics** - Model performance metrics
- **Responsive Design** - Mobile-ready for demos

### **Backend (Python Flask)**
- **WADI Data Processing** - Real water distribution data
- **Power Pattern Analysis** - NILM signature extraction
- **Anomaly Detection** - Statistical + ML approaches
- **Attack Classification** - Multi-class threat detection
- **RESTful APIs** - Real-time data endpoints

### **Deployment**
- **Docker Ready** - Container deployment
- **Cloud Native** - Vercel/Netlify/AWS compatible
- **Environment Config** - Production settings
- **Auto-scaling** - Load balancer ready

---

## 🔧 **Technology Stack**

### **Frontend:**
- React 18 + TypeScript
- Vite (Build Tool)
- Tailwind CSS (Styling)
- Recharts (Data Visualization)
- Lucide React (Icons)

### **Backend:**
- Python 3.11
- Flask (Web Framework)
- Pandas (Data Processing)
- Scikit-learn (ML Models)
- NumPy (Numerical Computing)

### **Data Integration:**
- **WADI Dataset** - Primary data source
- **CSV Support** - Generic data files
- **Modbus Integration** - Real-time ICS connectivity
- **ML Model Loading** - Custom anomaly detectors

---

## 📊 **Dashboard Features**

### **1. 🔍 Real-time Power Monitoring**
- Live NILM power consumption charts
- WADI sensor data conversion to power signatures
- Visual anomaly highlighting during attacks
- Historical trend analysis

### **2. 🛡️ System Health Dashboard**
- Water distribution component status
- Sensor connectivity monitoring
- ML model performance tracking
- Alert system health

### **3. 🚨 Security Alert Management**
- Real-time attack notifications
- WADI attack scenario alerts
- Severity classification (critical/warning/info)
- Alert acknowledgment and tracking

### **4. 📈 Attack Detection Analytics**
- ML model confidence scores
- Attack type probability analysis
- Model performance metrics
- WADI ground truth validation

### **5. 📋 Statistics Overview**
- Systems monitored count
- Detection accuracy rates
- Active alert summaries
- Data source indicators

---

## 🚀 **Deployment Options**

### **1. One-Click Deployment (Recommended)**
```bash
# Vercel (FREE)
git push origin main
# → Go to vercel.com → Import repo → Deploy
# Live at: https://your-app.vercel.app
```

### **2. Docker Deployment**
```bash
docker build -t ics-dashboard .
docker run -p 80:80 -p 5000:5000 ics-dashboard
```

### **3. Manual Cloud Deployment**
- **AWS:** ECS/EKS with Application Load Balancer
- **Azure:** Container Instances + App Service
- **GCP:** Cloud Run or Google Kubernetes Engine
- **DigitalOcean:** App Platform deployment

### **4. Edge/On-Premises**
- **Raspberry Pi** - Lightweight monitoring
- **Industrial Gateways** - OT network integration
- **Hybrid Cloud** - Edge + cloud processing

---

## 🎯 **Hackathon Presentation**

### **Demo Script:**
1. **"We've built an advanced ICS cybersecurity solution using SUTD's WADI dataset - real water distribution data with actual cyber attacks"**

2. **"Our NILM approach monitors power signatures to detect attacks without intrusive sensors"**

3. **"This dashboard shows real-time anomaly detection on actual industrial data"**

4. **"The red spikes you see are genuine cyber attacks from the WADI dataset"**

### **Technical Highlights:**
- Real industrial dataset (not synthetic)
- Academic research foundation
- Production-ready deployment
- Advanced ML integration
- Critical infrastructure focus

---

## 📝 **API Documentation**

### **Core Endpoints:**
```bash
GET /api/power-data        # Real-time NILM power data
GET /api/system-status     # Component health status
GET /api/alerts           # Security alerts
GET /api/attack-analysis  # ML model results
GET /api/statistics       # Dashboard metrics
GET /api/wadi-info        # WADI dataset information
```

### **Data Sources:**
```bash
GET /api/data-source      # Current data source info
GET /api/health          # System health check
```

---

## 🔒 **Security Features**

### **Network Security:**
- HTTPS/TLS encryption
- CORS configuration
- API rate limiting
- Input validation
- Security headers

### **Data Protection:**
- Secure data transmission
- Access control ready
- Audit logging capability  
- Backup/recovery support

---

## 📚 **Dataset Citation**

```bibtex
@article{ahmed2017wadi,
  title={WADI: a water distribution testbed for research in the design of secure cyber physical systems},
  author={Ahmed, Chuadhry Mujeeb and Palleti, Venkata Reddy and Mathur, Aditya P},
  journal={Proceedings of the 3rd International Workshop on Cyber-Physical Systems for Smart Water Networks},
  year={2017}
}
```

---

## 👥 **Team 0verr1de**

**Paranjay Chaudhary**
- Backend Development & ML Integration
- WADI Dataset Processing
- Anomaly Detection Algorithms

**Harthik MV** 
- Frontend Development & UI/UX
- Dashboard Visualization
- Deployment & DevOps

**Manipal Institute of Technology**  
*Advanced ICS Cybersecurity Research*

---

## 📄 **License**
MIT License - See LICENSE file for details

---

**🏆 Advanced ICS Cybersecurity Solution using Non-Intrusive Load Monitoring (NILM) with Real Industrial Dataset Integration**
