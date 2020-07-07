from Base import Base
from const import BaseURL
import json
import time


class Scraper(Base):

    def __init__(self):
        super().__init__()
        self.scraper_type = "Scraper"
        self.log_setup()

    @staticmethod
    def save_html(data, file='test'):
        with open(f'logs/{file}.html', 'a') as file:
            file.write(data)
            
    @staticmethod
    def save_json(data, file):
        # todo change json path
        with open(f"{file}.json", "w") as write_file:
            json.dump(data, write_file, indent=4)

    # def get_links(self, url):
    #     soup = self.get_content_simple(url)
    #     if self.status:

    def attach_domain(self, url):
        return f"{BaseURL}{url}"

    def get_nav_links(self, url):
        soup = self.link_requestor(url)
        if self.status:
            li_tags = soup.select_one('#cssmenu > ul').find_all('li', recursive=False)
            links = [li.find('a') for li in li_tags]
            links = {a.text.strip(): a.get('href') for a in links[1:6]}
            return links

        else:
            self.log(f"No home page found!")
            return self.status

    def get_blog_post(self, link):
        soup = self.link_requestor(self.attach_domain(link))
        if not self.status:
            return None
        div = soup.select_one('div.outer-warpper > div.columns')
        if div:
            title = div.select_one("h2").text
            detail = [p.text for p in div.select('p')]
            detail = "\n\n".join(detail)
            return {'title': title, 'detail': detail.encode('ascii', 'ignore').decode()}
        else:
            time.sleep(15)
            print(f"No response against {link}")
            return None

    def get_blog_data(self, tag):
        page = 12
        url = f"{BaseURL}{tag}?p={page}#page{page}"
        soup = self.link_requestor(url)
        if self.status:
            post_links = soup.select("div.blog-list > div > a")
            post_links = [a.get('href') for a in post_links]
            posts = []
            for link in post_links:
                post = self.get_blog_post(link)
                if not post:
                    continue
                posts.append(post)
            self.save_json(posts, "posts")
            return posts
        else:
            self.log("No posts found!")
            return self.status

    def about_firm(self, link):
        soup = self.link_requestor(self.attach_domain(link))
        data = soup.select('div.content-box > div > p')
        data = "\n".join(data)
        with open(f'data/firm.txt', 'w') as file:
            file.write(data)

    def get_testimonials(self, link):
        soup = self.link_requestor(self.attach_domain(link))
        output = []
        for div in soup.select('.testimonial-items'):
            name = ''
            for p in div.select('span'):
                name += p.text
            output.append({'author': name[2:], 'experience': div.select_one('p').text})
        self.save_json(output, 'testimonials')

    def get_attorneys(self, link):
        soup = self.link_requestor(self.attach_domain(link))
        output = []
        for div in soup.select('.member-item'):
            intro = [p.text for p in div.select('p')]
            output.append({'name': div.select_one('.page-title').text,
                           'intro': "\n".join(intro)})
        self.save_json(output, "attorneys")

    def get_practice_areas(self, link):
        soup = self.link_requestor(self.attach_domain(link))
        with open('data/test.html', 'w') as f:
            f.write(soup.prettify())
        atags = soup.select_one('.submenu-for-mobile').select('.has-sub > a')
        links = [(a.get('href'), a.text) for a in atags]
        practice_areas = []
        for link in links:
            soup = self.link_requestor(self.attach_domain(link[0]))
            text = [each.text for each in soup.select_one('.sub-right').find_all(['h2', 'p'])]
            practice_areas.append({'name': link[1],
                                   'description': ("\n".join(text)).encode('ascii', 'ignore').decode()})
        self.save_json(practice_areas, "practice_areas")

    def test(self, url):
        practice_areas = []
        soup = self.link_requestor(self.attach_domain(link))
        name = soup.select_one('h1.page-title')
        name = name.text if name else soup.select_one('div > div > h1').text
        print(name)
        text = [each.text for each in soup.find_all(['h2', 'p'])]
        self.save_html(soup.prettify(), name)
        # exit()
        practice_areas.append({'name': name,
                               'description': ("\n".join(text)).encode('ascii', 'ignore').decode()})

        self.save_json(practice_areas, "practice_areas")

    def get_post(self, url):
        soup = self.link_requestor(url)
        h1 = soup.select_one(".entry-title").text
        p_tags = soup.select(".entry-content p")
        content = "\n".join([p.text for p in p_tags])
        return {"name": h1, "description": content.encode('ascii', 'ignore').decode()}

    def get_posts(self, url):
        soup = self.link_requestor(url)
        divs = soup.select(".entry-title a")
        links = [div.get('href') for div in divs]
        posts = []
        print(len(links))
        for link in links:
            data = self.get_post(link)
            posts.append(data)
        print(len(posts))
        return posts

    def run(self):
        posts = []
        urls = ["https://www.hannlawfirm.com/blog/category/divorce/",
                "https://www.hannlawfirm.com/blog/category/divorce/page/2/",
                "https://www.hannlawfirm.com/blog/category/child-custody/",
                "https://www.hannlawfirm.com/blog/category/firm-news/",
                "https://www.hannlawfirm.com/blog/category/high-asset-divorce/",
                "https://www.hannlawfirm.com/blog/category/motor-vehicle-accidents/",
                "https://www.hannlawfirm.com/blog/category/wrongful-death/"]
        for url in urls:
            posts.extend(self.get_posts(url))
        self.save_json(posts, "posts")
        return True

if __name__ == "__main__":
    status = Scraper().run()
    print(f"{status}")
