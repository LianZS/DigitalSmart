import json
from django.http import StreamingHttpResponse, JsonResponse

from .tasks import NetWorker


class Crack:
    # http://127.0.0.1:8000/interface/api/downWYYMusic?name=听不见晚安
    def down_music(self, request):
        """
            下载音乐
        :param request:
        :return:
        """
        musicname = request.GET.get("name")  # 音乐名
        soft_type = request.GET.get("type")  # 软件类型，
        # netease：网易云，qq：qq音乐，kugou：酷狗音乐，kuwo：酷我，
        # xiami：虾米，baidu：百度，1ting：一听，migu：咪咕，lizhi：荔枝，
        # qingting：蜻蜓，ximalaya：喜马拉雅，kg：全民K歌，5singyc：5sing原创，
        # 5singfc：5sing翻唱
        if not musicname:
            return JsonResponse({"status": 0, "message": "error"})
        net = NetWorker()
        iter_down_info = net.get_music_list(musicname)  # 获取所有与之相关的音乐
        first = iter_down_info.__next__()  # 获取第一首
        dowun_url = first['url']
        strem = net.down_music_content(url=dowun_url)
        reponse = StreamingHttpResponse(strem)
        reponse['Content-Type'] = 'application/octet-stream'
        reponse['Content-Disposition'] = 'attachment;filename="example.mp3"'

        return reponse

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
    def down_baidu_doc(self,request):

