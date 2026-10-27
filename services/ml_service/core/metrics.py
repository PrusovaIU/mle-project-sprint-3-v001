from prometheus_client import Counter, Histogram


PREDICTIONS_TOTAL = Counter(
    'ml_predictions_total',
    'Количество выданных предсказаний'
)


PREDICTION_ERRORS_TOTAL = Counter(
    'ml_prediction_errors_total',
    'Количество ошибок'
)


INFERENCE_DURATION = Histogram(
    'ml_inference_duration_seconds',
    'Время работы модели',
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
