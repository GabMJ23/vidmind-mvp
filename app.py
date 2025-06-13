import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="VidMind - AI for Content Creators",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS simplifié et corrigé
st.markdown("""
<style>
    .main {
        background: #000000;
        color: white;
        padding: 0;
    }
    
    .stApp {
        background: #000000;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .main-interface {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        min-height: 800px;
        max-width: 900px;
        margin: 0 auto;
        padding: 60px 40px 40px 40px;
    }
    
    .logo {
        font-size: 52px;
        font-weight: 200;
        letter-spacing: 18px;
        color: #FFD700;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .tagline {
        font-size: 19px;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 50px;
        letter-spacing: 2px;
    }
    
    .conversation-area {
        width: 100%;
        max-width: 800px;
        margin-bottom: 30px;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        gap: 25px;
        padding: 0 20px;
    }
    
    .user-message {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 22px 22px 6px 22px;
        padding: 18px 24px;
        margin-left: 15%;
        font-size: 16px;
        line-height: 1.5;
        animation: slideInRight 0.3s ease-out;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    }
    
    .ai-message {
        background: transparent;
        padding: 24px 0;
        margin-right: 8%;
        font-size: 16px;
        line-height: 1.7;
        color: rgba(255, 255, 255, 0.95);
        animation: slideInLeft 0.3s ease-out;
        border-left: 3px solid rgba(255, 215, 0, 0.4);
        padding-left: 24px;
    }
    
    .ai-label {
        font-size: 11px;
        color: #FFD700;
        font-weight: 600;
        margin-bottom: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .video-selector {
        width: 100%;
        margin-bottom: 35px;
        text-align: center;
    }
    
    .video-pills {
        display: flex;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        margin-top: 20px;
    }
    
    .video-pill {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 12px 20px;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
        cursor: pointer;
        transition: all 0.3s ease;
        white-space: nowrap;
        position: relative;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .video-pill::before {
        content: '';
        width: 20px;
        height: 12px;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.3), rgba(255, 255, 255, 0.1));
        border: 1px solid rgba(255, 215, 0, 0.4);
        border-radius: 3px;
        position: relative;
        flex-shrink: 0;
    }
    
    .video-pill::after {
        content: '▶';
        position: absolute;
        left: 16px;
        font-size: 8px;
        color: rgba(255, 215, 0, 0.6);
    }
    
    .video-pill:hover {
        background: rgba(255, 215, 0, 0.12);
        border-color: rgba(255, 215, 0, 0.4);
        color: #FFD700;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.15);
    }
    
    .video-pill.active {
        background: rgba(255, 215, 0, 0.18);
        border-color: #FFD700;
        color: #FFD700;
        box-shadow: 0 4px 16px rgba(255, 215, 0, 0.2);
    }
    
    .options-section {
        width: 100%;
        max-width: 800px;
        margin-bottom: 25px;
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .input-zone {
        width: 100%;
        max-width: 800px;
        position: relative;
        margin-bottom: 20px;
    }
    
    .main-input {
        width: 100%;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 28px;
        padding: 18px 70px 18px 28px;
        font-size: 16px;
        color: white;
        outline: none;
        transition: all 0.3s ease;
        font-family: inherit;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    }
    
    .main-input:focus {
        border-color: rgba(255, 215, 0, 0.6);
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.1), 0 4px 20px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.06);
    }
    
    .main-input::placeholder {
        color: rgba(255, 255, 255, 0.45);
        font-weight: 300;
    }
    
    .upload-zone {
        width: 100%;
        max-width: 800px;
        margin-bottom: 25px;
        padding: 20px;
        border: 2px dashed rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        text-align: center;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(5px);
        display: none;
    }
    
    .upload-zone.active {
        display: block;
        animation: fadeInUp 0.3s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .upload-zone:hover {
        border-color: rgba(255, 215, 0, 0.3);
        background: rgba(255, 215, 0, 0.02);
    }
    
    .suggestions {
        margin-top: 25px;
        text-align: center;
        max-width: 800px;
        width: 100%;
    }
    
    .suggestions-label {
        font-size: 13px;
        color: rgba(255, 255, 255, 0.5);
        margin-bottom: 18px;
        font-weight: 300;
    }
    
    .thinking-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        color: rgba(255, 215, 0, 0.8);
        font-size: 14px;
        margin: 20px 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .thinking-dots {
        display: flex;
        gap: 4px;
    }
    
    .thinking-dot {
        width: 4px;
        height: 4px;
        background: #FFD700;
        border-radius: 50%;
        animation: dotPulse 1.4s ease-in-out infinite both;
    }
    
    .thinking-dot:nth-child(1) { animation-delay: -0.32s; }
    .thinking-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    @keyframes dotPulse {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    .empty-state {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 17px;
        font-weight: 300;
        margin: 80px 0;
        line-height: 1.6;
        max-width: 600px;
    }
    
    .empty-state .icon {
        font-size: 56px;
        margin-bottom: 25px;
        display: block;
        opacity: 0.25;
    }
    
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stAppViewContainer > .main .block-container {padding-top: 0;}
    
    @media (max-width: 768px) {
        .logo {
            font-size: 40px;
            letter-spacing: 14px;
        }
        
        .main-interface {
            padding: 40px 20px 20px 20px;
        }
        
        .conversation-area {
            padding: 0 10px;
            min-height: 300px;
        }
        
        .user-message {
            margin-left: 8%;
            padding: 16px 20px;
        }
        
        .ai-message {
            margin-right: 5%;
            padding: 20px 0;
            padding-left: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Données simplifiées
@st.cache_data
def load_videos():
    return [
        {"id": 1, "title": "JavaScript Avancé", "short": "JS"},
        {"id": 2, "title": "React Hooks", "short": "React"},
        {"id": 3, "title": "CSS Grid", "short": "CSS"},
        {"id": 4, "title": "Vue d'ensemble", "short": "Général"}
    ]

def generate_smart_response(question, video_context):
    """Génère des réponses intelligentes selon le contexte"""
    
    q_lower = question.lower()
    
    # Réponses contextuelles par vidéo
    responses = {
        "JavaScript Avancé": {
            "sentiment": "📊 **Analyse JS Avancé** : 89% positif • Les développeurs adorent vos explications sur les closures et async/await • 3 questions techniques en attente",
            "questions": "❓ **Questions prioritaires** : 2 sur les closures, 1 sur les Promises • Niveau : Intermédiaire-Avancé • Réponse recommandée sous 24h",
            "améliorer": "🎯 **Suggestions** : Ajouter plus d'exemples pratiques • Créer une suite sur les design patterns • L'audience demande du TypeScript",
            "default": "🔍 **JS Avancé** : Excellente performance ! Votre audience maîtrise les bases et veut du contenu plus poussé. Les closures sont votre point fort."
        },
        "React Hooks": {
            "sentiment": "📊 **Analyse React** : 92% positif • Parfait pour les débutants • Demandes de contenu plus avancé en hausse",
            "questions": "❓ **Questions React** : 4 sur useState, 2 sur useEffect • Beaucoup de débutants • Opportunité de créer une série complète",
            "améliorer": "🎯 **React Next** : Hooks personnalisés très demandés • Context API à couvrir • Performance avec useMemo/useCallback",
            "default": "⚛️ **React Hooks** : Contenu parfait pour débuter ! Votre pédagogie est appréciée. Prêt pour du contenu avancé ?"
        },
        "CSS Grid": {
            "sentiment": "📊 **Analyse CSS** : 85% positif • Quelques confusions Flexbox/Grid • Contenu visuel très apprécié",
            "questions": "❓ **Questions CSS** : Surtout sur Flexbox vs Grid • Demandes d'exemples concrets • Responsive design populaire",
            "améliorer": "🎯 **CSS Future** : Flexbox vs Grid très demandé • CSS animations en demande • Modern CSS (subgrid, container queries)",
            "default": "🎨 **CSS Grid** : Bon engagement ! L'audience veut plus de comparaisons pratiques et d'exemples responsives."
        },
        "Général": {
            "sentiment": "📊 **Vue globale** : 89% satisfaction • 47% de votre audience revient régulièrement • Croissance +23% ce mois",
            "questions": "❓ **Tendances questions** : 40% JavaScript, 35% React, 25% CSS • Niveau intermédiaire dominant • +15% questions avancées",
            "améliorer": "🎯 **Stratégie globale** : Votre audience évolue vers l'avancé • TypeScript émergent • DevOps/outils de dev demandés",
            "default": "🚀 **Votre chaîne** : Croissance constante ! Audience fidèle qui progresse avec vous. Prête pour plus de défis techniques."
        }
    }
    
    video_responses = responses.get(video_context, responses["Général"])
    
    # Détection du type de question
    if "sentiment" in q_lower or "pensent" in q_lower or "avis" in q_lower:
        return video_responses["sentiment"]
    elif "question" in q_lower or "attente" in q_lower or "répondre" in q_lower:
        return video_responses["questions"]
    elif "améliorer" in q_lower or "conseil" in q_lower or "suggestions" in q_lower:
        return video_responses["améliorer"]
    elif "prochaine" in q_lower or "suite" in q_lower or "contenu" in q_lower:
        next_topics = ["TypeScript Fundamentals", "Testing avec Jest", "Node.js Avancé", "Performance Web", "GraphQL Basics"]
        topic = random.choice(next_topics)
        return f"🎯 **Prochaine vidéo recommandée** : **{topic}** • Basé sur 12+ demandes récurrentes • Potentiel viral élevé • Parfait timing pour votre audience"
    else:
        return video_responses["default"]

def main():
    # Interface principale ultra-épurée
    st.markdown('<div class="main-interface">', unsafe_allow_html=True)
    
    # Logo et tagline
    st.markdown("""
    <div class="logo">VIDMIND</div>
    <div class="tagline">L'intelligence de votre créativité</div>
    """, unsafe_allow_html=True)
    
    # Initialisation des states
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_video" not in st.session_state:
        st.session_state.selected_video = "Général"
    if "show_upload" not in st.session_state:
        st.session_state.show_upload = False
    
    videos = load_videos()
    
    # Sélecteur de vidéo épuré avec miniatures
    st.markdown("""
    <div class="video-selector">
        <div style="font-size: 14px; color: rgba(255,255,255,0.5); margin-bottom: 15px;">
            Contexte de conversation
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pills de sélection vidéo avec miniatures
    cols = st.columns(len(videos))
    for i, video in enumerate(videos):
        with cols[i]:
            if st.button(
                video["short"], 
                key=f"video_{video['id']}",
                help=video["title"]
            ):
                st.session_state.selected_video = video["title"]
    
    # Options étendues
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📁 Importer fichier", key="import_file"):
            st.session_state.show_upload = not st.session_state.show_upload
    
    with col2:
        if st.button("📊 Analytics", key="analytics"):
            st.info("📈 Analytics détaillées bientôt disponibles")
    
    with col3:
        if st.button("🎯 Suggestions", key="suggestions"):
            suggestions_text = "🎯 Suggestions pour améliorer votre contenu :\n• Plus d'exemples pratiques\n• Créer une série sur TypeScript\n• Répondre aux questions en attente"
            st.session_state.messages.append({
                "role": "assistant",
                "content": suggestions_text
            })
            st.experimental_rerun()
    
    with col4:
        if st.button("💡 Insights", key="insights"):
            insights_text = "💡 Insights de votre audience :\n• Niveau technique : Intermédiaire-Avancé (67%)\n• Plateforme préférée : Desktop (78%)\n• Moment d'activité : 18h-22h\n• Sujets demandés : TypeScript, Testing, DevOps"
            st.session_state.messages.append({
                "role": "assistant",
                "content": insights_text
            })
            st.experimental_rerun()
    
    # Zone d'upload conditionnelle
    if st.session_state.show_upload:
        st.markdown("""
        <div class="upload-zone active">
            <div style="font-size: 32px; color: rgba(255,255,255,0.3); margin-bottom: 10px;">📤</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 14px; margin-bottom: 8px;">Glissez vos fichiers ici ou cliquez pour sélectionner</div>
            <div style="color: rgba(255,255,255,0.4); font-size: 12px;">CSV, JSON, TXT - Max 10MB</div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choisir un fichier",
            type=['csv', 'json', 'txt'],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📁 Fichier '{uploaded_file.name}' importé avec succès ! Je peux maintenant analyser ces données. Que voulez-vous savoir ?"
            })
            st.session_state.show_upload = False
            st.experimental_rerun()
    
    # Zone de conversation
    st.markdown('<div class="conversation-area">', unsafe_allow_html=True)
    
    # Affichage des messages
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="empty-state">
            <span class="icon">💭</span>
            Bonjour ! Je suis votre assistant IA pour {st.session_state.selected_video}<br>
            Posez-moi vos questions ou utilisez les options ci-dessus
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(f"""
                <div class="ai-message">
                    <div class="ai-label">VIDMIND AI</div>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Zone d'input principale
    user_input = st.text_input(
        "",
        placeholder=f"Que voulez-vous savoir sur {st.session_state.selected_video} ?",
        key="main_input",
        label_visibility="collapsed"
    )
    
    # Traitement de l'input
    if user_input and user_input.strip():
        # Ajouter le message utilisateur
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input
        })
        
        # Affichage thinking
        with st.empty():
            st.markdown("""
            <div class="thinking-indicator">
                <span>VidMind réfléchit</span>
                <div class="thinking-dots">
                    <div class="thinking-dot"></div>
                    <div class="thinking-dot"></div>
                    <div class="thinking-dot"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1.2)
        
        # Générer et ajouter la réponse
        ai_response = generate_smart_response(user_input, st.session_state.selected_video)
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })
        
        # Rerun pour afficher la conversation mise à jour
        st.experimental_rerun()
    
    # Suggestions contextuelles
    suggestions = {
        "JavaScript Avancé": ["Sentiment de cette vidéo ?", "Questions en attente ?", "Comment améliorer ?"],
        "React Hooks": ["Performance de React ?", "Niveau de l'audience ?", "Prochains hooks à couvrir ?"],
        "CSS Grid": ["Confusion Flexbox/Grid ?", "Exemples demandés ?", "CSS moderne ?"],
        "Général": ["Vue d'ensemble chaîne", "Tendances audience", "Stratégie contenu"]
    }
    
    current_suggestions = suggestions.get(st.session_state.selected_video, suggestions["Général"])
    
    if not st.session_state.messages:
        cols_sug = st.columns(len(current_suggestions))
        for i, suggestion in enumerate(current_suggestions):
            with cols_sug[i]:
                if st.button(suggestion, key=f"sug_{i}"):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": suggestion
                    })
                    ai_response = generate_smart_response(suggestion, st.session_state.selected_video)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar minimaliste
    with st.sidebar:
        st.markdown("### 📊 Aperçu Rapide")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nouveaux", "3", "+1")
            st.metric("Engagement", "89%", "+5%")
        with col2:
            st.metric("Sentiment", "92%", "+2%")
            st.metric("Questions", "7", "+3")
        
        st.markdown("---")
        
        if st.button("🔍 Analytics Complètes"):
            st.info("📈 Dashboard complet bientôt disponible")
        
        if st.button("📧 Exporter Insights"):
            st.success("📤 Rapport exporté vers votre email")
        
        st.markdown("### 🔴 Statut Live")
        st.markdown("""
        <div style="color: #4CAF50; font-size: 12px;">
        ● Connecté à YouTube API<br>
        ● IA VidMind Active<br>
        ● Sync temps réel ON
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
