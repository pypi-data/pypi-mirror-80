# -*- coding: utf-8 -*-
"""各実行クラスモジュール
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

import os
import shutil
from abc import ABCMeta, abstractmethod

import yaml

import codecs

PRESET_FOLDER = os.path.join(os.path.dirname(__file__), "preset")
SETTING_FILE_NAME = "boip.yaml"
TEMPLATE_FOLDER_NAME = "template"


class FileFormatter(object):
    """ファイルフォーマットクラス
    """

    def __init__(self, formatter_data):
        """initialize.

        Args:
            formatter_data (dict): フォーマットに使用するdict。
        """
        self.__formatter_data = formatter_data

    def __load_string_from_file(self, target_file):
        """fileから文字列を読み込む

        Args:
            target_file (str): ファイルパス

        Returns:
            str: ファイルの中身
        """
        with codecs.open(target_file, mode="r", encoding="utf-8") as f:
            return f.read()

    def __format_data(self, target_string):
        """文字列をフォーマットする

        Args:
            target_string (str): 対象の文字列

        Returns:
            str: フォーマット済みの文字列
        """
        format_after_data = target_string
        for key, value in self.__formatter_data.items():
            replace_word = "{" + key + "}"
            format_after_data = format_after_data.replace(replace_word, value)
        return format_after_data

    def __edit_file(self, target_file, target_string):
        """ファイルを編集する

        Args:
            target_string ([type]): [description]
        """
        with codecs.open(target_file, mode="w", encoding="utf-8") as f:
            f.write(target_string)

    def __change_extension(self, target_file_path, extension):
        """拡張子を変更する

        Args:
            target_file_path (str): 対象のファイルパス
            extension ([type]): 変更先の
        """
        target_file_dir = os.path.dirname(target_file_path)
        file_name = os.path.basename(target_file_path)
        no_extension_name = os.path.splitext(file_name)[0]
        change_extension_name = os.path.join(target_file_dir, no_extension_name + "." + extension)
        shutil.move(target_file_path, change_extension_name)

    def replace_file(self, target_file, replace_extension):
        """ファイルを上書きする

        Args:
            target_file ([type]): [description]
            insert_text ([type]): [description]
            after_extension ([type]): [description]
        """
        target_string = self.__load_string_from_file(target_file)
        after_string = self.__format_data(target_string)
        self.__edit_file(target_file, after_string)
        self.__change_extension(target_file, replace_extension)


class FolderFormatter(FileFormatter):
    """フォルダの置き換え実行クラス
    """

    def __init__(self, template_folder_path, convert_extension_data, formatter_data):
        """initialize.

        Args:
            template_folder_path (str): テンプレートフォルダパス
            convert_extension_data (dict): {変更前の拡張子: 変更後の拡張子}
            formatter_data (list): 置き換えに使うフォーマットデータ{"変数名": "置き換え後の文字"}
        """
        super(FolderFormatter, self).__init__(formatter_data)
        self.__path = template_folder_path
        self.__convert_extension_data = convert_extension_data

    def __search_extension_file(self, search_path, target_extension):
        """特定の拡張子のファイルを検索する

        Args:
            target_extension (str): 検索するパス

        Returns:
            str: 拡張子
        """
        found_files = []
        for root, dirs, files in os.walk(search_path):
            for filename in files:
                if filename.endswith(target_extension):
                    found_files.append(os.path.join(root, filename))
        return found_files

    def replace_files(self):
        """複数ファイルを上書きする
        """
        for before_extension, after_extension in self.__convert_extension_data.items():
            target_files = self.__search_extension_file(self.__path, before_extension)
            for target_file in target_files:
                super(FolderFormatter, self).replace_file(target_file, after_extension)


class BoipSetList(object):
    """質問とtemplateFolderのセットクラス
    """

    def __init__(self, additional_path=None):
        """initialize.

        Args:
            search_path (str, optional): boip_setを検索したいルートフォルダパス. Defaults to PRESET_FOLDER.
        """
        self.__boip_set_list = self.__get_boip_set_list(additional_path)

    def __get_boip_set_list(self, additional_path):
        # type: (str) -> list[SettingData]
        """boipSetを取得する

        Returns:
            list(SettingData): Setting Data list.
        """
        found_template_set = []
        search_path_list = [PRESET_FOLDER]
        if additional_path is not None:
            search_path_list.append(additional_path)
        for search_path in search_path_list:
            for root, dirs, files in os.walk(search_path):
                if TEMPLATE_FOLDER_NAME in dirs and SETTING_FILE_NAME in files:
                    file_index = files.index(SETTING_FILE_NAME)
                    setting_file = os.path.join(root, files[file_index])

                    dir_index = dirs.index(TEMPLATE_FOLDER_NAME)
                    template_folder = os.path.join(root, dirs[dir_index])

                    found_template_set.append(SettingData(setting_file, template_folder))

        return found_template_set

    def select_template_path(self, target_title):
        # type: (str) -> str
        """titleから該当のTemplateFolderPathを取得する

        Args:
            target_title (str): setting_file内のtitle名

        Returns:
            str: TemplateFolderPath
        """
        for template_set in self.__boip_set_list:
            if target_title == template_set.title:
                return template_set.template_path

    def select_questions(self, target_title):
        # type: (str) -> list[{str: str}]
        """titleから該当のquestionsを取得する

        Args:
            target_title (str): 検索したboip.yamlから選択したtile名

        Returns:
            list: [{"name": "質問の答えを格納する変数名", "message": "質問"}]
        """
        for template_set in self.__boip_set_list:
            if target_title == template_set.title:
                return template_set.questions

    def select_convert_extensions(self, target_title):
        # type: (str) -> {str, str}
        """titleから該当のconvert_extensionsを取得する

        Args:
            target_title (str): 対象のtitle名

        Returns:
            dict: {dist extensins: src extensins}
        """
        for template_set in self.__boip_set_list:
            if target_title == template_set.title:
                return template_set.convert_extensions

    def duplicate_template_folder(self, dis_folder, src_folder_name):
        # type: (str, str) -> str
        """TemplateFolderを複製する

        Args:
            dis_folder (str): 複製元のフォルダパス
            src_folder_name (str): 複製先のフォルダパス
        """
        current_directory = os.getcwd()

        target_folder = os.path.join(current_directory, src_folder_name)

        shutil.copytree(dis_folder, target_folder)
        return target_folder

    def get_title_list(self):
        # type: () -> list
        """タイトルリストを取得する

        Returns:
            list: タイトルリスト
        """
        title_list = []
        for template_set in self.__boip_set_list:
            title_list.append(template_set.title)
        return title_list


# =================================================================================
# Reader
# =================================================================================
class BaseReader(object):
    """ベースの読み込みクラス
    """
    __metaclass__ = ABCMeta

    def __init__(self, path):
        """initialize.

        Args:
            path (str): 対象のフォルダパス
        """
        self.read_path = path

    @ abstractmethod
    def get_read_data(self):
        # type: () -> None
        """読み込んだデータを返す
        """
        pass


class YamlFileReader(BaseReader):
    """YamlFile用のReader
    """

    def get_read_data(self):
        """読み込んだデータを返す

        Returns:
            dict: yaml data.
        """
        with open(self.read_path) as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            return yaml_data


# =================================================================================
# Data
# =================================================================================
class SettingData(object):
    """SettingDataデータ構造
    """

    def __init__(self, setting_file, template_folder, reader=YamlFileReader):
        self.__data = self.__get_load_data(setting_file, reader)
        self.__title = self.__data["title"]
        self.__questions = self.__data["question"]
        self.__convert_extensions = self.__data["convertExtensions"]
        self.__template_path = template_folder

    @ property
    def title(self):
        # type: () -> str
        """boip.yaml内のtitle

        Returns:
            str: title
        """
        return self.__title

    @ property
    def questions(self):
        # type: () -> list[{str: str}]
        """質問リスト

        Returns:
            list: 質問リスト
        """
        return self.__questions

    @ property
    def convert_extensions(self):
        """拡張子変更リスト

        Returns:
            dict: {変更前: 変更後}
        """
        # type: () -> {str: str}
        return self.__convert_extensions

    @ property
    def template_path(self):
        """テンプレートフォルダのパス

        Returns:
            str: フォルダパス
        """
        # type: () -> str
        return self.__template_path

    def __get_load_data(self, setting_file, reader):
        """データを読み込む

        Args:
            setting_file (str): 読み込みたいファイル
            reader (operation.BaseReader): ファイル読み込みクラス

        Returns:
            any: ファイル内のデータ
        """
        _reader = reader(setting_file)
        data = _reader.get_read_data()
        return data
