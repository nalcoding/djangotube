from django.shortcuts import render
# from django.core.urlresolvers import reverse
from .models import Video


def video_list(request):
    # video_list = Video.objects.all()
    return render(request, "video/video_list.html", context={})


def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, "video/video_detail.html", context={"video": video})


def video_search(request):
    print(request.GET)

    query_text = request.GET.get("query_text")
    # 문제에서 워드 뽑는 기능 추가 부분

    # 뽑은 키워드로 유튜브 동영상 목록 조회 부분

    video_list = Video.objects.all()

    print(type(video_list))

    for video in video_list:
        print(f'({video.id} | {video.title} | {video.video_key} | {video.start})')

    return render(request, "video/video_list.html", context={"video_list": video_list, "query_text": query_text})
