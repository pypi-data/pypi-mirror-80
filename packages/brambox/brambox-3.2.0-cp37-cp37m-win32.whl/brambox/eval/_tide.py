#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   Functions for computing tide statistics
#   https://github.com/dbolya/tide
#
import logging
import numpy as np
import pandas as pd
from tqdm.auto import tqdm as _tqdm
from .. import stat
from .. import util

__all__ = ['TIDE']
log = logging.getLogger(__name__)


class TIDE:
    """ Indetifies object detection errors, as defined in the `TIDE <tidecv_>`_ project. |br|
    This class caches results when computing them, so acessing them a second time is instant.

    Args:
        detection (pd.DataFrame): brambox detection dataframe
        annotation (pd.DataFrame): brambox annotation dataframe
        pos_thresh (float, optional): IoU threshold to count a detection as a true positive; Default **0.5**
        bg_thresh (float, optional): IoU threshold to count a detection as a background error (as opposed to a localisation error); Default **0.1**
        max_det (int, optional): Maximum number of detections per image (set to **None** to disable); Default **100**
        area_range(tuple of 2 numbers, optional): Area range to filter bounding boxes (See Note below); Default **None**
        tqdm (bool, optional): Whether to show a progress bar with tqdm; Default **True**

    Examples:
        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> tide = bb.eval.TIDE(det, anno)
        >>> print(tide.mdAP)
        mAP                    0.636573
        mdAP_localisation      0.067788
        mdAP_classification    0.024815
        mdAP_both              0.011547
        mdAP_duplicate         0.002132
        mdAP_background        0.040454
        mdAP_missed            0.075361
        mdAP_fp                0.166521
        mdAP_fn                0.137648

        If you only want to compute a few of the mAP values.

        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> tide = bb.eval.TIDE(det, anno)
        >>> print(tide.compute(mdep_localisation=True, mdap_classification=True, mdap_both=True))
        mdAP_localisation      0.067788
        mdAP_classification    0.024815
        mdAP_both              0.011547

        You can also access specific mAP values directly,
        but if you need multiple values it is more efficient to use compute.

        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> tide = bb.eval.TIDE(det, anno)
        >>> print(coco.mdAP_classification)
        0.024815
        >>> print(coco.mdAP_localisation)
        0.067788
        >>> # Faster alternative
        >>> print(coco.compute(mdAP_localisation=True, mdAP_classification=True))
        mdAP_localisation      0.067788
        mdAP_classification    0.024815
        >>> # After using compute, using the properties is "instant" as the results are cached
        >>> print(coco.mdAP_classification)
        0.024815

        You can also acess the underlying dAP values for each class independently

        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> coco = bb.eval.COCO(det, anno)
        >>> print(coco.dAP_duplicate)
        boat              0.003661
        umbrella          0.003789
        toaster           0.000000
        baseball glove    0.000135
        suitcase          0.001445
        cow               0.002164

        Note:
            For the case of `dAP_classification`,
            we sort the detections based on their corrected class labels and not the original class labels which were produced by the detector.

    Note:
        You can specify an minimum and maximum area to consider for detection, by using the `area_range` argument. |br|
        This works a lot like the small, medium and large area's when computing the COCO mAP.
        In fact it is so similar that this class has a `coco_areas` attribute, which you can use as area ranges:

        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> tide = bb.eval.TIDE(det, anno, area_range=bb.eval.TIDE.coco_areas['large'])
        >>> print(tide.mdAP)
        mAP                    0.770321
        mdAP_localisation      0.066165
        mdAP_classification    0.033556
        mdAP_both              0.014307
        mdAP_duplicate         0.002327
        mdAP_background        0.025024
        mdAP_missed            0.043250
        mdAP_fp                0.134258
        mdAP_fn                0.072322

    Warning:
        Since the official TIDE repo has not yet released there code to be able to filter bounding boxes on range,
        we cannot compare our code with theirs yet and thus have no way of validating our results.
    """
    coco_areas = {
        'small':    [None, 32**2],
        'medium':   [32**2, 96**2],
        'large':    [96**2, None],
    }                                                       #: Different coco area ranges which you can use with TIDE

    def __init__(self, detection, annotation, pos_thresh=0.5, bg_thresh=0.1, max_det=100, area_range=None, tqdm=True):
        self.pos_thresh = pos_thresh
        self.bg_thresh = bg_thresh
        self.area_range = area_range if area_range is not None else (None, None)
        self.tqdm = tqdm

        # Get dataframes
        self.annotation = annotation.copy()
        if max_det is not None:
            self.detection = (
                detection
                .sort_values('confidence', ascending=False)
                .groupby('image', sort=False)
                .head(max_det)
                .reset_index(drop=True)
            )
        else:
            self.detection = detection.copy()

        if area_range is not None:
            self.annotation['area'] = self.annotation.width * self.annotation.height
            self.detection['area'] = self.detection.width * self.detection.height

        # Get class labels
        self.class_label = set(list(self.annotation.class_label.unique()) + list(self.detection.class_label.unique()))
        if len(self.class_label) != self.annotation.class_label.nunique() or len(self.class_label) != self.detection.class_label.nunique():
            log.warn('Annotations and Detections do not contain the same class labels!')

        # Initialize private fields
        self._ap = None
        self._dap_loc = None
        self._dap_cls = None
        self._dap_dup = None
        self._dap_bg = None
        self._dap_both = None
        self._dap_miss = None
        self._dap_fp = None
        self._dap_fn = None
        self._err_det = None
        self._err_anno = None

    def compute(self, map=False, mdap_localisation=False, mdap_classification=False, mdap_both=False, mdap_duplicate=False, mdap_background=False, mdap_missed=False, mdap_fp=False, mdap_fn=False, errors=False, force=False):
        """ Compute and return the different mdAP values.

        Args:
            map (boolean, optional): Compute the mean AP for an IoU threshold of `self.pos_thresh` Default **False**
            mdap_localisation (boolean, optional): Compute the delta in mAP which would be added by fixing all localisation detection errors; Default **False**
            mdap_classification (boolean, optional): Compute the delta in mAP which would be added by fixing all classification detection errors; Default **False**
            mdap_both (boolean, optional): Compute the delta in mAP which would be added by fixing all detection errors that are both misclassified and mislocalised; Default **False**
            mdap_duplicate (boolean, optional): Compute the delta in mAP which would be added by fixing all duplicate detection errors; Default **False**
            mdap_background (boolean, optional): Compute the delta in mAP which would be added by fixing all background detection errors; Default **False**
            mdap_missed (boolean, optional): Compute the delta in mAP which would be added by fixing all missed annotation errors; Default **False**
            mdap_fp (boolean, optional): Compute the delta in mAP which would be added by fixing all FP errors; Default **False**
            mdap_fn (boolean, optional): Compute the delta in mAP which would be added by fixing all FN errors; Default **False**
            force (boolean, optional): Clear the cached values and force to recompute all values; Default **False**

        Returns:
            (pd.Series): Different mdAP values
        """
        result = dict()

        # Check if recompute is necessary
        if force:
            self.reset()
        else:
            if map is True and self._ap is not None:
                result['mAP'] = self._ap.mean(skipna=True)
                map = False
            if mdap_localisation is True and self._dap_loc is not None:
                result['mdAP_localisation'] = self._dap_loc.mean(skipna=True)
                mdap_localisation = False
            if mdap_classification is True and self._dap_cls is not None:
                result['mdAP_classification'] = self._dap_cls.mean(skipna=True)
                mdap_classification = False
            if mdap_both is True and self._dap_both is not None:
                result['mdAP_both'] = self._dap_both.mean(skipna=True)
                mdap_both = False
            if mdap_duplicate is True and self._dap_dup is not None:
                result['mdAP_duplicate'] = self._dap_dup.mean(skipna=True)
                mdap_duplicate = False
            if mdap_background is True and self._dap_bg is not None:
                result['mdAP_background'] = self._dap_bg.mean(skipna=True)
                mdap_background = False
            if mdap_missed is True and self._dap_miss is not None:
                result['mdAP_missed'] = self._dap_miss.mean(skipna=True)
                mdap_missed = False
            if mdap_fp is True and self._dap_fp is not None:
                result['mdAP_fp'] = self._dap_fp.mean(skipna=True)
                mdap_fp = False
            if mdap_fn is True and self._dap_fn is not None:
                result['mdAP_fn'] = self._dap_fn.mean(skipna=True)
                mdap_fn = False
            if errors is True and self._err_det is not None and self._err_anno is not None:
                errors = False

        # No recomputes
        if not any([map, mdap_localisation, mdap_classification, mdap_both, mdap_duplicate, mdap_background, mdap_missed, mdap_fp, mdap_fn, errors]):
            return pd.Series(result)

        # Setup dictionaries
        if self._ap is None:
            should_compute_ap = True
            self._ap = dict()
        else:
            should_compute_ap = False

        if mdap_localisation:
            self._dap_loc = dict()
        if mdap_classification:
            self._dap_cls = dict()
        if mdap_both:
            self._dap_both = dict()
        if mdap_duplicate:
            self._dap_dup = dict()
        if mdap_background:
            self._dap_bg = dict()
        if mdap_missed:
            self._dap_miss = dict()
        if mdap_fp:
            self._dap_fp = dict()
        if mdap_fn:
            self._dap_fn = dict()

        # Match detections and annotations
        dm, am = self.compute_matches(self.detection, self.annotation, self.pos_thresh)
        dm = dm.reset_index(drop=True)
        am = am.reset_index(drop=True)

        # Find Error Types
        if any([mdap_localisation, mdap_classification, mdap_both, mdap_duplicate, mdap_background, mdap_missed, errors]):
            err_det = util.DualGroupBy(dm, am, 'image', group_keys=False).apply(find_errors, pos_thresh=self.pos_thresh, bg_thresh=self.bg_thresh).set_index('index')
            if errors:
                tmp = err_det.drop(['anno'], axis=1).fillna(value=True).astype('int')
                tmp['none'] = 0.1
                tmp = tmp.idxmax(axis=1)
                tmp[tmp == 'none'] = pd.NA

                self._err_det = dm.drop(['tp', 'fp'], axis=1)
                self._err_det['error'] = tmp

            err_det['anno_label'] = dm.class_label
            err_det.loc[err_det.anno.notnull(), 'anno_label'] = am.class_label[err_det.anno[err_det.anno.notnull()]].values

            fn_anno = list(set(am.detection[am.detection.isnull()].index) - set(err_det.anno[err_det.anno.notnull()].unique()))
            fn_anno = np.array(fn_anno, dtype='int')
            if errors:
                tmp = np.zeros(len(self.annotation.index), dtype='bool')
                tmp[fn_anno] = True

                self._err_anno = am.drop(['detection', 'criteria'], axis=1)
                self._err_anno['error'] = tmp
                self._err_anno['error'] = self._err_anno.error.map({True: 'missed', False: pd.NA})

            am_nofn = np.ones(len(am.index), dtype='bool')
            am_nofn[fn_anno] = False
            am_nofn = am[am_nofn]

        # No recomputes
        if not any([map, mdap_localisation, mdap_classification, mdap_both, mdap_duplicate, mdap_background, mdap_missed]):
            return pd.Series(result)

        # Fix Errors
        cl_iter = _tqdm(self.class_label, desc='Fixing Errors') if self.tqdm else self.class_label
        for label in cl_iter:
            if self.tqdm:
                cl_iter.set_postfix(label=label)

            det_label_mask = dm.class_label == label
            dc = dm[det_label_mask]
            ac = am[am.class_label == label]

            # Regular AP
            if should_compute_ap:
                self._ap[label] = self.compute_ap(dc, ac, self.pos_thresh)

            # Localisation
            if mdap_localisation:
                err = err_det.loc[det_label_mask, 'localisation'].copy()
                err_null = err.isnull()
                err[err_null] = False

                dc_err = dc.copy()
                dc_err.loc[err, 'tp'] = True
                dc_err.loc[(err | err_null), 'fp'] = False
                self._dap_loc[label] = self.compute_ap(dc_err, ac, self.pos_thresh)

            # Classification
            if mdap_classification:
                # For classification errors, we need to select detections, whose fixed labels are the correct ones!
                classification_label_mask = err_det.anno_label == label
                err = err_det.loc[classification_label_mask, 'classification'].copy()
                err_null = err.isnull()
                err[err_null] = False

                dc_err = dm.loc[classification_label_mask].copy()
                dc_err.loc[err, 'tp'] = True
                dc_err.loc[(err | err_null), 'fp'] = False
                self._dap_cls[label] = self.compute_ap(dc_err, ac, self.pos_thresh)

            # Both
            if mdap_both:
                err = err_det.loc[det_label_mask, 'both']
                dc_err = dc.copy()
                dc_err.loc[err, 'fp'] = False
                self._dap_both[label] = self.compute_ap(dc_err, ac, self.pos_thresh)

            # Duplicate
            if mdap_duplicate:
                err = err_det.loc[det_label_mask, 'duplicate']
                dc_err = dc.copy()
                dc_err.loc[err, 'fp'] = False
                self._dap_dup[label] = self.compute_ap(dc_err, ac, self.pos_thresh)

            # Background
            if mdap_background:
                err = err_det.loc[det_label_mask, 'background']
                dc_err = dc.copy()
                dc_err.loc[err, 'fp'] = False
                self._dap_bg[label] = self.compute_ap(dc_err, ac, self.pos_thresh)

            # Missed
            if mdap_missed:
                ac_err = am_nofn[am_nofn.class_label == label]
                self._dap_miss[label] = self.compute_ap(dc, ac_err, self.pos_thresh)

            # FP
            if mdap_fp:
                dc_fp = dc.copy()
                dc_fp.fp = False
                self._dap_fp[label] = self.compute_ap(dc_fp, ac, self.pos_thresh)

            # FN
            if mdap_fn:
                ac_fn = ac.copy()
                ac_fn = ac_fn[~(ac_fn.detection.isnull())]
                self._dap_fn[label] = self.compute_ap(dc, ac_fn, self.pos_thresh)

        # Create dataframes
        if should_compute_ap:
            self._ap = pd.Series(self._ap)
            if map:
                result['mAP'] = self._ap.mean(skipna=True)

        if mdap_localisation:
            self._dap_loc = pd.Series(self._dap_loc) - self._ap
            result['mdAP_localisation'] = self._dap_loc.mean(skipna=True)
        if mdap_classification:
            self._dap_cls = pd.Series(self._dap_cls) - self._ap
            result['mdAP_classification'] = self._dap_cls.mean(skipna=True)
        if mdap_both:
            self._dap_both = pd.Series(self._dap_both) - self._ap
            result['mdAP_both'] = self._dap_both.mean(skipna=True)
        if mdap_duplicate:
            self._dap_dup = pd.Series(self._dap_dup) - self._ap
            result['mdAP_duplicate'] = self._dap_dup.mean(skipna=True)
        if mdap_background:
            self._dap_bg = pd.Series(self._dap_bg) - self._ap
            result['mdAP_background'] = self._dap_bg.mean(skipna=True)
        if mdap_missed:
            self._dap_miss = pd.Series(self._dap_miss) - self._ap
            result['mdAP_missed'] = self._dap_miss.mean(skipna=True)
        if mdap_fp:
            self._dap_fp = pd.Series(self._dap_fp) - self._ap
            result['mdAP_fp'] = self._dap_fp.mean(skipna=True)
        if mdap_fn:
            self._dap_fn = pd.Series(self._dap_fn) - self._ap
            result['mdAP_fn'] = self._dap_fn.mean(skipna=True)

        # Result
        return pd.Series(result)

    def reset(self):
        """ Remove any previously computed dAP values from cache. """
        self._ap = None
        self._dap_loc = None
        self._dap_cls = None
        self._dap_dup = None
        self._dap_bg = None
        self._dap_both = None
        self._dap_miss = None
        self._dap_fp = None
        self._dap_fn = None
        self._err_det = None
        self._err_anno = None

    def compute_matches(self, det, anno, iou):
        """ This function performs the actual matching of detections and annotations.
        It returns TP/FP columns for the detections and detection/criteria for the annotations. |br|
        This has been implemented as a separate function, so that you can inherit from this class and only overwrite this method and provide your own.

        Args:
            det (pd.DataFrame): brambox detection dataframe of only one class
            anno (pd.DataFrame): brambox detection dataframe of only one class
            iou (float): Intersection over Union values between 0 and 1
        """
        # Prepare annotations
        # Existing ignore annotations are considered regions and thus are matched with IgnoreMethod.MULTIPLE
        # We set annotations whose areas dont fall within the range to ignore, but they should be matched with IgnoreMethod.SINGLE
        # This also means the pdollar criteria will compute IoA for existing ignore regions, but IoU for detections outside of range
        anno = anno.copy()
        anno['ignore_method'] = stat.IgnoreMethod.SINGLE
        anno.loc[anno.ignore, 'ignore_method'] = stat.IgnoreMethod.MULTIPLE
        if self.area_range[0] is not None:
            anno.loc[anno.area < self.area_range[0], 'ignore'] = True
        if self.area_range[1] is not None:
            anno.loc[anno.area > self.area_range[1], 'ignore'] = True

        # Match annotations and detections
        # Afterwards, we filter the remaining detection boxes which are outside of the range and were not matched
        dm, am = stat.match_box(det, anno, iou, class_label=True, ignore=stat.IgnoreMethod.INDIVIDUAL)
        if self.area_range[0] is not None:
            dm.loc[dm.area < self.area_range[0], 'fp'] = False
        if self.area_range[1] is not None:
            dm.loc[dm.area > self.area_range[1], 'fp'] = False

        return dm, am

    def compute_ap(self, det, anno, iou):
        """ This function does the actual AP computation for annotations and detections of a specific class_label. |br|
        This has been implemented as a separate function, so that you can inherit from this class and only overwrite this method and provide your own.

        Args:
            det (pd.DataFrame): brambox detection dataframe of only one class, which has already been matched
            anno (pd.DataFrame): brambox detection dataframe of only one class, which has already been matched
            iou (float): Intersection over Union values between 0 and 1
        """
        return stat.auc_interpolated(stat.pr(det, anno, iou, smooth=True))

    @property
    def mdAP(self):
        """ Compute and return all mdAP values.
        This property is basically a shorthand for the compute function with all arguments enabled.
        """
        return self.compute(
            map=True,
            mdap_localisation=True,
            mdap_classification=True,
            mdap_both=True,
            mdap_duplicate=True,
            mdap_background=True,
            mdap_missed=True,
            mdap_fp=True,
            mdap_fn=True
        )

    @property
    def AP(self):
        """ Computes and returns the AP of each class at an IoU threshold of `pos_thresh`. """
        if self._ap is None:
            self.compute(map=True)
        return self._ap.copy()

    @property
    def mAP(self):
        """ Computes and return the mAP at an IoU threshold of `pos_thresh`. """
        return self.AP.mean(skipna=True)

    @property
    def dAP_localisation(self):
        """ Computes and returns the localisation dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_loc is None:
            self.compute(mdap_localisation=True)
        return self._dap_loc.copy()

    @property
    def mdAP_localisation(self):
        """ Computes and return the localisation mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_localisation.mean(skipna=True)

    @property
    def dAP_classification(self):
        """ Computes and returns the classification dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_cls is None:
            self.compute(mdap_classification=True)
        return self._dap_cls.copy()

    @property
    def mdAP_classification(self):
        """ Computes and return the classification mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_classification.mean(skipna=True)

    @property
    def dAP_both(self):
        """ Computes and returns the classification+localisation dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_both is None:
            self.compute(mdap_both=True)
        return self._dap_both.copy()

    @property
    def mdAP_both(self):
        """ Computes and return the classification+localisation mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_both.mean(skipna=True)

    @property
    def dAP_duplicate(self):
        """ Computes and returns the duplicate dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_dup is None:
            self.compute(mdap_duplicate=True)
        return self._dap_dup.copy()

    @property
    def mdAP_duplicate(self):
        """ Computes and return the duplicate mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_duplicate.mean(skipna=True)

    @property
    def dAP_background(self):
        """ Computes and returns the background dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_bg is None:
            self.compute(mdap_background=True)
        return self._dap_bg.copy()

    @property
    def mdAP_background(self):
        """ Computes and return the background mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_background.mean(skipna=True)

    @property
    def dAP_missed(self):
        """ Computes and returns the missed dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_miss is None:
            self.compute(mdap_missed=True)
        return self._dap_miss.copy()

    @property
    def mdAP_missed(self):
        """ Computes and return the missed mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_missed.mean(skipna=True)

    @property
    def dAP_fp(self):
        """ Computes and returns the FP dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_fp is None:
            self.compute(mdap_fp=True)
        return self._dap_fp.copy()

    @property
    def mdAP_fp(self):
        """ Computes and return the FP mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_fp.mean(skipna=True)

    @property
    def dAP_fn(self):
        """ Computes and returns the FN dAP of each class at an IoU threshold of `pos_thresh`. """
        if self._dap_fn is None:
            self.compute(mdap_fn=True)
        return self._dap_fn.copy()

    @property
    def mdAP_fn(self):
        """ Computes and return the FN mdAP at an IoU threshold of `pos_thresh`. """
        return self.dAP_fn.mean(skipna=True)

    @property
    def errors(self):
        """ Computes and returns the different error types. |br|
        This property returns your detection and annotation dataframe with an extra 'error' column, which explains the error type of that bounding box.
        If the bounding box is not an error, `pd.NA` is used.

        Return:
            (tuple of 2 dataframes): (det, anno)
        """
        if self._err_det is None or self._err_anno is None:
            self.compute(errors=True)
        return self._err_det.copy(), self._err_anno.copy()


def find_errors(det, anno, pos_thresh, bg_thresh):
    det_idx = det.index
    anno_idx = anno.index
    det = det.reset_index(drop=True)
    anno = anno.reset_index(drop=True)

    dl = len(det_idx)
    anno_gt = anno[~anno.ignore]
    det_unmatched = det[~det.tp]

    # Create error df
    false_list = [False] * dl
    det_errors = pd.DataFrame({
        'localisation': false_list,
        'classification': false_list,
        'both': false_list,
        'duplicate': false_list,
        'background': false_list,
        'index': det_idx,
        'anno': np.nan,
    })

    # No regular ground truth annotations -> all background errors
    if len(anno_gt.index) == 0:
        det_errors['background'] = det.fp
        return det_errors

    # Compute IoU  [len(det) x len(anno_gt)]
    same_cls = util.np_col(det, 'class_label')[:, None] == util.np_col(anno_gt, 'class_label')[None, :]
    diff_cls = ~same_cls
    used_gt = anno_gt['detection'].notnull().values[None, :]

    iou = stat.coordinates.iou(det, anno_gt)
    iou_cls = iou * same_cls
    iou_nocls = iou * diff_cls
    iou_used_cls = iou_cls * used_gt

    # Find error type
    used_gt_loc, used_gt_cls = [], []
    for d in det_unmatched.itertuples():
        # Localisation
        idx = iou_cls[d.Index, :].argmax()
        if bg_thresh <= iou_cls[d.Index, idx] <= pos_thresh:
            if pd.notnull(anno.at[idx, 'detection']) or idx in used_gt_loc:
                det_errors.at[d.Index, 'localisation'] = pd.NA
            else:
                det_errors.at[d.Index, 'localisation'] = True
                det_errors.at[d.Index, 'anno'] = anno_idx[idx]
                used_gt_loc.append(idx)
            continue

        # Class
        idx = iou_nocls[d.Index, :].argmax()
        if iou_nocls[d.Index, idx] >= pos_thresh:
            if pd.notnull(anno.at[idx, 'detection']) or idx in used_gt_cls:
                det_errors.at[d.Index, 'classification'] = pd.NA
            else:
                det_errors.at[d.Index, 'classification'] = True
                det_errors.at[d.Index, 'anno'] = anno_idx[idx]
                used_gt_cls.append(idx)
            continue

        # Duplicate
        dup_iou = iou_used_cls[d.Index, :].max()
        if dup_iou >= pos_thresh:
            det_errors.at[d.Index, 'duplicate'] = True
            continue

        # Background
        bg_iou = iou[d.Index, :].max()
        if bg_iou <= bg_thresh:
            det_errors.at[d.Index, 'background'] = True
            continue

        # Both (Any other error is labeled as both)
        det_errors.at[d.Index, 'both'] = True

    return det_errors.astype({
        'localisation': 'boolean',
        'classification': 'boolean',
        'both': 'boolean',
        'duplicate': 'boolean',
        'background': 'boolean',
        'anno': 'Int64',
    })
