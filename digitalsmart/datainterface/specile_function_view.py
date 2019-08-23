import time
import random
from threading  import  Thread
from django.views.decorators.csrf import csrf_exempt

from django.http import StreamingHttpResponse, JsonResponse

from .tasks import NetWorker


class Crack:
    # http://127.0.0.1:8000/interface/api/getMusic?name=我愿意平凡的陪在你身旁&type=netease
    def get_music(self, request):
        """
        获取音乐列表
        返回{'author': '作者', 'url': '下载链接', 'title': '歌名'}
        :param request:
        :return:
        """
        musicname = request.GET.get("name")  # 音乐名
        soft_type = request.GET.get("type")  # 软件类型，
        page = request.GET.get("page")  # 第几页
        if page is None:
            page = 1
        try:
            page = int(page)
        except Exception:
            return JsonResponse({"status": 0, "message": "error"})
        # netease：网易云，qq：qq音乐，kugou：酷狗音乐，kuwo：酷我，
        # xiami：虾米，baidu：百度，1ting：一听，migu：咪咕，lizhi：荔枝，
        # qingting：蜻蜓，ximalaya：喜马拉雅，kg：全民K歌，5singyc：5sing原创，
        # 5singfc：5sing翻唱
        if not musicname:
            return JsonResponse({"status": 0, "message": "error"})
        net = NetWorker()
        iter_music_info = net.get_music_list(musicname, soft_type, page)  # 获取所有与之相关的音乐，包括下载链接
        return JsonResponse({"data": list(iter_music_info)})

    # http://127.0.0.1:8000/interface/api/downMusic?url=下载链接
    def down_music(self, request):
        """
            下载音乐，根据上面get_music的链接下载
        :param request:
        :return:
        """

        dowun_url = request.GET.get("url")
        pre_path = request.path + "?url="
        href = request.get_full_path()
        dowun_url = href.replace(pre_path, "")

        if dowun_url is None:
            return JsonResponse({"status": 0, "message": "error"})
        # netease：网易云，qq：qq音乐，kugou：酷狗音乐，kuwo：酷我，
        # xiami：虾米，baidu：百度，1ting：一听，migu：咪咕，lizhi：荔枝，
        # qingting：蜻蜓，ximalaya：喜马拉雅，kg：全民K歌，5singyc：5sing原创，
        # 5singfc：5sing翻唱
        net = NetWorker()
        strem = net.down_music_content(url=dowun_url)
        response = StreamingHttpResponse(strem)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="example.mp3"'

        return response

    # http://127.0.0.1:8000/interface/api/validation?card=440514199804220817

    def identity_authentication(self, request):
        """
        身份认证
        :param request:
        :return:
        """

        idcard = request.GET.get("card")

        person_info = NetWorker().get_idcard_info(idcard)
        if person_info is None:
            return JsonResponse({"status": 0, "message": "身份证号有问题"})

        response = {
            "发证地区": person_info.area,
            "电话区号": person_info.phone,
            "出生日期": person_info.bir,
            "农历": person_info.lunar,
            '性别/生肖': person_info.gender,
            '当地经纬度': person_info.latlon
        }
        return JsonResponse(response)

    # def parse_baidudoc(self, request):
    #     """
    #     解析百度文档链接，并提供可下载链接
    #     :param request:
    #     :return:
    #     """
    #     pre_path = request.path + "?url="
    #     href = request.get_full_path()
    #     parse_url = href.replace(pre_path, "")
    #     # url = request.GET.get("url")
    #     file_type = request.GET.get("type")  # 类型有doc,pdf,ppt
    #     if not (parse_url and file_type):
    #         return JsonResponse({"status": 0, "message": "error"})
    #     net = NetWorker()
    #     doc_url = net.get_baidu_doc(parse_url, file_type)
    #     return JsonResponse(doc_url)
    #
    # # http://127.0.0.1:8000/interface/api/baidudoc?url=目标文档链接
    #
    # def down_baidu_doc(self, request):
    #     """
    #     下载百度文档
    #
    #     """
    #     pre_path = request.path + "?url="
    #     href = request.get_full_path()
    #     dowun_url = href.replace(pre_path, "")
    #
    #     file_type = request.GET.get("type")  # 类型有doc,pdf,ppt
    #     if not (dowun_url):
    #         return JsonResponse({"status": 0, "message": "error"})
    #     net = NetWorker()
    #     iter_doc = net.down_baidu_doc(dowun_url)
    #     response = StreamingHttpResponse(iter_doc)
    #     response['Content-Type'] = 'application/octet-stream'
    #
    #     response['Content-Disposition'] = 'attachment;filename={0}.{1}'.format(time.time(), file_type)
    #     return response

    # http://127.0.0.1:8000/interface/api/goodsprice?url=目标商品链接

    def get_goods_price_change(self, request):
        """
        获取某商品的价格变化情况
        支持天猫(detail.tmall.com、detail.m.tmall.com)、淘宝(item.taobao.com、h5.m.taobao.com)、
        京东(item.jd.com、item.m.jd.com)、一号店(item.yhd.com）、苏宁易购(product.suning.com)、
        网易考拉(goods.kaola.com)、当当网(product.dangdang.com)、亚马逊中国(www.amazon.cn)、国美(item.gome.com.cn)等电商
        商品详情的历史价格查询。

        """
        pre_path = request.path + "?url="
        href = request.get_full_path()
        url = href.replace(pre_path, "")

        if url is None:
            return JsonResponse({"status": 0, "message": "error"})
        net = NetWorker()
        try:
            iter_conten = net.get_goods_price_change(url)  # 获取价格变化情况
        except Exception:
            iter_conten = []
        response = {
            "data": list(iter_conten)
        }
        return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/goodsinfo?url=目标商品链接

    def get_goods_info(self, request):
        """
        获取商品卖家画像
        支持天猫(detail.tmall.com、detail.m.tmall.com)、淘宝(item.taobao.com、h5.m.taobao.com)、
        京东(item.jd.com、item.m.jd.com)、一号店(item.yhd.com）、苏宁易购(product.suning.com)、
        网易考拉(goods.kaola.com)、当当网(product.dangdang.com)、亚马逊中国(www.amazon.cn)、国美(item.gome.com.cn)等电商
        商品详情的历史价格查询。
        :param request:
        :return:
        """
        pre_path = request.path + "?url="
        href = request.get_full_path()
        url = href.replace(pre_path, "")  # 防止url后带有各类特殊符号导致与目标链接不匹配

        if url is None:
            return JsonResponse({"status": 0, "message": "error"})
        net = NetWorker()
        try:
            info = net.get_goods_info(url)  # 获取商品卖家画像
        except Exception:
            info = []
        response = {
            "data": info
        }
        return JsonResponse(response)

    # def webpage_to_pdf(self, request):
    #     pre_path = request.path + "?url="
    #     href = request.get_full_path()
    #     url = href.replace(pre_path, "")  # 防止url后带有各类特殊符号导致与目标链接不匹配
    #
    #     if url is None:
    #         return JsonResponse({"status": 0, "message": "error"})
    #     net = NetWorker()
    @csrf_exempt
    def upload_pdf(self, request):
        pdf_file = request.FILES.get('pdf')
        # 产生一个用户访问凭证，并且用来下载解析好的文件
        rid = int(time.time()) + random.randint(11, 1111111)
        # 解析pdf
        Thread(target=NetWorker().parse,args=(pdf_file,rid,)).start()

        return JsonResponse({"message": "success", "code": 1, "id": rid})
