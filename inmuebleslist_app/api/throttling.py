from rest_framework.throttling import UserRateThrottle


class InmuebleListThrottle(UserRateThrottle):
    scope = 'inmueble-list'


class InmuebleDetalleThrottle(UserRateThrottle):
    scope = 'inmueble-detalle'
