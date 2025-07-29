# 🎓 Study Abroad Cost Predictor

A comprehensive Electron-based application that uses Machine Learning to predict international study costs and provides data visualization tools for educational cost analysis.

## 🚀 Features

### 💰 Cost Prediction
- **ML-powered predictions** using Random Forest Regression
- Input parameters: Duration, Tuition, Rent, Visa fees, Insurance, Exchange rate, Living cost index
- Real-time cost estimation with popup results

### 📊 Data Visualization
- **25+ chart types** including heatmaps, histograms, scatter plots, treemaps, and more
- Interactive Plotly charts and static matplotlib visualizations
- Dropdown selection for easy chart type switching

### 📝 CSV Data Management
- **Load and edit CSV files** directly in the application
- Table view with inline editing capabilities
- Toggle between table and text editor views
- Download template functionality

### 📄 Report Generation
- **Comprehensive PDF reports** with prediction results
- Customizable chart selection for reports
- Professional formatting with input parameters and outputs
- Print functionality for hard copies

### 🖥️ Cross-Platform Support
- Windows, macOS, and Linux builds
- Fullscreen responsive design
- Smooth loading animations

## 📋 Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.7 or higher)
- **npm** package manager

### Python Dependencies
```bash
pip install pandas numpy scikit-learn matplotlib seaborn plotly joblib
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/sejal-pv/ML_model_to_predict_international_study_cost
cd ML_model_to_predict_international_study_cost
```

2. **Install Node.js dependencies**
```bash
npm install
```

3. **Install Python dependencies**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn plotly joblib
```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
npm start
```

### Windows Quick Start
```bash
start.bat
```

## 🏗️ Building Executables

### Install Build Tools
```bash
npm install electron-builder --save-dev
```

### Build Commands
```bash
# Windows installer
npm run build-win

# macOS DMG
npm run build-mac

# Linux AppImage
npm run build-linux

# All platforms
npm run build-all
```

### Windows Build Script
```bash
build.bat
```

**Output Location:** `dist/` folder

## 📖 Usage Guide

### 1. Cost Prediction
1. Navigate to **🎯 Predict Cost** tab
2. Enter study parameters:
   - Duration (0.6-5.0 years)
   - Tuition fees (USD)
   - Monthly rent (USD)
   - Visa application fees
   - Health insurance costs
   - Exchange rate
   - Living cost index (27-122)
3. Click **🔍 Predict Cost**
4. View results in popup window

### 2. Data Visualization
1. Go to **📊 Visualize Data** tab
2. Select chart type from dropdown (25+ options)
3. Charts load with smooth animations
4. Interactive charts support zoom and hover

### 3. CSV Data Management
1. Open **📝 Edit CSV** tab
2. Default dataset loads automatically
3. **Select CSV File** to load custom data
4. **Enable Editing** to modify table cells
5. **Toggle View** between table and text editor
6. **Save Changes** to update file

### 4. Report Generation
1. Access **📄 Reports** tab
2. Select desired charts from multi-select dropdown
3. **Generate PDF Report** or **Print Report**
4. Reports include:
   - Input parameters table
   - Prediction results
   - Selected visualizations

## 🗂️ File Structure

```
├── main.js                 # Electron main process
├── index.html             # Frontend interface
├── predict.py             # ML prediction script
├── visualize.py           # Chart generation script
├── package.json           # Node.js configuration
├── start.bat             # Windows startup script
├── build.bat             # Windows build script
├── International_Education_Costs_with_Calculations.csv
└── README.md             # Documentation
```

## 🔧 Technical Details

### Machine Learning Model
- **Algorithm:** Random Forest Regression
- **Features:** 7 input parameters
- **Training Data:** International education cost dataset
- **Output:** Annual cost prediction in USD

### Frontend Technologies
- **Electron** - Desktop application framework
- **HTML/CSS/JavaScript** - User interface
- **Plotly.js** - Interactive charts
- **Express.js** - Backend server

### Backend Technologies
- **Python** - ML processing
- **pandas** - Data manipulation
- **scikit-learn** - Machine learning
- **matplotlib/seaborn** - Static charts
- **plotly** - Interactive visualizations

## 🎨 Chart Types Available

| Category | Charts |
|----------|--------|
| **Statistical** | Correlation Heatmap, Histogram, Box Plot, Violin Plot |
| **Comparison** | Bar Chart, Scatter Plot, Bubble Chart |
| **Distribution** | Density Map, Ridge Plot, Strip Chart, Swarm Plot |
| **Hierarchical** | Treemap, Sunburst, Sankey Diagram |
| **Multi-dimensional** | Parallel Coordinates, Pairwise Comparison |
| **Specialized** | Waterfall, Funnel, Gauge, Faceted Analysis |

## 🚨 Troubleshooting

### Common Issues

**Python Module Errors:**
```bash
pip install joblib pandas numpy scikit-learn matplotlib seaborn plotly
```

**Port Already in Use:**
- Close other applications using port 3000
- Restart the application

**File Permission Errors:**
- Run as administrator on Windows
- Check file permissions on Linux/macOS

**Build Failures:**
```bash
npm install electron-builder --save-dev
npm run build-win
```

## 📊 Sample Data

The application includes a comprehensive dataset with:
- **600+ universities** worldwide
- **Multiple education levels** (Bachelor, Master, PhD)
- **Cost components** (tuition, living, visa, insurance)
- **Geographic coverage** across 50+ countries

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Sejal PV** - Original work - [sejal-pv](https://github.com/sejal-pv)
- **Savan S Vernekar** - Contributor - [savan-s-vernekar](https://github.com/savan-s-vernekar)

## 🙏 Acknowledgments

- International education cost data sources
- Open source ML libraries
- Electron community
- Chart.js and Plotly.js teams

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check troubleshooting section
- Review documentation

---

**Live Demo:** https://mlmodeltopredictinternationalstudycost-de8udqewuavdl9vu3ppunk.streamlit.app/

**Made with ❤️ in India**