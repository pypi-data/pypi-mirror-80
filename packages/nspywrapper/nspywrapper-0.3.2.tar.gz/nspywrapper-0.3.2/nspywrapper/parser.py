"""
    Copyright 2020 Andrew Brown (aka SherpDaWerp)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from .exceptions import *
from xml.etree.ElementTree import fromstring, Element, XMLParser


class nsParser:
    @staticmethod
    def data_to_etree(data):
        """ Takes a returned "data" object from the NationStates API and parses it into an XML ElementTree.

        :param data: data from the NationStates API
        :return: <ElementTree.Element> the root element of the XML data
        """
        try:
            decoded_data = data.decode("utf-8")
            prep_data = str(decoded_data).replace('\n', "")
        except IndexError:
            raise MalformedXML("Unable to decode and/or strip newlines from file.", data=data)

        resp_data = fromstring(prep_data, XMLParser(encoding="utf-8"))
        return resp_data

    @staticmethod
    def etree_to_dict(etree):
        """ Takes an ElementTree object from the NationStates API and crudely parses it into a dict

        :param etree: a parsed ElementTree.Element from the NS API. See function data_to_etree.
        :return: <dict> a dict/list structure containing the data in a more readable format.
        """
        if type(etree) == Element:
            if etree.text is not None:
                final_dict = {etree.tag: etree.text}
            else:
                tags = [child.tag for child in etree]
                duplicates = [dupe for dupe in tags if tags.count(dupe) > 1]
                list_of_children = list(nsParser.etree_to_dict(child) for child in etree)

                if duplicates:
                    if tags == duplicates:
                        final_dict = {etree.tag: list_of_children}
                    else:
                        list_of_not_dupes = list(
                            nsParser.etree_to_dict(single) for single in etree if single.tag not in duplicates)
                        list_of_just_dupes = list(
                            nsParser.etree_to_dict(dupe) for dupe in etree if dupe.tag in duplicates)
                        dupe_list_tag = duplicates[0]

                        output = {}
                        for x in list_of_not_dupes:
                            output.update(x)

                        output.update({dupe_list_tag + "S": list_of_just_dupes})
                        final_dict = {etree.tag: output}
                else:
                    output = {} 
                    for x in list_of_children:
                        output.update(x)
                    final_dict = {etree.tag: output}

            if etree.attrib is not None:
                final_dict.update(('@' + k, v) for k, v in etree.attrib.items())

            return final_dict
        else:
            return etree

    @staticmethod
    def data_to_dict(data):
        etree = nsParser.data_to_etree(data)
        dictionary = nsParser.etree_to_dict(etree)

        return dictionary
