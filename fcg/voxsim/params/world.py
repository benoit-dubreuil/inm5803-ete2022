import dataclasses

import fcg.typing


@dataclasses.dataclass(frozen=True)
class WorldParams:
    """White fiber configuration generation parameters wrapper of
    :meth:`simulator.factory.geometry_factory.geometry_factory.GeometryFactory.get_geometry_handler.

    Attributes
    ----------
    resolution : fcg.typing.Vec3i
        See the parameter :python:`resolution` of
        :meth:`simulator.factory.geometry_factory.geometry_factory.GeometryFactory.get_geometry_handler
    """

    resolution: fcg.typing.Vec3i = (1, 1, 1)
