
## API

### Url : doorbell/visit

#### POST: 방문 기록 남기기

#### request data
1. type(required) : 선택 타입
2. visit_reason(required) : 음성 데이터를 텍스트로 변환해서 넣어 보내주세요.

#### validation
- 원하는 타입이 없을 경우 -> 'Type is not exist' 출력
- 위의 data 중 하나라도 없을 경우 -> 'No required data.' 출력


### Url : doorbell/category

#### GET: 타입 리스트 불러오기

#### POST: 타입 생성하기

#### request data
1. type(required) : 생성할 타입

#### validation
- 필수 Data가 없을 경우 -> 'No required data.' 출력
- 문자열을 제외한 타입의 데이터를 넣을 경우 -> 'Unsupported data type.' 출력

