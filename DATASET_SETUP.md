# WADI Dataset Setup

The WADI (Water Distribution) dataset files are too large (>100MB each) to be stored in GitHub directly. 

## Required files:
- `ics-dashboard/data/wadi/WADI_14days_new.csv` (~100+ MB)
- `ics-dashboard/data/wadi/WADI_attackdataLABLE.csv` (~100+ MB)

## How to get the dataset:

### Option 1: Download from Google Drive (Recommended)
Download the pre-processed WADI dataset files used in this project:

1. **WADI_14days_new.csv** (Normal operation data): 
   - **View/Download**: [Google Drive Link](https://drive.google.com/file/d/1_wlwEdLzTuR4z3pmPGsxwSHpZK49pypz/view?usp=drive_link)
   - **Direct Download**: [Download CSV](https://drive.google.com/uc?export=download&id=1_wlwEdLzTuR4z3pmPGsxwSHpZK49pypz)

2. **WADI_attackdataLABLE.csv** (Attack scenarios): 
   - **View/Download**: [Google Drive Link](https://drive.google.com/file/d/1RxUFaiG_kJbie_UT-TZkoZkPFo0jNRu9/view?usp=drive_link)
   - **Direct Download**: [Download CSV](https://drive.google.com/uc?export=download&id=1RxUFaiG_kJbie_UT-TZkoZkPFo0jNRu9)

3. After downloading, place both files in `ics-dashboard/data/wadi/` directory

### Option 2: Download from official source
1. Visit the official WADI dataset repository or research paper
2. Download and process the original WADI dataset files
3. Place them in `ics-dashboard/data/wadi/` directory

### Option 3: Local Setup (if you already have the files)
If you have the files in your Downloads folder, copy them to the project:

#### Windows PowerShell:
```powershell
Copy-Item "C:\Users\Harthik M V\Downloads\archive\WADI_14days_new.csv" "ics-dashboard\data\wadi\"
Copy-Item "C:\Users\Harthik M V\Downloads\archive\WADI_attackdataLABLE.csv" "ics-dashboard\data\wadi\"
```

## After setup:
1. Ensure the files are in the correct directory: `ics-dashboard/data/wadi/`
2. Run the application following the instructions in the main README

## Note:
The application will not work without these dataset files. The files are excluded from Git due to their large size (>100MB GitHub limit). 