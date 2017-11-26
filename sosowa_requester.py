import pyquery
import requests
import json
import threading
import re
import collections

import article_entity

####
# sosowa_requester
# The http request sender for Touhou Sosowa.
#
# @author sy4may0
# @version 1.0
#
class sosowa_requester():
    __lock = threading.Lock()
    __reload_lock = threading.Lock()
    __instance = None

    __latest_page = None
    __config = None

    # Constructor(singleton)
    # 
    def __init__(self,config_file):
        if self.__config is None:
            f = open(config_file, 'r').read()
            self.__config = json.loads(f)

        if self.__latest_page is None:
            self.reload_sosowa_latest_pages()

    # instance created check.
    #
    def __new__(cls, *args, **kwargs):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super(sosowa_requester, cls).__new__(cls)
        return cls.__instance

    # get_sosowa_pages()
    # Get sosowa latest page number.
    #
    # @throws HtmlElementFailureException
    #
    def reload_sosowa_latest_pages(self):
        with self.__reload_lock:
            html = requests.get(self.__config["main_url"] + "/sosowa/ssw_l/")
            query = pyquery.PyQuery(html.text)

            el_active_page = self.__get_pyquery_element(html.text, query, 'a.active')
            self.__latest_page = int(el_active_page[0].text)


    # get_sosowa_product_list()
    # Get sosowa product list of a page.
    #
    # ! huge object will be create.
    #
    # @param page_num : sosowa page number
    #
    # @throws PageOverflowException
    # @throws HtmlElementFailureException
    #
    def get_sosowa_product_list(self, page_num):
        if page_num > self.__latest_page or page_num <= 0:
            raise PageOverflowException(page_num)

        result = collections.OrderedDict()

        html = requests.get(self.__config["main_url"] + "/sosowa/ssw_l/" + str(page_num))
        query = pyquery.PyQuery(html.text)

        articles = self.__get_pyquery_element(html.text, query, 'tr[id^="article"]')

        # article data scraping.
        for article in articles:
            
            e_article = article_entity.article_entity()

            e_article.set_article('p_belong', page_num)

            article_id = re.findall("[0-9]+", article.attrib['id'])
            if len(article_id) != 1:
                raise SosowaRequesterException("Article ID scraping failed.")
            e_article.set_article("id", article_id[0])

            td_title = self.__get_lxml_element(article, 'td.title')
            a_title = self.__get_lxml_element(td_title[0], 'a')
            if len(a_title) != 1:
                raise SosowaRequesterException("Article title scraping failed.")
            e_article.set_article("title", a_title[0].text)

            td_author = self.__get_lxml_element(article, 'td.name')
            a_author = self.__get_lxml_element(td_author[0], 'a')
            if len(a_author) != 1:
                raise SosowaRequesterException("Article author scraping failed.")
            e_article.set_article('author', a_author[0].text)

            td_d_upload = self.__get_lxml_element(article, 'td.dateTime')
            if len(td_d_upload) != 1:
                raise SosowaRequesterException("Article Upload date scraping failed.")
            e_article.set_article('d_upload', td_d_upload[0].text)

            td_c_page = self.__get_lxml_element(article, 'td[class~=\"pageCount\"]')
            if len(td_c_page) != 1:
                raise SosowaRequesterException("Article pageCount scraping failed.")
            e_article.set_article('c_page', td_c_page[0].text)

            td_size = self.__get_lxml_element(article, 'td[class~=\"size\"]')
            if len(td_size) != 1:
                raise SosowaRequesterException("Article size scraping failed.")
            e_article.set_article('size', td_size[0].text)

            td_c_evaluation = self.__get_lxml_element(article, 'td[class~=\"evaluationCount\"]')
            if len(td_c_evaluation) != 1:
                raise SosowaRequesterException("Article evaluationCount scraping failed.")
            e_article.set_article('c_evaluation', td_c_evaluation[0].text)

            td_c_comment = self.__get_lxml_element(article, 'td[class~=\"commentCount\"]')
            if len(td_c_comment) != 1:
                raise SosowaRequesterException("Article commentCount scraping failed.")
            e_article.set_article('c_comment', td_c_comment[0].text)

            td_points = self.__get_lxml_element(article, 'td[class~=\"points\"]')
            if len(td_points) != 1:
                raise SosowaRequesterException("Article points scraping failed.")
            e_article.set_article('points', td_points[0].text)

            td_rate = self.__get_lxml_element(article, 'td[class~=\"rate\"]')
            if len(td_rate) != 1:
                raise SosowaRequesterException("Article rate scraping failed.")
            e_article.set_article('rate', td_rate[0].text)

            result[e_article.get_article('id')] = e_article

        # tag data scraping.
        for key in result.keys():
            result_tags = list()
            csstag = 'tr#tags' + key 

            tr_article = self.__get_pyquery_element(html.text, query, csstag)
            if len(tr_article) != 1:
                raise SosowaRequesterExceprion("Article tag data tr table scraping failed.")


            # Tag suppose No data.
            try:
                li_tag = self.__get_lxml_element(tr_article[0], 'li')
            except HtmlElementFailureException:
                li_tag = []

            for tag in li_tag:
                a_tag = self.__get_lxml_element(tag, 'a')
                if len(a_tag) != 1:
                    raise SosowaRequesterExceprion("Article tag data scraping failed.")
                result_tags.append(a_tag[0].text)

            result[key].set_article('tag', result_tags)

        return result

   
    # get_sosowa_article()
    # Get sosowa article.
    #
    # @param article : Sosowa article entity.
    #
    def get_sosowa_article(self, article):
        url = list()
        url.append(self.__config['main_url'])
        url.append("sosowa/ssw_l")
        url.append(str(article.get_article('p_belong')))
        url.append(article.get_article('id'))

        html = requests.get("/".join(url))
        query = pyquery.PyQuery(html.text)

        # Scrape pager.
        page_list = []
        try:
            ul_pager = self.__get_pyquery_element(html.text, query, 'ul.pager')
            print(len(ul_pager))
            if len(ul_pager) != 2:
                raise SosowaRequesterException("Article pager scrape failed.")
            a_pager = self.__get_lxml_element(ul_pager[0], 'a')
            for pager in a_pager:
                if pager.text.isdigit():
                    page_list.append(pager.attrib['href'])

        except HtmlElementFailureException:
            page_list = ['']
        
        # Scrape content.
        contents = []
        i = 0
        for page in page_list:
            contents.append("[PAGE:" + str(i) + "]\n")
            if page != '':
                html = requests.get(self.__config['main_url'] + page)
                query = pyquery.PyQuery(html.text)

            d_content = self.__get_pyquery_element(html.text, query, 'div#contentBody')
            if len(d_content) != 1:
                raise SosowaRequesterException("Article contentBody scraping failed.")
            content = (d_content.html(method='html'))

            if content is not None:
                contents.append(content.replace('<br>', "\n"))

            i += 1
            
        article.set_article('content', "".join(contents))


        # Scrape afterword.
        d_afterword = self.__get_pyquery_element(html.text, query, 'div#afterwordBody')
        if len(d_afterword) != 1:
            raise SosowaRequesterException("Article afterwordBody scraping failed.")
        afterword = (d_afterword.html(method='html'))
        if afterword is not None:
            article.set_article('afterword', afterword.replace("<br>", "\n"))
        else:
            article.set_article('afterword', "None")

    # get_pyquery_element()
    # Get HTML Elements with checking.
    # If elements not found, raise HtmlElementFailureException.
    #
    # @throws HtmlElementFailureException
    #
    def __get_pyquery_element(self, htmltext, query, csstag):
        elements = query.find(csstag)
        if len(elements) <= 0 or elements is None:
            raise HtmlElementFailureException(csstag, htmltext)

        return elements

    # get_lxml_element()
    # Get HTML Elements with checking.
    # If elements not found, raise HtmlElementFailureException.
    #
    # @throws HtmlElementFailureException
    #
    def __get_lxml_element(self, element, csstag):
        elements = element.cssselect(csstag)
        if len(elements) <= 0 or elements is None:
            raise HtmlElementFailureException(csstag)

        return elements

####
# PageOverflowException
# This Exception is thrown at be called sosowa page number is out of range.
#
class PageOverflowException(Exception):
    def __init__(self, page_num):
        self.page_num = page_num
        self.message = "Page [" + self.page_num + "] is out of range."

    def get_page_num(self):
        return self.page_num

    def get_message(self):
        return self.message

####
# HtmlElementFailureException
# This Exception is thrown at HTML tag searching failure.
#
class HtmlElementFailureException(Exception):
    def __init__(self, csstag, htmltext = "No html source data"):
        self.htmltext = htmltext
        self.csstag = csstag
        self.message = "HTML Element find failed. CSS tag is [" + self.csstag + "]."

    def get_htmltext(self):
        return self.htmltext

    def get_csstag(self):
        return self.csstag

    def get_message(self):
        return self.message

####
# SosowaRequesterexception
# General Exception class for sosowa scraping.
#
class SosowaRequesterException(Exception):
    def __init__(self, message):
        self.message = message

    def get_message():
        return self.message


