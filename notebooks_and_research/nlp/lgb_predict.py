import lightgbm as lgb

def predict_nlp(embedding, model_path):
    bst = lgb.Booster(model_file=model_path)
    return bst.predict([embedding])