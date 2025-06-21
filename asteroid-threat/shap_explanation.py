import shap
import matplotlib.pyplot as plt

def explain_asteroid(asteroid_name, model, features_df):
    # find the index of the asteroid using its name
    index = features_df[features_df['name'] == asteroid_name].index[0]
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(features_df)
    
    shap.initjs()
    shap.force_plot(
        explainer.expected_value[1],
        shap_values[1][index],
        features_df.iloc[index],
        matplotlib=True
    )