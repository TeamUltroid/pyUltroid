#!/usr/bin/env python
# In[ ]:
#  coding: utf-8

###### Searching and Downloading Google Images to the local disk ######

# This is a modified file which is edited as per our needs.
# You can find original source here:
# https://github.com/hardikvasa/google-images-download


# Import Libraries
import http.client
import json
import os
import ssl
import time  # Importing the time library to check the time of code execution
from urllib.parse import quote

from .tools import async_searcher

http.client._MAXHEADERS = 1000

args_list = [
    "keywords",
    "prefix_keywords",
    "suffix_keywords",
    "limit",
    "format",
    "output_directory",
]


class googleimagesdownload:
    def __init__(self):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
        }

    # Downloading entire Web Document (Raw Page Content)
    async def download_page(self, url):
        try:
            return str(
                await async_searcher(
                    url,
                    headers=self._headers,
                )
            )
        except Exception as exc:
            print(url)
            print(str(exc))

    # Format the object in readable format

    def format_object(self, object):
        data = object[1]
        main = data[3]
        info = data[9]
        return {
            "image_height": main[2],
            "image_width": main[1],
            "image_link": main[0],
            "image_format": main[0][-1 * (len(main[0]) - main[0].rfind(".") - 1) :],
            "image_description": info["2003"][3],
            "image_source": info["2003"][2],
            "image_thumbnail_url": data[2][0],
        }

    # Building URL parameters

    def build_url_parameters(self, arguments):
        lang_url = ""

        time_range = ""

        exact_size = ""

        built_url = "&tbs="
        counter = 0
        params = {
            "format": [
                arguments["format"],
                {
                    "jpg": "ift:jpg",
                    "gif": "ift:gif",
                    "png": "ift:png",
                    "bmp": "ift:bmp",
                    "svg": "ift:svg",
                    "webp": "webp",
                    "ico": "ift:ico",
                    "raw": "ift:craw",
                },
            ],
        }
        for key, value in params.items():
            if value[0] is not None:
                ext_param = value[1][value[0]]
                # counter will tell if it is first param added or not
                if counter == 0:
                    # add it to the built url
                    built_url += ext_param
                else:
                    built_url = built_url + "," + ext_param
                counter += 1
        built_url = lang_url + built_url + exact_size + time_range
        return built_url

    # building main search URL

    async def build_search_url(self, search_term, params):
        url = (
            "https://www.google.com/search?q="
            + quote(search_term.encode("utf-8"))
            + "&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch"
            + params
            + "&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg"
        )

        return url

    # Download Images

    async def download_image(
        self,
        image_url,
        image_format,
        main_directory,
        dir_name,
        count,
        print_urls,
        save_source,
        img_src,
        format,
    ):
        try:
            try:
                data = await async_searcher(
                    image_url,
                    headers=self._headers,
                )
                extensions = [
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".png",
                    ".bmp",
                    ".svg",
                    ".webp",
                    ".ico",
                ]
                # keep everything after the last '/'
                image_name = str(image_url[(image_url.rfind("/")) + 1 :])
                if format and (not image_format or image_format != format):
                    download_status = "fail"
                    download_message = "Wrong image format returned. Skipping..."
                    return_image_name = ""
                    absolute_path = ""
                    return (
                        download_status,
                        download_message,
                        return_image_name,
                        absolute_path,
                    )

                if (
                    image_format == ""
                    or not image_format
                    or "." + image_format not in extensions
                ):
                    download_status = "fail"
                    download_message = "Invalid or missing image format. Skipping..."
                    return_image_name = ""
                    absolute_path = ""
                    return (
                        download_status,
                        download_message,
                        return_image_name,
                        absolute_path,
                    )
                if image_name.lower().find("." + image_format) < 0:
                    image_name = image_name + "." + image_format
                else:
                    image_name = image_name[
                        : image_name.lower().find("." + image_format)
                        + (len(image_format) + 1)
                    ]

                # prefix name in image
                prefix = prefix + " " if prefix else ""
                if no_numbering:
                    path = main_directory + "/" + dir_name + "/" + prefix + image_name
                else:
                    path = (
                        main_directory
                        + "/"
                        + dir_name
                        + "/"
                        + prefix
                        + str(count)
                        + "."
                        + image_name
                    )
                try:
                    with open(path, "wb") as output_file:
                        output_file.write(data)
                    if save_source:
                        list_path = main_directory + "/" + save_source + ".txt"
                        with open(list_path, "a") as list_file:
                            list_file.write(path + "\t" + img_src + "\n")
                    absolute_path = os.path.abspath(path)
                except OSError as e:
                    download_status = "fail"
                    download_message = (
                        "OSError on an image...trying next one..." + " Error: " + str(e)
                    )
                    return_image_name = ""
                    absolute_path = ""

                # return image name back to calling method to use it for
                # thumbnail downloads
                download_status = "success"
                download_message = (
                    "Completed Image ====> " + prefix + str(count) + "." + image_name
                )
                return_image_name = prefix + str(count) + "." + image_name

            except UnicodeEncodeError as e:
                download_status = "fail"
                download_message = (
                    "UnicodeEncodeError on an image...trying next one..."
                    + " Error: "
                    + str(e)
                )
                return_image_name = ""
                absolute_path = ""

        except ssl.CertificateError as e:
            download_status = "fail"
            download_message = (
                "CertificateError on an image...trying next one..."
                + " Error: "
                + str(e)
            )
            return_image_name = ""
            absolute_path = ""

        except IOError as e:  # If there is any IOError
            download_status = "fail"
            download_message = (
                "IOError on an image...trying next one..." + " Error: " + str(e)
            )
            return_image_name = ""
            absolute_path = ""

        return download_status, download_message, return_image_name, absolute_path

    # Finding 'Next Image' from the given raw page

    def _get_next_item(self, s):
        start_line = s.find("rg_meta notranslate")
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_links"
            return link, end_quote
        start_line = s.find('class="rg_meta notranslate">')
        start_object = s.find("{", start_line + 1)
        end_object = s.find("</div>", start_object + 1)
        object_raw = str(s[start_object:end_object])
        # remove escape characters based on python version
        try:
            object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
            final_object = json.loads(object_decode)
        except BaseException:
            final_object = ""
        return final_object, end_object

    # Getting all links with the help of '_images_get_next_image'

    def _get_image_objects(self, s):
        start_line = s.find("AF_initDataCallback({key: \\'ds:1\\'") - 10
        start_object = s.find("[", start_line + 1)
        end_object = s.find("</script>", start_object + 1) - 4
        object_raw = str(s[start_object:end_object])
        object_decode = bytes(object_raw[:-1], "utf-8").decode("unicode_escape")
        # LOGS.info(_format.paste_text(object_decode[:-15]))
        print(object_decode)
        try:
            json.loads(object_decode[:-15])[31][0][12][2]
        except BaseException:
            print(object_decode)

    async def _get_all_items(self, page, main_directory, dir_name, limit, arguments):
        items = []
        abs_path = []
        errorCount = 0
        i = 0
        count = 1
        # LOGS.info(f"page : {_format.paste_text(page)}")
        image_objects = self._get_image_objects(page)
        while count < limit + 1:
            if not image_objects:
                print("no_links")
                break
            else:
                # format the item for readability
                object = self.format_object(image_objects[i])

                # download the images
                (
                    download_status,
                    download_message,
                    return_image_name,
                    absolute_path,
                ) = self.download_image(
                    object["image_link"],
                    object["image_format"],
                    main_directory,
                    dir_name,
                    count,
                    arguments["format"],
                )
                # if not arguments["silent_mode"]:
                # print(download_message)
                if download_status == "success":

                    count += 1
                    object["image_filename"] = return_image_name
                    # Append all the links in the list named 'Links'
                    items.append(object)
                    abs_path.append(absolute_path)
                else:
                    errorCount += 1

            i += 1
        if count < limit:
            print(
                "\n\nUnfortunately all "
                + str(limit)
                + " could not be downloaded because some images were not downloadable. "
                + str(count - 1)
                + " is all we got for this search filter!"
            )
        return items, errorCount, abs_path

    # Bulk Download

    async def download(self, arguments):
        paths_agg = {}
        paths, errors = await self.download_executor(arguments)
        for i in paths:
            paths_agg[i] = paths[i]
        return paths_agg, errors

    async def download_executor(self, arguments):
        paths = {}
        errorCount = None
        for arg in args_list:
            if arg not in arguments:
                arguments[arg] = None
        # Initialization and Validation of user arguments
        if arguments["keywords"]:
            search_keyword = [str(item) for item in arguments["keywords"].split(",")]

        # Setting limit on number of images to be downloaded
        limit = int(arguments["limit"]) if arguments["limit"] else 100
        if arguments["keywords"] is None:
            print(
                "-------------------------------\n"
                "Uh oh! Keywords is a required argument \n\n"
                "Please refer to the documentation on guide to writing queries \n"
                "https://github.com/hardikvasa/google-images-download#examples"
                "\n\nexiting!\n"
                "-------------------------------"
            )

        # If this argument is present, set the custom output directory
        main_directory = arguments["output_directory"] or "downloads"
        if arguments["suffix_keywords"]:
            suffix_keywords = [
                " " + str(sk) for sk in arguments["suffix_keywords"].split(",")
            ]
        else:
            suffix_keywords = [""]

        # Additional words added to keywords
        if arguments["prefix_keywords"]:
            prefix_keywords = [
                str(sk) + " " for sk in arguments["prefix_keywords"].split(",")
            ]
        else:
            prefix_keywords = [""]

        total_errors = 0
        for pky in prefix_keywords:  # 1.for every prefix keywords
            for sky in suffix_keywords:  # 2.for every suffix keywords
                for i in range(len(search_keyword)):  # 3.for every main keyword
                    iteration = (
                        "\n"
                        + "Item no.: "
                        + str(i + 1)
                        + " -->"
                        + " Item name = "
                        + (pky)
                        + (search_keyword[i])
                        + (sky)
                    )
                    search_term = pky + search_keyword[i] + sky

                    dir_name = search_term + "-"

                    params = self.build_url_parameters(
                        arguments
                    )  # building URL with params

                    url = await self.build_search_url(
                        search_term,
                        params,
                    )

                    if limit > 100:
                        return
                    raw_html = await self.download_page(url)

                    items, errorCount, abs_path = await self._get_all_items(
                        raw_html, main_directory, dir_name, limit, arguments
                    )  # get all image items and download images
                    paths[pky + search_keyword[i] + sky] = abs_path

                    total_errors += errorCount
        return paths, total_errors
