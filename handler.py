from botocore.vendored import requests
import json
import random
from datetime import date


def lambda_handler(event, context):
    # 깃헙 graphql
    git_url = "https://api.github.com/graphql"
    headers = {"Content-Type": "application/json", "Accept": "application/vnd.github.inertia-preview+json",
               "Authorization": "Bearer :Github 토큰: "}

    # 오늘날짜
    t_day = date.today()
    years = str(t_day.year)
    months = str(t_day.month)

    if len(months) == 1:
        months = "0" + months
    days = str(t_day.day)
    if len(days) == 1:
        days = "0" + days

    # Graphql query 엑세스 값
    data = {
        "query": "query{user(login: \":Github 사용자명:\") { repositories(last: 100) { totalCount nodes { name defaultBranchRef { target { ...on Commit {history(since: \"" + years + "-" + months + "-" + days + "T09:00:00+00:00\") { totalCount}}}}}}}}"
    }

    git_req = requests.post(git_url, data=json.dumps(data), headers=headers)
    git_data = git_req.json()

    # 커밋 수 확인
    count = 0
    for each in git_data["data"]["user"]["repositories"]["nodes"]:
            if each['defaultBranchRef'] is not None:
                count = count + each['defaultBranchRef']['target']['history']['totalCount']


    # 안했다면.... 랜덤 초이스
    commitList = [
        "커밋은 하고 가야지?",
        "커밋 안하냐?",
        "커밋 좀 하지 그래?",
        "커밋 요정이 부릅니다. 커밋 하나무라",
        "커밋 좀 하고 자야지?",
        "이봐 커밋은?",
        "크아ㅏㅏㅏㅏㅏㅏㅏ 커밋해라ㅏㅏㅏㅏ"
    ]

    if count > 0:
        data = {"text": f"오늘도 커밋을 {count}개나 했구나! 닝갠아 훗"}
    else:
        data = {"text": random.choice(commitList)}

    # 슬랙 전송
    slack_url = ":Slack Incoming Web-Hook URL:"
    headers = {"Content-Type": "application/json"}

    slack_req = requests.post(slack_url, data=json.dumps(data), headers=headers)
    slack_data = slack_req.json()

    return slack_data
