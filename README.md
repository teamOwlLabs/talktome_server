
## API

### Create Visit : 방문 기록 남기기
#### url
> doorbell/visit
#### method
POST
#### request data
1. type(required) : 선택 타입
2. visit_reason(required) : 음성 데이터를 텍스트로 변환해서 넣어 보내주세요.
#### validation
- 원하는 타입이 없을 경우 -> 'Type is not exist' 출력
- 위의 data 중 하나라도 없을 경우 -> 'No required data.' 출력

