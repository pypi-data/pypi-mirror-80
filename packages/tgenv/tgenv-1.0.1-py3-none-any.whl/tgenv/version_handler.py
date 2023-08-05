"""    This file is part of tgenv.

    tgenv is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    tgenv is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with tgenv.  If not, see <https://www.gnu.org/licenses/>."""

import json

from .file_handler import read_versions, version_file_exists, write_version, copy_file

def get_local_versions(filepath: str) -> str:
    """ Returns local versions
    """
    versions = read_versions(filepath)
    versions = json.loads(versions)
    return versions

def add_version(version, filepath, version_file):
    """ Adds a version to the version file

    :param version: The version to add
    :type version: string
    :param filepath: The path to the version
    :type filepath: str
    :param version_file: The file containing the versions
    :type version_file: str
    """
    versions = get_local_versions(version_file)
    versions[version] = filepath
    write_version(version_file, json.dumps(versions))

def has_version(filepath, version):
    """ Checks if version exists
    """
    versions = get_local_versions(filepath)
    try:
        version_file_exists(versions[version])
        return True
    except FileNotFoundError:
        return False
    except KeyError:
        return False

def install_version(target_path, source_path, version):
    """ Installs a version
    """
    copy_file(source_path + version, target_path)
