def get_model_explainability_weights(risk_level: str) -> dict:
    """
    Computes explainability feature weight attributions for predictions.
    """
    if risk_level == "High":
        return {
            "Offense History Frequency": 55.0,
            "Network Co-offending Centrality": 25.0,
            "Severity Index of Offenses": 15.0,
            "Offender Age Weight": 5.0
        }
    return {
        "Offense History Frequency": 30.0,
        "Network Co-offending Centrality": 20.0,
        "Severity Index of Offenses": 40.0,
        "Offender Age Weight": 10.0
    }
