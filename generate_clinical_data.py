import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 70)
print("🔧 GÉNÉRATION DE DONNÉES CLINIQUES VALIDES")
print("=" * 70)

np.random.seed(42)

# Paramètres
n_patients = 500
sites = ['Hôpital Lyon Sud', 'HUG Genève', 'Hôpital Pitié-Salpêtrière', 
         'UZ Bruxelles', 'CHU de Marseille', 'CHU Montpellier']

# Créer les données
data = []

for patient_id in range(1, n_patients + 1):
    site = np.random.choice(sites)
    
    # Dates
    enrollment_date = datetime.now() - timedelta(days=np.random.randint(30, 365))
    visit_date = enrollment_date + timedelta(days=np.random.randint(1, 100))
    
    # Données cliniques
    baseline_hemoglobin = np.random.normal(12, 2)
    baseline_alt = np.random.normal(25, 15)
    baseline_creatinine = np.random.normal(0.9, 0.3)
    
    current_hemoglobin = baseline_hemoglobin + np.random.normal(0, 1)
    current_alt = baseline_alt + np.random.normal(0, 10)
    current_creatinine = baseline_creatinine + np.random.normal(0, 0.2)
    
    # Métriques
    visit_compliance = np.random.uniform(0.6, 1.0)
    query_rate = np.random.uniform(0, 0.3)
    data_entry_delay_days = np.random.randint(0, 30)
    protocol_deviation = np.random.randint(0, 5)
    tmf_completeness = np.random.uniform(70, 100)
    days_since_enrollment = (datetime.now() - enrollment_date).days
    risk_score = np.random.uniform(0, 100)
    
    # Détection anomalies/dropout
    is_dropout = np.random.choice([0, 1], p=[0.85, 0.15])
    
    # Anomalie si mesures anormales
    is_anomaly = 1 if (
        abs(current_hemoglobin - baseline_hemoglobin) > 3 or 
        current_alt > 80 or 
        query_rate > 0.2 or 
        tmf_completeness < 75
    ) else 0
    
    dropout_prediction = 1 if is_dropout or (risk_score > 70) else 0
    anomaly_flag = 'Anomalie' if is_anomaly else 'Normal'
    anomaly_detected = 'Oui' if is_anomaly else 'Non'
    
    # Catégorisation
    site_category = 'Academic' if 'Hôpital' in site or 'CHU' in site else 'Private'
    dropout_risk_level = 'High' if risk_score > 75 else ('Medium' if risk_score > 50 else 'Low')
    
    data.append({
        'patient_id': patient_id,
        'site_name': site,
        'age': np.random.randint(18, 85),
        'gender': np.random.choice(['M', 'F']),
        'enrollment_date': enrollment_date.strftime('%Y-%m-%d'),
        'baseline_hemoglobin': baseline_hemoglobin,
        'baseline_alt': baseline_alt,
        'baseline_creatinine': baseline_creatinine,
        'current_hemoglobin': current_hemoglobin,
        'current_alt': current_alt,
        'current_creatinine': current_creatinine,
        'visit_compliance': visit_compliance,
        'query_rate': query_rate,
        'data_entry_delay_days': data_entry_delay_days,
        'protocol_deviation': protocol_deviation,
        'protocol_deviations': protocol_deviation,  # Alias
        'tmf_completeness_%': tmf_completeness,
        'days_since_enrollment': days_since_enrollment,
        'risk_score': risk_score,
        'is_dropout': is_dropout,
        'is_anomaly': is_anomaly,
        'dropout_prediction': dropout_prediction,
        'anomaly_flag': anomaly_flag,
        'anomaly_detected': anomaly_detected,
        'site_category': site_category,
        'dropout_risk_level': dropout_risk_level,
        'lab_hemoglobin': current_hemoglobin,  # Alias pour lab_hemoglobin
        'lab_alt': current_alt,  # Alias pour lab_alt
    })

# Créer DataFrame
df = pd.DataFrame(data)

# Sauvegarder
filename = 'clinical_data_complete.csv'
df.to_csv(filename, index=False)

print(f"\n✅ Fichier créé: {filename}")
print(f"📊 {len(df)} patients générés")
print(f"🏥 {df['site_name'].nunique()} sites différents")
print(f"🔥 Anomalies détectées: {df['is_anomaly'].sum()}")
print(f"⚠️  Dropouts prédits: {df['dropout_prediction'].sum()}")

print("\n" + "=" * 70)
print("📋 COLONNES CRÉÉES:")
print("=" * 70)
print(df.columns.tolist())

print("\n" + "=" * 70)
print("📊 APERÇU:")
print("=" * 70)
print(df.head(10))

print("\n✨ Données prêtes pour le dashboard! ✨")
print(f"Vous pouvez maintenant relancer: streamlit run 3_dashboard_executive.py")