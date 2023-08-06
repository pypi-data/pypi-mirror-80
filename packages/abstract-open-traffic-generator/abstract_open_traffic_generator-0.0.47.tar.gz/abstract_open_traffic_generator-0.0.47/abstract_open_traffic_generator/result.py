

class Errors(object):
    """Generated from OpenAPI #/components/schemas/Result.Errors model

    TBD  

    Args
    ----
    - errors (list[Error]): TBD
    """
    def __init__(self, errors=[]):
        if isinstance(errors, (list, type(None))) is True:
            self.errors = [] if errors is None else list(errors)
        else:
            raise TypeError('errors must be an instance of (list, type(None))')


class Error(object):
    """Generated from OpenAPI #/components/schemas/Result.Error model

    TBD  

    Args
    ----
    - name (str): The unique name of an object in the configuration
    - message (str): Detailed error information
    """
    def __init__(self, name=None, message=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(message, (str, type(None))) is True:
            self.message = message
        else:
            raise TypeError('message must be an instance of (str, type(None))')


class Capability(object):
    """Generated from OpenAPI #/components/schemas/Result.Capability model

    TBD  

    Args
    ----
    - unsupported (list[str]): A list of #/components/schemas/... path that are not supported
    - formats (list[str]): A #/components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums
    """
    def __init__(self, unsupported=[], formats=[]):
        if isinstance(unsupported, (list, type(None))) is True:
            self.unsupported = [] if unsupported is None else list(unsupported)
        else:
            raise TypeError('unsupported must be an instance of (list, type(None))')
        if isinstance(formats, (list, type(None))) is True:
            self.formats = [] if formats is None else list(formats)
        else:
            raise TypeError('formats must be an instance of (list, type(None))')


class PortRequest(object):
    """Generated from OpenAPI #/components/schemas/Result.PortRequest model

    The flow result request to the traffic generator   

    Args
    ----
    - port_names (list[str]): The names of objects to return results for. An empty list will return all port row results
    - columns (list[Union[name, location, link, capture, frames_tx, frames_rx, frames_tx_rate, frames_rx_rate, bytes_tx, bytes_rx, bytes_tx_rate, bytes_rx_rate, pfc_class_0_frames_rx, pfc_class_1_frames_rx, pfc_class_2_frames_rx, pfc_class_3_frames_rx, pfc_class_4_frames_rx, pfc_class_5_frames_rx, pfc_class_6_frames_rx, pfc_class_7_frames_rx]]): The names of columns to return results for. An empty list will return all columns. The name column will always be included as it is the unique key. The following is a description of the columns:
        name The name of a configured port
        location The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.
        link The state of the test port link The string can be up, down or a custom error message.
        capture The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.
        frames_tx The current total number of frames transmitted
        frames_rx The current total number of valid frames received
        bytes_tx: The current total number of bytes transmitted
        bytes_rx: The current total number of valid bytes received
        frames_tx_rate: The current rate of frames transmitted
        frames_rx_rate: The current rate of valid frames received
        bytes_tx_rate: The current rate of bytes transmitted
        bytes_rx_rate: The current rate of bytes received
        pfc_class_0_frames_rx: The current total number of pfc class 0 frames received
        pfc_class_1_frames_rx: The current total number of pfc class 1 frames received
        pfc_class_2_frames_rx: The current total number of pfc class 2 frames received
        pfc_class_3_frames_rx: The current total number of pfc class 3 frames received
        pfc_class_4_frames_rx: The current total number of pfc class 4 frames received
        pfc_class_5_frames_rx: The current total number of pfc class 5 frames received
        pfc_class_6_frames_rx: The current total number of pfc class 6 frames received
        pfc_class_7_frames_rx: The current total number of pfc class 7 frames received
    """
    def __init__(self, port_names=[], columns=[]):
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = [] if port_names is None else list(port_names)
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(columns, (list, type(None))) is True:
            self.columns = [] if columns is None else list(columns)
        else:
            raise TypeError('columns must be an instance of (list, type(None))')


class Port(object):
    """Generated from OpenAPI #/components/schemas/Result.Port model

    A table of port results  

    Args
    ----
    - columns (list[str]): The columns requested
    - rows (list[list[str]]): A table of result values. Each row in rows is ordered by the columns property
    """
    def __init__(self, columns=[], rows=[]):
        if isinstance(columns, (list, type(None))) is True:
            self.columns = [] if columns is None else list(columns)
        else:
            raise TypeError('columns must be an instance of (list, type(None))')
        if isinstance(rows, (list, type(None))) is True:
            self.rows = [] if rows is None else list(rows)
        else:
            raise TypeError('rows must be an instance of (list, type(None))')


class FlowRequest(object):
    """Generated from OpenAPI #/components/schemas/Result.FlowRequest model

    The request to the traffic generator for flow results  

    Args
    ----
    - flow_names (list[str]): The names of flow objects to return results for. An empty list will return results for all flows
    - columns (list[Union[name, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]): The names of columns to return results for. An empty list will return all columns. The name column will always be included as it is the unique key. The following is a description of the columns:
        name The name of a configured flow
        port_tx The name of a configured port
        port_rx The name of a configured port
        frames_tx The current total number of frames transmitted
        frames_rx The current total number of valid frames received
        bytes_tx The current total number of bytes transmitted
        bytes_rx The current total number of bytes received
        frames_tx_rate The current rate of frames transmitted
        frames_rx_rate The current rate of valid frames received
        loss The percentage of lost frames
    - ingress_result_names (list[str]): Add any configured Flow.Pattern.ingress_result_name values that are to be included in the results. If the name is not configured then it will be excluded from the Result.Flow.columns and Result.Flow.rows. The name in the Result.Flow.columns will be a combination of the ingress_result_name and any system assigned name
    """
    def __init__(self, flow_names=[], columns=[], ingress_result_names=[]):
        if isinstance(flow_names, (list, type(None))) is True:
            self.flow_names = [] if flow_names is None else list(flow_names)
        else:
            raise TypeError('flow_names must be an instance of (list, type(None))')
        if isinstance(columns, (list, type(None))) is True:
            self.columns = [] if columns is None else list(columns)
        else:
            raise TypeError('columns must be an instance of (list, type(None))')
        if isinstance(ingress_result_names, (list, type(None))) is True:
            self.ingress_result_names = [] if ingress_result_names is None else list(ingress_result_names)
        else:
            raise TypeError('ingress_result_names must be an instance of (list, type(None))')


class Flow(object):
    """Generated from OpenAPI #/components/schemas/Result.Flow model

    A table of flow results  

    Args
    ----
    - columns (list[str]): The names of columns in the Request.Flow.columns and requested
    - rows (list[list[str]]): A table of result values. Each row in rows is ordered by the columns property
    """
    def __init__(self, columns=[], rows=[]):
        if isinstance(columns, (list, type(None))) is True:
            self.columns = [] if columns is None else list(columns)
        else:
            raise TypeError('columns must be an instance of (list, type(None))')
        if isinstance(rows, (list, type(None))) is True:
            self.rows = [] if rows is None else list(rows)
        else:
            raise TypeError('rows must be an instance of (list, type(None))')
