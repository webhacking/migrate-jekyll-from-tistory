import re, html2text
from Tistory.Post import Post

post = Post(blog='http://blog.hax0r.info', image_dir='assets/images/posts/')
for i in range(1, post.latest()):
    content = post.read(i)

    if content:
        print('수행 :' + str(i))
        h = html2text.HTML2Text()
        markdown = h.handle(content[0])

        replaced = """
            ---
            layout: post
            title: "%s"
            description: ""
            date: %s
            tags: %s
            comments: true
            share: true
            ---
        """ % (content[1]['title'], content[1]['published_date'], content[1]['tags'])

        file = open('Storage/Posts/' + str(content[1]['published_date']) + '-' + str(i) + '.md', 'w')
        file.write(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', replaced, flags=re.M) + '\n' + markdown)
        file.close()
