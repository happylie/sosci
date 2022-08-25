# Search of SSL Certification Information(SoSCI)
## Search of SSL Certification Information
### SSL 인증서 정보 검색
- https://happylie.tistory.com/156

### 설치 방법
1. Git Clone
```
$ https://github.com/happylie/sosci.git
```

### 실행 방법
1. Help
```
$ python sosci.py -h                             
usage: sosci.py [-h] [-u URL] [-e] [-v]

Search of SSL Certification Information(SoSCI)

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  Check URL(HTTPS URL or Hostname)
  -e, --expire       Certification Expire Date
  -v, --version      show program's version number and exit

```

2. Search of SSL Certification Information
```
$ python sosci.py -u https://happylie.tistory.com
{
"subject":{
	"countryName":"KR",
	"stateOrProvinceName":"Jeju-do",
	"localityName":"Jeju-si",
	"organizationName":"Kakao Corp.",
	"commonName":"*.tistory.com"
},
"issuer":{
	"countryName":"US",
	"organizationName":"DigiCert Inc",
	"organizationalUnitName":"www.digicert.com",
	"commonName":"Thawte TLS RSA CA G1"
},
"notBefore":"2022-03-14 00:00:00",
"notAfter":"2023-03-31 23:59:59",
"expireDate":"219 Days",
"subjectAltName":{
	"DNS":[
		"*.tistory.com",
		"tistory.com"
		]
	}
}
```
- 2.1 항목 정보 설명
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

3. Certification Expire Date
```
$ python sosci.py -u https://happylie.tistory.com -e
219 Days
```