import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

# Markdown and code cells
cells = []

# 1. Problem definition
cells.append(nbf.v4.new_markdown_cell("# X Fake Account Detection\n\n## 1. Problem definition\nThis notebook develops a machine-learning prototype for an X/Twitter account risk-detection system.\n\nThe goal is not to definitively classify a person as fake, but to estimate whether an account shows suspicious or anomalous behavioral patterns based on profile, activity, engagement, and content features.\n\nOutputs include a risk probability and risk level."))

# 2. Dataset loading
cells.append(nbf.v4.new_markdown_cell("## 2. Dataset loading\nLoad the dataset (initially synthetic for development)."))
cells.append(nbf.v4.new_code_cell("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport json\nimport os\n\n# Load dataset\ndata_path = '../dataset/accounts.csv'\ndf = pd.read_csv(data_path)\ndf.head()"))

# 3. Data exploration
cells.append(nbf.v4.new_markdown_cell("## 3. Data exploration\nUnderstand feature distributions and class balance."))
cells.append(nbf.v4.new_code_cell("print(df.info())\nprint('\\nClass balance:')\nprint(df['label'].value_counts(normalize=True))"))
cells.append(nbf.v4.new_code_cell("sns.countplot(x='label', data=df)\nplt.title('Distribution of Legit (0) vs Suspicious (1)')\nplt.show()"))

# 4. Data cleaning
cells.append(nbf.v4.new_markdown_cell("## 4. Data cleaning\nHandle any missing values. (Synthetic data is clean, but in production, we fill or drop appropriately)."))
cells.append(nbf.v4.new_code_cell("# Example: Fill missing values if any\n# df.fillna(0, inplace=True)\nprint('Missing values:\\n', df.isnull().sum().sum())"))

# 5. Feature engineering
cells.append(nbf.v4.new_markdown_cell("## 5. Feature engineering\nThe dataset already contains the engineered features (e.g., `followers_following_ratio`). Here we separate features and the target variable."))
cells.append(nbf.v4.new_code_cell("features = [\n    'account_age_days', 'followers_count', 'following_count', 'post_count', \n    'followers_following_ratio', 'profile_completeness', 'verified',\n    'posts_per_day', 'average_post_interval', 'posting_interval_std', \n    'reply_ratio', 'repost_ratio', 'original_post_ratio', 'activity_burst_score',\n    'average_likes', 'average_replies', 'average_reposts', 'average_quotes', \n    'engagement_rate', 'engagement_variance',\n    'duplicate_content_ratio', 'average_text_length', 'hashtag_frequency', \n    'mention_frequency', 'url_frequency', 'repeated_hashtag_ratio'\n]\n\nX = df[features]\ny = df['label']"))

# 6. Feature correlation/analysis
cells.append(nbf.v4.new_markdown_cell("## 6. Feature correlation/analysis\nVisualize correlations between features and the target label."))
cells.append(nbf.v4.new_code_cell("plt.figure(figsize=(15, 12))\ncorr = df[features + ['label']].corr()\nsns.heatmap(corr, annot=False, cmap='coolwarm')\nplt.title('Feature Correlation Matrix')\nplt.show()"))

# 7. Train/test split
cells.append(nbf.v4.new_markdown_cell("## 7. Train/test split\nSplit the data into training and testing sets."))
cells.append(nbf.v4.new_code_cell("from sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nprint(f'Train shape: {X_train.shape}, Test shape: {X_test.shape}')"))

# 8. Baseline models
cells.append(nbf.v4.new_markdown_cell("## 8. Baseline models\nTrain Logistic Regression and Random Forest as baselines."))
cells.append(nbf.v4.new_code_cell("from sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix\nfrom sklearn.preprocessing import StandardScaler\n\n# Scale data for Logistic Regression\nscaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)\n\n# Logistic Regression\nlr = LogisticRegression(max_iter=1000)\nlr.fit(X_train_scaled, y_train)\nlr_preds = lr.predict(X_test_scaled)\nprint('Logistic Regression F1:', f1_score(y_test, lr_preds))\n\n# Random Forest\nrf = RandomForestClassifier(random_state=42)\nrf.fit(X_train, y_train)\nrf_preds = rf.predict(X_test)\nprint('Random Forest F1:', f1_score(y_test, rf_preds))"))

# 9. XGBoost/LightGBM model
cells.append(nbf.v4.new_markdown_cell("## 9. XGBoost/LightGBM model\nCompare with gradient boosting (using XGBoost here)."))
cells.append(nbf.v4.new_code_cell("import xgboost as xgb\n\nxgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)\nxgb_model.fit(X_train, y_train)\nxgb_preds = xgb_model.predict(X_test)\nxgb_probs = xgb_model.predict_proba(X_test)[:, 1]\nprint('XGBoost F1:', f1_score(y_test, xgb_preds))"))

# 10. Model evaluation
cells.append(nbf.v4.new_markdown_cell("## 10. Model evaluation\nDetailed evaluation of the best model (XGBoost). Focus on Precision/Recall and False Positives."))
cells.append(nbf.v4.new_code_cell("from sklearn.metrics import precision_recall_curve, auc\n\nprint('--- XGBoost Evaluation ---')\nprint('Accuracy:', accuracy_score(y_test, xgb_preds))\nprint('Precision:', precision_score(y_test, xgb_preds))\nprint('Recall:', recall_score(y_test, xgb_preds))\nprint('F1-score:', f1_score(y_test, xgb_preds))\nprint('ROC-AUC:', roc_auc_score(y_test, xgb_probs))\n\nprecision, recall, _ = precision_recall_curve(y_test, xgb_probs)\npr_auc = auc(recall, precision)\nprint('PR-AUC:', pr_auc)\n\nprint('\\nConfusion Matrix:')\ncm = confusion_matrix(y_test, xgb_preds)\nsns.heatmap(cm, annot=True, fmt='d', cmap='Blues')\nplt.xlabel('Predicted')\nplt.ylabel('Actual')\nplt.show()"))

# 11. Feature importance
cells.append(nbf.v4.new_markdown_cell("## 11. Feature importance\nAnalyze which signals contribute most to the risk score."))
cells.append(nbf.v4.new_code_cell("importance = pd.DataFrame({'feature': features, 'importance': xgb_model.feature_importances_})\nimportance = importance.sort_values('importance', ascending=False)\nprint(importance.head(10))\n\nplt.figure(figsize=(10, 8))\nsns.barplot(x='importance', y='feature', data=importance.head(15))\nplt.title('Top 15 Feature Importances (XGBoost)')\nplt.show()"))

# 12. Error analysis
cells.append(nbf.v4.new_markdown_cell("## 12. Error analysis\nExamine false positives to understand why legitimate accounts might be flagged."))
cells.append(nbf.v4.new_code_cell("X_test_eval = X_test.copy()\nX_test_eval['true_label'] = y_test\nX_test_eval['pred_label'] = xgb_preds\nX_test_eval['risk_probability'] = xgb_probs\n\nfalse_positives = X_test_eval[(X_test_eval['true_label'] == 0) & (X_test_eval['pred_label'] == 1)]\nprint(f'Found {len(false_positives)} false positives.')\nif len(false_positives) > 0:\n    display(false_positives.head())"))

# 13. Save the best model
cells.append(nbf.v4.new_markdown_cell("## 13. Save the best model\nExport the model and the feature schema for FastAPI production use."))
cells.append(nbf.v4.new_code_cell("import joblib\n\nos.makedirs('../models', exist_ok=True)\nmodel_path = '../models/x_account_risk_model.pkl'\njoblib.dump(xgb_model, model_path)\n\nschema = {\n    'version': '1.0',\n    'features': features\n}\nwith open('../models/feature_schema.json', 'w') as f:\n    json.dump(schema, f, indent=4)\n    \nprint('Model and schema saved to ml/models/')"))

nb['cells'] = cells

os.makedirs('ml/notebooks', exist_ok=True)
with open('ml/notebooks/x_fake_account_detection.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook generated successfully!")
