from URLSetter import URLSetter_Naver

a = URLSetter_Naver()
urllist = a.GetUrlList()

for url in urllist :
    print(url.Category)
    print(url.Url)