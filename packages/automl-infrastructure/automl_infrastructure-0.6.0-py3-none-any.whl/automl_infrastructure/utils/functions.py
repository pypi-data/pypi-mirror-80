import string
from random import choice


def random_str(length, charset=string.digits):
    """returns random string with a given length."""
    return "".join(choice(charset) for _ in range(0, length))


def extract_ordered_classes(y_true_lst, classifier_prediction_lst):
    # extract all unique classes names
    unique_classes_names = []
    for j in range(len(classifier_prediction_lst)):
        for i in range(len(classifier_prediction_lst[j].classes_pred)):
            if classifier_prediction_lst[j].classes_pred[i] not in unique_classes_names:
                unique_classes_names.append(classifier_prediction_lst[j].classes_pred[i])
            if y_true_lst[j][i] not in unique_classes_names:
                unique_classes_names.append(y_true_lst[j][i])
    unique_classes_names = sorted(unique_classes_names)
    return unique_classes_names
