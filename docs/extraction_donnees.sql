-- ============================================================================
-- REQUÊTES SQL - EXTRACTION DONNÉES CLINIQUES
-- ============================================================================

-- 1. Patients et données cliniques
SELECT 
    patient_id, site_name, age, gender,
    baseline_hemoglobin, current_hemoglobin,
    current_alt, visit_compliance
FROM patients
WHERE study_id = 'STUDY_2025';

-- 2. Détection anomalies
SELECT 
    patient_id,
    CASE 
        WHEN current_hemoglobin > baseline_hemoglobin + 3 THEN 'ANOMALY'
        WHEN current_alt > 80 THEN 'ANOMALY'
        ELSE 'NORMAL'
    END AS status
FROM clinical_visits;

-- 3. Performance sites
SELECT 
    site_name,
    COUNT(*) as total_patients,
    AVG(query_rate) as avg_query_rate,
    AVG(tmf_completeness_%) as tmf_avg
FROM patients
GROUP BY site_name;

-- 4. Prédiction dropout
SELECT 
    patient_id, risk_score,
    CASE WHEN risk_score > 70 THEN 1 ELSE 0 END as dropout_risk
FROM patients;

-- 5. KPIs globaux
SELECT 
    COUNT(*) as total_patients,
    SUM(CASE WHEN is_anomaly = 1 THEN 1 ELSE 0 END) as anomalies,
    AVG(risk_score) as avg_risk
FROM patients;
```

---

## 2️⃣ requirements.txt

Crée le fichier avec ce contenu :
```
streamlit==1.28.1
pandas==2.0.3
plotly==5.17.0
scikit-learn==1.3.2
numpy==1.24.3
scipy==1.11.4 