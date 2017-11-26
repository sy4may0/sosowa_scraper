####
# article_entity
# Sosowa article entity class.
#
# @author sy4may0
# @version 1.0
#

class article_entity():
    __article_data = None

    # Constructor
    #
    def __init__(self):
        self.__article_data = dict()
        self.__article_data['p_belong'] = None
        self.__article_data['id'] = None
        self.__article_data['title'] = None
        self.__article_data['author'] = None
        self.__article_data['d_upload'] = None
        self.__article_data['c_page'] = None
        self.__article_data['size'] = None
        self.__article_data['c_evaluation'] = None
        self.__article_data['c_comment'] = None
        self.__article_data['points'] = None
        self.__article_data['rate'] = None
        self.__article_data['tag'] = None
        self.__article_data['content'] = None
        self.__article_data['afterword'] = None

    # set_article()
    # Set article data.
    #
    # @param key : following keys.
    #     title, author, d_upload, c_page, size, 
    #     c_evalution, c_comment, points, rate, tag
    # @param value : Value for key.
    #
    def set_article(self, key, value):
        if key in self.__article_data:
            self.__article_data[key] = value
        else:
            raise KeyNotFoundExeption(key)

    # get_article()
    # Get article data.
    #
    # @param key : following keys.
    #     title, author, d_upload, c_page, size, 
    #     c_evalution, c_comment, points, rate, tag
    #
    def get_article(self, key):
        if key in self.__article_data:
            return self.__article_data[key]
        else:
            raise KeyNotFoundException(key)

    # show_detail()
    # show shaping detail text data.
    #
    def show_detail(self):
        result = []

        result.append(self.__article_data['id'])
        result.append('::')

        title = self.__article_data['title']
        if len(title) > 32:
            pad_title = title[0:32]
        else:
            pad_title = title.ljust(32, " ")
        result.append(pad_title)

        result.append('\n    AUTHOR:')
        author = self.__article_data['author']
        if len(author) > 16:
            pad_author = author[0:16]
        else:
            pad_author = author.ljust(16, " ")
        result.append(pad_author)

        result.append(" UPLOAD:")
        result.append(self.__article_data['d_upload'])

        result.append(" SIZE:")
        result.append(self.__article_data['size'].ljust(10, " "))

        result.append(" EVAL:")
        result.append(self.__article_data['c_evaluation'].ljust(10, " "))

        result.append(" COMMENT:")
        result.append(self.__article_data['c_comment'].ljust(5, " "))

        result.append(" POINT:")
        result.append(self.__article_data['points'].ljust(7, " "))

        result.append(" RATE:")
        result.append(self.__article_data['rate'].ljust(7, " "))

        result.append("\n    TAG:")
        if self.__article_data['tag'] is not None:
            for t in self.__article_data['tag']:
                result.append(t)
                result.append(" ")
            
        print("".join(result))

    # show_content()
    # show shaping content data.
    #
    def show_content(self):
        result = []
        result.append("[TITLE]\n")
        result.append(self.__article_data['title'])
        result.append("\n\n[CONTENT]\n")
        result.append(self.__article_data['content'])
        result.append("\n\n[AFTERWORD]\n")
        result.append(self.__article_data['afterword'])

        print("".join(result))

####
# KeyNotFoundException
# This exception thrown at article data key has not found.
class KeyNotFoundException(Exception):
    def __init__(self, key):
        self.key = key
        self.message = "Article data key [" + self.key + "] is not found."

    def get_key():
        return self.key

    def get_message():
        return self.message

