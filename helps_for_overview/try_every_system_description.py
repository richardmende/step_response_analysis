from optimize_models import optimize_model


model_types = ['PT', 'IT']
max_order = 4  # PT1 bis PT4 / IT1 bis IT4

best_overall_score = float('inf')
best_overall_model = None
best_overall_params = None

for model_type in model_types:
    for order in range(1, max_order + 1):
        print(f"Optimizing {model_type}{order}...")
        score, params = optimize_model(model_type, order) #time_values, smoothed_values_savgol) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(f"Score: {score:.4f}, Params: {params}")
        
        if score < best_overall_score:
            best_overall_score = score
            best_overall_model = (model_type, order)
            best_overall_params = params
