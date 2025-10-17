"""
Configuration métier pour l'environnement clinique
Paramètres réglementaires FDA/EMA et seuils critiques
Auteur: Lévi Junior BOUBANDA
"""

# ============= CONFIGURATION RÉGLEMENTAIRE =============

# Seuils FDA/EMA
REGULATORY_THRESHOLDS = {
    'query_rate_max': 0.20,              # Maximum 20% acceptable
    'dropout_rate_target': 0.10,         # Cible <10% dropout
    'tmf_completeness_min': 80,          # Minimum 80% pour audit
    'data_entry_delay_max': 5,           # Maximum 5 jours
    'protocol_deviation_critical': 3,    # >3 déviations = critique
    'sdv_coverage_min': 0.10,           # Minimum 10% SDV
    'monitoring_frequency_days': 30      # Visite monitoring mensuelle
}

# ============= SCORING & POIDS =============

# Poids pour le calcul du score de risque
RISK_WEIGHTS = {
    'query_rate': 0.30,
    'protocol_deviation': 0.35,
    'dropout_risk': 0.20,
    'data_delay': 0.15
}

# Catégories de risque
RISK_CATEGORIES = {
    'low': (0, 10),
    'medium': (10, 20),
    'high': (20, 100)
}

# ============= PARAMÈTRES FINANCIERS =============

# Coûts en euros
COST_PARAMETERS = {
    'cost_per_patient': 50000,
    'cost_per_dropout': 75000,
    'cost_per_audit_finding': 100000,
    'cost_per_protocol_deviation': 25000,
    'cost_per_query': 50,
    'monitor_hourly_rate': 150,
    'savings_per_automated_check': 500,
    'ai_implementation_cost': 100000,
    'ai_monthly_maintenance': 5000
}

# ============= MESSAGES & ALERTES =============

# Messages de conformité
COMPLIANCE_MESSAGES = {
    'high_risk': {
        'level': 'CRITICAL',
        'icon': '🔴',
        'message': "Site non-conforme aux standards ICH-GCP. Action immédiate requise.",
        'action': "Déclencher plan de remédiation sous 24h"
    },
    'medium_risk': {
        'level': 'WARNING',
        'icon': '⚠️',
        'message': "Risque de non-conformité détecté. Surveillance renforcée nécessaire.",
        'action': "Plan d'action sous 48h"
    },
    'low_risk': {
        'level': 'OK',
        'icon': '✅',
        'message': "Site conforme. Maintenir la surveillance standard.",
        'action': "Monitoring de routine"
    }
}

# Templates d'alertes email
EMAIL_TEMPLATES = {
    'critical_anomaly': {
        'subject': "⚠️ URGENT: Anomalie Critique Détectée - Patient {patient_id}",
        'body': """
        Une anomalie critique a été détectée nécessitant une action immédiate.
        
        Patient: {patient_id}
        Site: {site_name}
        Type: {anomaly_type}
        Valeurs: {values}
        
        Action requise: Revue clinique immédiate
        Délai: Sous 24 heures
        """
    },
    'high_dropout_risk': {
        'subject': "📊 Alerte: Risque élevé de dropout - {n_patients} patients",
        'body': """
        Le système IA a identifié {n_patients} patients à haut risque de dropout.
        
        Sites concernés: {sites}
        Probabilité moyenne: {avg_probability:.1%}
        
        Recommandation: Activer le protocole de rétention patient
        """
    }
}

# ============= CONFIGURATION SITES =============

# Mapping des sites et leurs caractéristiques
SITE_CONFIGURATION = {
    'FR-PAR-001': {
        'name': 'Hôpital Pitié-Salpêtrière',
        'country': 'France',
        'timezone': 'Europe/Paris',
        'language': 'fr',
        'regulatory_body': 'ANSM'
    },
    'FR-LYO-002': {
        'name': 'Hôpital Lyon Sud',
        'country': 'France',
        'timezone': 'Europe/Paris',
        'language': 'fr',
        'regulatory_body': 'ANSM'
    },
    'FR-MAR-003': {
        'name': 'CHU Marseille',
        'country': 'France',
        'timezone': 'Europe/Paris',
        'language': 'fr',
        'regulatory_body': 'ANSM'
    },
    'BE-BRU-004': {
        'name': 'UZ Brussel',
        'country': 'Belgium',
        'timezone': 'Europe/Brussels',
        'language': 'nl',
        'regulatory_body': 'FAMHP'
    },
    'CH-GEN-005': {
        'name': 'HUG Genève',
        'country': 'Switzerland',
        'timezone': 'Europe/Zurich',
        'language': 'fr',
        'regulatory_body': 'Swissmedic'
    }
}

# ============= PARAMÈTRES ML =============

# Configuration des modèles
ML_CONFIGURATION = {
    'dropout_model': {
        'type': 'RandomForest',
        'n_estimators': 100,
        'max_depth': 5,
        'threshold': 0.7,
        'features': ['age', 'data_entry_delay_days', 'query_rate', 
                    'days_since_last_visit', 'tmf_completeness_%']
    },
    'anomaly_model': {
        'type': 'IsolationForest',
        'contamination': 0.05,
        'features': ['lab_hemoglobin', 'lab_creatinine', 'lab_alt',
                    'query_rate', 'data_entry_delay_days']
    },
    'clustering_model': {
        'type': 'KMeans',
        'n_clusters': 3,
        'features': ['query_rate', 'tmf_completeness_%', 
                    'protocol_deviation', 'data_entry_delay_days']
    }
}

# ============= EXPORTS & FORMATS =============

# Configuration des exports
EXPORT_CONFIGURATION = {
    'date_format': '%Y-%m-%d',
    'datetime_format': '%Y-%m-%d %H:%M:%S',
    'decimal_places': 2,
    'encoding': 'utf-8',
    'csv_separator': ',',
    'report_formats': ['html', 'pdf', 'csv', 'excel']
}

# ============= VALIDATION RULES =============

# Règles de validation des données
VALIDATION_RULES = {
    'lab_hemoglobin': {'min': 7.0, 'max': 18.0, 'unit': 'g/dL'},
    'lab_creatinine': {'min': 0.5, 'max': 2.0, 'unit': 'mg/dL'},
    'lab_alt': {'min': 10, 'max': 100, 'unit': 'U/L'},
    'age': {'min': 18, 'max': 85, 'unit': 'years'},
    'tmf_completeness_%': {'min': 0, 'max': 100, 'unit': '%'},
    'query_rate': {'min': 0, 'max': 1, 'unit': 'ratio'}
}

# ============= FONCTIONS UTILITAIRES =============

def get_risk_level(score):
    """Détermine le niveau de risque basé sur le score"""
    if score < RISK_CATEGORIES['low'][1]:
        return 'low'
    elif score < RISK_CATEGORIES['medium'][1]:
        return 'medium'
    else:
        return 'high'

def get_compliance_message(risk_level):
    """Retourne le message de conformité approprié"""
    return COMPLIANCE_MESSAGES.get(risk_level + '_risk', COMPLIANCE_MESSAGES['low_risk'])

def validate_lab_value(param, value):
    """Valide une valeur laboratoire"""
    rules = VALIDATION_RULES.get(param, {})
    if not rules:
        return True
    return rules['min'] <= value <= rules['max']

# ============= CONFIGURATION API =============

# Endpoints pour intégration future
API_ENDPOINTS = {
    'edc_system': 'https://api.edc-system.com/v1/',
    'ctms_system': 'https://api.ctms-system.com/v2/',
    'etmf_system': 'https://api.etmf-system.com/v1/',
    'central_monitoring': 'https://api.monitoring.com/v3/'
}

print("✅ Configuration clinique chargée avec succès")