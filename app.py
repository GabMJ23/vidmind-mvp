import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="VidMind - AI for Content Creators",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Custom pour look premium
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%);
        color: white;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%);
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .video-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px;
        margin: 15px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .video-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(255, 215, 0, 0.15);
        border-color: rgba(255, 215, 0, 0.3);
    }
    
    .comment-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%);
        border-left: 4px solid #FFD700;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .insight-metric {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.08) 0%, rgba(255, 235, 59, 0.03) 100%);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .ai-response {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.06) 0%, rgba(30, 30, 30, 0.8) 100%);
        border-left: 4px solid #FFD700;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        animation: fadeInUp 0.5s ease-out;
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
    
    h1, h2, h3 {
        color: #FFD700 !important;
        font-weight: 300 !important;
    }
    
    .main-title {
        text-align: center;
        font-size: 3.5em !important;
        font-weight: 200 !important;
        letter-spacing: 12px;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.6);
        font-size: 1.3em;
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: black !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 12px 30px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4) !important;
    }
    
    .stSelectbox label, .stTextInput label {
        color: #FFD700 !important;
        font-weight: 500 !important;
    }
    
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# Données simulées réalistes
@st.cache_data
def load_sample_data():
    videos = [
        {
            "id": 1,
            "title": "JavaScript Avancé - Les Concepts Qui Font la Différence",
            "views": "156K",
            "comments_count": 24,
            "days_ago": 3,
            "engagement": 89
        },
        {
            "id": 2, 
            "title": "React Hooks - Le Guide Complet pour Débutants",
            "views": "89K",
            "comments_count": 12,
            "days_ago": 7,
            "engagement": 92
        },
        {
            "id": 3,
            "title": "CSS Grid - Layouts Modernes en 20 Minutes", 
            "views": "43K",
            "comments_count": 5,
            "days_ago": 2,
            "engagement": 85
        }
    ]
    
    comments = [
        {
            "video_id": 1,
            "author": "Sarah_Dev92",
            "text": "Super vidéo ! Mais j'ai une question sur les closures, comment ça marche exactement avec les variables ?",
            "minutes_ago": 5,
            "type": "question",
            "urgency": "high"
        },
        {
            "video_id": 2,
            "author": "DevPro_Official", 
            "text": "Merci pour cette explication claire ! Ça m'a beaucoup aidé pour mon projet React.",
            "minutes_ago": 12,
            "type": "thanks",
            "urgency": "low"
        },
        {
            "video_id": 3,
            "author": "TechNinja_Dev",
            "text": "Excellent tuto sur CSS Grid ! Est-ce que tu peux faire une vidéo sur Flexbox vs Grid ?",
            "minutes_ago": 18,
            "type": "suggestion", 
            "urgency": "medium"
        }
    ]
    
    return videos, comments

# Fonction pour générer des réponses IA
def generate_ai_response(comment_text, tone="professional"):
    if "closure" in comment_text.lower():
        return "Excellente question ! Les closures permettent à une fonction d'accéder aux variables de son scope parent même après que ce scope soit fermé. Je prépare justement une vidéo dédiée aux closures ! 🚀"
    elif "merci" in comment_text.lower():
        return "Avec grand plaisir ! 😊 Ça me fait vraiment plaisir de savoir que ça t'a aidé pour ton projet."
    else:
        return "Excellente suggestion ! Je note ça dans ma liste pour les prochaines vidéos ! 📝"

# Interface principale
def main():
    # Header avec logo
    st.markdown("""
    <div class="main-container">
        <h1 class="main-title">VIDMIND</h1>
        <p class="subtitle">L'Intelligence de Votre Créativité</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation en onglets
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "💬 Commentaires", "📊 Analytics", "🤖 Chat IA"])
    
    videos, comments = load_sample_data()
    
    with tab1:
        show_dashboard(videos, comments)
    with tab2:
        show_comments_management(videos, comments)
    with tab3:
        show_analytics(videos, comments)
    with tab4:
        show_ai_chat(videos, comments)

def show_dashboard(videos, comments):
    st.markdown("## 🎯 Vue d'Ensemble")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="insight-metric">
            <h3>🔔 Nouveaux</h3>
            <h2>3</h2>
            <p>Commentaires</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-metric">
            <h3>😊 Sentiment</h3>
            <h2>92%</h2>
            <p>Positif</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-metric">
            <h3>❓ Questions</h3>
            <h2>7</h2>
            <p>En attente</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="insight-metric">
            <h3>⚡ Temps</h3>
            <h2>4h30</h2>
            <p>Économisé</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🎥 Vos Vidéos Récentes")
    
    for video in videos:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="video-card">
                <h4>📹 {video['title']}</h4>
                <p>👁️ {video['views']} vues • 💬 {video['comments_count']} commentaires • 📅 Il y a {video['days_ago']} jours</p>
                <div style="background: rgba(255,215,0,0.2); padding: 5px 10px; border-radius: 15px; display: inline-block; margin-top: 10px;">
                    <small>🎯 Engagement: {video['engagement']}%</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"💬 Analyser", key=f"analyze_{video['id']}"):
                st.info(f"Analyse de '{video['title']}' en cours...")

def show_comments_management(videos, comments):
    st.markdown("## 💬 Gestion des Commentaires")
    
    # Affichage des commentaires
    for comment in comments:
        video = next(v for v in videos if v['id'] == comment['video_id'])
        
        # Header du commentaire
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; margin: 10px 0;">
            <small style="color: #FFD700;">📹 {video['title']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Commentaire principal
        urgency_colors = {"high": "#FF4444", "medium": "#FFA500", "low": "#4CAF50"}
        st.markdown(f"""
        <div class="comment-card" style="border-left-color: {urgency_colors[comment['urgency']]};">
            <strong>@{comment['author']}</strong> a écrit il y a {comment['minutes_ago']} min:
            <br><br>
            "{comment['text']}"
            <br><br>
            <span style="background: {urgency_colors[comment['urgency']]}20; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">
                {comment['type'].upper()} • {comment['urgency'].upper()}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Actions
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button(f"✨ Répondre avec IA", key=f"ai_reply_{comment['author']}"):
                with st.spinner("🤖 Génération de la réponse..."):
                    time.sleep(1.5)
                    response = generate_ai_response(comment['text'])
                    
                    st.markdown(f"""
                    <div class="ai-response">
                        <strong>🤖 Réponse générée :</strong><br><br>
                        {response}
                        <br><br>
                        <small>🎯 Prédiction engagement: +85%</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("📤 Publier sur YouTube", key=f"publish_{comment['author']}"):
                        st.success("✅ Réponse publiée avec succès !")
        
        with col2:
            if st.button(f"⏰ Plus tard", key=f"later_{comment['author']}"):
                st.info("📝 Ajouté à votre liste TODO")
        
        with col3:
            if st.button(f"✅ Lu", key=f"read_{comment['author']}"):
                st.success("👁️ Marqué comme lu")

def show_analytics(videos, comments):
    st.markdown("## 📊 Analytics Créateur")
    
    # Graphique sentiment
    dates = [(datetime.now() - timedelta(days=x)) for x in range(7, 0, -1)]
    sentiment_scores = [88, 91, 85, 92, 89, 94, 92]
    
    fig_sentiment = px.line(
        x=dates, 
        y=sentiment_scores,
        title="📈 Evolution du Sentiment Communauté (7 derniers jours)",
        color_discrete_sequence=["#FFD700"]
    )
    fig_sentiment.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Recommandations
    st.markdown("### 🎯 Recommandations IA")
    recommendations = [
        "🚀 **Prochaine vidéo suggérée**: 'Promises et async/await avancé' (12 demandes)",
        "📈 **Tendance**: Vos vidéos React génèrent +47% d'engagement",
        "💡 **Insight**: Sarah_Dev92 pose souvent des questions techniques",
        "🎯 **Optimisation**: Votre audience devient plus avancée (+23%)"
    ]
    
    for rec in recommendations:
        st.markdown(f"""
        <div style="background: rgba(255,215,0,0.1); border-left: 3px solid #FFD700; padding: 15px; margin: 10px 0; border-radius: 8px;">
            {rec}
        </div>
        """, unsafe_allow_html=True)

def show_ai_chat(videos, comments):
    st.markdown("## 🤖 Chat avec l'IA VidMind")
    
    # Sélection de vidéo
    video_titles = [f"{v['title']}" for v in videos]
    selected_video = st.selectbox("🎥 Sélectionner une vidéo pour le contexte:", video_titles)
    
    st.markdown("### 💬 Conversation")
    
    # Initialiser l'historique
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Afficher l'historique
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="text-align: right; margin: 10px 0;">
                <div style="background: rgba(255,255,255,0.1); padding: 10px 15px; border-radius: 15px 15px 5px 15px; display: inline-block; max-width: 70%;">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: left; margin: 10px 0;">
                <div style="background: rgba(255,215,0,0.1); border-left: 3px solid #FFD700; padding: 10px 15px; border-radius: 5px 15px 15px 15px; display: inline-block; max-width: 85%;">
                    <strong>🤖 VidMind:</strong><br>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Input utilisateur
    user_input = st.text_input("💭 Posez votre question...", key="user_input")
    
    if st.button("📤 Envoyer") and user_input:
        # Ajouter message utilisateur
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Simuler réponse IA
        with st.spinner("🤖 VidMind réfléchit..."):
            time.sleep(1.5)
            
            if "sentiment" in user_input.lower():
                ai_response = "Basé sur l'analyse des commentaires, le sentiment est **positif à 89%** ! 😊 Les viewers apprécient vos explications claires."
            elif "question" in user_input.lower():
                ai_response = "J'ai identifié **5 questions techniques** qui nécessitent votre attention. Les plus urgentes concernent les closures et useState."
            else:
                ai_response = f"Excellente question ! Basé sur l'analyse de '{selected_video}', votre audience est très engagée. Voulez-vous que je détaille un aspect particulier ?"
            
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        # Recharger la page pour afficher les nouveaux messages
        st.experimental_rerun()
    
    # Suggestions
    st.markdown("### 💡 Questions Suggérées")
    suggestions = [
        "Que pensent les gens de cette vidéo ?",
        "Quelles questions sont en attente ?", 
        "Quel devrait être le sujet de ma prochaine vidéo ?",
        "Comment améliorer mes prochaines vidéos ?"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                st.experimental_rerun()

if __name__ == "__main__":
    main()
