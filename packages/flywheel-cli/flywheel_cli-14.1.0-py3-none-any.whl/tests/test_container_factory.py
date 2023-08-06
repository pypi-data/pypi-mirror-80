import copy

import pytest

from flywheel_cli.importers.container_factory import ContainerFactory, ContainerResolver


class MockContainer:
    def __init__(self, _id, uid=None, label=None):
        self.id = _id
        self.uid = uid
        self.label = label


class MockContainerResolver(ContainerResolver):
    def __init__(self, hierarchy=None, reserved_uids=None):
        # Each path is a tuple of id, uid and (optionally) label
        self.hierarchy = hierarchy or {}
        self.created_nodes = []
        self.reserved_uids = reserved_uids or {}

    def resolve_path(self, container_type, path):
        last = None
        for part in path:
            node = (last or self.hierarchy).get(part)
            if not node:
                return None, None
            last = node

        if last:
            return last["_meta"]["_id"], last["_meta"].get("uid")

        return None, None

    def resolve_children(self, container_type, path):
        last = None
        for part in path:
            node = (last or self.hierarchy).get(part)
            if not node:
                return []
            last = node

        if last:
            return [
                MockContainer(**v["_meta"]) for k, v in last.items() if k != "_meta"
            ]

        return []

    def create_container(self, parent, container):
        self.created_nodes.append((parent, container))
        return "created_" + container.label.lower()

    def check_unique_uids(self, request):
        resp = {}
        for container, uids in request.items():
            resp.setdefault(container, [])
            for uid in uids:
                if uid in self.reserved_uids.get(container, []):
                    resp[container].append(uid)
        return resp


def test_resolve_group_not_exist():
    resolver = MockContainerResolver()
    factory = ContainerFactory(resolver)
    context = {"group": {"_id": "foo"}}

    result = factory.resolve(context)
    assert result is not None
    assert result.container_type == "group"
    assert result.id == "foo"
    assert not result.exists

    result2 = factory.resolve(context)
    assert id(result) == id(result2)


def test_resolve_group_exists():
    resolver = MockContainerResolver({"foo": {"_meta": {"_id": "foo"}}})

    factory = ContainerFactory(resolver)
    context = {"group": {"_id": "foo"}}

    result = factory.resolve(context)
    assert result is not None
    assert result.container_type == "group"
    assert result.id == "foo"
    assert result.exists


def test_resolve_missing_level():
    resolver = MockContainerResolver()
    factory = ContainerFactory(resolver)

    context = {
        "group": {"_id": "scitran"},
        "project": {"label": "Project1"},
        "subject": {"label": "Subject1"},
        "acquisition": {"label": "Acquisition1"},
    }

    result = factory.resolve(context)
    assert result is None


def test_resolve_acquisition():
    resolver = MockContainerResolver(
        {
            "scitran": {
                "_meta": {"_id": "scitran"},
                "Project1": {"_meta": {"_id": "project1"}},
            }
        }
    )

    factory = ContainerFactory(resolver)

    group_context = {
        "group": {"_id": "scitran"},
    }

    project_context = {
        "group": {"_id": "scitran"},
        "project": {"label": "Project1"},
    }

    acquisition_context = {
        "group": {"_id": "scitran"},
        "project": {"label": "Project1"},
        "subject": {"label": "Subject1"},
        "session": {"label": "Session1"},
        "acquisition": {"label": "Acquisition1", "uid": "1234"},
    }

    result = factory.resolve(acquisition_context)
    assert result is not None
    assert result.container_type == "acquisition"
    assert result.id is None
    assert result.label == "Acquisition1"
    assert not result.exists
    acquisition_node = result

    result = factory.resolve(group_context)
    assert result is not None
    assert result.container_type == "group"
    assert result.id is "scitran"
    assert result.exists

    result = factory.resolve(project_context)
    assert result is not None
    assert result.container_type == "project"
    assert result.id is "project1"
    assert result.label == "Project1"
    assert result.exists

    result = factory.resolve(acquisition_context)
    assert result == acquisition_node

    acquisition_context2 = copy.deepcopy(acquisition_context)
    acquisition_context2["acquisition"]["uid"] = "5678"

    result = factory.resolve(acquisition_context2, create=False)
    assert result is None

    result = factory.resolve(acquisition_context2)
    assert result is not None
    assert result.container_type == "acquisition"
    assert result.id is None
    assert result.label == "Acquisition1"
    assert not result.exists
    assert result != acquisition_node


def test_creation():
    resolver = MockContainerResolver(
        {
            "scitran": {
                "_meta": {"_id": "scitran"},
                "Project1": {"_meta": {"_id": "project1"}},
            }
        }
    )

    factory = ContainerFactory(resolver)

    context = {
        "group": {"_id": "scitran"},
        "project": {"label": "Project1"},
        "subject": {"label": "Subject1"},
        "session": {"label": "Session1"},
        "acquisition": {"label": "Acquisition1"},
    }

    factory.resolve(context)

    nodes_to_create = []

    def create_fn(parent, child):
        nodes_to_create.append((parent, child))
        return "created_" + child.label.lower()

    factory.create_containers()

    # Should be in hierarchical order for a single tree
    itr = iter(resolver.created_nodes)

    parent, child = next(itr)
    assert parent.container_type == "project"
    assert parent.id == "project1"
    assert child.container_type == "subject"
    assert child.id == "created_subject1"
    assert child.exists

    parent, child = next(itr)
    assert parent.container_type == "subject"
    assert parent.id == "created_subject1"
    assert child.container_type == "session"
    assert child.id == "created_session1"
    assert child.exists

    parent, child = next(itr)
    assert parent.container_type == "session"
    assert parent.id == "created_session1"
    assert child.container_type == "acquisition"
    assert child.id == "created_acquisition1"
    assert child.exists

    try:
        next(itr)
        pytest.fail("Unexpected invocation to create node")
    except StopIteration:
        pass


def test_get_first_project():
    resolver = MockContainerResolver()
    factory = ContainerFactory(resolver)

    assert factory.get_first_project() is None

    context = {
        "group": {"_id": "scitran"},
    }
    factory.resolve(context)
    assert factory.get_first_project() is None

    context = {"group": {"_id": "scitran"}, "project": {"label": "Project1"}}
    factory.resolve(context)
    result = factory.get_first_project()
    assert result is not None
    assert result.label == "Project1"

    context = {"group": {"_id": "scitran"}, "project": {"label": "Project2"}}
    factory.resolve(context)
    result = factory.get_first_project()
    assert result is not None
    assert result.label == "Project1"


@pytest.mark.parametrize(
    "context",
    [
        {
            "group": {"_id": "scitran"},
            "project": {"_id": "pid"},
            "subject": {"label": "Subject1"},
            "session": {"label": "Session1"},
            "acquisition": {"label": "Acquisition1"},
        },
        {
            "group": {"_id": "scitran"},
            "project": {"_id": "pid", "label": "Project1"},
            "subject": {"label": "Subject1"},
            "session": {"_id": "sid"},
            "acquisition": {"label": "Acquisition1"},
        },
        {
            "group": {"_id": "scitran"},
            "project": {"_id": "pid", "label": "Project1"},
            "subject": {"label": "Subject1"},
            "session": {"_id": "sid", "label": "Session1"},
            "acquisition": {"_id": "aid"},
        },
    ],
)
def test_invalid_container(context):
    resolver = MockContainerResolver()

    factory = ContainerFactory(resolver)

    with pytest.raises(ValueError):
        factory.resolve(context)


def test_resolve_with_uid():
    resolver = MockContainerResolver(
        {
            "scitran": {
                "_meta": {"_id": "scitran"},
                "Project1": {"_meta": {"_id": "project1"}},
            }
        }
    )

    factory = ContainerFactory(resolver)

    group_context = {
        "group": {"_id": "scitran"},
    }

    project_context = {
        "group": {"_id": "scitran"},
        "project": {"label": "Project1"},
    }

    session_context = {
        "group": {"_id": "scitran"},
        "project": {"label": "Project1"},
        "subject": {"label": "Subject1"},
        "session": {"label": "Session1"},
    }

    result = factory.resolve(session_context)
    assert result is not None
    assert result.container_type == "session"
    assert result.id is None
    assert result.uid is None
    assert result.label == "Session1"
    assert not result.exists
    session_node = result

    session_context = {
        "group": {"_id": "scitran"},
        "project": {"label": "Project1"},
        "subject": {"label": "Subject1"},
        "session": {"label": "Session1", "uid": "1.2.3"},
    }
    result = factory.resolve(session_context)
    assert result == session_node
    assert result is not None
    assert result.container_type == "session"
    assert result.id is None
    assert result.uid == "1.2.3"
    assert result.label == "Session1"
    assert not result.exists
