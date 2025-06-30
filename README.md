⚔️ Pokémon Battle Predictor

🚀 Project Overview
This is an end-to-end Machine Learning + Web App project that predicts which Pokémon will win in a battle based on their stats, type effectiveness, and legendary status. It features an interactive Streamlit app with:

->🎮 Beautiful UI with Pokémon-themed styling

->🎵 Background Pokémon intro music

->🔮 Winner prediction with a simulation interface

->🧠 A powerful stacked ensemble ML model


💡 Motivation
As a childhood Pokémon fan, I often debated with friends:

“Who would win if Charizard fought Blastoise?”

This curiosity inspired me to build this ML project, combining my love for Pokémon with data science, feature engineering, and full-stack deployment skills.


🛠 Tech Stack

->Python, Pandas, NumPy

->Scikit-learn, XGBoost

->Streamlit for Web App

->HTML/CSS for advanced UI customization


🤖 ML Model

This project uses a multi-level ensemble approach:

1.Stacked Model 1

->Random Forest

->XGBoost

->Logistic Regression

->SVM

->Meta-learner: MLPClassifier

2.Stacked Model 2

->SVM

->XGBoost

->Random Forest

->KNN

->Meta-learner: Logistic Regression

3.Final Ensemble

->Soft Voting of both stacked models for robust generalization.

This architecture ensures high accuracy and reduced bias/variance, making predictions more reliable.

📝 Features

✅ Predicts the winner between any two Pokémon

✅ Uses type effectiveness calculation

✅ Considers legendary status and stat differences

✅ Beautiful simulation interface with VS animations

✅ Background instrumental music for an immersive experience
