## Commit-fairy Slack-bot (커밋요정)
![커밋요정](https://github.com/CodeMath/slack_commit_fairy/blob/master/screenshot/screenshot.png?raw=true)

본인 깃헙(Github) 계정의 repository들을 조회하며 그날 하루 커밋을 했는지 체크해주는 커밋요정입니다.

AWS Lambda에 최적화 되어있고, Python3.6을 사용했습니다.

## Requirement

### 특별히 설치할 것은 없습니다.(NO pip install -r requirements.txt)

> `requests` 조차 설치하는게 귀찮아서(?), `botocore` 에서 가져옵니다.


### 깃헙 OAuth2 토큰

깃헙 settings 메뉴에 들어가서, Developer settings > Personal access tokens를 발행합니다.

선택할 스코프는,
```
 [V] repo : 레포 읽기용

 [V] read:user : 프로필 조회용
```
정도 하면 됩니다. 

### 슬랙 incoming hook

> 이 부분은 설명이 잘된 블로그 글 참고하시면...(?)


## Github GraphQL API V4

이 부분이 조금 난해합니다. 기존 MySQL을 사용하셨던 분이라면 그나마 다행이지만, 모르시는 분들은 복붙 하시면 됩니다. GraphQL의 자세한 내용은 [이곳](https://www.slideshare.net/deview/112rest-graph-ql-relay), [저곳](https://velopert.com/2318),[공식](http://graphql.org)의 내용을 참고하세요.


실제 GraphQL을 테스트하시려면, [GraphQL Explorer](https://developer.github.com/v4/explorer/) 에서 하시면 됩니다.
 
아래 코드는 GraphQL 에서 사용되는 코드입니다.

```
query{
  user(login: ":사용자이름:") {
    repositories(last: 100) {
      totalCount
      nodes {
        name
        defaultBranchRef {
          target {
            ...on Commit {
              history(since: "2018-04-03T00:00:00+00:00") {
                totalCount
              }
            }
          }
        }
      }
    }
  }
}
```

테스트해보시면 어떤식으로 데이터가 떨어지는지 쉽게 확인할 수 있습니다.


## AWS Lambda 트리거
AWS의 Lambda에 클라우드와치 이벤트로 cron-job을 할 수 있습니다.

트리거 부분에서 cron스케쥴을 등록하시고 저장을 하시면 됩니다.

자세한 내용은 [공식문서](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html)를 참조하세요.


## Contribute & License
Anyone can become a contributor!


최대한 챱챱챱 빠르게 만드는게 좋아해서... 포크해서 아무나 가져다쓰세요~(별도 한번씩 눌러주시고....)

MIT License © [codemath](https://github.com/CodeMath)
