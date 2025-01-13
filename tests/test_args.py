from net_report import args


def test_default_args():
    NUMBER_OF_ARGS = 4
    parser = args.parse_args([])
    assert not parser.version
    assert not parser.check_config
    assert not parser.skip_config_check
    assert not parser.quick
    assert len(vars(parser)) == NUMBER_OF_ARGS


def test_version():
    parser = args.parse_args(["--version"])
    assert parser.version


def test_check_config():
    parser_short = args.parse_args(["-c"])
    parser_long = args.parse_args(["--check-config"])
    assert parser_short.check_config
    assert parser_long.check_config


def test_skip_config_check():
    parser_short = args.parse_args(["-s"])
    parser_long = args.parse_args(["--skip-config-check"])
    assert parser_short.skip_config_check
    assert parser_long.skip_config_check


def test_quick():
    parser_short = args.parse_args(["-q"])
    parser_long = args.parse_args(["--quick"])
    assert parser_short.quick
    assert parser_long.quick
