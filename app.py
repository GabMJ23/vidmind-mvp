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

# CSS Ultra-Épuré Steve Jobs Style
st.markdown("""
<style>
    /* Reset et base */
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
    
    /* Container principal centré */
    .main-interface {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        max-width: 800px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    
    /* Logo VidMind épuré */
    .logo {
        font-size: 48px;
        font-weight: 200;
        letter-spacing: 16px;
        color: #FFD700;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .tagline {
        font-size: 18px;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 60px;
        letter-spacing: 2px;
    }
    
    /* Zone de conversation épurée */
    .conversation-area {
        width: 100%;
        max-width: 700px;
        margin-bottom: 40px;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    /* Messages utilisateur */
    .user-message {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px 20px 4px 20px;
        padding: 16px 20px;
        margin-left: 20%;
        font-size: 16px;
        line-height: 1.5;
        animation: slideInRight 0.3s ease-out;
    }
    
    /* Messages IA */
    .ai-message {
        background: transparent;
        padding: 20px 0;
        margin-right: 10%;
        font-size: 16px;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.95);
        animation: slideInLeft 0.3s ease-out;
        border-left: 2px solid rgba(255, 215, 0, 0.3);
        padding-left: 20px;
    }
    
    .ai-label {
        font-size: 12px;
        color: #FFD700;
        font-weight: 500;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Sélecteur de vidéo minimaliste */
    .video-selector {
        width: 100%;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .video-pills {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 15px;
    }
    
    .video-pill {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 13px;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .video-pill:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: rgba(255, 215, 0, 0.3);
        color: #FFD700;
        transform: translateY(-2px);
    }
    
    .video-pill.active {
        background: rgba(255, 215, 0, 0.15);
        border-color: #FFD700;
        color: #FFD700;
    }
    
    /* Input zone ultra-épurée */
    .input-zone {
        width: 100%;
        position: relative;
    }
    
    .main-input {
        width: 100%;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 16px 60px 16px 24px;
        font-size: 16px;
        color: white;
        outline: none;
        transition: all 0.3s ease;
        font-family: inherit;
    }
    
    .main-input:focus {
        border-color: rgba(255, 215, 0, 0.5);
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .main-input::placeholder {
        color: rgba(255, 255, 255, 0.4);
        font-weight: 300;
    }
    
    .send-button {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 16px;
    }
    
    .send-button:hover {
        transform: translateY(-50%) scale(1.1);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    
    /* Suggestions épurées */
    .suggestions {
        margin-top: 30px;
        text-align: center;
    }
    
    .suggestions-label {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.5);
        margin-bottom: 15px;
        font-weight: 300;
    }
    
    .suggestion-pills {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    .suggestion-pill {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 6px 14px;
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        cursor: pointer;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .suggestion-pill:hover {
        background: rgba(255, 215, 0, 0.08);
        border-color: rgba(255, 215, 0, 0.2);
        color: rgba(255, 215, 0, 0.8);
        transform: translateY(-1px);
    }
    
    /* Sidebar minimaliste */
    .sidebar-toggle {
        position: fixed;
        top: 30px;
        left: 30px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        color: rgba(255, 255, 255, 0.6);
        z-index: 1000;
    }
    
    .sidebar-toggle:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: rgba(255, 215, 0, 0.3);
        color: #FFD700;
    }
    
    /* État de loading épuré */
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
    
    /* Masquer les éléments Streamlit */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stAppViewContainer > .main .block-container {padding-top: 0;}
    
    /* Messages vides élégants */
    .empty-state {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 16px;
        font-weight: 300;
        margin: 60px 0;
        line-height: 1.6;
    }
    
    .empty-state .icon {
        font-size: 48px;
        margin-bottom: 20px;
        display: block;
        opacity: 0.3;
    }
    
    /* Mode compact pour mobile */
    @media (max-width: 768px) {
        .logo {
            font-size: 36px;
            letter-spacing: 12px;
        }
        
        .main-interface {
            padding: 20px 15px;
        }
        
        .user-message {
            margin-left: 10%;
        }
        
        .ai-message {
            margin-right: 5%;
        }
        
        .video-pills {
            gap: 8px;
        }
        
        .video-pill {
            font-size: 12px;
            padding: 6px 12px;
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
    
    videos = load_videos()
    
    # Sélecteur de vidéo épuré
    st.markdown("""
    <div class="video-selector">
        <div style="font-size: 14px; color: rgba(255,255,255,0.5); margin-bottom: 10px;">
            Contexte de conversation
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pills de sélection vidéo
    cols = st.columns(len(videos))
    for i, video in enumerate(videos):
        with cols[i]:
            if st.button(
                video["short"], 
                key=f"video_{video['id']}",
                help=video["title"]
            ):
                st.session_state.selected_video = video["title"]
                # Ajouter message de contexte
                st.session_state.messages.append({
                    "role": "system",
                    "content": f"Contexte changé vers : {video['title']}"
                })
    
    # Zone de conversation
    st.markdown('<div class="conversation-area">', unsafe_allow_html=True)
    
    # Affichage des messages
    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <span class="icon">💭</span>
            Posez-moi n'importe quelle question sur vos vidéos<br>
            ou discutons de votre stratégie créative
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
    st.markdown('<div class="input-zone">', unsafe_allow_html=True)
    
    # Input avec gestion des événements
    user_input = st.text_input(
        "",
        placeholder=f"Que voulez-vous savoir sur {st.session_state.selected_video} ?",
        key="main_input",
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    if not st.session_state.messages:  # Afficher seulement si pas de conversation
        st.markdown(f"""
        <div class="suggestions">
            <div class="suggestions-label">Suggestions</div>
            <div class="suggestion-pills">
                {"".join([f'<div class="suggestion-pill" onclick="document.getElementById(\'main_input\').value=\'{s}\'">{s}</div>' for s in current_suggestions])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar minimaliste pour analytics
    with st.sidebar:
        st.markdown("### 📊 Aperçu Rapide")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nouveaux", "3", "+1")
        with col2:
            st.metric("Sentiment", "89%", "+2%")
        
        if st.button("🔍 Analytics Détaillées"):
            st.info("Analytics complètes disponibles prochainement")

if __name__ == "__main__":
    main()
