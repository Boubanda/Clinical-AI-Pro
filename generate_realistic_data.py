"""
Générateur de données cliniques réalistes pour tester votre modèle ML
- Patterns vrais de dropouts
- Anomalies laboratoire réalistes
- Variations site-to-site
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Configuration
n_patients = 500
sites = ['CHU Marseille', 'UZ Bruxelles', 'Hôpital Pitié-Salpêtrière', 
         'Hôpital Lyon Sud', 'HUG Genève']
protocol_duration = 180  # jours

# Créer base patients
data = {
    'patient_id': [f'PAT-{i:04d}' for i in range(1, n_patients + 1)],
    'site_name': np.random.choice(sites, n_patients),
    'age': np.random.normal(55, 15, n_patients).astype(int),
    'gender': np.random.choice(['M', 'F'], n_patients),
    'enrollment_date': [datetime.now() - timedelta(days=np.random.randint(10, 180)) for _ in range(n_patients)],
}

df = pd.DataFrame(data)

# Variables cliniques réalistes
df['baseline_hemoglobin'] = np.random.normal(13, 2, n_patients)  # g/dL
df['baseline_alt'] = np.random.normal(35, 15, n_patients)  # U/L
df['baseline_creatinine'] = np.random.normal(0.9, 0.3, n_patients)  # mg/dL

# Évolution pendant l'étude
df['current_hemoglobin'] = df['baseline_hemoglobin'] + np.random.normal(0, 1.5, n_patients)
df['current_alt'] = df['baseline_alt'] + np.random.normal(0, 20, n_patients)
df['current_creatinine'] = df['baseline_creatinine'] + np.random.normal(0, 0.2, n_patients)

# Variables comportementales
df['visit_compliance'] = np.random.uniform(0.5, 1.0, n_patients)  # % visites complétées
df['query_rate'] = np.random.exponential(0.08, n_patients)  # Taux de requêtes
df['data_entry_delay_days'] = np.random.exponential(2, n_patients)  # Délai saisie
df['protocol_deviations'] = np.random.poisson(2, n_patients)  # Nb déviation protocole

# Indicateurs qualité
df['tmf_completeness_%'] = np.random.uniform(70, 100, n_patients)
df['query_resolution_time_days'] = np.random.exponential(5, n_patients)

# ===== DROPOUT PATTERN RÉALISTE =====
dropout_prob = np.where(
    (df['query_rate'] > 0.15) |  # Beaucoup de requêtes = risque
    (df['visit_compliance'] < 0.7) |  # Faible compliance = risque
    (df['protocol_deviations'] > 4) |  # Déviation = risque
    (np.abs(df['current_hemoglobin'] - df['baseline_hemoglobin']) > 3) |  # Changement hém
    (np.abs(df['current_alt'] - df['baseline_alt']) > 60),  # Changement ALT
    0.35,  # Probabilité dropout si conditions
    0.08   # Probabilité baseline
)

df['is_dropout'] = (np.random.random(n_patients) < dropout_prob).astype(int)

# ===== ANOMALIES RÉALISTES =====
# Quelques patients avec vraies anomalies
anomaly_indices = np.random.choice(n_patients, size=25, replace=False)
df['is_anomaly'] = 0
df.loc[anomaly_indices, 'is_anomaly'] = 1

# Injecter anomalies réalistes
for idx in anomaly_indices:
    anomaly_type = np.random.choice(['extreme_lab', 'impossible_value', 'data_quality'])
    if anomaly_type == 'extreme_lab':
        df.at[idx, 'current_hemoglobin'] = np.random.choice([3, 20])  # Hors norme
    elif anomaly_type == 'impossible_value':
        df.at[idx, 'visit_compliance'] = np.random.uniform(1.01, 1.5)  # > 100%
    else:
        df.at[idx, 'query_rate'] = np.random.uniform(0.8, 2.0)  # Très élevé

# Variables dérivées (comme dans votre modèle)
df['days_since_enrollment'] = [(datetime.now() - enrollment).days 
                                for enrollment in df['enrollment_date']]
df['risk_score'] = (
    df['query_rate'] * 0.25 +
    (1 - df['visit_compliance']) * 0.25 +
    df['protocol_deviations'] / 10 * 0.20 +
    (np.abs(df['current_hemoglobin'] - df['baseline_hemoglobin']) / 5) * 0.15 +
    (np.abs(df['current_alt'] - df['baseline_alt']) / 100) * 0.15
)

# Prédiction dropout simple (baseline pour comparaison)
df['dropout_prediction_simple'] = (df['risk_score'] > 0.4).astype(int)

# Sélectionner colonnes pertinentes
output_columns = [
    'patient_id', 'site_name', 'age', 'gender', 'enrollment_date',
    'baseline_hemoglobin', 'baseline_alt', 'baseline_creatinine',
    'current_hemoglobin', 'current_alt', 'current_creatinine',
    'visit_compliance', 'query_rate', 'data_entry_delay_days',
    'protocol_deviations', 'tmf_completeness_%', 'query_resolution_time_days',
    'days_since_enrollment', 'risk_score', 'is_dropout', 'is_anomaly',
    'dropout_prediction_simple'
]

df_final = df[output_columns].copy()
df_final = df_final.round(3)

# Sauvegarder
df_final.to_csv('clinical_data_realistic_test.csv', index=False)

print("✅ Dataset généré: clinical_data_realistic_test.csv")
print(f"   - {len(df_final)} patients")
print(f"   - {len(df_final.columns)} features")
print(f"   - {df_final['is_dropout'].sum()} dropouts ({df_final['is_dropout'].mean()*100:.1f}%)")
print(f"   - {df_final['is_anomaly'].sum()} anomalies détectées")
print("\nStatistiques par site:")
print(df_final.groupby('site_name')[['is_dropout', 'is_anomaly', 'risk_score']].agg({
    'is_dropout': ['sum', 'mean'],
    'is_anomaly': 'sum',
    'risk_score': 'mean'
}).round(3))

# Afficher aperçu
print("\n📊 Aperçu données:")
print(df_final.head(10))

# Export statistiques
print(f"\n📈 Corrélations avec dropout:")
for col in ['query_rate', 'visit_compliance', 'protocol_deviations', 'risk_score']:
    corr = df_final[col].corr(df_final['is_dropout'])
    print(f"   {col}: {corr:.3f}")