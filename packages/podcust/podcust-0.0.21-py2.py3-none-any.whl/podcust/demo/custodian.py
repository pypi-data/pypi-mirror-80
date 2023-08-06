"""
Custodian Class for Demo container.
"""

import subprocess
from typing import Tuple


class DemoCust:
    """
    Main class for handling the httpdemo container.

    The httpdemo container just spawns an a container with an apache web server
    service serving the Fedora Test page through http.

    :param name: The Repository name of the image this class is custodian for.
    """

    name: str
    image_id: str

    def __init__(self, name: str = "localhost/httpdemo"):
        """
        Initialize DemoCust class.
        """
        self.name = name
        self.image_id = ""

    def find_stored_image_id(self) -> Tuple[str, str]:
        """
        This function looks if the system has an appropriate container image and
        returns the id of that image.

        Current implementation assumes that the first match is the one we are after.

        TODO: Specify what tag we want to match?
        """

        image_id: str = ""
        check = subprocess.run(
            "podman images",
            text=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # split results line by line and remove all but one whitespace
        processed_lines = []
        for line in check.stdout.splitlines():
            # default split separator is spaces, too many spaces act as one separator
            tmp = " ".join(line.split())
            processed_lines.append(tmp.split(" "))

        # We expect the first line to have the columns below:
        # ['REPOSITORY', 'TAG', 'IMAGE', 'ID', 'CREATED', 'SIZE']
        for il in processed_lines:
            if il[0] == self.name:
                image_id = il[2]

        return (self.name, image_id)

    def remove_stored_image(self):
        """
        Removes a stored container image corresponding to the name
        the class has been instantiated to.
        """

        _, image_id = self.find_stored_image_id()
        command_text = "podman image rm $image_id"
        command_text = command_text.replace("$image_id", image_id)
        print(f"Removing image {self.name} with image id {image_id}")
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
