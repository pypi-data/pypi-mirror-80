from unittest import mock

from flywheel_cli.commands.ingest import Command


def test_add_argument_groups():
    argparser_mock = mock.Mock()
    command = Command(argparser_mock, "name")

    argparser_mock.reset_mock()
    groups = command.add_argument_groups()
    assert len(groups) == 1
    assert argparser_mock.mock_calls == [
        mock.call.add_parser().add_argument_group(title="General"),
    ]


def test_add_arguments():
    class DummyCommand(Command):
        arg_groups = {}
        arg_table = [
            {
                "name": "z_name",
                "positional": True,
                "help": "z_name",
            },
            {"name": "c_name", "help": "c_name", "default": "123"},
            {
                "name": "a_name",
                "positional": True,
                "help": "a_name",
            },
            {
                "name": "d_name",
                "help": "d_name",
            },
            {
                "name": "b_name",
                "help": "b_name",
            },
            {
                "name": "a_name",
                "positional": True,
                "help": "a_name_2",
            },
            {
                "name": "b_name",
                "help": "b_name_2",
            },
        ]

    argparser_mock = mock.Mock()
    command = DummyCommand(argparser_mock, "name")

    argparser_mock.reset_mock()
    command.add_arguments()
    assert argparser_mock.mock_calls == [
        mock.call.add_parser().add_argument("z_name", default=None, help="z_name"),
        mock.call.add_parser().add_argument("a_name", default=None, help="a_name"),
        mock.call.add_parser().add_argument(
            "--b-name", default=None, dest="b_name", help="b_name"
        ),
        mock.call.add_parser().add_argument(
            "--c-name", default="123", dest="c_name", help="c_name (default: 123)"
        ),
        mock.call.add_parser().add_argument(
            "--d-name", default=None, dest="d_name", help="d_name"
        ),
    ]
