import logging


def new_logger(*loggers):
    names = []
    for obj in loggers:
        if isinstance(obj, str):
            names.append(obj)
        elif hasattr(obj, "name"):
            names.append(obj.name)
    return logging.getLogger(".".join(names))


pydent_logger = new_logger("pydent")
session_logger = new_logger(pydent_logger, "session")
aqhttp_logger = new_logger(session_logger, "http")
browser_logger = new_logger(pydent_logger, "browser")
planning_logger = new_logger(browser_logger, "planner")
planning_optimizer_logger = new_logger(planning_logger, "optimizer")
