# 강의실 예약 웹 — 예약 규칙은 전부 solution.py의 RoomBooking이 처리한다.
# 이 파일은 입력을 받아 RoomBooking에 넘기고 결과를 보여 주기만 한다.
from flask import Flask, render_template, request

from solution import RoomBooking, ROOMS, DAYS

app = Flask(__name__)
rb = RoomBooking()  # 서버가 켜져 있는 동안 예약을 기억한다


def to_number(text):
    """문자열을 숫자로만 바꾼다. 규칙 판단은 하지 않고 solution.py에 맡긴다."""
    text = (text or "").strip()
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text  # 숫자가 아니면 그대로 넘겨서 solution.py가 거절하게 한다


def page(result=None, view_room=ROOMS[0], view_day=DAYS[0]):
    return render_template(
        "index.html",
        rooms=ROOMS, days=DAYS, result=result,
        view_room=view_room, view_day=view_day,
        schedule=rb.get_schedule(view_room, view_day),
    )


@app.get("/")
def index():
    room = request.args.get("room", ROOMS[0])
    day = request.args.get("day", DAYS[0])
    return page(view_room=room, view_day=day)


@app.post("/book")
def book():
    f = request.form
    room, day, name = f.get("room"), f.get("day"), f.get("name", "").strip()
    start, end = to_number(f.get("start")), to_number(f.get("end"))
    ok = rb.book(room, day, start, end, name)
    desc = f"{name} · {room} · {day} · {f.get('start')}~{f.get('end')}시 예약"
    return page({"kind": "예약", "ok": ok, "desc": desc}, room, day)


@app.post("/cancel")
def cancel():
    f = request.form
    room, day, name = f.get("room"), f.get("day"), f.get("name", "").strip()
    start = to_number(f.get("start"))
    ok = rb.cancel(room, day, start, name)
    desc = f"{name} · {room} · {day} · {f.get('start')}시 예약 취소"
    return page({"kind": "취소", "ok": ok, "desc": desc}, room, day)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
