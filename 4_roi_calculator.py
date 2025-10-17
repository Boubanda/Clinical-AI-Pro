"""
Calculateur de ROI pour la plateforme Clinical Intelligence
Calcule les économies et le retour sur investissement
Auteur: Lévi Junior BOUBANDA
"""
import pandas as pd
import numpy as np
from datetime import datetime

print("💰 CALCUL DU RETOUR SUR INVESTISSEMENT (ROI)")
print("="*60)

# Charger les données
df = pd.read_csv('clinical_predictions.csv')
sites = pd.read_csv('site_performance.csv')

# ============= PARAMÈTRES FINANCIERS =============
# Coûts unitaires (en euros)
COSTS = {
    'patient_monitoring_manual': 500,      # Par patient par mois
    'patient_monitoring_ai': 150,          # Avec IA
    'dropout_cost': 75000,                 # Coût d'un patient perdu
    'protocol_deviation_cost': 25000,      # Par déviation
    'audit_finding_cost': 100000,          # Par finding majeur
    'query_resolution_manual': 50,         # Par query
    'query_resolution_ai': 10,             # Avec IA
    'implementation_cost': 100000,         # Coût initial IA
    'monthly_maintenance': 5000            # Maintenance mensuelle
}

# ============= CALCULS ÉCONOMIES =============
print("\n📊 ANALYSE DES ÉCONOMIES")
print("-" * 50)

n_patients = len(df)
n_sites = len(sites)
study_duration_months = 12

# 1. Économies sur le monitoring
monitoring_savings = (COSTS['patient_monitoring_manual'] - COSTS['patient_monitoring_ai']) * n_patients * study_duration_months
print(f"💵 Économies monitoring: €{monitoring_savings:,.0f}")

# 2. Dropouts évités
current_dropout_rate = df['dropout_prediction'].mean()
baseline_dropout_rate = 0.18  # Taux historique sans IA
dropouts_prevented = int(n_patients * (baseline_dropout_rate - current_dropout_rate))
dropout_savings = dropouts_prevented * COSTS['dropout_cost']
print(f"👥 Dropouts évités: {dropouts_prevented} patients")
print(f"💵 Économies dropouts: €{dropout_savings:,.0f}")

# 3. Déviations protocolaires évitées
deviations_with_ai = df['protocol_deviation'].sum()
deviations_baseline = int(deviations_with_ai * 1.5)  # 50% de plus sans IA
deviations_prevented = deviations_baseline - deviations_with_ai
deviation_savings = deviations_prevented * COSTS['protocol_deviation_cost']
print(f"📋 Déviations évitées: {deviations_prevented}")
print(f"💵 Économies déviations: €{deviation_savings:,.0f}")

# 4. Queries réduites
total_queries = int(df['query_rate'].sum() * 100)
query_savings = total_queries * (COSTS['query_resolution_manual'] - COSTS['query_resolution_ai'])
print(f"📝 Queries traitées par IA: {total_queries}")
print(f"💵 Économies queries: €{query_savings:,.0f}")

# 5. Audit findings évités
anomalies_caught = (df['is_anomaly'] == 'Anomalie').sum()
potential_findings_prevented = max(1, anomalies_caught // 10)  # 1 finding pour 10 anomalies
audit_savings = potential_findings_prevented * COSTS['audit_finding_cost']
print(f"🔍 Findings évités: {potential_findings_prevented}")
print(f"💵 Économies audit: €{audit_savings:,.0f}")

# ============= CALCUL ROI TOTAL =============
print("\n💰 RÉSUMÉ FINANCIER")
print("-" * 50)

# Économies totales
total_savings = (monitoring_savings + dropout_savings + 
                deviation_savings + query_savings + audit_savings)

# Coûts totaux
total_costs = COSTS['implementation_cost'] + (COSTS['monthly_maintenance'] * study_duration_months)

# ROI net
net_savings = total_savings - total_costs
roi_percentage = (net_savings / total_costs) * 100
payback_months = total_costs / (total_savings / study_duration_months) if total_savings > 0 else float('inf')

print(f"✅ Économies totales: €{total_savings:,.0f}")
print(f"💸 Coûts totaux: €{total_costs:,.0f}")
print(f"💎 Économies nettes: €{net_savings:,.0f}")
print(f"📈 ROI: {roi_percentage:.0f}%")
print(f"⏱️  Retour sur investissement: {payback_months:.1f} mois")

# ============= PROJECTION 3 ANS =============
print("\n📊 PROJECTION SUR 3 ANS")
print("-" * 50)

years = [1, 2, 3]
projections = []

for year in years:
    annual_savings = total_savings * year
    annual_costs = COSTS['implementation_cost'] + (COSTS['monthly_maintenance'] * 12 * year)
    net = annual_savings - annual_costs
    projections.append({
        'Année': year,
        'Économies': annual_savings,
        'Coûts': annual_costs,
        'Net': net,
        'ROI': (net / annual_costs * 100) if annual_costs > 0 else 0
    })

projection_df = pd.DataFrame(projections)
print(projection_df.to_string(index=False))

# ============= BREAKDOWN PAR SITE =============
print("\n🏥 IMPACT PAR SITE")
print("-" * 50)

for _, site in sites.iterrows():
    site_patients = df[df['site_id'] == site['site_id']].shape[0]
    site_savings = (site_patients / n_patients) * total_savings
    print(f"{site['site_id']}: €{site_savings:,.0f} ({site['performance']})")

# ============= EXPORT RAPPORT ROI =============
roi_report = {
    'date': datetime.now().strftime('%Y-%m-%d'),
    'total_patients': n_patients,
    'total_sites': n_sites,
    'study_duration_months': study_duration_months,
    'total_savings': total_savings,
    'total_costs': total_costs,
    'net_savings': net_savings,
    'roi_percentage': roi_percentage,
    'payback_months': payback_months,
    'dropouts_prevented': dropouts_prevented,
    'deviations_prevented': deviations_prevented,
    'findings_prevented': potential_findings_prevented
}

roi_df = pd.DataFrame([roi_report])
roi_df.to_csv('roi_report.csv', index=False)

print("\n" + "="*60)
print("✅ ANALYSE ROI TERMINÉE")
print("="*60)
print(f"""
💎 RÉSULTAT FINAL:
   • ROI: {roi_percentage:.0f}%
   • Économies nettes annuelles: €{net_savings:,.0f}
   • Temps de retour: {payback_months:.1f} mois
   • Impact qualité: +{(1-current_dropout_rate/baseline_dropout_rate)*100:.0f}%
   
📄 Rapport exporté: roi_report.csv
""")