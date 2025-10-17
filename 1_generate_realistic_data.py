"""
Générateur de données cliniques conformes FDA/EMA
Simule: EDC, CTMS, eTMF, Central Monitoring
Auteur: Lévi Junior BOUBANDA
"""
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker(['fr_FR', 'en_US'])
np.random.seed(42)

print("🚀 Génération de données cliniques avancées...")
print("="*60)

# Configuration étude clinique Phase III
STUDY_SITES = {
    'FR-PAR-001': {'name': 'Hôpital Pitié-Salpêtrière', 'performance': 0.9},
    'FR-LYO-002': {'name': 'Hôpital Lyon Sud', 'performance': 0.85},
    'FR-MAR-003': {'name': 'CHU Marseille', 'performance': 0.75},
    'BE-BRU-004': {'name': 'UZ Brussel', 'performance': 0.88},
    'CH-GEN-005': {'name': 'HUG Genève', 'performance': 0.92}
}

# Protocoles d'étude
VISITS = ['Screening', 'Baseline', 'Week-2', 'Week-4', 'Week-8', 'Week-12', 'EOS']
ADVERSE_EVENTS = ['Headache', 'Nausea', 'Fatigue', 'None', 'None', 'None']

n_patients = 500
patients = []

for i in range(n_patients):
    site_id = random.choice(list(STUDY_SITES.keys()))
    site_perf = STUDY_SITES[site_id]['performance']
    
    patient = {
        'patient_id': f'PAT-{site_id[-3:]}-{i:04d}',
        'site_id': site_id,
        'site_name': STUDY_SITES[site_id]['name'],
        'enrollment_date': fake.date_between('-6M', 'today'),
        'age': max(18, min(85, np.random.normal(52, 12))),
        'gender': random.choice(['M', 'F']),
        'visit_compliance': random.random() < site_perf,
        
        # Métriques EDC
        'data_entry_delay_days': max(0, np.random.normal(3, 2)),
        'query_rate': max(0, min(1, np.random.normal(0.15, 0.05))),
        'sdv_ready': random.random() < 0.8,
        
        # Métriques CTMS
        'protocol_deviation': random.random() < 0.1,
        'adverse_event': random.choice(ADVERSE_EVENTS),
        'dropout_risk': random.random() < 0.15,
        
        # Métriques eTMF
        'essential_docs_complete': random.random() < site_perf,
        'tmf_completeness_%': min(100, max(60, np.random.normal(85, 10))),
        
        # KPIs critiques
        'days_since_last_visit': np.random.randint(0, 30),
        'monitor_review_needed': random.random() < 0.3,
        
        # Métriques laboratoire
        'lab_hemoglobin': max(8, min(18, np.random.normal(13.5, 1.5))),
        'lab_creatinine': max(0.5, min(2.5, np.random.normal(1.0, 0.2))),
        'lab_alt': max(10, min(100, np.random.normal(30, 10)))
    }
    patients.append(patient)

df = pd.DataFrame(patients)

# Ajouter score de risque composite
df['risk_score'] = (
    df['query_rate'] * 30 + 
    df['protocol_deviation'].astype(int) * 40 + 
    (df['dropout_risk'] * 30)
).round(1)

# Catégoriser les sites
df['site_category'] = pd.cut(df['risk_score'], 
                            bins=[0, 10, 20, 100], 
                            labels=['Low Risk', 'Medium Risk', 'High Risk'])

# Ajouter quelques anomalies intentionnelles
anomaly_indices = np.random.choice(df.index, size=25, replace=False)
df.loc[anomaly_indices, 'lab_hemoglobin'] = np.random.choice([7.0, 19.0], 25)
df.loc[anomaly_indices, 'lab_alt'] = np.random.choice([5, 120], 25)

# Sauvegarder
df.to_csv('clinical_data_pro.csv', index=False)

print(f"✅ {n_patients} patients générés avec {len(STUDY_SITES)} sites")
print(f"📊 Colonnes créées: {len(df.columns)}")
print(f"🎯 Sites à haut risque: {(df['site_category'] == 'High Risk').sum()} patients")
print(f"⚠️  Anomalies injectées: {len(anomaly_indices)} patients")
print(f"\n📈 Aperçu des données:")
print(df.head())
print(f"\n💾 Données sauvegardées dans: clinical_data_pro.csv")