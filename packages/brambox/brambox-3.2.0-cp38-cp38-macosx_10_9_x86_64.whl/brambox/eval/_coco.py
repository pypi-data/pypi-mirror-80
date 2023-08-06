#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   Functions for computing coco statistics
#   https://github.com/cocodataset/cocoapi
#
import logging
from statistics import mean
from tqdm.auto import tqdm as _tqdm
import pandas as pd
from .. import stat

__all__ = ['COCO']
log = logging.getLogger(__name__)


class COCO:
    """ Computes the Average Precision values as defined in `COCO <cocoapi_>`_. |br|
    This class caches results when computing them, so acessing them a second time is instant.

    Args:
        detection (pd.DataFrame): brambox detection dataframe
        annotation (pd.DataFrame): brambox annotation dataframe
        max_det (int, optional): Maximum number of detections per image (set to **None** to disable); Default **100**
        tqdm (bool, optional): Whether to show a progress bar with tqdm; Default **True**

    Example:
        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> coco = bb.eval.COCO(det, anno)
        >>> print(coco.mAP)
        mAP_50        0.636573
        mAP_75        0.446958
        mAP_coco      0.412408
        mAP_small     0.191750
        mAP_medium    0.392910
        mAP_large     0.518912

        If you only want to compute a few of the mAP values.

        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> coco = bb.eval.COCO(det, anno)
        >>> print(coco.compute(map_50=True, map_75=True, map_coco=True))
        mAP_50        0.636573
        mAP_75        0.446958
        mAP_coco      0.412408

        You can also access specific mAP values directly,
        but if you need multiple values it is more efficient to use compute.

        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> coco = bb.eval.COCO(det, anno)
        >>> print(coco.mAP_75)
        0.446958
        >>> print(coco.mAP_small)
        0.191750
        >>> # Faster alternative
        >>> print(coco.compute(map_75=True, map_small=True))
        mAP_75        0.446958
        mAP_small     0.191750
        >>> # After using compute, using the properties is "instant" as the results are cached
        >>> print(coco.mAP_75)
        0.446958

        You can also acess the underlying AP values for each class independently

        >>> anno = bb.io.load(...)
        >>> det = bb.io.load(...)
        >>> coco = bb.eval.COCO(det, anno)
        >>> print(coco.AP_75)
        carrot      0.215381
        boat        0.262389
        train       0.688132
        keyboard    0.537184
        sink        0.378610

    Warning:
        Compared to the pycocotools, the area is computed differently here. |br|
        In pycocotools, they compute the area of the annotations as the area of the segmentation mask
        as opposed to the area of the bounding box, which is used here.
    """
    iou_range = [iou/100 for iou in (range(50, 100, 5))]    #: IoU range for AP_coco, AP_small, AP_medium and AP_large
    areas = {
        'small':    [None, 32**2],
        'medium':   [32**2, 96**2],
        'large':    [96**2, None],
    }                                                       #: Different area ranges for AP_small, AP_medium and AP_large

    def __init__(self, detection, annotation, max_det=100, tqdm=True):
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

        # Compute areas
        self.detection['area'] = self.detection.width * self.detection.height
        self.annotation['area'] = self.annotation.width * self.annotation.height

        # Get class labels
        self.class_label = set(list(self.annotation.class_label.unique()) + list(self.detection.class_label.unique()))
        if len(self.class_label) != self.annotation.class_label.nunique() or len(self.class_label) != self.detection.class_label.nunique():
            log.warn('Annotations and Detections do not contain the same class labels!')

        # Initialize private fields
        self._ap_50 = None
        self._ap_75 = None
        self._ap_coco = None
        self._ap_small = None
        self._ap_medium = None
        self._ap_large = None

    def compute(self, map_50=False, map_75=False, map_coco=False, map_small=False, map_medium=False, map_large=False, force=False):
        """ Compute and return the different mAP values.

        Args:
            map_50 (boolean, optional): Compute the mean AP for an IoU threshold of 50%; Default **False**
            map_75 (boolean, optional): Compute the mean AP for an IoU threshold of 75%; Default **False**
            map_coco (boolean, optional): Compute the mean AP for an IoU threshold of {50%, 55%, 60%, ... 95%}; Default **False**
            map_small (boolean, optional): Compute the mean AP for an IoU threshold of {50%, 55%, 60%, ... 95%} for small objects; Default **False**
            map_medium (boolean, optional): Compute the mean AP for an IoU threshold of {50%, 55%, 60%, ... 95%} for medium objects; Default **False**
            map_large (boolean, optional): Compute the mean AP for an IoU threshold of {50%, 55%, 60%, ... 95%} for large objects; Default **False**
            force (boolean, optional): Clear the cached values and force to recompute all values; Default **False**

        Returns:
            (pd.Series): Different mAP values
        """
        result = dict()

        # Check if recompute is necessary
        if force:
            self.reset()
        else:
            if map_50 is True and self._ap_50 is not None:
                result['mAP_50'] = self._ap_50.mean(skipna=True)
                map_50 = False
            if map_75 is True and self._ap_75 is not None:
                result['mAP_75'] = self._ap_75.mean(skipna=True)
                map_75 = False
            if map_coco is True and self._ap_coco is not None:
                result['mAP_coco'] = self._ap_coco.mean(skipna=True)
                map_coco = False
            if map_small is True and self._ap_small is not None:
                result['mAP_small'] = self._ap_small.mean(skipna=True)
                map_small = False
            if map_medium is True and self._ap_medium is not None:
                result['mAP_medium'] = self._ap_medium.mean(skipna=True)
                map_medium = False
            if map_large is True and self._ap_large is not None:
                result['mAP_large'] = self._ap_large.mean(skipna=True)
                map_large = False

        # No recomputes
        if not any([map_50, map_75, map_coco, map_small, map_medium, map_large]):
            return pd.Series(result)

        # Setup dictionaries
        if map_50:
            self._ap_50 = dict()
        if map_75:
            self._ap_75 = dict()
        if map_coco:
            self._ap_coco = dict()
        if map_small:
            self._ap_small = dict()
        if map_medium:
            self._ap_medium = dict()
        if map_large:
            self._ap_large = dict()

        # Compute AP values
        cl_iter = _tqdm(self.class_label, desc='Computing AP') if self.tqdm else self.class_label
        for label in cl_iter:
            if self.tqdm:
                cl_iter.set_postfix(label=label)

            ac = self.annotation[self.annotation.class_label == label]
            dc = self.detection[self.detection.class_label == label]

            if map_50:
                self._ap_50[label] = self.compute_ap(dc, ac, [0.50])
            if map_75:
                self._ap_75[label] = self.compute_ap(dc, ac, [0.75])
            if map_coco:
                self._ap_coco[label] = self.compute_ap(dc, ac, self.iou_range)
            if map_small:
                self._ap_small[label] = self.compute_ap(dc, ac, self.iou_range, *self.areas['small'])
            if map_medium:
                self._ap_medium[label] = self.compute_ap(dc, ac, self.iou_range, *self.areas['medium'])
            if map_large:
                self._ap_large[label] = self.compute_ap(dc, ac, self.iou_range, *self.areas['large'])

        # Create dataframes
        if map_50:
            self._ap_50 = pd.Series(self._ap_50)
            result['mAP_50'] = self._ap_50.mean(skipna=True)
        if map_75:
            self._ap_75 = pd.Series(self._ap_75)
            result['mAP_75'] = self._ap_75.mean(skipna=True)
        if map_coco:
            self._ap_coco = pd.Series(self._ap_coco)
            result['mAP_coco'] = self._ap_coco.mean(skipna=True)
        if map_small:
            self._ap_small = pd.Series(self._ap_small)
            result['mAP_small'] = self._ap_small.mean(skipna=True)
        if map_medium:
            self._ap_medium = pd.Series(self._ap_medium)
            result['mAP_medium'] = self._ap_medium.mean(skipna=True)
        if map_large:
            self._ap_large = pd.Series(self._ap_large)
            result['mAP_large'] = self._ap_large.mean(skipna=True)

        # Result
        return pd.Series(result)

    def reset(self):
        """ Remove any previously computed AP values from cache. """
        self._ap_50 = None
        self._ap_75 = None
        self._ap_coco = None
        self._ap_small = None
        self._ap_medium = None
        self._ap_large = None

    def compute_ap(self, det, anno, ious, areamin=None, areamax=None):
        """ This function does the actual AP computation for annotations and detections of a specific class_label. |br|
        This has been implemented as a separate function, so that you can inherit from this class and only overwrite this method and provide your own.

        Args:
            det (pd.DataFrame): brambox detection dataframe of only one class
            anno (pd.DataFrame): brambox detection dataframe of only one class
            ious (list of floats): Intersection over Union values between 0 and 1
            areamin (int | None, optional): Minimal area objects should have to count for the AP; Default **None**
            areamax (int | None, optional): Maximal area objects should have to count for the AP; Default **None**
        """
        # Prepare annotations
        # Existing ignore annotations are considered regions and thus are matched with IgnoreMethod.MULTIPLE
        # We set annotations whose areas dont fall within the range to ignore, but they should be matched with IgnoreMethod.SINGLE
        # This also means the pdollar criteria will compute IoA for existing ignore regions, but IoU for detections outside of range
        anno = anno.copy()
        anno['ignore_method'] = stat.IgnoreMethod.SINGLE
        anno.loc[anno.ignore, 'ignore_method'] = stat.IgnoreMethod.MULTIPLE
        if areamin is not None:
            anno.loc[anno.area < areamin, 'ignore'] = True
        if areamax is not None:
            anno.loc[anno.area > areamax, 'ignore'] = True

        # Compute matches
        # This is done separately so that we can remove detections that dont fall within the area range and are false positives
        matches = stat.match_det(det, anno, ious, class_label=False, ignore=stat.IgnoreMethod.INDIVIDUAL)

        aps = []
        li = len(ious)
        for iou in ious:
            # If multiple IoUs are selected, we need compute the PR-func for each by setting the TP/FP columns manually
            if li > 1:
                matches['tp'] = matches[f'tp-{iou}']
                matches['fp'] = matches[f'fp-{iou}']

            # Ignore any detection that did not match with an annotation and is not within the area range
            if areamin is not None:
                matches.loc[matches.area < areamin, 'fp'] = False
            if areamax is not None:
                matches.loc[matches.area > areamax, 'fp'] = False

            # Compute PR
            # The COCOAPI computes smoothed PR-curves, so we do the same
            pr = stat.pr(matches, anno, iou, smooth=True)

            # Compute AP
            # The COCOAPI computes this using an interpolated Riemann Sum.
            aps.append(stat.auc_interpolated(pr))

        return mean(aps)

    @property
    def mAP(self):
        """ Compute and return all mAP values.
        This property is basically a shorthand for the compute function with all map arguments enabled.
        """
        return self.compute(map_50=True, map_75=True, map_coco=True, map_small=True, map_medium=True, map_large=True)

    @property
    def AP_50(self):
        """ Computes and returns the AP of each class at an IoU threshold of 50%. """
        if self._ap_50 is None:
            self.compute(map_50=True)
        return self._ap_50.copy()

    @property
    def mAP_50(self):
        """ Computes and return the mAP at an IoU threshold of 50%. """
        return self.AP_50.mean(skipna=True)

    @property
    def AP_75(self):
        """ Computes and returns the AP of each class at an IoU threshold of 75%. """
        if self._ap_75 is None:
            self.compute(map_75=True)
        return self._ap_75.copy()

    @property
    def mAP_75(self):
        """ Computes and return the mAP at an IoU threshold of 75%. """
        return self.AP_75.mean(skipna=True)

    @property
    def AP_coco(self):
        """ Computes and returns the averaged AP of each class at an IoU threshold of {50%, 55%, 60%, ..., 95%}. """
        if self._ap_75 is None:
            self.compute(map_coco=True)
        return self._ap_coco.copy()

    @property
    def mAP_coco(self):
        """ Computes and return the mAP at an IoU threshold of {50%, 55%, 60%, ..., 95%}. """
        return self.AP_coco.mean(skipna=True)

    @property
    def AP_small(self):
        """ Computes and returns the averaged AP of each class at an IoU threshold of {50%, 55%, 60%, ..., 95%},
        while only considering small objects: :math:`area < 32^2`.
        """
        if self._ap_small is None:
            self.compute(map_small=True)
        return self._ap_small.copy()

    @property
    def mAP_small(self):
        """ Computes and return the mAP at an IoU threshold of {50%, 55%, 60%, ..., 95%},
        while only considering small objects: :math:`area < 32^2`.
        """
        return self.AP_small.mean(skipna=True)

    @property
    def AP_medium(self):
        """ Computes and returns the averaged AP of each class at an IoU threshold of {50%, 55%, 60%, ..., 95%},
        while only considering medium objects: :math:`32^2 < area < 96^2`.
        """
        if self._ap_medium is None:
            self.compute(map_medium=True)
        return self._ap_medium.copy()

    @property
    def mAP_medium(self):
        """ Computes and return the mAP at an IoU threshold of {50%, 55%, 60%, ..., 95%},
        while only considering medium objects: :math:`32^2 < area < 96^2`.
        """
        return self.AP_medium.mean(skipna=True)

    @property
    def AP_large(self):
        """ Computes and returns the averaged AP of each class at an IoU threshold of {50%, 55%, 60%, ..., 95%},
        while only considering large objects: :math:`area > 96^2`.
        """
        if self._ap_large is None:
            self.compute(map_large=True)
        return self._ap_large.copy()

    @property
    def mAP_large(self):
        """ Computes and return the mAP at an IoU threshold of {50%, 55%, 60%, ..., 95%},
        while only considering large objects: :math:`area > 96^2`.
        """
        return self.AP_large.mean(skipna=True)
