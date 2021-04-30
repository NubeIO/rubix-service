import inspect


def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                if not inspect.isabstract(child):
                    subclasses.add(child)
                work.append(child)
    return subclasses


def get_instance(klass, app_type: str):
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if not inspect.isabstract(child):
                if child().app_type == app_type:
                    return child()
            work.append(child)
    return None
