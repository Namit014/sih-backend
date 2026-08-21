# GEMINI.md — X Fake Account Detection Project

## 0. Purpose

You are the primary coding assistant for this project.

Build a production-ready MVP for detecting suspicious/anomalous X accounts using data from the official X API, feature engineering, and machine learning.

The system must NOT claim that a person is definitively fake. It produces an Account Risk Score and explains the signals contributing to that score.

Priorities:
1. Accuracy and correctness
2. Clean architecture
3. Reproducibility
4. Security
5. Minimal unnecessary complexity
6. Clear documentation
7. Easy handoff between ML and backend developers

Do not add technologies just because they are popular. Every dependency must have a reason.

---

## 1. Product Definition

User flow:

```text
User enters X username/profile URL
        ↓
FastAPI backend
        ↓
Official X API
        ↓
User profile + accessible posts
        ↓
Normalize raw data
        ↓
Feature extraction
        ↓
ML model
        ↓
Risk probability / score
        ↓
Gemini explanation
        ↓
Frontend result
```

Output:
- Account information
- Risk score: 0–100
- Risk level
- Main suspicious/anomalous signals
- Model probability where appropriate
- Human-readable explanation

Use wording such as:
> This account shows several suspicious behavioral signals.

Never say:
> This person is fake.

---

## 2. Preferred Tech Stack

### Frontend
- Next.js
- TypeScript
- React
- Tailwind CSS

### Backend
- Python
- FastAPI
- Pydantic
- httpx

### X integration
- Official X API
- Server-side authentication only

### Database
- PostgreSQL
- Supabase is acceptable

### Machine Learning
Research:
- Jupyter Notebook
- pandas
- NumPy
- scikit-learn

Candidate models:
- Logistic Regression
- Random Forest
- XGBoost
- LightGBM

Do not assume XGBoost is automatically best. Compare models using validation results.

### LLM
- Gemini API

Gemini is an explanation layer, NOT the primary classifier.

### Optional later
- Redis
- Background workers
- Object storage
- Network analysis
- Computer vision

Do not add these to V1 unless there is a concrete requirement.

---

## 3. What We Do NOT Need

Do NOT introduce these into the core V1:
- RAG
- Qdrant
- Pinecone
- Vector databases
- Embedding pipelines
- Kafka
- Kubernetes
- Microservices
- Complex agent frameworks
- Deep-learning models without evidence that they improve results

This is primarily a structured-data classification problem.

---

## 4. Repository Structure

Use this unless the existing repository has a strong reason to differ:

```text
x-fake-detection/
├── GEMINI.md
├── README.md
├── .gitignore
├── .env.example
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── API_REQUIREMENTS.md
│   └── ML_FEATURES.md
├── ml/
│   ├── notebooks/
│   │   └── x_fake_account_detection.ipynb
│   ├── dataset/
│   │   └── README.md
│   ├── models/
│   └── src/
│       ├── features.py
│       └── evaluation.py
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── analysis.py
│   │   ├── services/
│   │   │   ├── x_api.py
│   │   │   ├── feature_engineering.py
│   │   │   ├── ml_model.py
│   │   │   └── gemini.py
│   │   ├── schemas/
│   │   │   └── analysis.py
│   │   └── core/
│   │       └── config.py
│   ├── tests/
│   └── requirements.txt
└── sample_data/
    ├── sample_user.json
    └── sample_posts.json
```

Inspect the existing repository before moving or duplicating files.

---

## 5. X API Rules

Use the official X API.

Never put X API secrets in:
- frontend code
- client-side JavaScript
- Git
- README files
- notebooks
- API responses

Use environment variables:

```env
X_BEARER_TOKEN=
GEMINI_API_KEY=
DATABASE_URL=
```

Provide only `.env.example` with placeholders.

Never fabricate API fields.

The exact fields available depend on the current X endpoint and the project's access level.

If a field is unavailable:
1. Do not invent it.
2. Do not silently substitute unrelated data.
3. Return null or an explicit unavailable state.
4. Make feature extraction robust to missing data.

---

## 6. X Data Model

### User
Support:
```text
id
username
name
description
created_at
profile_image_url
followers_count
following_count
tweet_count
verified / verification indicators when available
protected when available
url when available
location when available
```

### Post
Support:
```text
id
author_id
text
created_at
public_metrics
reply information
referenced posts
entities
mentions
hashtags
urls
media indicators
language when available
```

Do not assume every account has every field.

---

## 7. Data Collection Strategy

V1 focuses on:
```text
1 user lookup
+
accessible recent/user posts
+
available public metrics
```

Do NOT make the entire follower graph mandatory.

Do NOT download huge quantities of data without a reason.

Minimize API usage and respect X API limits, pricing, and terms.

Implement pagination correctly.

Implement reasonable timeout and retry behavior.

Do not retry indefinitely.

---

## 8. Feature Engineering

Features must be reproducible.

The exact feature schema used during ML training must be identical to production inference.

Initial features:

### Profile
```text
account_age_days
followers_count
following_count
post_count
followers_following_ratio
profile_completeness
verification_indicator
```

### Activity
```text
posts_per_day
average_post_interval
posting_interval_std
reply_ratio
repost_ratio
original_post_ratio
activity_burst_score
```

### Engagement
```text
average_likes
average_replies
average_reposts
average_quotes
engagement_rate
engagement_variance
```

### Content
```text
duplicate_content_ratio
average_text_length
hashtag_frequency
mention_frequency
url_frequency
repeated_hashtag_ratio
```

Only implement a feature if it can be calculated reliably from available data.

---

## 9. Feature Engineering Rules

Never leak future information into training.

Avoid target leakage.

Handle division by zero safely.

Handle missing values deliberately.

Document every feature:
- feature name
- definition
- input fields
- calculation
- missing-data behavior

Keep feature order/versioned.

Example:
```text
FEATURE_SCHEMA_VERSION = "1.0"
```

Save the feature schema alongside the model.

---

## 10. ML Notebook

Create:

`ml/notebooks/x_fake_account_detection.ipynb`

Sections:
1. Problem definition
2. Dataset loading
3. Data quality
4. Exploratory analysis
5. Feature engineering
6. Train/test split
7. Baseline models
8. Candidate models
9. Evaluation
10. Error analysis
11. Explainability
12. Save model

Evaluate:
- Precision
- Recall
- F1
- ROC-AUC
- PR-AUC
- Confusion matrix

Do NOT use accuracy as the only metric.

Inspect false positives and false negatives.

Use feature importance. SHAP may be added if useful.

Export:
```text
models/x_account_risk_model.pkl
feature_schema.json
model_metadata.json
```

---

## 11. Dataset Rules

A model cannot learn reliable detection without good labels.

Clearly distinguish:
- synthetic data
- manually labeled data
- real-world labeled data

Do not claim production accuracy from synthetic data.

Track:
```text
dataset version
number of accounts
class distribution
label source
collection date
feature version
model version
```

Never hard-code an accuracy claim unless measured on an appropriate held-out dataset.

---

## 12. Model Output

Prefer probability output:

```json
{
  "risk_probability": 0.78
}
```

UI score:
```text
risk_score = probability * 100
```

Initial configurable interpretation:
```text
0–25   Low concern
26–50  Moderate
51–75  Suspicious
76–100 High risk
```

These thresholds are experimental and must be validated.

---

## 13. FastAPI

Create:

```text
POST /api/analyze
```

Request:
```json
{
  "username": "example"
}
```

Response:
```json
{
  "account": {
    "username": "example",
    "name": "...",
    "followers": 1200,
    "following": 450
  },
  "risk": {
    "score": 78,
    "probability": 0.78,
    "level": "high"
  },
  "signals": [
    "High posting frequency",
    "High repetitive-content ratio"
  ],
  "explanation": "..."
}
```

Use Pydantic response models.

Validate usernames/profile URLs.

Return appropriate HTTP errors.

Do not expose credentials.

---

## 14. Service Separation

### x_api.py
Only:
- X authentication
- X requests
- pagination
- response normalization
- API error handling

### feature_engineering.py
Only:
- normalized data → feature vector

### ml_model.py
Only:
- load model
- validate feature schema
- run inference

### gemini.py
Only:
- prepare explanation input
- call Gemini
- return explanation

### analysis.py
Orchestrates:
```text
X API
→ normalization
→ feature extraction
→ ML inference
→ Gemini explanation
```

Do not put everything in `main.py`.

---

## 15. Gemini Rules

Gemini is NOT the detector.

The ML model produces the risk probability.

Gemini explains the result.

Gemini should receive structured evidence, for example:

```json
{
  "risk_score": 78,
  "risk_level": "high",
  "signals": [
    {
      "feature": "posts_per_day",
      "value": 20.0
    },
    {
      "feature": "duplicate_content_ratio",
      "value": 0.38
    }
  ]
}
```

Gemini must:
- never invent evidence
- never claim certainty
- never say a person is fake
- explain only supplied signals
- use cautious language
- stay concise

If Gemini fails, the ML risk result must still work.

---

## 16. Security

Never commit:
```text
.env
API keys
Bearer tokens
Gemini keys
database passwords
private credentials
```

Use `.env` locally and `.env.example` for documentation.

`.env` must be in `.gitignore`.

Validate external inputs.

Do not log secrets or authorization headers.

---

## 17. Testing

Create:
```text
tests/
├── test_x_api.py
├── test_features.py
├── test_ml_model.py
├── test_gemini.py
└── test_analysis.py
```

Test:
- valid username
- invalid username
- missing fields
- empty post list
- zero followers
- zero following
- missing metrics
- API failure
- rate limiting
- ML model unavailable
- Gemini failure

The system should still return the ML result if Gemini is unavailable.

---

## 18. Error Handling

One external service failure must not unnecessarily crash the whole application.

```text
X API failure
→ useful API error

ML failure
→ analysis failure

Gemini failure
→ risk score + explanation unavailable
```

Gemini is optional to the core result.

---

## 19. Development Workflow

Before coding:
1. Inspect the existing repository.
2. Read GEMINI.md.
3. Identify existing architecture.
4. Avoid duplicate files/services.
5. Check package versions.
6. Make a short implementation plan.
7. Implement the smallest complete change.
8. Run tests.
9. Fix errors.
10. Update documentation if architecture changed.

Do not rewrite unrelated code.

Do not install packages without a reason.

---

## 20. Token-Efficiency Rules

Do NOT scan the entire repository for every request.

Read first:
```text
GEMINI.md
README.md
relevant source files
```

Only inspect files needed for the current task.

Ignore:
```text
node_modules/
.venv/
venv/
.git/
.next/
dist/
build/
__pycache__/
large datasets/
model binaries/
```

Do not repeatedly reread unchanged files.

When complete, summarize:
```text
Changed:
- ...

Tested:
- ...

Remaining:
- ...
```

---

## 21. Git Rules

Use small logical commits:

```text
feat: add X user lookup
feat: add post retrieval
feat: add feature extraction
feat: add ML inference
feat: add Gemini explanation
test: add feature engineering tests
fix: handle missing X metrics
```

Never commit secrets.

---

## 22. Definition of Done

A feature is complete only when:
- Code is implemented.
- Validation works.
- Error handling exists.
- Tests pass.
- No secrets are exposed.
- Documentation is updated if needed.
- Existing functionality still works.

For ML features:
- feature definition is documented
- training/inference use the same schema
- evaluation metrics are recorded
- model version is recorded
- dataset source/version is recorded

---

## 23. MVP Priority

Build in this order:

```text
PHASE 1
X API
↓
Get one user
↓
Get accessible user posts

PHASE 2
Normalize data
↓
Feature engineering

PHASE 3
Jupyter ML notebook
↓
Dataset
↓
Model comparison
↓
Evaluation
↓
Export model

PHASE 4
FastAPI inference
↓
Load model
↓
Return risk score

PHASE 5
Gemini explanation

PHASE 6
Frontend dashboard

PHASE 7
Improved dataset + model

PHASE 8
Optional network/cross-platform analysis
```

---

## 24. Golden Rule

Do not over-engineer V1.

The first successful milestone is:

```text
X username
   ↓
X API
   ↓
real account data
   ↓
features
   ↓
trained model
   ↓
risk score
   ↓
Gemini explanation
```

If this pipeline works reliably end-to-end, improve the model and dataset before adding complex infrastructure.

Do not add RAG, vector databases, agents, distributed systems, or complex infrastructure unless a measured product requirement justifies them.
