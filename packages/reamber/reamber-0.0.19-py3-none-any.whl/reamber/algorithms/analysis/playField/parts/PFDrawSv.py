from __future__ import annotations
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj


class PFDrawSv(PFDrawable):

    def __init__(self,
                 decimalPlaces: int = 2,
                 color: str = "#4ef279",
                 xOffset: int = 0,
                 yOffset: int = 0):
        """ Draws Svs on the field, only works with maps that have svs
        :param decimalPlaces: The number of decimal places to display
        :param color: The color of the text
        :param xOffset: Padding from the right, useful if you have multiple text drawables overlapping
        :param yOffset: The offset to move the text
        """
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.decimalPlaces = decimalPlaces
        self.color = color

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """
        assert isinstance(pf.m, OsuMapObj) or isinstance(pf.m, QuaMapObj), "Only sv maps are supported."

        for sv in pf.m.svs:
            txt = f"{sv.multiplier:.{self.decimalPlaces}f}"
            w, h = pf.canvasDraw.textsize(txt)
            x = pf.canvasW - w - self.xOffset
            y = pf.canvasH - int((sv.offset - pf.start) / pf.durationPerPx) - int(h/2) - self.yOffset
            pf.canvasDraw.text(xy=(x, y),
                               text=txt,
                               fill=self.color)

        return pf
