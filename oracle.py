import os


class Oracle:
    def __init__(self, data_dir="data/"):
        """
        Initialize an Oracle instance.

        Args:
            data_dir (str): The root directory where the data is stored.
                             This directory should contain subdirectories based on coordinate values.
        """
        self.data_dir = data_dir

    def input(self, first, second, third):
        """
        Set the input values that determine the coordinate-based file paths.

        These input values will be used to compute:
            - first_cord: first % 8
            - second_cord: second % 8
            - third_cord: third % 6

        Args:
            first (int): The first integer value.
            second (int): The second integer value.
            third (int): The third integer value.
        """
        self.first = first
        self.second = second
        self.third = third

    def convert_to_cord(self):
        """
        Convert the input values to coordinate values using modulo arithmetic.

        The conversion rules are:
            - first_cord = first % 8
            - second_cord = second % 8
            - third_cord = third % 6

        These computed coordinates are used to construct the directory paths for retrieving files.
        """
        self.first_cord = self.first % 8
        self.second_cord = self.second % 8
        self.third_cord = self.third % 6

    def get_parent_directory(self):
        """
        Get the parent directory based on the computed first and second coordinates.

        The parent directory is expected to follow the naming convention:
            "<first_cord>-<second_cord>"

        Returns:
            str: The absolute path to the parent directory.

        Raises:
            FileNotFoundError: If the parent directory does not exist.
        """
        parent_dir = os.path.join(
            self.data_dir, f"{self.first_cord}-{self.second_cord}"
        )
        if not os.path.exists(parent_dir):
            raise FileNotFoundError(f"Parent directory {parent_dir} not found.")
        return parent_dir

    def get_child_directory(self):
        """
        Get the child directory based on the computed third coordinate, under the parent directory.

        The child directory is expected to be a subdirectory of the parent directory,
        with its name equal to the third coordinate value.

        Returns:
            str: The absolute path to the child directory.

        Raises:
            FileNotFoundError: If the child directory does not exist.
        """
        child_dir = os.path.join(self.get_parent_directory(), str(self.third_cord))
        if not os.path.exists(child_dir):
            raise FileNotFoundError(f"Child directory {child_dir} not found.")
        return child_dir

    def get_txt_file(self, directory):
        """
        Retrieve and read the contents of "body.txt" located in the html subfolder of a given directory.

        This function expects the following folder structure:
            <directory>/
                └── html/
                        └── body.txt

        Args:
            directory (str): The directory (either parent or child) to search in.

        Returns:
            str: The text content of "body.txt".

        Raises:
            FileNotFoundError: If the html folder or "body.txt" file is not found.
        """
        file_path = os.path.join(directory, "html", "body.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"'body.txt' not found in {file_path}.")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

    def get_image_path(self, directory):
        """
        Retrieve the path to the image file ("image.jpg") located in the images subfolder of a given directory.

        This function expects the following folder structure:
            <directory>/
                └── images/
                        └── image.jpg

        Args:
            directory (str): The directory (either parent or child) to search in.

        Returns:
            str: The absolute path to "image.jpg".

        Raises:
            FileNotFoundError: If the images folder or "image.jpg" file is not found.
        """
        image_path = os.path.join(directory, "images", "image.jpg")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found in {image_path}.")
        return image_path
