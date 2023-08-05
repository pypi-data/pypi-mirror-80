# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import pathlib
import sys

import click

from kadi_apy.cli.main import kadi_apy
from kadi_apy.cli.utils import apy_command
from kadi_apy.cli.utils import id_identifier_options
from kadi_apy.cli.utils import item_add_tag
from kadi_apy.cli.utils import item_add_user
from kadi_apy.cli.utils import item_create
from kadi_apy.cli.utils import item_delete
from kadi_apy.cli.utils import item_edit
from kadi_apy.cli.utils import item_print_info
from kadi_apy.cli.utils import item_remove_tag
from kadi_apy.cli.utils import item_remove_user
from kadi_apy.cli.utils import print_request_error
from kadi_apy.cli.utils import record_add_files
from kadi_apy.cli.utils import record_add_metadatum
from kadi_apy.cli.utils import record_add_record_link
from kadi_apy.cli.utils import search_items
from kadi_apy.cli.utils import search_resources_init
from kadi_apy.cli.utils import validate_metadatum
from kadi_apy.lib.records import Record


@kadi_apy.group()
def records():
    """Commands to manage records."""


@records.command()
@click.option(
    "-i", "--identifier", required=True, help="Identifier of the record", default=None
)
@click.option("-t", "--title", default="my title", type=str, help="Title of the record")
@click.option(
    "-v",
    "--visibility",
    help="Visibility of the record",
    default="private",
    type=click.Choice(["private", "public"]),
)
@click.option(
    "-p",
    "--pipe",
    help="Use this flag if you want to pipe the returned record id.",
    is_flag=True,
)
@apy_command
def create(**kwargs):
    """Create a record."""

    item_create(class_type=Record, **kwargs)


@records.command()
@id_identifier_options(item="record", helptext="to edit")
@click.option(
    "-v",
    "--visibility",
    help="Visibility of the record",
    default=None,
    type=click.Choice(["private", "public"]),
)
@click.option("-t", "--title", default=None, type=str, help="Title of the record")
@click.option(
    "-d", "--description", default=None, type=str, help="Description of the record"
)
@click.option("-y", "--type", default=None, type=str, help="Type of the record")
@apy_command
def edit(record_id, identifier, **kwargs):
    """Edit visibility, title or description of a record."""

    r = Record(identifier=identifier, id=record_id)

    item_edit(r, **kwargs)


@records.command()
@id_identifier_options(item="record")
@click.option(
    "-u",
    "--user-id",
    required=True,
    help="ID of the user to add",
    default=None,
    type=int,
)
@click.option(
    "-p",
    "--permission-new",
    help="Permission of new user",
    default="member",
    type=click.Choice(["member", "editor", "admin"], case_sensitive=False),
)
@apy_command
def add_user(record_id, identifier, user_id, permission_new):
    """Add a user to a record."""

    r = Record(identifier=identifier, id=record_id)

    item_add_user(r, user_id=user_id, permission_new=permission_new)


@records.command()
@id_identifier_options(item="record")
@click.option(
    "-d",
    "--description",
    help="Show the description of the record",
    is_flag=True,
    default=False,
)
@click.option(
    "-l",
    "--filelist",
    help="Show the filelist of the record",
    is_flag=True,
    default=False,
)
@click.option("-p", "--page", help="Page for filelist", type=int, default=1)
@click.option(
    "-m",
    "--metadata",
    help="Show the metadata of the record",
    is_flag=True,
    default=False,
)
@click.option(
    "-v",
    "--visibility",
    help="Show the visibility of the record",
    is_flag=True,
    default=False,
)
@apy_command
def show_info(record_id, identifier, **kwargs):
    """Prints information of a record."""

    r = Record(identifier=identifier, id=record_id)

    item_print_info(r, **kwargs)


@records.command()
@id_identifier_options(item="record")
@click.option("-n", "--file-name", required=True, help="Name of the file or folder")
@click.option(
    "-p",
    "--pattern",
    help="Pattern for selection certains files, e.g. '*.txt'. "
    "Only when uploading a folder content.",
    default="*",
    type=str,
)
@click.option(
    "-f",
    "--force",
    help="Enable if existing file(s) with identical name(s) should be replaced.",
    is_flag=True,
    default=False,
)
@apy_command
def add_files(record_id, identifier, **kwargs):
    """Add a file or a folder content to a record."""

    r = Record(identifier=identifier, id=record_id)

    record_add_files(r, **kwargs)


@records.command()
@id_identifier_options(item="record")
@click.option(
    "-u",
    "--user-id",
    required=True,
    help="ID of the user to remove",
    default=None,
    type=int,
)
@apy_command
def remove_user(record_id, identifier, user_id):
    """Remove a user from a record."""

    r = Record(identifier=identifier, id=record_id)

    item_remove_user(r, user_id)


@records.command()
@id_identifier_options(item="record", helptext="to delete")
@click.option(
    "--i-am-sure", help="Enable this option to delete the record", is_flag=True
)
@apy_command
def delete(record_id, identifier, i_am_sure):
    """Delete a record."""

    r = Record(identifier=identifier, id=record_id)

    item_delete(r, i_am_sure)


@records.command()
@id_identifier_options(item="record", helptext="to add a metadatum")
@click.option(
    "-m", "--metadatum", required=True, help="Name of metadatum to add", type=str
)
@click.option("-v", "--value", required=True, help="Value of metadatum to add")
@click.option(
    "-t",
    "--type",
    help="Type of metadatum to add",
    type=click.Choice(["string", "integer", "float", "boolean"], case_sensitive=False),
    default="string",
)
@click.option(
    "-u",
    "--unit",
    help="Unit of metadatum to add",
    type=str,
    default=None,
)
@click.option(
    "-f",
    "--force",
    help="Force overwriting existing metadatum with identical name",
    is_flag=True,
    default=False,
)
@apy_command
def add_metadatum(record_id, identifier, force, metadatum, value, type, unit):
    """Add a metadatum to a record."""

    r = Record(identifier=identifier, id=record_id)

    metadatum_new = validate_metadatum(
        metadatum=metadatum, value=value, type=type, unit=unit
    )

    record_add_metadatum(r, metadatum_new=metadatum_new, force=force)


@records.command()
@id_identifier_options(
    item="record", helptext="to add metadata as dictionary or as a list of dictionaries"
)
@click.option("-m", "--metadata", help="Metadata string input", type=str, default=None)
@click.option(
    "-p",
    "--file",
    help="Path to file containing metadata",
    type=click.Path(exists=True, file_okay=True),
    default=None,
)
@click.option(
    "-f",
    "--force",
    help="Force deleting and overwriting existing metadata",
    is_flag=True,
    default=False,
)
@apy_command
def add_metadata(record_id, identifier, metadata, file, force):
    """Add metadata with dict or a list of dicts as input."""

    if (metadata is None and file is None) or (
        metadata is not None and file is not None
    ):
        click.echo("Please specify either '-m' or '-p'.")
        sys.exit(1)

    r = Record(identifier=identifier, id=record_id)

    try:
        if file:
            with open(file) as f:
                metadata = json.load(f)
        else:
            metadata = json.loads(metadata)
    except json.JSONDecodeError as e:
        click.echo(f"Error loading JSON input ({e}).")
        sys.exit(1)

    response = r.add_metadata(metadata_new=metadata, force=force)

    if response.status_code == 200:
        click.echo(f"Successfully added metadata to {r!r}.")
    else:
        print_request_error(response=response)


@records.command()
@id_identifier_options(item="record", helptext="to delete a metadatum")
@click.option(
    "-m", "--metadatum", required=True, help="Name of metadatum to remove", type=str
)
@apy_command
def delete_metadatum(record_id, identifier, metadatum):
    """Delete a metadatum of a record."""

    r = Record(identifier=identifier, id=record_id)

    if r.check_metadatum(metadatum):
        response = r.remove_metadatum(metadatum)
        if response.status_code == 200:
            click.echo(f"Successfully removed metadatum '{metadatum}' from {repr(r)}.")
        else:
            click.echo(
                f"Something went wrong when trying to remove metadatum '{metadatum}' "
                f"from {repr(r)}."
            )
            print_request_error(response=response)
    else:
        click.echo(
            f"Metadatum '{metadatum}' is not present in {repr(r)}. Nothing to do."
        )


def _rename_duplicate_entry(filepath_store, index):
    path = pathlib.Path(filepath_store)
    base = ""
    if len(path.parts) > 1:
        base = os.path.join(*path.parts[:-1])
    file_name = f"{path.stem}_{index}{path.suffix}"
    return os.path.join(base, file_name)


@records.command()
@id_identifier_options(item="record", helptext="to download files from")
@click.option("-n", "--file-name", help="Name of file to download", type=str)
@click.option("-i", "--file-id", help="Id of file to download", type=str)
@click.option(
    "-p",
    "--filepath",
    help="Path (folder) to store the file",
    type=click.Path(exists=True),
    default=".",
)
@click.option(
    "-f",
    "--force",
    help="Force overwriting file in the given folder",
    is_flag=True,
    default=False,
)
@apy_command
def get_file(record_id, identifier, file_name, file_id, filepath, force):
    """Download one file or all files from a record."""

    r = Record(identifier=identifier, id=record_id)

    list_file_ids = []
    list_file_names = []

    if file_id is not None:
        list_file_ids.append(file_id)
        list_file_names.append(r.get_file_name(file_id))

    elif file_name is not None:
        list_file_ids.append(r.get_file_id(file_name))
        list_file_names.append(file_name)

    else:
        page = 1
        response = r.get_filelist(page=page, per_page=100)

        if response.status_code == 200:
            payload = response.json()
            total_pages = payload["_pagination"]["total_pages"]
            for page in range(1, total_pages + 1):
                if page != 1:
                    response = r.get_filelist(page=page, per_page=100)
                    payload = response.json()

                for results in payload["items"]:
                    list_file_ids.append(results["id"])
                    list_file_names.append(results["name"])
        else:
            print_request_error(response=response)

        number_files = len(list_file_ids)
        if number_files == 0:
            click.echo(f"No files present in {repr(r)}.")
            sys.exit(1)
        else:
            click.echo(f"Starting to download {number_files} file(s) from {repr(r)}.")

    list_downloaded = []

    for name_iter, id_iter in zip(list_file_names, list_file_ids):
        filepath_store = os.path.join(filepath, name_iter)
        index = 2
        filepath_temp = filepath_store

        if force:
            while filepath_temp in list_downloaded:
                filepath_temp = _rename_duplicate_entry(filepath_store, index)
                index += 1

            list_downloaded.append(filepath_temp)

        else:
            while os.path.isfile(filepath_temp):
                filepath_temp = _rename_duplicate_entry(filepath_store, index)
                index += 1

        response = r.download_file(id_iter, filepath_temp)

        if response.status_code == 200:
            click.echo(
                f"Successfully downloaded file '{name_iter}' from {repr(r)} and stored "
                f"in {filepath_temp}."
            )
        else:
            click.echo(
                f"Something went wrong when trying to download file '{file_name}' from "
                f"{repr(r)}. \nMaybe the file '{file_name}' is not present in "
                f"{repr(r)}."
            )
            print_request_error(response=response)


@records.command()
@id_identifier_options(item="record")
@click.option("-t", "--tag", required=True, help="Tag to add", type=str)
@apy_command
def add_tag(record_id, identifier, tag):
    """Add a tag to a record."""

    r = Record(identifier=identifier, id=record_id)

    item_add_tag(r, tag)


@records.command()
@id_identifier_options(item="record")
@click.option("-t", "--tag", required=True, help="Tag to remove", type=str)
@apy_command
def remove_tag(record_id, identifier, tag):
    """Aemove a tag from a record."""

    r = Record(identifier=identifier, id=record_id)

    item_remove_tag(r, tag)


@records.command()
@id_identifier_options(item="record")
@click.option(
    "-l",
    "--record-link-id",
    required=True,
    help="ID of the record to be linked",
    type=int,
)
@click.option("-n", "--name", required=True, help="Name of the linking", type=str)
@apy_command
def add_record_link(record_id, identifier, record_link_id, name):
    """Add a record link to a record."""

    r = Record(identifier=identifier, id=record_id)

    record_add_record_link(r, record_to=record_link_id, name=name)


@records.command()
@id_identifier_options(item="record")
@click.option("-l", "--record-link-id", required=True, help="Record link ID.", type=int)
@apy_command
def delete_record_link(record_id, identifier, record_link_id):
    """Delete a record link."""

    r = Record(identifier=identifier, id=record_id)

    response = r.delete_record_link(record_link_id=record_link_id)
    if response.status_code == 204:
        click.echo(
            f"Linking of record {record_id} with link id {record_link_id} was deleted."
        )
    else:
        print_request_error(response=response)


@records.command()
@id_identifier_options(item="record")
@click.option("-p", "--page", help="Page for search results", type=int, default=1)
@click.option(
    "-d",
    "--direction",
    help="Page for search results",
    type=click.Choice(["to", "from"], case_sensitive=False),
    default="to",
)
@click.option(
    "-n",
    "--per-page",
    help="Number of results per page",
    type=click.IntRange(1, 5, clamp=True),
    default=10,
)
@apy_command
def show_record_links_to(record_id, identifier, page, per_page, direction):
    """Print record links to another record."""

    r = Record(identifier=identifier, id=record_id)

    response = r.get_record_links(page=page, per_page=per_page, direction=direction)
    if response.status_code == 200:
        payload = response.json()
        click.echo(
            f"Found {payload['_pagination']['total_items']} record(s) on "
            f"{payload['_pagination']['total_pages']} page(s).\n"
            f"Showing results of page {page}:"
        )
        record_direction = f"record_{direction}"
        for results in payload["items"]:
            click.echo(
                f"Linkage id {results['id']}: Linkag name: '{results['name']}'. Record "
                f"{r.id} is linked {direction} record {results[record_direction]['id']}"
                f" with the title '{results[record_direction]['title']}'."
            )
    else:
        print_request_error(response=response)


@records.command()
@id_identifier_options(item="record")
@click.option("-n", "--name", required=True, help="Name of the metadatum", type=str)
@click.option(
    "-i",
    "--information",
    required=True,
    help="Specify the information to print",
    type=click.Choice(["value", "unit", "type"]),
)
@click.option(
    "-p",
    "--pipe",
    help="Use this flag if you want to pipe the returned information.",
    is_flag=True,
)
@apy_command
def get_metadatum(record_id, identifier, name, information, pipe):
    """Print a information of a metadatum."""

    r = Record(identifier=identifier, id=record_id)

    found = False
    for obj in r.meta["extras"]:
        if obj["key"] == name:
            found = True
            try:
                content = obj[information]
                if not pipe:
                    return click.echo(
                        f"The metadatum '{name}' has the {information} '{content}'."
                    )

                return click.echo(content)
            except:
                click.echo(f"Metadatum '{name}' has no {information}.")

    if found == False:
        click.echo(f"Metadatum '{name}' is not present in {repr(r)}.")


@records.command()
@click.option("-t", "--tag", help="Tag(s) for search", type=str, multiple=True)
@click.option(
    "-m",
    "--mimetype",
    help="MIME types for search",
    type=str,
    multiple=True,
)
@click.option("-p", "--page", help="Page for search results", type=int, default=1)
@click.option(
    "-n",
    "--per-page",
    help="Number of results per page",
    type=click.IntRange(1, 100, clamp=True),
    default=10,
)
@click.option(
    "-u",
    "--user",
    help="Show created records or specific user ID. Only those with read access are "
    "shown",
    type=int,
    default=None,
)
@click.option(
    "-i",
    "--my_user_id",
    help="Show only own created records.",
    is_flag=True,
)
@apy_command
def get_records(user, my_user_id, **kwargs):
    """Search for records."""

    s = search_resources_init()

    search_items(s, Record, user=user, my_user_id=my_user_id, **kwargs)


@records.command()
@id_identifier_options(item="record")
@click.option("-f", "--file", required=True, help="The ID or identifier of the file.")
@click.option("-n", "--name", help="The new name of the file.")
@click.option("-m", "--mimetype", help="The new MIME type of the file.")
@apy_command
def edit_file(record_id, identifier, file, name, mimetype):
    """Edit the metadata of a file of a record."""

    r = Record(identifier=identifier, id=record_id)

    response = r.edit_file(file, name=name, mimetype=mimetype)
    if response.status_code != 200:
        print_request_error(response)
    else:
        click.echo("File updated successfully.")


@records.command()
@id_identifier_options(item="record")
@click.option("-f", "--file", required=True, help="The ID or identifier of the file.")
@apy_command
def delete_file(record_id, identifier, file):
    """Delete a file of a record."""

    r = Record(identifier=identifier, id=record_id)

    response = r.delete_file(file)
    if response.status_code != 204:
        print_request_error(response)
    else:
        click.echo("File deleted successfully.")


@records.command()
@id_identifier_options(item="record")
@click.option(
    "--i-am-sure", help="Enable this option to delete the record", is_flag=True
)
@apy_command
def delete_files(record_id, identifier, i_am_sure):
    """Delete all files of a record."""

    r = Record(identifier=identifier, id=record_id)

    if not i_am_sure:
        click.echo(
            f"If you are sure you want to delete all files in {r!r}, "
            "use the flag --i-am-sure."
        )
        sys.exit(1)

    response = r.get_filelist(page=1, per_page=100)

    if response.status_code == 200:
        payload = response.json()
        total_pages = payload["_pagination"]["total_pages"]
        for page in range(1, total_pages + 1):
            for results in payload["items"]:
                response_delete = r.delete_file(file_id_or_name=results["id"])
                if response_delete.status_code != 204:
                    print_request_error(response_delete)
                else:
                    click.echo(f"Deleting file was {results['name']} successful.")
            if page < total_pages:
                response = r.get_filelist(page=1, per_page=100)
                if response.status_code == 200:
                    payload = response.json()
                else:
                    print_request_error(response)

    else:
        print_request_error(response)
