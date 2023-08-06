

class PortLink(object):
    """Generated from OpenAPI #/components/schemas/Control.PortLink model

    Control port link state  

    Args
    ----
    - port_names (list[str]): The names of port objects to. An empty list will control all port objects
    - state (Union[up, down]): The link state
    """
    def __init__(self, port_names=[], state=None):
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = [] if port_names is None else list(port_names)
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')


class FlowTransmit(object):
    """Generated from OpenAPI #/components/schemas/Control.FlowTransmit model

    Control flow transmit state  

    Args
    ----
    - flow_names (list[str]): The names of flow objects to control. An empty list will control all flow objects
    - state (Union[start, stop, pause]): The transmit state
    """
    def __init__(self, flow_names=[], state=None):
        if isinstance(flow_names, (list, type(None))) is True:
            self.flow_names = [] if flow_names is None else list(flow_names)
        else:
            raise TypeError('flow_names must be an instance of (list, type(None))')
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
