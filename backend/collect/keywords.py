"""
2026 SNS 유행 음식 키워드 정의
- 한 번의 API 호출은 최대 5개 그룹까지 → 7개를 두 묶음으로 분리
- 각 그룹은 메인 키워드 + 변형 검색어로 구성하여 데이터 풍부도 확보
"""

KEYWORD_GROUPS_BATCH_1 = [
    {"groupName": "우베",          "keywords": ["우베", "우베 디저트", "ube"]},
    {"groupName": "샌드베이글",    "keywords": ["샌드베이글", "샌드 베이글", "베이글 샌드위치"]},
    {"groupName": "창억떡",        "keywords": ["창억떡", "창억"]},
    {"groupName": "버터떡",        "keywords": ["버터떡", "버터 떡"]},
    {"groupName": "두바이쫀득쿠키", "keywords": ["두바이쫀득쿠키", "두바이 쿠키", "두바이 초콜릿"]},
]

KEYWORD_GROUPS_BATCH_2 = [
    {"groupName": "저당",          "keywords": ["저당", "저당 디저트", "제로슈가"]},
    {"groupName": "봄동비빔밥",    "keywords": ["봄동비빔밥", "봄동", "봄동무침"]},
]

ALL_BATCHES = [KEYWORD_GROUPS_BATCH_1, KEYWORD_GROUPS_BATCH_2]

AGE_GROUPS = [
    ("10대", ["1", "2"]),
    ("20대", ["3", "4"]),
    ("30대", ["5", "6"]),
    ("40대", ["7", "8"]),
    ("50대 이상", ["9", "10", "11"]),
]

GENDERS = [("남성", "m"), ("여성", "f")]
DEVICES = [("모바일", "mo"), ("PC", "pc")]
