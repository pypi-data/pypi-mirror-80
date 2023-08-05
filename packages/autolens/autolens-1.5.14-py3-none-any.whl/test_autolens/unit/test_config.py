from os import path

from autoconf import conf
import autofit as af
import autolens as al
import pytest

directory = path.dirname(path.realpath(__file__))


class MockClass:
    pass


@pytest.fixture(name="label_config")
def make_label_config():
    return conf.instance.label


class TestLabel:
    def test_basic(self, label_config):
        assert label_config.label("centre_0") == "x"
        assert label_config.label("redshift") == "z"

    def test_escaped(self, label_config):
        assert label_config.label("gamma") == r"\gamma"
        assert label_config.label("contribution_factor") == r"\omega0"

    def test_subscript(self, label_config):
        assert label_config.subscript(al.lp.EllipticalLightProfile) == "l"

    def test_inheritance(self, label_config):
        assert label_config.subscript(al.lp.EllipticalGaussian) == "l"

    def test_exception(self, label_config):
        with pytest.raises(af.exc.PriorException):
            label_config.subscript(MockClass)
