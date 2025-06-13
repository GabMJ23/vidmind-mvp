def show_ai_chat_enhanced(videos, comments):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Sélecteur de vidéo moderne avec preview
    st.markdown("### 🎥 Sélectionner une vidéo pour analyser")
    
    # Créer une interface de sélection visuelle
    cols = st.columns(len(videos))
    selected_video_id = None
    
    for i, video in enumerate(videos):
        with cols[i]:
            # Card cliquable pour chaque vidéo
            card_style = "video-card"
            if st.button(
                f"📹 {video['title'][:30]}...\n\n👁️ {video['views']} vues\n💬 {video['comments_count']} commentaires", 
                key=f"video_select_{video['id']}",
                use_container_width=True
            ):
                st.session_state.selected_chat_video = video['id']
                selected_video_id = video['id']
    
    # Récupérer la vidéo sélectionnée
    if 'selected_chat_video' not in st.session_state:
        st.session_state.selected_chat_video = videos[0]['id']
    
    current_video = next(v for v in videos if v['id'] == st.session_state.selected_chat_video)
    
    st.markdown(f"""
    <div class="video-card">
        <h4>🎬 Conversation sur : {current_video['title']}</h4>
        <p>👁️ {current_video['views']} vues • 💬 {current_video['comments_count']} commentaires • 🎯 {current_video['engagement']}% engagement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Zone de chat moderne
    st.markdown("### 💭 Conversation avec VidMind AI")
    
    # Initialiser l'historique de chat par vidéo
    chat_key = f"chat_history_{st.session_state.selected_chat_video}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {
                "role": "assistant", 
                "content": f"👋 Salut ! Je suis VidMind AI. J'ai analysé tous les commentaires de votre vidéo **{current_video['title']}**. Que voulez-vous savoir sur votre audience ?"
            }
        ]
    
    # Container pour les messages avec défilement
    chat_container = st.container()
    
    with chat_container:
        # Affichage des messages avec style moderne
        for message in st.session_state[chat_key]:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 15px 0;">
                    <div class="chat-message-user">
                        <strong>Vous :</strong><br>
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 15px 0;">
                    <div class="chat-message-ai">
                        <strong>🤖 VidMind AI :</strong><br>
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Interface d'input moderne
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "💭 Tapez votre question...", 
            key=f"user_input_{st.session_state.selected_chat_video}",
            placeholder="Ex: Que pensent les gens de cette vidéo ? Quelles questions sont en attente ?"
        )
    
    with col2:
        send_button = st.button("🚀 Envoyer", key=f"send_{st.session_state.selected_chat_video}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Traitement de l'envoi
    if (send_button and user_input) or (user_input and user_input != st.session_state.get(f"last_input_{st.session_state.selected_chat_video}", "")):
        # Éviter les doublons
        st.session_state[f"last_input_{st.session_state.selected_chat_video}"] = user_input
        
        # Ajouter message utilisateur
        st.session_state[chat_key].append({"role": "user", "content": user_input})
        
        # Simuler la réponse IA avec typing indicator
        with st.spinner("🤖 VidMind réfléchit..."):
            time.sleep(1.2)
            
            # Générer une réponse contextuelle intelligente
            ai_response = generate_contextual_response(user_input, current_video, comments)
            
            # Ajouter la réponse IA
            st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
        
        st.rerun()
    
    # Suggestions de questions intelligentes
    st.markdown("### 💡 Questions Suggérées")
    
    suggestions = [
        "🔍 Analyser le sentiment global de cette vidéo",
        "❓ Quelles questions techniques sont en attente ?",
        "🎯 Recommandations pour ma prochaine vidéo",
        "📈 Comment améliorer l'engagement sur ce contenu ?",
        "👥 Qui sont mes viewers les plus actifs ?",
        "🏆 Points forts de cette vidéo selon l'audience"
    ]
    
    # Afficher les suggestions en grille
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}_{st.session_state.selected_chat_video}", use_container_width=True):
                # Ajouter la suggestion comme message utilisateur
                st.session_state[chat_key].append({"role": "user", "content": suggestion})
                
                # Générer réponse immédiate
                ai_response = generate_contextual_response(suggestion, current_video, comments)
                st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
                
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_contextual_response(user_input, video, comments):
    """Génère des réponses IA contextuelles et intelligentes"""
    
    # Analyser le type de question
    input_lower = user_input.lower()
    
    if "sentiment" in input_lower or "pensent" in input_lower:
        return f"""
        📊 **Analyse du sentiment pour "{video['title']}"** :
        
        • **{video['engagement']}% d'engagement positif** (excellent score !)
        • **Commentaires analysés** : {video['comments_count']} 
        • **Sentiment global** : 😊 Très positif
        
        🎯 **Points forts identifiés** :
        - Vos explications sont claires et accessibles
        - L'audience apprécie votre approche pédagogique
        - Bon équilibre entre théorie et pratique
        
        ⚡ **Insight caché** : Cette vidéo génère +{random.randint(15, 30)}% plus d'engagement que votre moyenne !
        """
        
    elif "question" in input_lower or "attente" in input_lower:
        video_comments = [c for c in comments if c['video_id'] == video['id'] and c['type'] == 'question']
        if video_comments:
            comment = video_comments[0]
            return f"""
            ❓ **Questions techniques en attente** :
            
            🔥 **Question prioritaire** :
            **@{comment['author']}** : "{comment['text'][:100]}..."
            ⏰ *Il y a {comment['minutes_ago']} minutes*
            
            🎯 **Pourquoi répondre rapidement** :
            - Question très technique (niveau avancé)
            - Potentiel viral si bien expliqué
            - {random.randint(3, 8)} autres viewers ont la même question
            
            💡 **Suggestion de réponse** : Je peux générer 3 types de réponses (technique/amicale/pédagogique). Voulez-vous que je vous aide ?
            """
        else:
            return "🎉 Excellente nouvelle ! Aucune question technique en attente. Votre audience semble bien comprendre le contenu !"
    
    elif "prochaine" in input_lower or "recommandation" in input_lower:
        topics = ["Async/Await avancé", "Design Patterns", "Performance Optimization", "Testing automatisé", "Architecture microservices"]
        selected_topic = random.choice(topics)
        return f"""
        🚀 **Recommandations pour votre prochaine vidéo** :
        
        📈 **Sujet #1 recommandé** : **{selected_topic}**
        - **{random.randint(8, 15)} demandes récurrentes** dans vos commentaires
        - **Potentiel viral** : 🔥🔥🔥🔥
        - **Audience cible** : Développeurs intermédiaires/avancés
        
        🎯 **Angle suggéré** :
        - Focus sur les cas pratiques réels
        - Exemples de code commentés
        - Pièges à éviter (très demandé !)
        
        💡 **Bonus insight** : Vos vidéos techniques génèrent +{random.randint(20, 45)}% plus de commentaires que vos vidéos générales !
        """
    
    elif "améliorer" in input_lower or "engagement" in input_lower:
        return f"""
        📈 **Stratégies pour booster l'engagement** :
        
        🔥 **Actions immédiates** :
        - **Répondre aux {random.randint(2, 5)} questions en attente** (+15% engagement estimé)
        - **Épingler un commentaire** pour guider la discussion
        - **Poser une question** en fin de vidéo pour inciter les réactions
        
        🎯 **Optimisations détectées** :
        - Vos viewers restent **{random.randint(75, 95)}% du temps** sur la vidéo
        - **Pic d'engagement** à 0:45 et 3:20 (moments clés)
        - **Call-to-action** efficace à 85%
        
        💡 **Insight exclusif** : Vos réponses rapides génèrent +{random.randint(25, 40)}% de likes supplémentaires !
        """
    
    elif "actif" in input_lower or "viewer" in input_lower:
        active_commenters = ["Sarah_Dev92", "TechNinja_Dev", "DevPro_Official", "CodeMaster_2024"]
        return f"""
        👥 **Vos viewers les plus actifs** :
        
        🏆 **Top contributeurs** :
        • **@{active_commenters[0]}** - {random.randint(8, 15)} commentaires techniques de qualité
        • **@{active_commenters[1]}** - {random.randint(5, 12)} questions pertinentes
        • **@{active_commenters[2]}** - {random.randint(6, 10)} retours constructifs
        
        💡 **Potentiels ambassadeurs** :
        - {active_commenters[0]} : Expertise élevée, influence communauté
        - {active_commenters[1]} : Questions qui génèrent des discussions
        
        🎯 **Suggestion** : Considérez ces viewers pour beta-tester vos futurs contenus !
        """
    
    else:
        # Réponse générale intelligente
        return f"""
        🤖 **Analyse globale de "{video['title']}"** :
        
        📊 **Métriques clés** :
        - **{video['views']}** vues avec **{video['engagement']}%** d'engagement
        - **{video['comments_count']}** commentaires ({random.randint(80, 95)}% positifs)
        - **Temps de visionnage moyen** : {random.randint(4, 8)} min {random.randint(10, 59)}s
        
        🎯 **Ce qui fonctionne bien** :
        - Rythme de présentation optimal
        - Exemples pratiques appréciés
        - Structure claire et logique
        
        💡 **Axes d'amélioration** :
        - Ajouter plus d'exemples concrets
        - Créer une suite sur le sujet avancé
        
        ❓ **Question spécifique** ? Demandez-moi ce que vous voulez savoir !
        """import streamlit as st
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
        background-color: #000000;
        color: white;
    }
    
    .stApp {
        background-color: #000000;
    }
    
    .video-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .comment-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid #FFD700;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }
    
    .insight-metric {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 235, 59, 0.05));
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    
    .ai-response {
        background: rgba(30, 30, 30, 0.8);
        border-left: 3px solid #FFD700;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    h1, h2, h3 {
        color: #FFD700 !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #FFD700, #FFA000);
        color: black;
        border: none;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .stSelectbox label {
        color: #FFD700 !important;
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
            "text": "Super vidéo ! Mais j'ai une question sur les closures, comment ça marche exactement avec les variables ? J'ai du mal à comprendre pourquoi la variable reste accessible même après la fin de la fonction parent. 🤔",
            "minutes_ago": 5,
            "type": "question",
            "urgency": "high"
        },
        {
            "video_id": 2,
            "author": "DevPro_Official", 
            "text": "Merci pour cette explication claire ! Ça m'a beaucoup aidé pour mon projet React. Grâce à toi j'ai enfin compris useState et useEffect. Tu as un don pour expliquer simplement ! 🙏",
            "minutes_ago": 12,
            "type": "thanks",
            "urgency": "low"
        },
        {
            "video_id": 3,
            "author": "TechNinja_Dev",
            "text": "Excellent tuto sur CSS Grid ! Est-ce que tu peux faire une vidéo sur Flexbox vs Grid ? Je ne sais jamais quand utiliser quoi dans mes projets. Ce serait top d'avoir une comparaison pratique ! 💪",
            "minutes_ago": 18,
            "type": "suggestion", 
            "urgency": "medium"
        }
    ]
    
    return videos, comments

# Fonction pour générer des réponses IA
def generate_ai_response(comment_text, tone="professional"):
    responses = {
        "professional": {
            "closures": "Excellente question ! Les closures permettent à une fonction d'accéder aux variables de son scope parent même après que ce scope soit fermé. En gros, la fonction 'capture' l'environnement dans lequel elle a été créée. Je prépare justement une vidéo dédiée aux closures avec des exemples concrets ! 🚀",
            "thanks": "Avec grand plaisir ! 😊 Ça me fait vraiment plaisir de savoir que ça t'a aidé pour ton projet. N'hésite pas si tu as d'autres questions !",
            "suggestion": "Excellente idée ! Flexbox vs Grid, c'est un classique mais tellement important. Je note ça dans ma liste pour les prochaines vidéos ! 📝"
        },
        "friendly": {
            "closures": "Hey ! Super question 😊 Alors les closures c'est comme si une fonction gardait un 'souvenir' de où elle a été créée. Même quand le contexte original disparaît, elle peut encore accéder aux variables ! C'est magique non ? 🪄",
            "thanks": "Awww merci beaucoup ! 🥰 Ça me fait chaud au cœur ! Continue comme ça pour ton projet, tu vas cartonner ! 💪",
            "suggestion": "Ooh excellente idée ! 💡 Je pense souvent à faire cette comparaison justement. Je vais creuser ça très bientôt ! Merci pour l'inspi ! ✨"
        },
        "expert": {
            "closures": "Les closures sont un concept fondamental en JavaScript. Techniquement, une closure est formée quand une fonction interne référence des variables de sa fonction externe. Le moteur JS maintient une référence vers l'environnement lexical même après l'exécution de la fonction externe.",
            "thanks": "Content que le contenu soit utile pour votre implémentation. Les hooks React nécessitent effectivement une approche méthodique pour être maîtrisés correctement.",
            "suggestion": "Pertinente observation. Flexbox excelle pour les composants unidimensionnels tandis que Grid est optimal pour les layouts bidimensionnels. Une analyse comparative détaillée serait effectivement valuable."
        }
    }
    
    # Simple matching based on keywords
    if "closure" in comment_text.lower():
        return responses[tone]["closures"]
    elif "merci" in comment_text.lower() or "aidé" in comment_text.lower():
        return responses[tone]["thanks"] 
    elif "vidéo" in comment_text.lower() and "?" in comment_text:
        return responses[tone]["suggestion"]
    else:
        return responses[tone]["thanks"]  # default

# Interface principale
def main():
    # Header avec logo ultra-moderne
    st.markdown("""
    <div class="main-container">
        <h1 class="main-title">VIDMIND</h1>
        <p class="subtitle">L'Intelligence de Votre Créativité</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation moderne en onglets
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "💬 Commentaires", "📊 Analytics", "🤖 Chat IA"])
    
    videos, comments = load_sample_data()
    
    with tab1:
        show_dashboard(videos, comments)
    with tab2:
        show_comments_management(videos, comments)
    with tab3:
        show_analytics(videos, comments)
    with tab4:
        show_ai_chat_enhanced(videos, comments)

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
        with st.container():
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
                    st.session_state.selected_video = video['id']
                    st.rerun()

def show_comments_management(videos, comments):
    st.markdown("## 💬 Gestion des Commentaires")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        urgency_filter = st.selectbox("🚨 Urgence", ["Tous", "High", "Medium", "Low"])
    with col2:
        type_filter = st.selectbox("📝 Type", ["Tous", "Question", "Thanks", "Suggestion"])
    
    # Affichage des commentaires
    for comment in comments:
        # Appliquer les filtres
        if urgency_filter != "Tous" and comment['urgency'].lower() != urgency_filter.lower():
            continue
        if type_filter != "Tous" and comment['type'].lower() != type_filter.lower():
            continue
            
        video = next(v for v in videos if v['id'] == comment['video_id'])
        
        with st.container():
            # Header du commentaire avec info vidéo
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; margin: 10px 0;">
                <small style="color: #FFD700;">📹 {video['title']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Commentaire principal
            urgency_color = {"high": "#FF4444", "medium": "#FFA500", "low": "#4CAF50"}
            st.markdown(f"""
            <div class="comment-card" style="border-left-color: {urgency_color[comment['urgency']]};">
                <strong>@{comment['author']}</strong> a écrit il y a {comment['minutes_ago']} min:
                <br><br>
                "{comment['text']}"
                <br><br>
                <span style="background: {urgency_color[comment['urgency']]}20; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">
                    {comment['type'].upper()} • {comment['urgency'].upper()}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Actions
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                if st.button(f"✨ Répondre avec IA", key=f"ai_reply_{comment['author']}"):
                    with st.spinner("🤖 Génération de la réponse..."):
                        time.sleep(1.5)  # Simulation du processing
                        
                        # Sélection du ton
                        tone = st.selectbox("🎭 Choisir le ton:", ["professional", "friendly", "expert"], key=f"tone_{comment['author']}")
                        
                        response = generate_ai_response(comment['text'], tone)
                        
                        st.markdown(f"""
                        <div class="ai-response">
                            <strong>🤖 Réponse générée ({tone}):</strong><br><br>
                            {response}
                            <br><br>
                            <small>🎯 Prédiction engagement: +85%</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("📤 Publier sur YouTube", key=f"publish_{comment['author']}"):
                                st.success("✅ Réponse publiée avec succès !")
                        with col_b:
                            if st.button("✏️ Modifier", key=f"edit_{comment['author']}"):
                                st.info("🔧 Fonctionnalité d'édition bientôt disponible")
            
            with col2:
                if st.button(f"⏰ Plus tard", key=f"later_{comment['author']}"):
                    st.info("📝 Ajouté à votre liste TODO")
            
            with col3:
                if st.button(f"✅ Lu", key=f"read_{comment['author']}"):
                    st.success("👁️ Marqué comme lu")
            
            st.markdown("---")

def show_analytics(videos, comments):
    st.markdown("## 📊 Analytics Créateur")
    
    # Graphique sentiment dans le temps
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
    
    # Répartition des types de commentaires
    comment_types = ["Questions", "Remerciements", "Suggestions", "Critiques"]
    type_counts = [45, 30, 20, 5]
    
    fig_types = px.pie(
        values=type_counts,
        names=comment_types,
        title="🥧 Répartition des Types de Commentaires",
        color_discrete_sequence=["#FFD700", "#FFA500", "#FF6B35", "#FF4444"]
    )
    fig_types.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_types, use_container_width=True)
    
    # Recommandations IA
    st.markdown("### 🎯 Recommandations IA")
    
    recommendations = [
        "🚀 **Prochaine vidéo suggérée**: 'Promises et async/await avancé' (12 demandes récurrentes)",
        "⚡ **Pic d'activité**: Vos vidéos React génèrent +47% d'engagement vs JavaScript vanilla",
        "💡 **Insight caché**: Sarah_Dev92 et TechNinja_Dev posent souvent des questions techniques - potentiels ambassadeurs",
        "📈 **Tendance**: Votre audience devient plus avancée techniquement (+23% questions complexes)"
    ]
    
    for rec in recommendations:
        st.markdown(f"""
        <div style="background: rgba(255,215,0,0.1); border-left: 3px solid #FFD700; padding: 15px; margin: 10px 0; border-radius: 8px;">
            {rec}
        </div>
        """, unsafe_allow_html=True)

def show_ai_chat(videos, comments):
    st.markdown("## 🤖 Chat avec l'IA VidMind")
    
    # Sélection de vidéo pour le contexte
    video_titles = [f"{v['title']}" for v in videos]
    selected_video = st.selectbox("🎥 Sélectionner une vidéo pour le contexte:", video_titles)
    
    st.markdown("### 💬 Conversation")
    
    # Initialiser l'historique de chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Zone de chat
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
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
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📤 Envoyer") and user_input:
            # Ajouter message utilisateur
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Simuler la réponse IA
            with st.spinner("🤖 VidMind réfléchit..."):
                time.sleep(1.5)
                
                # Générer une réponse contextuelle
                if "sentiment" in user_input.lower():
                    ai_response = "Basé sur l'analyse des commentaires de cette vidéo, le sentiment est **positif à 89%** ! 😊 Les viewers apprécient particulièrement vos explications claires. J'ai détecté 3 questions techniques qui mériteraient une réponse."
                elif "question" in user_input.lower():
                    ai_response = "J'ai identifié **5 questions techniques** qui nécessitent votre attention :<br><br>• **@TechGuru**: 'Comment optimiser les re-renders avec useMemo ?'<br>• **@ReactNewbie**: 'Peut-on utiliser plusieurs useState dans un composant ?'<br><br>Ces questions ont reçu plusieurs likes, indiquant un intérêt général."
                elif "prochaine" in user_input.lower():
                    ai_response = "Basé sur les demandes récurrentes, votre prochaine vidéo devrait couvrir :<br><br>🎯 **Sujets les plus demandés:**<br>• Promises et async/await avancé (12 mentions)<br>• Design patterns en JavaScript (8 mentions)<br>• Optimisation et performance (6 mentions)"
                else:
                    ai_response = f"Excellente question ! Basé sur l'analyse de vos commentaires pour '{selected_video}', je peux vous dire que votre audience est très engagée. Voulez-vous que je détaille un aspect particulier ?"
                
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            st.rerun()
    
    # Suggestions de questions
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
                st.rerun()

if __name__ == "__main__":
    main()
