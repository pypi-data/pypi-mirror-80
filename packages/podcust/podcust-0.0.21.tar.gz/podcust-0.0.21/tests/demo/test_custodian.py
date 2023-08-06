"""
Unit Tests for DemoCust class.
"""
from podcust.demo import custodian
import mock
from subprocess import CompletedProcess


class TestDemoCust:
    def setup_class(cls):
        cls.demo = custodian.DemoCust()

    @mock.patch("podcust.demo.custodian.subprocess.run")
    def test_demo_find_stored_image(self, mocked_run):
        """
        Example output from podman images:
        REPOSITORY                         TAG     IMAGE ID      CREATED       SIZE
        localhost/httpdemo                 latest  5ff443b54997  46 hours ago  582 MB

        The hardcoded result needs to be updated properly, from a an eralier run test!
        """
        mocked_run.return_value = CompletedProcess(
            args="podman images",
            returncode=0,
            stdout=(
                "REPOSITORY                         TAG     IMAGE ID      CREATED       SIZE\n"
                "localhost/httpdemo                 latest  5ff443b54997  46 hours ago  582 MB\n"
                "registry.fedoraproject.org/fedora  latest  00ff39a8bf19  2 months ago  189 MB"
            ),
            stderr="",
        )
        result = self.demo.find_stored_image_id()
        assert result == ("localhost/httpdemo", "5ff443b54997")

    @mock.patch("podcust.demo.custodian.DemoCust.find_stored_image_id")
    @mock.patch("podcust.demo.custodian.subprocess.run")
    def test_demo_remove_stored_image(self, mocked_run, mocked_image):
        """"""
        mocked_image.return_value = (self.demo.name, "5ff443b54997")
        self.demo.remove_stored_image()
        mocked_run.assert_called_with(
            "podman image rm 5ff443b54997", text=True, shell=True, stdout=-1, stderr=-1
        )
