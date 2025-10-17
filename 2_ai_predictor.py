"""
Suite IA avancée pour prédiction clinique - VERSION FINALE
Utilise XGBoost pour capturer les patterns cliniques
Sortie optimisée pour dashboard Streamlit
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

print("🤖 Lancement de la suite IA Clinical Analytics...")
print("="*60)

# Charger données
df = pd.read_csv('clinical_data_realistic_test.csv')
print(f"📊 Données chargées: {len(df)} patients\n")

# ============= MODÈLE 1: PRÉDICTION DROPOUT =============
print("📊 MODÈLE 1: Prédiction risque d'abandon patient (XGBoost)")
print("-" * 50)

# Features pour prédiction
features_dropout = ['age', 'data_entry_delay_days', 'query_rate', 
                   'visit_compliance', 'protocol_deviations', 'risk_score']
X = df[features_dropout].copy()
y = df['is_dropout'].astype(int)

print(f"📈 Distribution dropout: {y.sum()} positifs / {len(y)} total ({y.mean()*100:.1f}%)")

# Division train/test (stratifié pour équilibrer)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# XGBoost Model
xgb_model = XGBClassifier(
    n_estimators=150,
    max_depth=6,
    learning_rate=0.05,
    random_state=42,
    eval_metric='logloss'
)
xgb_model.fit(X_train, y_train, verbose=False)

# Prédictions
y_pred = xgb_model.predict(X_test)
y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]
df['dropout_prediction'] = xgb_model.predict_proba(X)[:, 1]

# Métriques
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
auc_score = roc_auc_score(y_test, y_pred_proba)

high_risk_patients = (df['dropout_prediction'] > 0.6).sum()
very_high_risk = (df['dropout_prediction'] > 0.8).sum()

print(f"⚠️  Patients à risque moyen (>0.6): {high_risk_patients}")
print(f"🔴 Patients à très haut risque (>0.8): {very_high_risk}")
print(f"\n📊 Métriques modèle:")
print(f"   Accuracy: {accuracy:.1%} | Precision: {precision:.1%} | Recall: {recall:.1%}")
print(f"   AUC-ROC: {auc_score:.3f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': features_dropout,
    'importance': xgb_model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n🎯 Features les plus prédictives:")
for idx, row in feature_importance.head(3).iterrows():
    print(f"   {idx+1}. {row['feature']}: {row['importance']:.3f}")

# ============= MODÈLE 2: DÉTECTION ANOMALIES =============
print("\n🔍 MODÈLE 2: Détection d'anomalies multicritères")
print("-" * 50)

# Features pour anomalies
features_anomaly = ['current_hemoglobin', 'current_creatinine', 'current_alt', 
                   'query_rate', 'data_entry_delay_days', 'protocol_deviations']
X_anomaly = df[features_anomaly].copy()

# Normalisation
scaler = StandardScaler()
X_anomaly_scaled = scaler.fit_transform(X_anomaly)

# Isolation Forest
iso_model = IsolationForest(contamination=0.05, random_state=42)
df['anomaly_flag'] = iso_model.fit_predict(X_anomaly_scaled)
df['anomaly_detected'] = df['anomaly_flag'].apply(lambda x: 'Anomalie' if x == -1 else 'Normal')

n_anomalies = (df['anomaly_flag'] == -1).sum()
print(f"🚨 Anomalies détectées: {n_anomalies} patients ({n_anomalies/len(df)*100:.1f}%)")

# Analyse par site
print(f"\n📍 Répartition anomalies par site:")
anomaly_by_site = df[df['anomaly_flag'] == -1].groupby('site_name').size().sort_values(ascending=False)
for site, count in anomaly_by_site.items():
    site_total = len(df[df['site_name'] == site])
    pct = count / site_total * 100
    print(f"   {site}: {count} anomalies ({pct:.1f}% du site)")

# ============= MODÈLE 3: CLUSTERING SITES =============
print("\n🎯 MODÈLE 3: Segmentation intelligente des sites")
print("-" * 50)

# Agrégation par site
site_metrics = df.groupby('site_name').agg({
    'query_rate': 'mean',
    'tmf_completeness_%': 'mean',
    'protocol_deviations': 'sum',
    'data_entry_delay_days': 'mean',
    'dropout_prediction': 'mean',
    'is_dropout': 'mean',
    'visit_compliance': 'mean'
}).reset_index()

site_metrics['n_patients'] = df.groupby('site_name').size().values
site_metrics = site_metrics.rename(columns={'site_name': 'site_id'})

# Normalisation pour clustering
X_cluster = scaler.fit_transform(site_metrics.iloc[:, 1:].select_dtypes(np.number))

# K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
site_metrics['cluster'] = kmeans.fit_predict(X_cluster)

# Mapping basé sur performance
cluster_perf = site_metrics.groupby('cluster')['tmf_completeness_%'].mean().sort_values(ascending=False)
cluster_map = {
    cluster_perf.index[0]: '⭐ Top Performer',
    cluster_perf.index[1]: '📊 Standard',
    cluster_perf.index[2]: '⚠️ À Améliorer'
}
site_metrics['performance'] = site_metrics['cluster'].map(cluster_map)

print("📈 Classification des sites:")
for _, row in site_metrics.iterrows():
    print(f"\n   {row['site_id']}: {row['performance']}")
    print(f"      Patients: {row['n_patients']:.0f} | TMF: {row['tmf_completeness_%']:.1f}% | Dropout: {row['is_dropout']:.1%}")
    print(f"      Query rate: {row['query_rate']:.2%} | Compliance: {row['visit_compliance']:.1%}")

# ============= CALCUL MÉTRIQUES GLOBALES =============
print("\n📊 MÉTRIQUES GLOBALES")
print("-" * 50)

total_deviations = df['protocol_deviations'].sum()
avg_query_rate = df['query_rate'].mean()
compliance_rate = df['visit_compliance'].mean()
total_dropouts = df['is_dropout'].sum()
dropout_pct = (total_dropouts / len(df)) * 100

print(f"📋 Déviations protocolaires totales: {total_deviations:.0f}")
print(f"📝 Taux de queries moyen: {avg_query_rate:.2%}")
print(f"✅ Taux de compliance moyen: {compliance_rate:.1%}")
print(f"🚨 Dropouts observés: {total_dropouts} / {len(df)} ({dropout_pct:.1f}%)")

# ============= PRÉPARATION POUR LE DASHBOARD =============
# Ajouter colonne site_category pour le dashboard
df['site_category'] = 'Center'

# Ajouter des colonnes de résumé utiles
df['dropout_risk_level'] = df['dropout_prediction'].apply(
    lambda x: 'Très Haut Risque' if x > 0.8 else ('Haut Risque' if x > 0.6 else 'Risque Modéré' if x > 0.4 else 'Bas Risque'))

# ============= EXPORT RÉSULTATS =============
df.to_csv('clinical_predictions.csv', index=False)
site_metrics.to_csv('site_performance.csv', index=False)

print(f"\n✅ Fichiers sauvegardés:")
print(f"   • clinical_predictions.csv ({len(df)} lignes)")
print(f"   • site_performance.csv ({len(site_metrics)} sites)")

print("\n" + "="*60)
print("✅ ANALYSE IA TERMINÉE")
print("="*60)
print(f"""
📊 Résumé exécutif:
   • Patients analysés: {len(df)}
   • Modèles entraînés: 3 (XGBoost + IsolationForest + K-Means)
   • Accuracy dropout: {accuracy:.1%}
   • AUC-ROC: {auc_score:.3f}
   • Anomalies détectées: {n_anomalies}
   • Sites à améliorer: {(site_metrics['performance'] == '⚠️ À Améliorer').sum()}
   
💡 Prochaine étape: streamlit run 3_dashboard_executive.py
""")