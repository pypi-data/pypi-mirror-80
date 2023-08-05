class CustomAnalysisPlotOptions(object):
    """
    This class serves as a container to hold plotting options. It is used in the view model to configure the plot
    and will be passed down to the custom analysis method which produces the plot.
    """

    def __init__(self, restrict_interpolation, lower_power_boundary, upper_power_boundary, mark_iip2):
        self.restrict_interpolation = restrict_interpolation    # if true not all data will be used for interpolation
        self.lower_power_boundary = lower_power_boundary        # lower interpolation boundary
        self.upper_power_boundary = upper_power_boundary        # upper interpolation boundary
        self.mark_iip2 = mark_iip2 