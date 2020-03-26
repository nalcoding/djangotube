from kor2vec import Kor2Vec
import argparse
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pickle
from numpy import dot
from numpy.linalg import norm
import numpy as np
from pprint import pprint

from apiclient.discovery import build
from apiclient.errors import HttpError
from pytube import YouTube

from konlpy.tag import Mecab
mecab = Mecab()


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDLHO83i_gqvURvCZkzBC_7607JAu-x27M"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query, max_results):
    '''
    유튜브 API 호출하는 함수
    '''
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
    search_response = youtube.search().list(q=query,
                                            part="id,snippet",
                                            maxResults=max_results).execute()
    videos = []
    channels = []
    playlists = []

    outputs = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
            outputs.append("https://www.youtube.com/watch?v=" +
                           search_result["id"]["videoId"])
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")

    return outputs


def data_preprocess(question, multiple, answer, output_type):
    '''
    입력된 문제정보 전처리 함수

    output_type 인자 설명
    1) 문제 / 보기 --> q
    2) 문제 + 정답 / 보기 --> q_a
    3) 문제 + 보기 --> q_m
    '''

    result = []
    tmp_list = []
    multiple = multiple.strip()
    tmp_list.append(multiple[1:multiple.index(chr(9313))])
    tmp_list.append(multiple[multiple.index(
        chr(9313))+1:multiple.index(chr(9314))])
    tmp_list.append(multiple[multiple.index(
        chr(9314))+1:multiple.index(chr(9315))])
    try:
        tmp_list.append(multiple[multiple.index(
            chr(9315))+1:multiple.index(chr(9316))])
        tmp_list.append(multiple[multiple.index(chr(9316))+1:])
    except ValueError:
        tmp_list.append(multiple[multiple.index(chr(9315))+1:])

    if output_type == "q":
        result = (question, question+"".join(tmp_list))
    elif output_type == "q_a":
        if type(answer) == str:
            two_answer = answer.split(",")
            for ta in two_answer:
                question += tmp_list[int(ta)-1]
            result = (question, question+"".join(tmp_list))
        else:
            result = (question+tmp_list[answer-1], question+"".join(tmp_list))
    elif output_type == "q_m":
        for t_l in tmp_list:
            question += t_l
        result = (question, question)
    else:
        raise TypeError

    return result


def question_keyword_extract(Q):
    '''
    문제에서 특정 단어 제거하고 명사 추출 함수
    '''
    Q_nouns = mecab.nouns(Q)
    Q_result = ' '.join(Q_nouns)
    Q_result = Q_result.replace('것', '')
    Q_result = Q_result.replace('다음', '')
    Q_result = Q_result.replace('설명', '')

    return Q_result


def subtitles_extract(url_list):
    '''
    검색된 영상에서 자막 추출하는 함수
    '''
    url_video_info_output = {}

    for itr, video_url in enumerate(url_list):

        video_info_set = {}

        yt = YouTube(video_url)
        try:
            caption = yt.captions.get_by_language_code('ko')

            subtitles_str = caption.generate_srt_captions()
            subtitles_list = subtitles_str.split("\n")
        except AttributeError:
            continue

        time = []
        for i in range(1, len(subtitles_list), 4):
            time.append(subtitles_list[i])

        text = []
        for i in range(2, len(subtitles_list), 4):
            text.append(subtitles_list[i])

        sub_tuple = []
        for i, j in zip(time, text):
            sub_tuple.append((i, j))

        video_info_set['url'] = video_url
        video_info_set['title'] = yt.title
        video_info_set['author'] = yt.author
        video_info_set['views'] = yt.views
        video_info_set['length'] = yt.length
        video_info_set['description'] = yt.description
        video_info_set['subtitles'] = sub_tuple

        url_video_info_output[itr] = video_info_set

    return url_video_info_output


def subtitles_finding(final_output, video_find, question):
    '''
    수집한 자막에서 키워드 검색하여 자막 추출하는 함수
    '''
    video_num = list(final_output.keys())
    subtitle_candidate = []
    for v in video_num:
        for itr, sub in enumerate(final_output[v]['subtitles']):
            overlap = []
            for f in video_find:
                if f in sub[1]:
                    #                     print("===== 키워드 : ", f, "=====")
                    #                     print("===== 키워드 포함 자막 : ", sub, "=====")
                    url_key = final_output[v]["url"].split("=")[-1]
                    output_url = "https://youtu.be/" + url_key + "?t="
                    time_start = sub[0].split(
                        "-->")[0].split(",")[0].split(":")
                    sec = int(time_start[0])*3600 + \
                        int(time_start[1])*60 + int(time_start[2])
                    output_url += str(sec)
#                     print("===== 해당 지점 URL : ", output_url, "=====")
                    tmp_sum = ""
                    related = " ".join(
                        [tmp_sum + kk[1] for kk in final_output[v]['subtitles'][itr:itr+10]])
#                     print("===== 입력 문제 : ", question, "=====")
#                     print("===== 해당 지점 10시점 뒤 자막 내용 : ", related, "=====")
#                     print("")

                    if related not in overlap:
                        subtitle_candidate.append((output_url, related))

                    overlap.append(related)

    return subtitle_candidate


def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))


def word2vec_feature_extract(question, subtitle_candidate):
    '''
    모델에서 feature 추출해서 유사도 검사하여 최종 결과 내는 함수
    '''
    kor2vec = Kor2Vec.load("./kor2vec_model/model.kor2vec.ep9")

    q_feature = kor2vec.embedding(question, seq_len=64, numpy=True)
    prep_subtitle = []
    for i in subtitle_candidate:
        prep_subtitle.append(i[1])
    sub_input = kor2vec.to_seqs(prep_subtitle, seq_len=64)
    sub_features = kor2vec.forward(sub_input).detach().numpy()

    cosine_sim_list = []
    for itr, sub in enumerate(sub_features):
        tmp_cos = cos_sim(np.hstack(q_feature), np.hstack(sub))
        cosine_sim_list.append((subtitle_candidate[itr], tmp_cos))

    return cosine_sim_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", help="input question")
    parser.add_argument("--multiple", help="input multiple_choice")
    parser.add_argument("--answer", help="input answer")
    parser.add_argument("--subject", help="input subject 정보처리기사 or 한국사")
    parser.add_argument("--max_results", help="Max results", default=10)

    args = parser.parse_args()

    result = data_preprocess(args.question, args.multiple,
                             args.answer, output_type='q_a')
    print(result)

    question_input = question_keyword_extract(result[0])

    video_find = list(set(question_keyword_extract(
        result[1]).replace("  ", "").strip().split(" ")))

    query = args.subject + " 인강 " + question_input

    print("="*80)
    print(query)
    print("="*80)

    try:
        outputs = youtube_search(query, args.max_results)
    except HttpError:
        print("An HTTP error %d occurred:\n%s")

    print(outputs)

    final_output = subtitles_extract(outputs)

    subtitle_candidate = subtitles_finding(final_output, video_find, result)

    final_result = word2vec_feature_extract(result[1], subtitle_candidate)
    pprint(sorted(final_result, key=lambda sim: sim[1]))
    print("===== 문제 + 정답 + 보기: ", result[1], "=====")

