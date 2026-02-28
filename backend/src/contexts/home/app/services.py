# src/contexts/home/app/services.py


from src.contexts.locations.app.services import get_default_location, list_locations
from src.contexts.locations.infra.repo import SqlLocationRepository

# from src.contexts.observations.app.services import get_latest_or_fetch
# from src.contexts.observations.infra.repo import SqlObservationRepository  # 이 클래스가 있다면

def get_home_view():
    location_repo = SqlLocationRepository()

    default_loc = get_default_location(location_repo)
    locations = list_locations(location_repo)

    
    observations = None
    # if default_loc:
    #    observation_repo = SqlObservationRepository()  # 있다면
    #    observations = get_latest_or_fetch(observation_repo, default_loc.id)
    

    return {
        "default_location": default_loc,
        "observations": observations,
        "locations": locations,
    }