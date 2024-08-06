from typing import List,Optional
from location import Location
from truck import Truck
from package import Package
from status import Status
from datetime import datetime, timedelta




class Route:
    def __init__(self, id: int, locations: List[Location]):
         self._id = id
         self._locations = locations
         self._truck: Optional[Truck] = None
         self._packages: List[Package] = []
         self._current_location: Optional[Location] = None
         self._current_eta: Optional[datetime] = None

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

    def assign_truck(self, truck: Truck):
        if truck.is_free != Status.AVAILABLE:
            raise ValueError("Truck is not available.")
        self._truck = truck
        # truck.is_free = Status.BUSY.value

    def assign_package(self, package: Package):
        if package.id_pack in [p.id_pack for p in self._packages]:
            raise ValueError("Package is already assigned to this route.")
        self._packages.append(package)

    def update_current_location(self, location: Location, eta: datetime):
        self._current_location = location
        self._current_eta = eta


    def check_and_unload_packages(self):
        if self._current_location is None or self._current_eta is None:
            return "Current location or ETA not set."

        delivered_packages = []
        current_time = datetime.now()

        if current_time >= self._current_eta:
            for package in self._packages:
                if package.end_location == self._current_location.name:
                    package.is_delivered = True
                    
            
            for package in delivered_packages:
                self._packages.remove(package)
        
        if delivered_packages:
            return f"Delivered packages at {self._current_location.name}: {[package.id_pack for package in delivered_packages]}"
        else:
            return f"No packages delivered at {self._current_location.name}."
