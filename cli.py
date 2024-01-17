import argparse
import sys

from impl import *


# TODO: make the monitor setup configurable.
# Seizure's three monitors are hard-coded.
monitor_names = {"LEFT": "2", "MIDDLE": "1", "RIGHT": "0"}


def __check_attr(attr: str) -> Attribute:
    try:
        return Attribute[attr]
    except KeyError:
        global_parser.error(f"{attr} is not a valid attribute."
                            f"\nValid attributes are: {', '.join(Attribute.__members__)}")


def __check_mon(mon: str) -> int:
    if mon in monitor_names:
        mon = monitor_names[mon]
    try:
        return int(mon)
    except ValueError:
        global_parser.error(f"{mon} is not a valid monitor."
                            f"\nValid monitors are: {', '.join(monitor_names)}, or an index")


def __check_val(attr: Attribute, val: str) -> InputSource | PowerMode | int:
    match attr:
        case Attribute.SRC:
            try:
                return InputSource[val]
            except KeyError:
                global_parser.error(f"{val} is an invalid input source."
                                    f"\nValid input sources are: {', '.join(InputSource.__members__)}"
                                    "\nNOTE: A particular monitor will probably support only some of these values,"
                                    " if any. Check your monitor's specs for the inputs it accepts.")

        case Attribute.CNT:
            try:
                return int(val)
            except ValueError:
                global_parser.error(f"{val} is an invalid contrast value."
                                    f"\nValid contrast values are typically 0-100.")

        case Attribute.LUM:
            try:
                return int(val)
            except ValueError:
                global_parser.error(f"{val} is an invalid luminance value."
                                    f"\nValid luminance values are typically 0-100.")

        case Attribute.PWR:
            try:
                return PowerMode[val]
            except KeyError:
                global_parser.error(f"{val} is an invalid power mode."
                                    f"\nValid power modes are: {', '.join(PowerMode.__members__)}")


def __get_attr(args):
    attr = __check_attr(args.attr)
    mon = __check_mon(args.mon)

    val = get_attribute(mon, attr)
    print(val)


def __set_attr(args):
    attr = __check_attr(args.attr)
    mon = __check_mon(args.mon)

    val = __check_val(attr, args.val)

    set_attribute(mon, attr, val)


def __tog_attr(args):
    attr = __check_attr(args.attr)
    mon = __check_mon(args.mon)

    val1 = __check_val(attr, args.val1)
    val2 = __check_val(attr, args.val2)

    toggle_attribute(mon, attr, val1, val2)


global_parser = argparse.ArgumentParser(description="Boss your monitors around.")
subparsers = global_parser.add_subparsers(title="subcommands", help="basic commands", dest="subcommand", required=True)

get_parser = subparsers.add_parser("get", help="return the value of a given attribute")
get_parser.set_defaults(func=__get_attr)
get_parser.add_argument("attr", type=str.upper, help="the attribute to return")

set_parser = subparsers.add_parser("set", help="sets a given attribute to a given value")
set_parser.set_defaults(func=__set_attr)
set_parser.add_argument("attr", type=str.upper, help="the attribute to set")
set_parser.add_argument("val", type=str.upper, help="the value to set the attribute to")

tog_parser = subparsers.add_parser("tog", help="toggles a given attribute between two given values")
tog_parser.set_defaults(func=__tog_attr)
tog_parser.add_argument("attr", type=str.upper, help="the attribute to toggle")
tog_parser.add_argument("val1", type=str.upper, help="the first value to toggle between")
tog_parser.add_argument("val2", type=str.upper, help="the second value to toggle between")

global_parser.add_argument("mon", type=str.upper, help="the monitor to control")


def run(args):
    args = global_parser.parse_args(args)
    try:
        args.func(args)
    except MonitorBossError as e:
        print(f"{global_parser.prog}: error: {e}", file=sys.stderr)
        sys.exit(1)
