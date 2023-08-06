

class Config(object):
    """Generated from OpenAPI #/components/schemas/Config.Config model

    A container for all models that are part of the configuration  

    Args
    ----
    - ports (list[Port]): The ports that will be configured on the traffic generator
    - device_groups (list[DeviceGroup]): The device groups that will be configured on the traffic generator
    - flows (list[Flow]): The flows that will be configured on the traffic generator
    - layer1 (list[Layer1]): The layer1 settings that will be configured on the traffic generator
    - captures (list[Capture]): The captures that will be configured on the traffic generator
    - options (Options): Global configuration options
    """
    def __init__(self, ports=[], device_groups=[], flows=[], layer1=[], captures=[], options=None):
        from abstract_open_traffic_generator.config import Options
        if isinstance(ports, (list, type(None))) is True:
            self.ports = [] if ports is None else list(ports)
        else:
            raise TypeError('ports must be an instance of (list, type(None))')
        if isinstance(device_groups, (list, type(None))) is True:
            self.device_groups = [] if device_groups is None else list(device_groups)
        else:
            raise TypeError('device_groups must be an instance of (list, type(None))')
        if isinstance(flows, (list, type(None))) is True:
            self.flows = [] if flows is None else list(flows)
        else:
            raise TypeError('flows must be an instance of (list, type(None))')
        if isinstance(layer1, (list, type(None))) is True:
            self.layer1 = [] if layer1 is None else list(layer1)
        else:
            raise TypeError('layer1 must be an instance of (list, type(None))')
        if isinstance(captures, (list, type(None))) is True:
            self.captures = [] if captures is None else list(captures)
        else:
            raise TypeError('captures must be an instance of (list, type(None))')
        if isinstance(options, (Options, type(None))) is True:
            self.options = options
        else:
            raise TypeError('options must be an instance of (Options, type(None))')


class Options(object):
    """Generated from OpenAPI #/components/schemas/Config.Options model

    Global configuration options  

    Args
    ----
    - port_options (Options): Common port options that apply to all configured Port.Port objects.
    """
    def __init__(self, port_options=None):
        from abstract_open_traffic_generator.port import Options
        if isinstance(port_options, (Options, type(None))) is True:
            self.port_options = port_options
        else:
            raise TypeError('port_options must be an instance of (Options, type(None))')
