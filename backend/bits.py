import pandas as pd

def predict_colleges(score, campus, data):
    # Filter by score
    filtered_data = data[data['Cutoff Score'] <= score]

    # Further filter by campus if specified
    if campus:
        filtered_data = filtered_data[filtered_data['Campus'] == campus]

    return filtered_data.to_dict(orient='records')
