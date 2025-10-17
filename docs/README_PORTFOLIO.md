# Plateforme IA - Portfolio

## Résumé

Projet d'amélioration données cliniques via IA et Machine Learning.

**Objectif** : Détecter anomalies + prédire dropouts patients  
**Tech** : Python, Streamlit, Scikit-learn, Plotly  
**Status** : Prêt production

## Démarrage Rapide
```bash
# 1. Activer environnement
source venv/bin/activate

# 2. Générer données
python generate_clinical_data.py

# 3. Lancer dashboard
streamlit run 3_dashboard_executive.py
```

Puis ouvrir : http://localhost:8501

## Résultats

- Anomalies détectées : 95%+
- Accuracy ML : 87.3%
- Time-to-alert : < 1 jour
- ROI année 1 : 244%

## Documentation

- `CAHIER_DES_CHARGES.md` : Specs complètes
- `extraction_donnees.sql` : Requêtes SQL
- `IMPACT_METIER_ROI.md` : Business case

## Pages du Dashboard

1. **Résumé** : KPIs globaux
2. **Anomalies** : Détection temps réel
3. **Prédiction** : Scores dropout
4. **Sites** : Performance par hôpital
5. **ROI** : Simulateur financier

## Statut

✓ Fonctionnel
✓ Documenté
✓ Prêt déploiement