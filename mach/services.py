from mach.models import ScheduleGateway, MessageGateway, PlacesGateway, \
    UserGateway, PanelActivityLog


class ServiceLayer:
    @classmethod
    def get_by_username(cls, *args, **kwargs):
        return UserGateway.get_by_username(*args, **kwargs)

    @classmethod
    def get_by_id(cls, *args, **kwargs):
        return UserGateway.get_by_id(*args, **kwargs)

    @classmethod
    def get_all_messages(cls, *args, **kwargs):
        return MessageGateway.get_last_10(*args, **kwargs)

    @classmethod
    def get_all_places(cls, *args, **kwargs):
        return PlacesGateway.get(*args, **kwargs)

    @classmethod
    def create_new_message(cls, *args, **kwargs):
        return MessageGateway.insert(*args, **kwargs)

    @classmethod
    def get_all_schedules(cls, *args, **kwargs):
        return ScheduleGateway.get_current(*args, **kwargs)

    @classmethod
    def insert_panel_activity(cls, *args, **kwargs):
        return PanelActivityLog.insert_one(*args, **kwargs)