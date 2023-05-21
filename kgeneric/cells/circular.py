"""Circular bends.

A circular bend has a constant radius.
"""

import numpy as np

from kfactory import kdb
from kfactory.kcell import KCell, LayerEnum, cell
from kfactory.utils.enclosure import LayerEnclosure
from kfactory.utils.enclosure import extrude_path

__all__ = ["bend_circular"]


@cell
def bend_circular(
    width: float,
    radius: float,
    layer: int | LayerEnum,
    enclosure: LayerEnclosure | None = None,
    theta: float = 90,
    theta_step: float = 1,
) -> KCell:
    """Circular radius bend [um].

    Args:
        width: Width of the core. [um]
        radius: Radius of the backbone. [um]
        layer: Layer index of the target layer.
        enclosure: :py:class:`kfactory.utils.Enclosure` object to describe the
            claddings.
        theta: Angle amount of the bend.
        theta_step: Angle amount per backbone point of the bend.
    """
    c = KCell()
    r = radius
    backbone = [
        kdb.DPoint(x, y)
        for x, y in [
            [np.sin(_theta / 180 * np.pi) * r, (-np.cos(_theta / 180 * np.pi) + 1) * r]
            for _theta in np.linspace(
                0, theta, int(theta // theta_step + 0.5), endpoint=True
            )
        ]
    ]

    extrude_path(
        target=c,
        layer=layer,
        path=backbone,
        width=width,
        enclosure=enclosure,
        start_angle=0,
        end_angle=theta,
    )

    c.create_port(
        name="o1",
        trans=kdb.Trans(2, False, 0, 0),
        width=int(width / c.kcl.dbu),
        layer=layer,
    )

    match theta:
        case 90:
            c.create_port(
                name="o2",
                trans=kdb.DTrans(1, False, radius, radius).to_itype(c.kcl.dbu),
                width=int(width / c.kcl.dbu),
                layer=layer,
            )
        case 180:
            c.create_port(
                name="o2",
                trans=kdb.DTrans(0, False, 0, 2 * radius).to_itype(c.kcl.dbu),
                width=int(width / c.kcl.dbu),
                layer=layer,
            )

    return c


if __name__ == "__main__":
    from kgeneric.pdk import LAYER

    c = bend_circular(width=1, radius=5, layer=LAYER.WG)
    c.draw_ports()
    c.show()
