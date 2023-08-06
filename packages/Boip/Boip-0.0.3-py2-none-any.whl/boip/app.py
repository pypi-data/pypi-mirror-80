# -*- coding: utf-8 -*-
"""メイン処理  
質問の生成、folder生成など。
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division
import sys

import PyInquirer

from .operation import BoipSetList, FolderFormatter

if sys.version_info[0] >= 3:
    unicode = str


class BoipQuestionCreator(object):
    """Boipのクエスト生成クラス
    """

    def __init__(self, target_path=None):
        """initialize.

        Args:
            target_path (str, optional): BoipSetを追加で検索する用のパス。DefaultsはNone
        """
        self.boip_set_list = BoipSetList(target_path)
        self.title = None
        self.question_answer = None
        self.duplicate_folder_path = None

    def __create_template_selector(self):
        """テンプレートを選択する質問を生成

        Returns:
            dict: {title: choice_title}
        """
        title_list = self.boip_set_list.get_title_list()
        questions = [
            {
                "type": "list",
                "name": "title",
                "message": "choice template.",
                "choices": title_list
            }
        ]
        answers = PyInquirer.prompt(questions)
        title = answers["title"]
        self.title = title

    def __create_multi_question(self):
        """複数の質問を生成

        Args:
            target_title (str): 設定fileのタイトル

        Returns:
            list: questions.
        """
        add_questions = self.boip_set_list.select_questions(self.title)
        questions = []
        for quest in add_questions:
            quest = {key: unicode(value) for key, value in quest.items()}

            question_template = {
                "type": "input",
            }
            question_template.update(quest)

            questions.append(question_template)
        questions_answers = PyInquirer.prompt(questions)
        self.question_answer = questions_answers

    def __create_folder_question(self):
        """folderを確認する質問を作成

        Returns:
            [type]: [description]
        """
        question = {
            "type": "input",
            "name": "folder_name",
            "message": "Create folder name?"
        }
        folder_answer = PyInquirer.prompt(question)
        if folder_answer["folder_name"] == "":
            raise self.NotFoundFolderName("フォルダ名が不正です。")

        folder_name = folder_answer["folder_name"]

        template_path = self.boip_set_list.select_template_path(self.title)

        copy_path = self.boip_set_list.duplicate_template_folder(template_path, folder_name)

        self.duplicate_folder_path = copy_path

    def __replace_file(self):
        """ファイルを上書きする
        """
        convert_extension_data = self.boip_set_list.select_convert_extensions(self.title)
        _ins = FolderFormatter(self.duplicate_folder_path, convert_extension_data, self.question_answer)
        _ins.replace_files()

    def create_question(self):
        """質問を作成する  
        """
        self.__create_template_selector()
        self.__create_multi_question()
        self.__create_folder_question()
        self.__replace_file()

    class NotFoundFolderName(Exception):
        pass
