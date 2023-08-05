from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from random import uniform, randint
from uuid import uuid4

import jinete as jit

if TYPE_CHECKING:
    from typing import (
        Set,
        Type,
        Optional,
    )


def generate_one_surface(*args, **kwargs) -> jit.Surface:
    kwargs["metric"] = jit.DistanceMetric.MANHATTAN
    return jit.GeometricSurface(*args, **kwargs)


def generate_surfaces(n: int, *args, **kwargs) -> Set[jit.Surface]:
    return {generate_one_surface(*args, **kwargs) for _ in range(n)}


def generate_one_position(
    x_min: float = -100,
    x_max: float = 100,
    y_min: float = -100,
    y_max: float = 100,
    surface: jit.Surface = None,
    *args,
    **kwargs,
) -> jit.Position:
    if surface is None:
        surface = generate_one_surface(*args, **kwargs)

    return surface.get_or_create_position([uniform(x_min, x_max), uniform(y_min, y_max)])


def generate_positions(n: int, surface: jit.Surface = None, *args, **kwargs) -> Set[jit.Position]:
    if surface is None:
        surface = generate_one_surface(*args, **kwargs)
    kwargs["surface"] = surface
    return {generate_one_position(*args, **kwargs) for _ in range(n)}


def generate_one_trip(
    identifier: str = None,
    origin_position: jit.Position = None,
    destination_position: jit.Position = None,
    earliest: float = None,
    earliest_min: float = 0,
    earliest_max: float = 86400,
    timeout: float = None,
    timeout_min: float = 1800,
    timeout_max: float = 7200,
    load_time: float = None,
    load_time_min: float = 300,
    load_time_max: float = 900,
    capacity: float = None,
    capacity_min: int = 1,
    capacity_max: int = 3,
    *args,
    **kwargs,
) -> jit.Trip:
    if identifier is None:
        identifier = f"{randint(1, 999):0d}"
    if origin_position is None:
        origin_position = generate_one_position(*args, **kwargs)
    if destination_position is None:
        destination_position = generate_one_position(*args, **kwargs)
    if earliest is None:
        earliest = uniform(earliest_min, earliest_max)
    if timeout is None:
        timeout = uniform(timeout_min, timeout_max)
    if capacity is None:
        capacity = randint(capacity_min, capacity_max)
    if load_time is None:
        load_time = uniform(load_time_min, load_time_max)

    return jit.Trip(
        identifier,
        origin=jit.Service(position=origin_position, earliest=earliest, latest=earliest + timeout, duration=load_time,),
        destination=jit.Service(position=destination_position,),
        capacity=capacity,
    )


def generate_trips(n: int, *args, **kwargs) -> Set[jit.Trip]:
    return {generate_one_trip(str(i), *args, **kwargs) for i in range(n)}


def generate_one_job(
    trips_count: int = None,
    trips_count_min: int = 1,
    trips_count_max: int = 100,
    objective_cls: Optional[Type[jit.Objective]] = None,
    *args,
    **kwargs,
) -> jit.Job:
    if trips_count is None:
        trips_count = randint(trips_count_min, trips_count_max)
    if objective_cls is None:
        objective_cls = jit.DialARideObjective

    trips = generate_trips(trips_count, *args, **kwargs)
    job = jit.Job(trips, objective_cls)
    return job


def generate_one_planning(
    routes_count: int = None, routes_count_min: int = 1, routes_count_max: int = 100, *args, **kwargs
) -> jit.Planning:
    if routes_count is None:
        routes_count = randint(routes_count_min, routes_count_max)
    trips = generate_routes(routes_count, *args, **kwargs)
    planning = jit.Planning(trips)
    return planning


def generate_jobs(n: int, *args, **kwargs) -> Set[jit.Job]:
    return {generate_one_job(*args, **kwargs) for _ in range(n)}


def generate_one_planned_trip(
    feasible: bool,
    vehicle: jit.Vehicle = None,
    previous_stop: jit.Stop = None,
    pickup_stop: jit.Stop = None,
    delivery_stop: jit.Stop = None,
    origin_position: jit.Position = None,
    destination_position: jit.Position = None,
    *args,
    **kwargs,
) -> jit.PlannedTrip:
    if vehicle is None:
        vehicle = generate_one_vehicle()
    if previous_stop is None:
        previous_stop = jit.Stop(vehicle, vehicle.origin_position, previous_stop)

    if feasible:
        kwargs["earliest"] = 0.0
        kwargs["timeout"] = float("inf")
        kwargs["capacity"] = vehicle.capacity
    else:
        previous_stop.starting_time = jit.MAX_FLOAT

    if origin_position is None:
        origin_position = generate_one_position()

    if destination_position is None:
        destination_position = generate_one_position()

    if pickup_stop is None:
        pickup_stop = jit.Stop(vehicle, origin_position, previous_stop)
    else:
        origin_position = pickup_stop.position

    if delivery_stop is None:
        delivery_stop = jit.Stop(vehicle, destination_position, pickup_stop)
    else:
        destination_position = delivery_stop.position

    trip = generate_one_trip(
        origin_position=origin_position, destination_position=destination_position, *args, **kwargs,
    )

    return jit.PlannedTrip(vehicle=vehicle, trip=trip, pickup=pickup_stop, delivery=delivery_stop,)


def generate_one_vehicle(
    capacity_min: int = 1,
    capacity_max: int = 3,
    earliest_min: float = 0,
    earliest_max: float = 86400,
    timeout: float = None,
    timeout_min: float = 14400,
    timeout_max: float = 28800,
    idx: int = 0,
    *args,
    **kwargs,
) -> jit.Vehicle:
    # TODO: Increase parameter options.
    capacity = randint(capacity_min, capacity_max)
    position = generate_one_position(*args, **kwargs)
    earliest = uniform(earliest_min, earliest_max)
    if timeout is None:
        timeout = uniform(timeout_min, timeout_max)
    latest = earliest + timeout

    origin = jit.Service(position=position, earliest=earliest, latest=latest)
    return jit.Vehicle(str(idx), origin, capacity=capacity)


def generate_vehicles(n: int, *args, **kwargs) -> Set[jit.Vehicle]:
    vehicles = set()
    for idx in range(n):
        kwargs["idx"] = idx
        vehicle = generate_one_vehicle(*args, **kwargs)
        vehicles.add(vehicle)
    return vehicles


def generate_one_route(
    feasible: bool = True,
    planned_trips_count: int = None,
    planned_trips_min: int = 1,
    planned_trips_max: int = 20,
    surface: jit.Surface = None,
    *args,
    **kwargs,
) -> jit.Route:
    if surface is None:
        surface = generate_one_surface(*args, **kwargs)
    if feasible:
        kwargs["timeout"] = float("inf")

    vehicle = generate_one_vehicle(surface=surface, *args, **kwargs)
    route = jit.Route(vehicle)

    if planned_trips_count is None:
        planned_trips_count = randint(planned_trips_min, planned_trips_max)

    for i in range(planned_trips_count):
        planned_trip = generate_one_planned_trip(
            feasible=feasible, vehicle=vehicle, previous_stop=route.current_stop, surface=surface,
        )

        route.append_planned_trip(planned_trip)
    return route


def generate_routes(n: int, *args, **kwargs) -> Set[jit.Route]:
    return {generate_one_route(*args, **kwargs) for _ in range(n)}


def generate_one_loader() -> Type[jit.Loader]:
    file_path = Path(__file__).parent / "res" / "problem-4.txt"

    class MyLoader(jit.FileLoader):
        def __init__(self):
            super().__init__(
                file_path=file_path, formatter_cls=jit.CordeauLaporteLoaderFormatter,
            )

    return MyLoader


def generate_one_result():
    from pathlib import Path

    file_path = Path(__file__).parents[1] / "res" / "datasets" / "hashcode" / "a_example.in"

    class MyLoader(jit.FileLoader):
        def __init__(self, *args, **kwargs):
            super().__init__(
                file_path=file_path, formatter_cls=jit.HashCodeLoaderFormatter, *args, **kwargs,
            )

    class MyAlgorithm(jit.InsertionAlgorithm):
        def __init__(self, *args, **kwargs):
            super().__init__(
                neighborhood_max_size=None, criterion_cls=jit.HashCodeRouteCriterion, *args, **kwargs,
            )

    dispatcher = jit.StaticDispatcher(MyLoader, MyAlgorithm,)
    result = dispatcher.run()

    return result
