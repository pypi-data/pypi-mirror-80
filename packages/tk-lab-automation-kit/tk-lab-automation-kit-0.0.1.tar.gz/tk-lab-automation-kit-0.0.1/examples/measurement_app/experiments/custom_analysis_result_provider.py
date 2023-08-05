class CustomAnalysisResultProvider(object):
    """
    This class is a container that holds variables to propagate important values from the custom analysis function
    to the view.
    """

    def __init__(self):
        self.IIP3 = None            # slot for displaying the calculated IIP3 point
        self.OIP3 = None            # slot for displaying the calculated OIP3 point
        self.min_IM3Ord12 = None    # slot for displaying the measured minimum power of the IM3Ord12
        self.min_f1 = None          # slot for displaying the measured minimum power of the f1
        self.min_f2 = None          # slot for displaying the measured minimum power of the f2
        self.min_IM3Ord21 = None    # slot for displaying the measured minimum power of the IM3Ord21
        self.min_H2Ord1 = None      # slot for displaying the measured minimum power of the H2Ord1
        self.min_IM2Ord12 = None    # slot for displaying the measured minimum power of the IM2Ord12
        self.min_H2Ord2 = None      # slot for displaying the measured minimum power of the H2Ord2
        self.max_IM3Ord12 = None    # slot for displaying the measured maximum power of the IM3Ord12
        self.max_f1 = None          # slot for displaying the measured maximum power of the f1
        self.max_f2 = None          # slot for displaying the measured maximum power of the f2
        self.max_IM3Ord21 = None    # slot for displaying the measured maximum power of the IM3Ord21
        self.max_H2Ord1 = None      # slot for displaying the measured maximum power of the H2Ord1
        self.max_IM2Ord12 = None    # slot for displaying the measured maximum power of the IM2Ord12
        self.max_H2Ord2 = None      # slot for displaying the measured maximum power of the H2Ord2