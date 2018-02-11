import os
import re
import requests
from datetime import datetime

from PIL import Image
from Tistory.Base import Base
from bs4 import BeautifulSoup


class Post(Base):

    def __init__(self, image_dir, blog):
        super().__init__()

        self.image_dir = "Storage/Images/"
        self.blog = blog

        if image_dir :
            self.image_dir = image_dir


    def make_relate_dir(self, page_number):
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

        if not os.path.exists(self.image_dir + str(page_number)):
            os.makedirs(self.image_dir + str(page_number))

    @staticmethod
    def clean(html):
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', html)

    def latest(self):
        response = requests.get(self.blog + '/', headers=self.header)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.select('body')

        posts_numbers = []
        for link in body[0].find_all('a'):
            if link.has_attr('href'):
                if not link['href'].replace('/', '').isdigit():
                    continue
                posts_numbers.append(int(link['href'].replace('/', '')))
        return sorted(posts_numbers, reverse=True)[0]

    def read(self, page_number):
        response = requests.get(self.blog + '/' + str(page_number), headers=self.header)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.select('.tt_article_useless_p_margin')
        if not body:
            return False

        for image in body[0].find_all('img'):
            self.make_relate_dir(page_number)

            path, file_name = os.path.split(image['src'])
            im = Image.open(requests.get(image['src'], stream=True).raw)
            im.save(os.path.join(self.image_dir + str(page_number), file_name + "." + im.format), quality=85)

            image['src'] = self.image_dir + str(page_number) + "/" + file_name + "." + im.format

        tags = []
        title = soup.select('h3.tit_post')[0].text
        published_date = datetime.strptime(re.search(r'\d{4}.\d{2}.\d{2}', str(soup.select('span.info_post')[0])).group(), '%Y.%m.%d').date()

        category = str('0x00 개발/PHP').split(' ')[1].split('/')[0]
        sub_category = str('0x00 개발/PHP').split(' ')[1].split('/')[1]

        for tag in soup.select('#mArticle dl.list_tag a'):
            tags.append(tag.text)

        for code in soup.find_all("code"):
            code.replace_with(self.clean(str(code.findChildren()[0])))

        content = str(body[0]).split('<div class="container_postbtn">')[0]
        return content, {
            'title' : title,
            'published_date' : published_date,
            'category' : category,
            'sub_category' : sub_category,
            'tags' : tags
        }

