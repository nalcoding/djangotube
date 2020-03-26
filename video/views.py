from django.shortcuts import render
# from django.core.urlresolvers import reverse
from .models import Video
import requests
from django.conf import settings


def video_list(request):
    # video_list = Video.objects.all()
    return render(request, "video/video_list.html", context={})


def video_detail(request, video_key, start):
    # video = Video.objects.get(id=video_id)
    video = {"video_key": video_key, "start": start}
    print("video => ", video)

    return render(request, "video/video_detail.html", context={"video": video})


def video_search(request):
    print(request.GET)
    question = request.GET.get("question")
    multiple = request.GET.get("multiple")
    answer = request.GET.get("answer")
    subject = request.GET.get("subject")

    form = {
        "question": question,
        "multiple": multiple,
        "answer": answer,
        "subject": subject,
    }

    video_list = get_predict()

    return render(request, "video/video_list.html", context={"video_list": video_list, **form})


def video_search_org(request):
    print(request.GET)

    query_text = request.GET.get("query_text")

    # 문제에서 워드 뽑는 기능 추가 부분

    # 뽑은 키워드로 유튜브 동영상 목록 조회 부분
    # video_list = Video.objects.all()
    # for video in video_list:
    #     print(f'({video.id} | {video.title} | {video.video_key} | {video.start})')

    youtube_items = youtube(query_text)
    items = youtube_items.get('youtube_items')

    video_list = []
    # video_list = [{"video_key": 10, "title": "제목1"},
    #               {"video_key": 20, "title": "제목2"}]

    for item in items:
        # id = item.get('id')
        # snippet = item.get('snippet')
        video_id = (item.get('id')).get('videoId')
        video_title = (item.get('snippet')).get('title')

        video = {}
        video["start"] = "100"
        video["video_key"] = video_id
        video["title"] = video_title

        print(video)
        video_list.append(video)

    return render(request, "video/video_list.html", context={"video_list": video_list, "query_text": query_text})


def youtube(keyword):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': getattr(settings, 'YOUTUBE_API_KEY'),
        'part': 'snippet',
        'type': 'video',
        'maxResults': '5',
        'q': keyword,
    }

    response = requests.get(url, params)
    response_dict = response.json()

    context = {
        'youtube_items': response_dict['items']
    }

    return context


def get_predict():
    final_result = [{
        "video_key": "ow9M_JG55AY",
        "title": "고조선의 8조법금(고조선 금법 8조)을 통한 역사적 모습 유추",
        "points": [
            {"start": 139, "predict": 30},
            {"start": 300, "predict": 22}
        ]
    }, {
        "video_key": "gCDTOQGsR1A",
        "title": "교과서에 나오지 않는 고조선 8조법 전문 공개",
        "points": [
            {"start": 150, "predict": 43},
            {"start": 170, "predict": 32}
        ]
    }
    ]
    return final_result


'''
    youtube_items = {
        'youtube_items': [
            {
                'kind': 'youtube#searchResult',
                'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/18ABO0hDhpD9TACmpx_wPYSbmWM"',
                'id': {'kind': 'youtube#video', 'videoId': 'Ro19_gTRsNA'},
                'snippet': {'publishedAt': '2020-03-24T15:08:47.000Z',
                            'channelId': 'UCA_Co0sST8P2-Y0HxLX40-g',
                            'title': '[민아 Vlog] 민아가 하와이 음식들을 점령했다!!',
                            'description': '안녕하세요 알로하 :) 작년에 갔었던 하와이편 두번째 편 입니다 이번 편은 제가 하와이에서 먹었던 음식들을 알려드리려고 해요 야심한 밤에...',
                            'thumbnails': {
                                'default': {
                                    'url': 'https://i.ytimg.com/vi/Ro19_gTRsNA/default.jpg',
                                    'width': 120, 'height': 90},
                                'medium': {
                                    'url': 'https://i.ytimg.com/vi/Ro19_gTRsNA/mqdefault.jpg',
                                    'width': 320, 'height': 180},
                                'high': {
                                    'url': 'https://i.ytimg.com/vi/Ro19_gTRsNA/hqdefault.jpg',
                                    'width': 480, 'height': 360}
                            },
                            'channelTitle': 'Minah 민아',
                            'liveBroadcastContent': 'none'
                            }
            },
            {
                'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/7E9BZuC4gSr8qrpWLnRPhKrNIa4"', 'id': {'kind': 'youtube#video', 'videoId': 'VRm81UvRAm4'}, 'snippet': {'publishedAt': '2020-03-17T05:30:10.000Z', 'channelId': 'UCA_Co0sST8P2-Y0HxLX40-g', 'title': '[민아 VLOG] 2019 민아 하와이여행편 MINAH&#39;S VACATION in HAWAii =)', 'description': '오랜만에 영상 올리네요 헤헤 작년에 하와이여행 다녀온거 편집해봤어요 제 첫 작품이랄까요.. 헷 부끄럽지만 잘 봐주세요 사실 하와이갈땐 브이로...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/VRm81UvRAm4/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/VRm81UvRAm4/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/VRm81UvRAm4/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Minah 민아', 'liveBroadcastContent': 'none'}}, {'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/2boINUgYrsoleauA9QslYA9QHXA"', 'id': {'kind': 'youtube#video', 'videoId': 'BWROdI-AgAU'}, 'snippet': {'publishedAt': '2020-01-17T09:00:08.000Z', 'channelId': 'UCwx6n_4OcLgzAGdty0RWCoA', 'title': '[제철알바 특집] 왜 이제왔어...? 제작진 당황시킨 역대급 심의빌런🔥의 무박 2일 찜질방 알바 리뷰ㅣ워크맨 ep.36', 'description': 'JOB것들아~~~♥ 인력소장이다,,,,~~~ 1월인데 다덜,,,찜질방 목욕탕 갔다왔는가~~~~?? 다덜 새해에~~ 떼밀고,,~~~ 쇄신허자~~~~!!! 세상의 모든 job것들을...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/BWROdI-AgAU/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/BWROdI-AgAU/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/BWROdI-AgAU/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': '워크맨-Workman', 'liveBroadcastContent': 'none'}}, {'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/B7NKxbbVuE-jz-ewsRPoAJ8N_NM"', 'id': {'kind': 'youtube#video', 'videoId': 'Nl8PO1lp4kk'}, 'snippet': {'publishedAt': '2017-04-06T13:39:42.000Z', 'channelId': 'UCepUWUpH45hRTi-QePdq1Bg', 'title': 'I Can See Your Voice 4 최초! 걸스데이 민아&amp;친언니 합동무대! ′Something′ 170406 EP.6', 'description': '방송 최초! 걸스데이 민아&워너비 린아의 합동 무대! 예쁜 외모도! 뛰어난 노래 실력도! 똑 닮은 자매♥ Something - 걸스데이(Girl′s Day) 매주 목요일...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/Nl8PO1lp4kk/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/Nl8PO1lp4kk/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/Nl8PO1lp4kk/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Mnet Official', 'liveBroadcastContent': 'none'}}, {'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/w_-PBtQEvHICIPf1QD-M7G2PpAA"', 'id': {'kind': 'youtube#video', 'videoId': 'dAkLIiT8N0I'}, 'snippet': {'publishedAt': '2017-03-25T13:50:12.000Z', 'channelId': 'UCFL1sCAksD6_7JIZwwHcwjQ', 'title': '[파닥파닥] 지금의 민아(Min Ah)를 있게 한 열혈 댄스 &quot;강호동(Kang Ho Dong) 죽일 거야!!&quot; 아는 형님(Knowing bros) 68회', 'description': '(궁금) 신인시절 열정으로 췄던 민아의 파닥 댄스! 보여달라는 호동에 과격한 리액션 하는 민아(ㅋㅋ) 파닥 춤을 추고 호동에게 "죽일 거야, 너...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/dAkLIiT8N0I/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/dAkLIiT8N0I/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/dAkLIiT8N0I/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'JTBC Entertainment', 'liveBroadcastContent': 'none'}}, {
                'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/VsKjTr97ioW-Gs92JY2XyQ-3epM"', 'id': {'kind': 'youtube#video', 'videoId': 'qmcn7AtwUU8'}, 'snippet': {'publishedAt': '2014-07-17T15:59:12.000Z', 'channelId': 'UCiBr0bK06imaMbLc8sAEz0A', 'title': '[HOT] 별바라기 - 여신 걸그룹 걸스데이! 데뷔초엔 뱃살돌!? 쿠션 던지는 민아! 20140717', 'description': '20140717 별바라기 여신 걸그룹 걸스데이! 데뷔초엔 뱃살돌!? 쿠션 던지는 민아!', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/qmcn7AtwUU8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/qmcn7AtwUU8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/qmcn7AtwUU8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'MBCentertainment', 'liveBroadcastContent': 'none'}}, {'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/a-0iDBLeUYFXsoh5lWTnOCErZGE"', 'id': {'kind': 'youtube#video', 'videoId': 'RWJxWvtQBoQ'}, 'snippet': {'publishedAt': '2015-03-21T02:46:18.000Z', 'channelId': 'UC2JHHauJLCWbcaeeY-x_xoQ', 'title': '민아 - 나도 여자에요 Minah - I am a woman too 266회 걸스데이 Girl&#39;s Day', 'description': "150320 민아 유희열 3 Minah 나도여자에요 I am a woman too 60 fps E266 걸스데이 Girl's Day 150321 (150317 녹화) E266 1 ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/RWJxWvtQBoQ/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/RWJxWvtQBoQ/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/RWJxWvtQBoQ/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'gsdsomething03', 'liveBroadcastContent': 'none'}}, {'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/KrairM30UkzaIS74jBGFx3c0wxg"', 'id': {'kind': 'youtube#video', 'videoId': 'riYKx2HwjS8'}, 'snippet': {'publishedAt': '2019-12-11T08:00:04.000Z', 'channelId': 'UCmxDK1eWo-KvQQJ23p95XGw', 'title': '⚡김민아 성지순례⚡기상캐스터 김민아, &#39;기분 좋은.. 경험&#39;에 쓰러지다!? 깝민아의 방광드립부터 아이유 따라잡기 ASMR 도전까지! | 주가 빛나는 밤에 ep.8', 'description': '안녕하세요 게스트 잘 뽑는 프로 주빛밤입니다~ JTBC의 딸, 제2의 장성규, 김민아 oh☆재등판☆oh 방광용량 드립은 진짜 미친거 아닌갘ㅋㅋㅋㅋㅋ왜...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/riYKx2HwjS8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/riYKx2HwjS8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/riYKx2HwjS8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': '스튜디오 룰루랄라- studio lululala', 'liveBroadcastContent': 'none'}}, {'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/-GjTiOGDrTjQQ1Si1rDM1qGaT3k"', 'id': {'kind': 'youtube#video', 'videoId': 'f8IZnOhKZ0E'}, 'snippet': {'publishedAt': '2015-03-24T14:38:54.000Z', 'channelId': 'UCFL1sCAksD6_7JIZwwHcwjQ', 'title': '걸스데이 민아, 설렘 폭발♥ &#39;비밀번호 486 ♪&#39; 끝까지간다 21회', 'description': "걸스데이 민아가 부르는 윤하의 '비밀번호 486 ♪' 모든 boy들은 설렘 설렘~", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/f8IZnOhKZ0E/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/f8IZnOhKZ0E/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/f8IZnOhKZ0E/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'JTBC Entertainment', 'liveBroadcastContent': 'none'}}, {'kind': 'youtube#searchResult', 'etag': '"ksCrgYQhtFrXgbHAhi9Fo5t0C2I/NLIbth4SLz-CzXfK7tFyYmsmJlE"', 'id': {'kind': 'youtube#video', 'videoId': 'yP0bddFLSnA'}, 'snippet': {'publishedAt': '2020-03-18T15:12:17.000Z', 'channelId': 'UCiBr0bK06imaMbLc8sAEz0A', 'title': '[라디오스타] 양동근에게 직접 춤을 배우는 구라&amp;민아 ＂나보다 더 못하네!♨＂ 20200319', 'description': "More 'Radio Star' clips are available iMBC http://www.imbc.com/broad/tv/ent/goldfish/vod/ WAVVE ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/yP0bddFLSnA/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/yP0bddFLSnA/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/yP0bddFLSnA/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'MBCentertainment', 'liveBroadcastContent': 'none'}}]}

    # print(context)
'''
