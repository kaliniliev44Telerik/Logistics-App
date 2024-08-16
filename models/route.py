from typing import List, Optional
from models import package
from models.location import Location
from models.package_status import PackageStatus
from models.truck import Truck
from models.package import Package, DISTANCE_TABLE
from models.truck_status import Status
from datetime import date, datetime, timedelta,time
from models.route_status import RouteStatus


class Route:
    def __init__(self, id: int, locations: List[Location]):
        self._id = id
        self._locations = locations
        self._truck: Optional[Truck] = None
        self._packages: List[Package] = []
        self._current_location: Optional[Location] = None
        self._current_eta: Optional[datetime] = None
        
        self._departure_time: Optional[datetime] = None

        self._current_load = 0.0  # Current load in kg
        self._status = RouteStatus.PENDING
        self.arrival_time = None

    @property
    def arrival_time(self):
        return self.arrival_time
    @arrival_time.setter
    def arrival_time(self, value):
        self._arrival_time = value
    @property
    def status(self) -> RouteStatus:
        return self._status
    
    @status.setter
    def status(self, status: RouteStatus):
        self._status = status

    @property
    def departure_time(self) -> Optional[datetime]:
        return self._departure_time

    @departure_time.setter
    def departure_time(self, departure: datetime):
        self._departure_time = departure



    @property
    def id(self) -> int:
        return self._id
    
    @property
    def locations(self) -> List[Location]:
        return self._locations
    
    @locations.setter
    def locations(self, locations: List[Location]):
        self._locations = locations

    @property
    def truck(self) -> Optional[Truck]:
        return self._truck
    
    @truck.setter
    def truck(self, truck: Truck):
        self._truck = truck

    @property
    def packages(self) -> List[Package]:
        return self._packages
    
    @packages.setter
    def packages(self, packages: List[Package]):
        self._packages = packages

    @property
    def current_location(self) -> Optional[Location]:
        return self._current_location

    @current_location.setter
    def current_location(self, location: Location):
        self._current_location = location

    @property
    def current_eta(self) -> Optional[datetime]:
        return self._current_eta

    @current_eta.setter
    def current_eta(self, eta: datetime):
        self._current_eta = eta

    @property
    def max_capacity(self) -> float:
        """
        The maximum capacity is determined by the assigned truck.
        """
        if self._truck:
            return self._truck.capacity
        return 0.0  # No capacity if no truck is assigned

    @property
    def current_load(self) -> float:
        return self._current_load
    
    

    def has_capacity(self, package_weight: float) -> bool:
        """
        Check if the route has enough capacity to add a new package.
        """
        return (self._current_load + package_weight) <= self.max_capacity

    def assign_package(self, package: Package):
        """
        Assign a package to the route if there is enough capacity.
        """
        if not self._truck:
            raise ValueError("Cannot assign package to a route with no truck assigned.")
        
        if not self.has_capacity(package.weight):
            raise ValueError("Route cannot accept this package: capacity exceeded.")
        
        if package.id in [p.id for p in self._packages]:
            raise ValueError("Package is already assigned to this route.")
        
        package.pack_status = PackageStatus.OUTFORDELIVERY
        self._packages.append(package)
        self._current_load += package.weight


    def assign_truck(self, truck: Truck):
        if truck.is_free != Status.AVAILABLE:
            raise ValueError("Truck is not available.")
        self._truck = truck
        self._current_load = 0.0  # Reset load since we're assigning a new truck

    def update_current_location(self, location: Location, eta: datetime):
        self._current_location = location
        self._current_eta = eta

    
   
        