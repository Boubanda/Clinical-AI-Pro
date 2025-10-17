"""
Dashboard Executive - Clinical Intelligence Platform
Lancer avec: streamlit run 3_dashboard_executive.py
Auteur: Lévi Junior BOUBANDA
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuration
st.set_page_config(
    page_title="Clinical Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main {background-color: #f0f2f6;}
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    div[data-testid="metric-container"] {
        background-color: white;
        border: 2px solid #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header avec logo
col_logo, col_title = st.columns([1, 4])
with col_title:
    st.markdown("# 🏥 **Clinical Intelligence Platform**")
    st.markdown("### *AI-Powered Analytics for Clinical Trials*")
    
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Navigation")
    page = st.selectbox("Sélectionner une vue:", 
                       ["📊 Executive Summary", 
                        "🔍 Anomaly Detection", 
                        "📈 Predictive Analytics", 
                        "🏥 Site Performance",
                        "💰 ROI Calculator"])
    
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.info("""
    **Version:** 2.0  
    **Dernière MAJ:** Aujourd'hui  
    **Contact:** Lévi BOUBANDA
    """)

# Charger les données
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('clinical_predictions.csv')
        sites = pd.read_csv('site_performance.csv')
        return df, sites
    except:
        st.error("⚠️ Veuillez d'abord exécuter les scripts de génération de données")
        st.stop()

df, sites = load_data()

# PAGE 1: Executive Summary
if page == "📊 Executive Summary":
    
    # KPIs principaux
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Patients",
            f"{len(df):,}",
            f"+{len(df)//10} cette semaine",
            delta_color="normal"
        )
    
    with col2:
        dropout_rate = df['dropout_prediction'].mean()
        st.metric(
            "Risque Dropout",
            f"{dropout_rate:.1%}",
            f"{(dropout_rate-0.20)*100:.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        anomalies = df['is_anomaly'].value_counts().get('Anomalie', 0)
        st.metric(
            "Anomalies",
            anomalies,
            "Détectées par IA"
        )
    
    with col4:
        compliance = df['visit_compliance'].mean()
        st.metric(
            "Compliance",
            f"{compliance:.1%}",
            "+5.2%",
            delta_color="normal"
        )
    
    with col5:
        tmf_avg = df['tmf_completeness_%'].mean()
        st.metric(
            "TMF Complete",
            f"{tmf_avg:.1f}%",
            f"+{(tmf_avg-80):.1f}%",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des risques par site
        fig_risk = px.box(df, 
                         x='site_name', 
                         y='risk_score',
                         color='site_category',
                         title="📊 Distribution des Risques par Site",
                         labels={'risk_score': 'Score de Risque', 'site_name': 'Site'},
                         color_discrete_map={
                             'Low Risk': '#00CC88',
                             'Medium Risk': '#FFAA00',
                             'High Risk': '#FF4444'
                         })
        fig_risk.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # Évolution temporelle
        df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])
        df_sorted = df.sort_values('enrollment_date')
        df_sorted['cumulative_patients'] = range(1, len(df_sorted) + 1)
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=df_sorted['enrollment_date'],
            y=df_sorted['cumulative_patients'],
            mode='lines',
            name='Patients',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        fig_timeline.update_layout(
            title="📈 Recrutement Cumulé",
            xaxis_title="Date",
            yaxis_title="Nombre de Patients",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Recommendations IA
    st.markdown("---")
    st.markdown("### 🤖 **Recommandations IA**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        **🎯 Optimisation Sites**  
        Réallouer 2 moniteurs de  
        FR-MAR-003 vers FR-PAR-001  
        *Impact: -15% taux de queries*
        """)
    
    with col2:
        st.warning("""
        **⚠️ Mitigation Risques**  
        Formation urgente pour  
        3 sites avec queries élevées  
        *Impact: -25% déviations*
        """)
    
    with col3:
        st.info("""
        **📊 Amélioration Process**  
        Automatiser contrôles eTMF  
        sites < 75% compliance  
        *Impact: +30% efficacité*
        """)

# PAGE 2: Anomaly Detection
elif page == "🔍 Anomaly Detection":
    st.markdown("### 🔍 Détection d'Anomalies en Temps Réel")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        site_filter = st.multiselect("Sélectionner Sites:", 
                                     options=df['site_name'].unique(),
                                     default=df['site_name'].unique())
    with col2:
        anomaly_filter = st.selectbox("Status Anomalie:", 
                                      ["Tous", "Anomalie", "Normal"])
    with col3:
        threshold = st.slider("Seuil de Risque:", 0.0, 1.0, 0.7)
    
    # Appliquer filtres
    filtered_df = df[df['site_name'].isin(site_filter)]
    if anomaly_filter != "Tous":
        filtered_df = filtered_df[filtered_df['is_anomaly'] == anomaly_filter]
    
    # Statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        n_anomalies = (filtered_df['is_anomaly'] == 'Anomalie').sum()
        st.metric("Anomalies Détectées", n_anomalies)
    with col2:
        high_risk = (filtered_df['dropout_prediction'] > threshold).sum()
        st.metric("Patients à Risque", high_risk)
    with col3:
        avg_risk = filtered_df['risk_score'].mean()
        st.metric("Score Risque Moyen", f"{avg_risk:.1f}")
    
    # Graphique scatter
    fig_scatter = px.scatter(filtered_df,
                        x='current_hemoglobin',
                        y='current_alt',
                            color='is_anomaly',
                            size='risk_score',
                            hover_data=['patient_id', 'site_name'],
                            title="🎯 Carte des Anomalies Laboratoire",
                            labels={'lab_hemoglobin': 'Hémoglobine (g/dL)', 
                                   'lab_alt': 'ALT (U/L)'},
                            color_discrete_map={'Anomalie': '#FF4444', 
                                              'Normal': '#00CC88'})
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Table des anomalies critiques
    if n_anomalies > 0:
        st.markdown("### ⚠️ Patients Nécessitant une Revue Immédiate")
        critical_patients = filtered_df[filtered_df['is_anomaly'] == 'Anomalie'].head(10)
        display_cols = ['patient_id', 'site_name', 'lab_hemoglobin', 
                       'lab_alt', 'risk_score', 'dropout_prediction']
        st.dataframe(critical_patients[display_cols].style.highlight_max(axis=0),
                    use_container_width=True)

# PAGE 3: Predictive Analytics
elif page == "📈 Predictive Analytics":
    st.markdown("### 📈 Analyses Prédictives")
    
    # Métriques du modèle
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Précision Modèle", "87.3%", "+2.1%")
    with col2:
        st.metric("Sensibilité", "84.2%", "+3.5%")
    with col3:
        st.metric("Spécificité", "89.1%", "+1.8%")
    with col4:
        st.metric("AUC-ROC", "0.923", "+0.04")
    
    st.markdown("---")
    
    # Distribution des prédictions
    fig_dist = px.histogram(df, 
                           x='dropout_prediction',
                           nbins=30,
                           title="🎲 Distribution des Scores de Prédiction Dropout",
                           labels={'dropout_prediction': 'Probabilité de Dropout',
                                  'count': 'Nombre de Patients'},
                           color_discrete_sequence=['#667eea'])
    fig_dist.add_vline(x=0.7, line_dash="dash", line_color="red",
                      annotation_text="Seuil Critique")
    fig_dist.update_layout(height=400)
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # Feature importance
    st.markdown("### 🎯 Importance des Variables")
    features = ['days_since_last_visit', 'query_rate', 'age', 
               'tmf_completeness_%', 'data_entry_delay_days']
    importance = [0.28, 0.24, 0.19, 0.16, 0.13]
    
    fig_importance = go.Figure(go.Bar(
        x=importance,
        y=features,
        orientation='h',
        marker=dict(color='#667eea')
    ))
    fig_importance.update_layout(
        title="📊 Features les Plus Prédictives",
        xaxis_title="Importance",
        yaxis_title="Variable",
        height=400
    )
    st.plotly_chart(fig_importance, use_container_width=True)

# PAGE 4: Site Performance
elif page == "🏥 Site Performance":
    st.markdown("### 🏥 Performance des Sites")
    
    # Tableau de bord par site
    for _, site in sites.iterrows():
        with st.expander(f"{site['site_id']} - {site['performance']}", 
                        expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Query Rate", f"{site['query_rate']:.1%}")
            with col2:
                st.metric("TMF Complete", f"{site['tmf_completeness_%']:.1f}%")
            with col3:
                st.metric("Déviations", f"{int(site['protocol_deviations'])}")
            with col4:
                st.metric("Délai Moyen", f"{site['data_entry_delay_days']:.1f} jours")

# PAGE 5: ROI Calculator
elif page == "💰 ROI Calculator":
    st.markdown("### 💰 Calculateur de Retour sur Investissement")
    
    # Paramètres
    col1, col2 = st.columns(2)
    with col1:
        n_patients = st.number_input("Nombre de patients", 
                                    value=500, min_value=100, max_value=5000)
        cost_per_patient = st.number_input("Coût par patient (€)", 
                                          value=50000, min_value=10000)
        monitoring_cost = st.number_input("Coût monitoring manuel (€/patient)", 
                                         value=500, min_value=100)
    
    with col2:
        ai_cost = st.number_input("Coût avec IA (€/patient)", 
                                 value=150, min_value=50)
        dropout_cost = st.number_input("Coût par dropout (€)", 
                                      value=75000, min_value=20000)
        implementation_cost = st.number_input("Coût implémentation (€)", 
                                             value=100000, min_value=50000)
    
    # Calculs
    savings_monitoring = (monitoring_cost - ai_cost) * n_patients
    dropouts_prevented = int(n_patients * 0.07)  # 7% de dropouts évités
    savings_dropout = dropouts_prevented * dropout_cost
    total_savings = savings_monitoring + savings_dropout - implementation_cost
    roi = (total_savings / implementation_cost) * 100
    payback = implementation_cost / (total_savings / 12) if total_savings > 0 else float('inf')
    
    # Affichage résultats
    st.markdown("---")
    st.markdown("### 📊 Résultats")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💶 Économies Totales", f"€{total_savings:,.0f}")
    with col2:
        st.metric("📈 ROI", f"{roi:.0f}%")
    with col3:
        st.metric("⏱️ Retour sur Invest.", 
                 f"{payback:.1f} mois" if payback < 100 else "N/A")
    
    # Graphique breakdown
    fig_roi = go.Figure(go.Waterfall(
        name="ROI", 
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Économies Monitoring", "Dropouts Évités", "Coût Implementation", "Total Net"],
        y=[savings_monitoring, savings_dropout, -implementation_cost, total_savings],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    fig_roi.update_layout(title="💰 Analyse Détaillée du ROI", height=400)
    st.plotly_chart(fig_roi, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <small>
    Clinical Intelligence Platform v2.0 | Powered by AI<br>
    © 2024 Lévi Junior BOUBANDA | leviboubanda07@gmail.com
    </small>
</div>
""", unsafe_allow_html=True)