import GLXClansKeeper


class Keeper(GLXClansKeeper.Interface):
    def __init__(self):
        GLXClansKeeper.Interface.__init__(self)
        self.__lang = None
        self.__charset = None
        self.lang = None
        self.charset = None

    @property
    def lang(self):
        """
        A reference to HTTP_ACCEPT_LANGUAGE

        :return: Reference List HTTP_ACCEPT_LANGUAGE
        :rtype: str
        """
        return self.__lang

    @lang.setter
    def lang(self, value=None):
        """
        Set the ``lang`` property value

        Default value is ``en`` and be restore when ``lang`` is set to None

        :param value: The lang use on the html document
        :type value: str or none
        :raise TypeError: When ``lang`` value is not str type or None
        """
        if value is None:
            value = 'en'
        if type(value) != str:
            raise TypeError('"lang" value must be a str type or None')
        if self.lang != value:
            self.__lang = value

    @property
    def charset(self):
        """
        The ``charset`` property, Specify the character encoding for the HTML document

        http://webcheatsheet.com/html/character_sets_list.php

        :return: the character encoding
        :rtype: str
        """
        return self.__charset

    @charset.setter
    def charset(self, value=None):
        """
        set the ``charset`` property

        Default value is 'utf-8' and be restore when ``charset`` is set to None

        In theory, any character encoding can be used, but no browser understands all of them.
        The more widely a character encoding is used, the better the chance that a browser will understand it.

        https://www.iana.org/assignments/character-sets/character-sets.txt

        :param value: the charset use on html and markdown document
        :type value: str or none
        :raise TypeError: ``charset`` is not a str type or None
        """
        if value is None:
            value = 'utf-8'
        if type(value) != str:
            raise TypeError('"charset" value must be a str type or None')
        if self.charset != value:
            self.__charset = value

    def run(self):  # pragma: no cover
        """
        That function , make the job.

        Everything must be set before star it function.

        """
        self.start()
