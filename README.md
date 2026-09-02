#Canadian Credit Risk Analytics & Underwriting Portal

An institutional-grade credit risk portfolio management dashboard and data engineering pipeline built using Python, Pandas, Pydeck, and Streamlit. This project processes loan applications, automates credit tier stratification, and maps geospatial asset risk density concentrations across Canada.

---

## 🛠️ Technology Stack
*   **Data Processing:** Python, Pandas, NumPy
*   **Interactive Front-End:** Streamlit, Custom HTML/CSS
*   **Geospatial Mapping Layer:** Pydeck (High-Contrast ScreenGrid Mapping)
*   **Version Control:** Git & GitHub Workspace

---

## ⚙️ Core Architecture & Features

### 1. Data Transformation Pipeline (`pipeline.py`)
*   **Feature Engineering:** Automates credit score segmentations mapping applicants from Tier 1 (Super Prime) down to Tier 4 (Subprime) based on institutional standards.
*   **Geospatial Noise Layer:** Programmatically models regional coordinate attributes (`Latitude` and `Longitude`) matching Canadian provincial distributions to ensure seamless geo-mapping layers.
*   **Metric Safety:** Formulates clean Debt-to-Income (DTI) metrics while guarding the pipeline against divide-by-zero database errors.

### 2. Live Credit Underwriting Desk Dashboard (`app.py`)
*   **Advanced Control Centers:** Multi-select filtering widgets allowing portfolio managers to slice metrics by risk tiers and geographic scope in real time.
*   **Fail-Safe Architecture:** Implements validation conditional rules preventing UI metric breaks or zero-division errors when analytical search filters are completely cleared.
*   **HTML/CSS Layout Enhancements:** High-performance dashboard cards featuring drop-shadow hover animations and gradient banners matching production-ready web application standards.

---

## 📂 System Directory Blueprint
```text
canadian-banking-analytics/
├── data/
│   ├── loan_data.csv               # Raw source data file (Kaggle)
│   └── clean_bank_data.csv         # Standardized asset built by pipeline.py
├── pipeline.py                     # Data processing script
└── app.py                          # Streamlit application layout
```

---

## 🚀 How to Run the Environment Locally

1. **Clone the project directories:**
   ```bash
   git clone https://github.com
   cd canadian-banking-analytics
   ```

2. **Execute the underlying transformation engine script to construct your data layer:**
   ```bash
   python pipeline.py
   ```

3. **Fire up your interactive interface dashboard server portal:**
   ```bash
   python -m streamlit run app.py
   ```
