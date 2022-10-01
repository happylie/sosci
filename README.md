# Search of SSL Certification Information(SoSCI)
<div>
<img src="https://img.shields.io/badge/Python->=3.x-blue?logo=python&logoColor=white" />
</div>

## SSL 인증서 정보 검색(Search of SSL Certification Information)
- https://happylie.tistory.com/156

### 설치 방법
1. Git Clone
```bash
$ https://github.com/happylie/sosci.git
```

### 실행 방법
#### 1. Help
```bash
$ python sosci.py -h                             
usage: sosci.py [-h] [-e] [-v] url

Search of SSL Certification Information(SoSCI)

positional arguments:
  url            Check URL(HTTPS URL or Hostname)

optional arguments:
  -h, --help     show this help message and exit
  -e, --expire   Certification Expire Date (default: False)
  -v, --version  show program's version number and exit
```

#### 2. Search of SSL Certification Information
```bash
$ python sosci.py https://happylie.tistory.com          
{
    "result": {
        "expireDate": "181 Days",
        "issuer": {
            "commonName": "Thawte TLS RSA CA G1",
            "countryName": "US",
            "organizationName": "DigiCert Inc",
            "organizationalUnitName": "www.digicert.com"
        },
        "notAfter": "2023-03-31 23:59:59",
        "notBefore": "2022-03-14 00:00:00",
        "subject": {
            "commonName": "*.tistory.com",
            "countryName": "KR",
            "localityName": "Jeju-si",
            "organizationName": "Kakao Corp.",
            "stateOrProvinceName": "Jeju-do"
        },
        "subjectAltName": {
            "DNS": [
                "*.tistory.com",
                "tistory.com"
            ]
        }
    },
    "status": {
        "code": 0,
        "msg": "SSL Certification Information"
    }
}
```
##### 2.1 항목 정보 설명
```text
+ status : 상태 정보
  - code : Code 정보  
      - 0 : (정상)
      - 1 : (에러)
  - mgs : Status 메세지 내용
 + result : 결과 정보
  - subject : 제목 이름
    - countryName : 국가 또는 지역
    - stateOrProvinceName : 주/도
    - localityName : 소재지
    - organizationName : 조직
    - commonName : 일반 이름
  - issuer : 발급자 이름
    - countryName : 국가 또는 지역 
    - organizationName : 조직
    - organizationalUnitName : 조직 단위 
    - commonName : 일반 이름
  - notBefore : 인증서 유효 시작일
  - notAfter : 인증서 유효 만료일
  - expireDate : 현재부터 인증서 만료일 
  - subjectAltName : 주체 대체 이름
    - DNS : DNS 정보
```

#### 3. Certification Expire Date
```bash
$ python sosci.py https://happylie.tistory.com -e
{
    "result": {
        "expireDate": "181 Days"
    },
    "status": {
        "code": 0,
        "msg": "SSL Expire Date"
    }
}
```