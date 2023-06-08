from formatters.native import native_formatter
from formatters.json import json_formatter
from formatters.xml import xml_formatter
from formatters.yaml import yaml_formatter
from formatters.messagepack import messagepack_formatter
from formatters.gpb import gpb_formatter
from formatters.apacheavro import apacheavro_formatter


def get_formatter_by_name(format):
    match format:
        case "native":
            return native_formatter
        case "json":
            return json_formatter
        case "xml":
            return xml_formatter
        case "yaml":
            return yaml_formatter
        case "messagepack":
            return messagepack_formatter
        case "gpb":
            return gpb_formatter
        case "apacheavro":
            return apacheavro_formatter
        case _:
            raise ValueError(f"Unknown format {format}")
