import sys
import logging
import time
import data_generation as dgen
import numpy as np
import asgl
import metrics_computation as mc

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    start_time = time.time()

    data_equal = dgen.EqualGroupSize(n_obs=5200, ro=0.2, error_distribution='student_t',
                                     e_df=5, random_state=1, group_size=10, non_zero_groups=7,
                                     non_zero_coef=5, num_groups=15)

    x, y, beta, group_index = data_equal.data_generation().values()

    logging.info('solving adaptive model')
    lambda1 = 10.0 ** np.arange(-3, 1.51, 0.1)
    tvt_alasso = asgl.TVT(model='lm', penalization='alasso', lambda1=lambda1, parallel=False,
                          weight_technique='pca_pct', variability_pct=0.9, error_type='MSE',
                          random_state=1, train_size=100, validate_size=100)
    alasso_result = tvt_alasso.train_validate_test(x=x, y=y)
    alasso_prediction_error = alasso_result['test_error']
    alasso_betas = alasso_result['optimal_betas'][1:]  # Remove intercep
    logging.info('adaptive model solved. Starting metrics computation')

    metrics_object = mc.MetricsComputation(metrics=['true_positive_rate', 'false_negative_rate', 'true_negative_rate',
                                                    'false_positive_rate', 'precision', 'f_score',
                                                    'correct_selection_rate', 'beta_error', 'number_positives',
                                                    'store_beta'])
    metrics = metrics_object.fit(predicted_beta=alasso_betas, true_beta=beta)

    end_time = time.time()
    execution_time = np.round(end_time - start_time, 2)
    logging.info(f'Computations finished with no error.\nExecution time = {execution_time} seconds')

###################################################
