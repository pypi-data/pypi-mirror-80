import json

import requests


class XesWork:
    def __init__(self, work_id):
        self.url = 'https://code.xueersi.com/api/compilers/v2/{}?id={}'.format(work_id, work_id)
        self.headers = {'Content-Type': 'application/json'}
        self.a = requests.get(self.url, headers=self.headers)
        self.a.encoding = 'gzip'
        self.p = self.a.text
        #self.respon = self.p.encode('ascii').decode('unicode_escape')
        self.response = json.loads(self.p, strict=False)
        #self.response = self.respons.replace('{', ',').replace('}', ',').replace('\"', '').split(',')
        #del self.response[0]
        self.picture_url = "https://livefile.xesimg.com/programme/assets/7ddec8b247e63d9971addecd8b752b3d.jpg"

    def get_name(self):
        #return self.response['data']['name']
        return self.response

    def get_description(self):
        if self.response['data']['description'] == '':
            return None
        else:
            return self.response['data']['description']

    def get_likes(self):
        return self.response['data']['likes']

    def get_unlikes(self):
        return self.response['data']['unlikes']

    def get_favorites(self):
        return self.response['data']['favorites']

    def get_adapt_numbers(self):
        return self.response['data']['source_code_views']

    def download_icon(self):
        import os
        os.makedirs('./', exist_ok=True)
        from urllib.request import urlretrieve
        urlretrieve(self.picture_url, './icon.jpg')
        os.system('icon.jpg')
        string = "start explorer " + os.getcwd()
        os.system(string)
        return True

    def get_author_name(self):
        return self.response['data']['username']

    def get_author_id(self):
        return self.response['data']['user_id']

    def get_work_tags(self):
        tags = self.response['data']['tags']
        list_of_tags = tags.split()
        return list_of_tags

    def get_hot(self):
        return self.response['data']['popular_score']

    def get_views(self):
        return self.response['data']['views']

    def get_first_published_time(self):
        return self.response['data']['published_at']

    def get_latest_modified_time(self):
        return self.response['data']['modified_at']

    def get_latest_updated_time(self):
        return self.response['data']['updated_at']

    def get_created_time(self):
        return self.response['data']['created_at']

    def is_hidden_code(self):
        if self.response['data']['hidden_code'] == 2:
            return False
        else:
            return True


class XesUserSpace:
    def __init__(self, user_id):
        self.url_1 = 'https://code.xueersi.com/api/space/index?user_id=' + str(user_id)
        self.url_2 = 'https://code.xueersi.com/api/space/profile?user_id=' + str(user_id)
        self.headers = {'Content-Type': 'application/json',}
        self.p_1 = requests.get(self.url_1, headers=self.headers).text
        self.p_2 = requests.get(self.url_2, headers=self.headers).text
        self.response_index = json.loads(self.p_1, strict=False)
        self.response_profile = json.loads(self.p_2, strict=False)
        self.head_url = self.response_profile['data']['avater_path']

    def download_user_head(self):
        #类似于分类讨论【捂脸】
        if self.head_url[-3, -1] == 'gif':
            import os
            import shutil
            os.makedirs('./', exist_ok=False)
            from urllib.request import urlretrieve
            urlretrieve(self.head_url, './icon.gif')
            shutil.move(os.getcwd() + '/icon.gif', os.path.join(os.path.expanduser("~"), 'Desktop'))
            return '已成功将该用户头像下载到桌面'
        elif self.head_url[-3, -1] == 'jpg':
            import os
            import shutil
            os.makedirs('./', exist_ok=False)
            from urllib.request import urlretrieve
            urlretrieve(self.head_url, './icon.jpg')
            shutil.move(os.getcwd() + '/icon.jpg', os.path.join(os.path.expanduser("~"), 'Desktop'))
            return '已成功将该用户头像下载到桌面'
        else:
            import os
            import shutil
            os.makedirs('./', exist_ok=False)
            from urllib.request import urlretrieve
            urlretrieve(self.head_url, './icon.png')
            shutil.move(os.getcwd() + '/icon.png', os.path.join(os.path.expanduser("~"), 'Desktop'))
            return '已成功将该用户头像下载到桌面'

    def get_fans_number(self):
        #这孩子多少粉了？
        return self.response_profile['data']['fans']

    def get_follows_number(self):
        #这孩子有几个偶像（关注了几个人）？
        return self.response_profile['data']['follows']

    def is_follow(self):
        #你有没有关注他呢？？？
        if self.response_profile['data']['is_follow'] == 1:
            return True
        else:
            return False

    def get_realname(self):
        #他真名叫啥？
        return self.response_profile['data']['realname']

    def get_sign(self):
        #个性签名是什么？
        return self.response_profile['data']['signature']

    def get_number_of_works(self):
        #他一共有多少作品（加上没发布的）？
        return self.response_index['data']['overview']['works']

    def get_number_of_likes(self):
        #他的所有作品一共获了多少赞？
        return self.response_index['data']['overview']['likes']

    def get_number_of_views(self):
        #总浏览量
        return self.response_index['data']['overview']['views']

    def get_adapted_number(self):
        #被改编多少次？
        return self.response_index['data']['overview']['source_code_views']

    def get_favorites(self):
        #被收藏多少次？
        return self.response_index['data']['overview']['favorites']

    def get_first_eight_fans(self):
        #获取他前八个粉丝的姓名和id
        a_list = []
        for i in self.response_index['data']['fans']['data']:
            a_list.append((i['id'], i['realname']))
        return a_list

    def get_first_eight_favourites(self):
        #获取他前八个收藏的id、name、作者id和作者名
        a_list = []
        for i in self.response_index['data']['favourites']['data']:
            a_list.append((i['id'], i['name'], i['user_id'], i['user_name']))
        return a_list

    def get_representative_work(self):
        #代表作
        return self.response_index['data']['representative_work']['name']
