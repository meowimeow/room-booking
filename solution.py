# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9
CLOSE_HOUR = 21
MAX_HOURS = 3
MAX_PER_DAY = 2


def _is_int(x):
    # bool은 int의 하위 타입이므로 따로 제외한다
    return isinstance(x, int) and not isinstance(x, bool)


class RoomBooking:
    def __init__(self):
        # {(room, day): [(start, end, name), ...]}
        self._bookings = {}

    def _valid_slot(self, room, day):
        return (isinstance(room, str) and isinstance(day, str)
                and room in ROOMS and day in DAYS)

    def book(self, room, day, start, end, name):
        if not self._valid_slot(room, day):
            return False
        if not (_is_int(start) and _is_int(end)):
            return False
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return False
        if start >= end:
            return False
        if end - start > MAX_HOURS:
            return False

        slot = self._bookings.get((room, day), [])
        for s, e, _ in slot:
            if start < e and s < end:  # 겹침 (끝=시작은 허용)
                return False

        # 같은 사람은 같은 요일에 강의실 합산 최대 2건
        count = 0
        for r in ROOMS:
            for _, _, n in self._bookings.get((r, day), []):
                if n == name:
                    count += 1
        if count >= MAX_PER_DAY:
            return False

        self._bookings.setdefault((room, day), []).append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not self._valid_slot(room, day) or not _is_int(start):
            return False
        slot = self._bookings.get((room, day), [])
        for i, (s, e, n) in enumerate(slot):
            if s == start:
                if n != name:
                    return False
                del slot[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not self._valid_slot(room, day):
            return []
        return sorted(self._bookings.get((room, day), []), key=lambda b: b[0])
