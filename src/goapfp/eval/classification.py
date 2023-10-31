import numpy as np
import numpy.typing as npt
from typing import List, Dict
from sklearn.metrics._ranking import _binary_clf_curve
from sklearn.metrics import auc


def _calculate_metrics(
        prediction: npt.NDArray,
        labels: npt.NDArray,
        metrics: List[str] = ["auroc", "aupr", "f_max"]) -> Dict:
    assert prediction.shape == labels.shape
    assert len(metrics) > 0
    res = {}
    N = np.prod(labels.shape)
    dat = np.zeros((N, 2))
    dat[:, 0] = prediction.flatten()
    dat[:, 1] = labels.flatten()
    dat = dat[dat[:, 0].argsort()]

    qty_pos = np.sum(dat[:, 1] > 0)
    qty_neg = N - qty_pos

    # threshold list
    th_list, idx = np.unique(dat[:, 0], return_index=True)

    qty_pos = np.sum(dat[:, 1] > 0)
    qty_neg = N - qty_pos

    n_steps = len(th_list)
    if qty_pos * qty_neg == 0 or n_steps < 2:
        if "auroc" in metrics:
            res["auroc"] = 0.5
        if "aupr" in metrics:
            res["aupr"] = qty_pos / N
        if "f_max" in metrics:
            res["f_max"] = 0.0
        return res

    FP, TP, TH = _binary_clf_curve(dat[:, 1], dat[:, 0], pos_label=1.0)
    # TN = qty_neg - FP
    FN = qty_pos - TP

    FPR = FP / qty_neg
    TPR = TP / qty_pos

    rec = TP / (TP + FN)
    pre = TP / (TP + FP)

    if "auroc" in metrics:
        res["auroc"] = auc(FPR, TPR)
    if "aupr" in metrics:
        res["aupr"] = auc(rec, pre)
    if "f_max" in metrics:
        res["f_max"] = np.max(2.0 * (np.multiply(pre, rec)) /
                              (pre + rec + np.finfo(np.double).tiny))

    return res


def _calculate_s_min(
        prediction: npt.NDArray,
        labels: npt.NDArray,
        ic: npt.NDArray | float) -> float:
    assert prediction.shape == labels.shape
    if isinstance(ic, float):
        assert ic >= 0
    else:
        assert ic.shape[0] == prediction.shape[0]
    smin = np.inf
    ths, idx = np.unique(prediction, return_index=True)
    for th in ths:
        FN = ((prediction < th) & (labels > 0)).astype(np.float32)
        FP = ((prediction >= th) & (labels < 1)).astype(np.float32)
        ru = np.sum(FN * ic)/labels.shape[0]
        mi = np.sum(FP * ic)/labels.shape[0]
        s = np.sqrt(ru**2 + mi**2)
        if s < smin:
            smin = s
    return smin


def per_gene(prediction: npt.NDArray,
             labels: npt.NDArray,
             metrics: List[str] = ["auroc", "aupr", "f_max", "s_min"],
             information_content: npt.NDArray | None = None) -> Dict:
    """
    given a prediction and real labels, calculates multiple classification
    metrics on a per-gene basis. For improved performance.

    Parameters
    ----------

    prediction : ndarray
        float array of shape (p, t) with proteins in the rows and GO terms in
        the columns.
    labels : ndarray
        binary array of shape (p, t) with proteins in the rows and GO terms in
        the columns.
    metrics : List of str
        a list of the metrics to compute, supported metrics are:
        - `auroc` area unther the ROC curve
        - `aupr` area under the precision-recall curve
        - `f_max`
        - `s_min` semantic distance. If this is provided, `information_content`
            must be set
    information_content : ndarray, optional
        float array with shape (t,), specifying the information content of that
        term.

    Returns
    -------
    metrics : Dict
        keys are the metrics passed to this functions, and values on each key
        are a list of the computed metric for all proteins `p` in the order
        they appear in the `prediction` matrix.
    """
    assert prediction.shape == labels.shape
    if "s_min" in metrics:
        assert information_content is not None
    assert len(metrics) > 0
    metrics = {m: [] for m in metrics}

    for prot_i in range(labels.shape[0]):
        res = _calculate_metrics(prediction[prot_i, :],
                                 labels[prot_i, :],
                                 [m for m in metrics if m != "s_min"])
        for m, val in res.items():
            metrics[m].append(val)
        if "s_min" in metrics:
            metrics["s_min"].append(_calculate_s_min(prediction[prot_i, :],
                                                     labels[prot_i, :],
                                                     information_content))
    return metrics


def per_term(prediction: npt.NDArray,
             labels: npt.NDArray,
             metrics: List[str] = ["auroc", "aupr", "f_max", "s_min"],
             information_content: npt.NDArray | None = None) -> Dict:
    """
    given a prediction and real labels, calculates multiple classification
    metrics on a per-term basis.

    Parameters
    ----------

    prediction : ndarray
        float array of shape (p, t) with proteins in the rows and GO terms in
        the columns.
    labels : ndarray
        binary array of shape (p, t) with proteins in the rows and GO terms in
        the columns.
    metrics : List of str
        a list of the metrics to compute, supported metrics are:
        - `auroc` area unther the ROC curve
        - `aupr` area under the precision-recall curve
        - `f_max`
        - `s_min` semantic distance. If this is provided, `information_content`
            must be set
    information_content : ndarray, optional
        float array with shape (t,), specifying the information content of that
        term.

    Returns
    -------
    metrics : Dict
        keys are the metrics passed to this functions, and values on each key
        are a list of the computed metric for all terms `t` in the order
        they appear in the `prediction` matrix.
    """
    assert prediction.shape == labels.shape
    if "s_min" in metrics:
        assert information_content is not None
    assert len(metrics) > 0
    metrics = {m: [] for m in metrics}

    for term_i in range(labels.shape[1]):
        res = _calculate_metrics(prediction[:, term_i],
                                 labels[:, term_i],
                                 [m for m in metrics if m != "s_min"])
        for m, val in res.items():
            metrics[m].append(val)
        if "s_min" in metrics:
            metrics["s_min"].append(
                    _calculate_s_min(prediction[:, term_i],
                                     labels[:, term_i],
                                     information_content[term_i]))
    return metrics
