import os
import json
from shutil import rmtree, copyfileobj
from airtable import Airtable
from urllib.parse import urlparse
import requests

"""
 █████╗ ██╗██████╗ ████████╗ █████╗ ██████╗ ██╗     ███████╗
██╔══██╗██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝
███████║██║██████╔╝   ██║   ███████║██████╔╝██║     █████╗  
██╔══██║██║██╔══██╗   ██║   ██╔══██║██╔══██╗██║     ██╔══╝  
██║  ██║██║██║  ██║   ██║   ██║  ██║██████╔╝███████╗███████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝

 ██████╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
██╔════╝██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝ 
██║     ███████║██║     ███████║██║██╔██╗ ██║██║  ███╗
██║     ██╔══██║██║     ██╔══██║██║██║╚██╗██║██║   ██║
╚██████╗██║  ██║╚██████╗██║  ██║██║██║ ╚████║╚██████╔╝
 ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
Author: Ross Mountjoy and Thomas Huxley                                             
"""


def remove_empty_folders(path, remove_root=True):
    'Function to remove empty folders'
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and remove_root:
        print("Removing empty folder:", path)
        os.rmdir(path)


def get_record_attachments(record):
    if "fields" in record:
        fields = record["fields"]
        for key in fields.keys():
            field = fields[key]
            if isinstance(field, list) and "url" in field[0]:
                return {"key": key, "field": field}
    return None


class Base:
    def __init__(self, base_id, api_key, json_folder=None):
        self.base_id = base_id
        self.api_key = api_key
        self.cache_url_base = None
        self.existing_table = None

        # get json folder path
        if json_folder is None:
            curr_folder = os.path.dirname(__file__)
            main_json_folder = os.path.join(curr_folder, "json")
        else:
            main_json_folder = os.path.abspath(json_folder)
        if not os.path.isdir(main_json_folder):
            os.mkdir(main_json_folder)
        self.json_folder = os.path.join(main_json_folder, self.base_id)
        if not os.path.isdir(self.json_folder):
            os.mkdir(self.json_folder)

    def load_current_table(self, table_name):
        cache_exists = False
        try:
            with open(
                    os.path.join(self.json_folder, f"{table_name}.json"), "r"
            ) as json_file:
                self.existing_table = json.load(json_file)["list"]
                cache_exists = True
        except EnvironmentError:
            print("oops")

        return cache_exists

    def attachment_exists(self, attachment_url, current_attachments):
        for attachment in current_attachments:
            current_attachment_url_parsed = urlparse(attachment["url"])
            path = self.json_folder + current_attachment_url_parsed.path
            if os.path.isfile(path):
                return attachment
        return None

    def save_attachment(self, url):
        parsed_url = urlparse(url)

        filename = parsed_url.path.split("/")[-1]
        pathname = self.json_folder + parsed_url.path

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            os.makedirs(os.path.dirname(pathname), exist_ok=True)
            with open(pathname, 'wb') as f:
                copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', parsed_url.path)
            return self.cache_url_base + '/' + self.base_id + '/' + parsed_url.path
        else:
            print('Image Couldn\'t be retreived')
            return False

    def delete_attachment(self, attachment):
        parsed_url = urlparse(attachment["url"])
        pathname = self.json_folder + parsed_url.path
        os.remove(pathname)

        if "thumbnails" in attachment:
            thumbnail_sizes = ["small", "large", "full"]
            for size in thumbnail_sizes:
                if size in attachment["thumbnails"]:
                    url = attachment["thumbnails"][size]["url"]
                    parsed_url = urlparse(url)
                    pathname = self.json_folder + parsed_url.path
                    os.remove(pathname)
        return

    def delete_old_attachments(self, new_attachments, record_id):
        if self.existing_table is None:
            return

        rec = [rec for rec in self.existing_table if rec["id"] == record_id][0]
        if rec:
            current_record = rec
        else:
            return

        if "fields" not in current_record:
            return

        if new_attachments["key"] not in current_record:
            return

        current_attachments = current_record[new_attachments["key"]]
        for c_attachment in current_attachments:
            attachment_exists = False
            for n_attachment in new_attachments["field"]:
                if c_attachment["id"] == n_attachment["id"]:
                    attachment_exists = True
            if not attachment_exists:
                # Delete the attachment!
                self.delete_attachment(c_attachment)

        # Remove all empty folders
        remove_empty_folders(self.json_folder, False)
        return

    def cache_attachment(self, field, record_id):
        cache_exists = self.existing_table is not None

        current_record = None
        if cache_exists:
            rec = [rec for rec in self.existing_table if rec["id"] == record_id][0]
            if rec:
                current_record = rec

        if current_record:
            current_record_attachments = get_record_attachments(current_record)
            attachment_exists = self.attachment_exists(field["url"], current_record_attachments["field"])
            if attachment_exists:
                return attachment_exists
            else:
                print('attachment does not exist currently')

        original_url = field["url"]
        new_attachment_url = self.save_attachment(original_url)
        if new_attachment_url:
            field["url"] = new_attachment_url

        if "thumbnails" in field:
            thumbnail_sizes = ["small", "large", "full"]
            for size in thumbnail_sizes:
                if size in field["thumbnails"]:
                    url = field["thumbnails"][size]["url"]
                    new_attachment_url = self.save_attachment(url)
                    if new_attachment_url:
                        field["thumbnails"][size]["url"] = new_attachment_url

        return field

    def cache_attachments(self, json_data):
        for rIndex, record in enumerate(json_data["list"]):
            attachments = get_record_attachments(record)
            if "field" in attachments:
                for idx, attachment in enumerate(attachments["field"]):
                    attachments["field"][idx] = self.cache_attachment(attachments["field"][idx], record["id"])
                    self.delete_old_attachments(attachments, record["id"])
                json_data["list"][rIndex]["fields"][attachments["key"]] = attachments["field"]

        return json_data

    def cache_table(self, table_name, attachment_cache=False, **kwargs):
        """
        save table using airtable-python-wrapper's get_all function as a json file
        :param attachment_cache:
        :param table_name:
        :param kwargs:
        :return:
        """
        airtable = Airtable(self.base_id, table_name, self.api_key)
        at_json = {"list": airtable.get_all(**kwargs)}
        if attachment_cache:
            self.cache_url_base = attachment_cache
            self.load_current_table(table_name)
            at_json = self.cache_attachments(at_json)
        json_path = os.path.join(self.json_folder, f"{table_name}.json")
        if os.path.isfile(json_path):
            os.remove(json_path)
        with open(json_path, "w") as new_file:
            json.dump(at_json, new_file)

    def clear_cache(self):
        """
        delete all json files out of this base's json folder
        :return:
        """
        rmtree(self.json_folder)
        os.mkdir(self.json_folder)


class Table:
    def __init__(self, base_id, table_name, json_folder=None):
        self.base_id = base_id
        self.table_name = table_name
        self.list = None

        # get json folder path
        if json_folder is None:
            curr_folder = os.path.dirname(__file__)
            main_json_folder = os.path.join(curr_folder, "json")
        else:
            main_json_folder = os.path.abspath(json_folder)
        self.json_folder = os.path.join(main_json_folder, self.base_id)

    def get(self, rec_id, resolve_fields=None):
        """
        reads json file for given record id, optionally resolves relationships,
        then returns the record as a dict
        :param rec_id:
        :param resolve_fields:
        :return:
        """
        self.__get_dict_list_from_json_file()
        if resolve_fields:
            self.__resolve_relationships(resolve_fields)
        recs = [rec for rec in self.list if rec["id"] == rec_id]
        if not recs:
            return None
        return recs[0]

    def query(self, resolve_fields=None):
        """
        reads json file for all records, optionally resolves relationships,
        then sets self.list as a list of dicts.
        :param resolve_fields:
        :return:
        """
        self.__get_dict_list_from_json_file()
        if resolve_fields:
            self.__resolve_relationships(resolve_fields)
        if len(self.list) < 1:
            self.list = None
        return self

    def filter_by(self, fields):
        """
        filters self.list by a given dict of {<field>:<value>}
        :param fields:
        :return:
        """
        for field, value in fields.items():
            self.list = [rec for rec in self.list if rec["fields"].get(field) == value]
        if len(self.list) < 1:
            self.list = None
        return self

    def order_by(self, field, desc=False):
        """
        orders self.list by the given field, set desc to order descending
        :param field:
        :param desc:
        :return:
        """
        try:
            self.list = sorted(self.list, key=lambda i: i["fields"].get(field, None))
        except TypeError:
            raise Exception(
                f"Invalid field error: '{field}' does not exist in {self.table_name}'s ['fields'] dict."
            )

        if len(self.list) < 1:
            self.list = None
        if desc and self.list:
            self.list.reverse()
        return self

    def all(self):
        """
        returns all of self.list
        :return:
        """
        self.query()
        return self.list

    def first(self):
        """
        returns the first record in self.list
        :return:
        """
        if len(self.list) < 1:
            return None
        return self.list[0]

    def last(self):
        """
        returns the last record in self.list
        :return:
        """
        if len(self.list) < 1:
            return None
        return self.list[-1]

    def __get_dict_list_from_json_file(self):
        with open(
                os.path.join(self.json_folder, f"{self.table_name}.json"), "r"
        ) as json_file:
            table_dict = json.load(json_file)
        self.list = table_dict["list"]

    def __resolve_relationships(self, resolve_fields):
        for table_name, rel_field in resolve_fields.items():
            for rec in self.list:
                full_rec_list = []
                if rec["fields"].get(rel_field, None):
                    for related_rec in rec["fields"][rel_field]:
                        d = Table(base_id=self.base_id, table_name=self.table_name)
                        full_rec_list.append(d.get(related_rec))
                    rec["fields"][rel_field] = full_rec_list
