
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


### Url : doorbell/token

### POST: 토큰 추가하기

#### request data
1. token(required) : 메시지를 보낼 기기의 FCM TOKEN

#### remark
한번에 하나만 등록할 수 있게해서 새로운 token을 등록하면 기존 token은 전부 삭제 처리


### Url : doorbell/visit/latest/

### GET: 가장 최근의 미확인 방문요청 보기


### Url : doorbell/address/

### GET: 내 IP Address 가져가기 

