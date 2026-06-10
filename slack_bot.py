import datetime
import holidays
import requests
import os

kr_holidays = holidays.KR(years=datetime.date.today().year)

def is_business_day(date):
    if date.weekday() >= 5 or date in kr_holidays:
        return False
    return True

def should_send_today():
    today = datetime.date.today()
    target_day = datetime.date(today.year, today.month, 5)

    if is_business_day(target_day):
        return today == target_day

    check_date = target_day - datetime.timedelta(days=1)
    while not is_business_day(check_date):
        check_date -= datetime.timedelta(days=1)

    return today == check_date

def send_slack_dm():
    # 보안을 위해 슬랙 주소는 GitHub Secrets에서 가져옵니다.
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("에러: SLACK_WEBHOOK_URL 설정이 없습니다.")
        return

    payload = {
        "text": "📅 **영업일 기준 5일 오전 10시 알림**\당장 AI 지출결의서 내라!!!!!!!."
    }
    
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("슬랙 DM 전송 완료")
    else:
        print(f"전송 실패: {response.status_code}")

if __name__ == "__main__":
    if should_send_today():
        print("조건 일치: 슬랙 DM을 발송합니다.")
        send_slack_dm()
    else:
        print("조건 불일치: 오늘은 알림 발송일이 아닙니다.")
        send_slack_dm()
