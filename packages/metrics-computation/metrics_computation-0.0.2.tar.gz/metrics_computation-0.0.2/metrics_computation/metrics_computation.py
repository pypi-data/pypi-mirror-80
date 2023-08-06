import logging
import sys
import numpy as np

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MetricsComputation:
    def __init__(self, tol=1e-5, metrics=('true_positive_rate', 'true_negative_rate')):
        self.tol = tol
        self.metrics = metrics
        self.valid_metrics = ['true_positive_rate', 'false_negative_rate', 'true_negative_rate', 'false_positive_rate',
                              'precision', 'f_score', 'correct_selection_rate', 'number_positives', 'store_beta',
                              'beta_error']

    def __str__(self):
        r = f'Computation of several metrics for beta coefficients.\nPositives = coefficients different than ' \
            f'zero\nNegatives = coefficients equal to zero\nValid metrics are:\n{self.valid_metrics} '
        return r

    def _preprocessing_metrics(self):
        if isinstance(self.metrics, str):
            self.metrics = [self.metrics]
        metrics_corrected = []
        for elem in self.metrics:
            if elem not in self.valid_metrics:
                logging.warning(f'Invalid metric provided. Metric: {elem}\nValid metrics:{self.valid_metrics}\n'
                                f'Metric removed')
            else:
                metrics_corrected.append(elem)
        return metrics_corrected

    def _store_beta_one(self, beta):
        index_non_zero_beta = np.ndarray.astype(np.where(np.abs(beta) > self.tol)[0], 'int').tolist()
        val_non_zero_beta = beta[index_non_zero_beta].tolist()
        return index_non_zero_beta, val_non_zero_beta

    def _store_beta(self, predicted_beta, true_beta):
        index_non_zero_predicted_beta, value_non_zero_predicted_beta = self._store_beta_one(predicted_beta)
        index_non_zero_true_beta, value_non_zero_true_beta = self._store_beta_one(true_beta)
        result = dict(
            predicted_beta=dict(
                index_non_zero_predicted_beta=index_non_zero_predicted_beta,
                value_non_zero_predicted_beta=value_non_zero_predicted_beta),
            true_beta=dict(
                index_non_zero_true_beta=index_non_zero_true_beta,
                value_non_zero_true_beta=value_non_zero_true_beta))
        return result

    def _number_positives_one(self, beta):
        number_positives = len(np.where(np.abs(beta) > self.tol)[0])
        return number_positives

    def _number_positives(self, predicted_beta, true_beta):
        number_positives_predicted_beta = self._number_positives_one(predicted_beta)
        number_positives_true_beta = self._number_positives_one(true_beta)
        result = dict(
            number_positives_predicted_beta=number_positives_predicted_beta,
            number_positives_true_beta=number_positives_true_beta)
        return result

    # TRUE POSITIVE RATE / FALSE NEGATIVE RATE ########################################################################

    def _true_positive_rate(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: True positive rate (also called sensitivity). True positives / real positives. TPR + FNR = 1
        """
        true_positive = np.sum(np.logical_and(np.abs(true_beta) > self.tol, np.abs(predicted_beta) > self.tol))
        real_positive = np.sum(np.abs(true_beta) > self.tol)
        if real_positive == 0:
            true_positive_rate = 0
        else:
            true_positive_rate = true_positive / real_positive
        return true_positive_rate

    def _false_negative_rate(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: False negative rate. False negatives / real positives. TPR + FNR = 1
        """
        false_negative_rate = 1 - self._true_positive_rate(predicted_beta, true_beta)
        return false_negative_rate

    # TRUE NEGATIVE RATE / FALSE POSITIVE RATE ########################################################################

    def _true_negative_rate(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: True negative rate (also called specificity). True negatives / real negatives. TNR + FPR = 1
        """
        true_negative = np.sum(np.logical_and(np.abs(true_beta) <= self.tol, np.abs(predicted_beta) <= self.tol))
        real_negative = np.sum(np.abs(true_beta) <= self.tol)
        if real_negative == 0:
            true_negative_rate = 0
        else:
            true_negative_rate = true_negative / real_negative
        return true_negative_rate

    def _false_positive_rate(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: False positive rate. False negatives / real positives. TNR + FPR = 1
        """
        false_positive_rate = 1 - self._true_negative_rate(predicted_beta, true_beta)
        return false_positive_rate

    # PRECISION #######################################################################################################

    def _precision(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: Precision = (true positive) / (true positive + false positive)
        """
        true_positive = np.sum(np.logical_and(np.abs(true_beta) > self.tol, np.abs(predicted_beta) > self.tol))
        false_positive = np.sum(np.logical_and(np.abs(true_beta) <= self.tol, np.abs(predicted_beta) > self.tol))
        if (true_positive + false_positive) == 0:
            precision = 0
        else:
            precision = true_positive / (true_positive + false_positive)
        return precision

    # F SCORE #########################################################################################################

    def _f_score(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: F-score = 2*(precision * recall)/(precision + recall) where
                 precision = (true positive) / (true positive + false positive)
                 TPR = recall = (true positive) / (true positive + false negative)
        """
        precision = self._precision(predicted_beta, true_beta)
        recall = self._true_positive_rate(predicted_beta, true_beta)
        if precision+recall == 0:
            f_score = 0
        else:
            f_score = 2 * (precision * recall) / (precision + recall)
        return f_score

    # CORRECT SELECTION RATE ##########################################################################################

    def _correct_selection_rate(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: Correct selection rate: (true positive + true negative) / total number of parameters
        """
        true_positive = np.sum(np.logical_and(np.abs(true_beta) > self.tol, np.abs(predicted_beta) > self.tol))
        true_negative = np.sum(np.logical_and(np.abs(true_beta) <= self.tol, np.abs(predicted_beta) <= self.tol))
        correct_selection_rate = (true_positive + true_negative) / len(true_beta)
        return correct_selection_rate

    # BETA ERROR #####################################################################################################

    def _beta_error(self, predicted_beta, true_beta):
        """
        :param predicted_beta: Beta from a regression model
        :param true_beta: True beta
        :return: L2 norm of the difference between predicted beta and true beta
        """
        beta_error = np.linalg.norm(true_beta - predicted_beta, 2)
        return beta_error

    # FITTING METHOD #################################################################################################

    def _get_metrics_name(self, metric):
        return '_' + metric

    def fit(self, predicted_beta, true_beta):
        self._preprocessing_metrics()  # Convert metric into a list
        tmp = [(elt, getattr(self, self._get_metrics_name(elt))(predicted_beta, true_beta)) for elt in self.metrics]
        metrics_dictionary = dict(tmp)
        return metrics_dictionary
