import math
import datetime
from datetime import timedelta
import ephem
import calendar
from itertools import cycle

UTCNOW = datetime.datetime.utcnow

ZODIAC =('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
ZU = [chr(uu) for uu in range(0x2648, 0x2654)]
NUM = ("nought", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
SUIT = {
   "s": "swords",
   "w": "wands",
   "d": "disks",
   "c": "cups"
}
MAJOR = {
    0: "The Fool",
    1: "The Magician",
    2: "The High Priestess",
    3: "The Empress",
    4: "The Emperor",
    5: "The Hierophant",
    6: "The Lovers",
    7: "The Chariot",
    8: "Strength",
    9: "The Hermit",
    10: "Wheel of Fortune",
    11: "Justice",
    12: "The Hanged Man",
    13: "Death",
    14: "Temperance",
    15: "The Devil",
    16: "The Tower",
    17: "The Star",
    18: "The Moon",
    19: "The Sun",
    20: "Judgement",
    21: "The World",
}

ZODIAC_ATU = {
    0: 4,
    1: 5,
    2: 6,
    3: 7,
    4: 8,
    5: 9,
    6: 11,
    7: 13,
    8: 14,
    9: 15,
    10: 17,
    11: 18,
}

PLANET = {
    3: {
        "name": "Saturn",
        "glyph": u"\u2644",
        "atu": 21,
    },
    4: {
        "name": "Jupiter",
        "glyph": u"\u2643",
        "atu": 10,
    },
    5: {
        "name": "Mars",
        "glyph": u"\u2642",
        "atu": 16,
    },
    6: {
        "name": "Sun",
        "glyph": u"\u2609",
        "atu": 19,
    },
    7: {
        "name": "Venus",
        "glyph": u"\u2640",
        "atu": 3,
    },
    8: {
        "name": "Mercury",
        "glyph": u"\u263F",
        "atu": 1,
    },
    9: {
        "name": "Moon",
        "glyph": u"\u263D",
        "atu": 2,
    },
}


def fmt_data(dat=None):
    dat = [int_to_roman(_) for _ in get_thelema_date(dat)]
    maj, minor = dat[0], dat[1].lower()
    sol, lun = [zodiac_body(_) for _ in (6, 9)]
    decan = sol["decan"].upper()
    card = sol["small"]
    suit = SUIT[card["suit"]].title()
    suit_num = NUM[int(card["n"])].title()
    card_txt = f"{suit_num} of {suit}"
    prose = f"Sol in {sol['body_zodiac']}, Lunar in {lun['body_zodiac']}"
    res = {
        "date": f"{maj}:{minor} {sol['body_symbol']} {sol['zodiac_symbol']}  {lun['body_symbol']} {lun['zodiac_symbol']}",
        "title_decan": sol['small']['m'],
        "img_decan": f"img/cards/{decan}.png",
        "prose": prose,
        "card_decan": f"{card_txt} - {sol['small']['m']}"
    }
    return res


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


def get_planet_info(pos_time=UTCNOW()):
    planet = PLANET.copy()
    for key in range(3, 10):
        planet[key]["body"] = getattr(ephem, PLANET[key]["name"])(pos_time, epoch="1904")
        planet[key]["atu"] = PLANET[key]["atu"]
    return planet


def int_to_roman(number):
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = ""
    for i in range(len(ints)):
        count = int(number / ints[i])
        result += nums[i] * count
        number -= ints[i] * count
    return result


def get_sign(rad):
    return ZODIAC[int(math.degrees(rad) / 30)]


def get_deg(rad):
    """
    Return progress of sign in constellation, degrees + minutes
    """
    sgn = int(math.degrees(rad) / 30)
    deg = (math.degrees(rad) / 30 - sgn) * 30
    i_deg = int(deg)
    return sgn, deg, i_deg, (deg - i_deg) * 60


def days_till_vernal(dat=None):
    """
    Number of days until vernal equinox
    NB. if the date is after VE, then result is negative
    """
    if dat is None:
        dat = datetime.datetime.now()
    nve = ephem.next_vernal_equinox(str(dat.year))
    return nve - ephem.date(dat)  # Float number of days +ve if before VE, -ve if after VE


def get_thelema_date(dat=None):
    """
    Get major minor arcana, default to today
    """
    if dat is None:
        dat = datetime.datetime.now()

    base = ephem.next_vernal_equinox("1904").datetime()
    year = (dat.year - base.year) if days_till_vernal(dat=dat) < 0 else (dat.year - base.year - 1)
    (maj, minor) = divmod(year, 22)
    return (maj, minor)


def _small_cards():
    MEANINGS = {
        "w": ["Dominion", "Virtue", "Completion", "Strife", "Victory", "Valour", "Swiftness", "Strength", "Oppression"],
        "d": ["Change", "Works", "Power", "Worry", "Success", "Failure", "Prudence", "Gain", "Wealth"],
        "s": ["Peace", "Sorrow", "Truce", "Defeat", "Science", "Futility", "Interference", "Cruelty", "Ruin"],
        "c": ["Love", "Abundance", "Luxury", "Disappointment", "Pleasure", "Debauch", "Indolence", "Happiness", "Satiety"],
    }
    suit_iter = cycle("wwwdddsssccc")
    num_iter = cycle(range(2, 11))
    planet_iter = cycle([5, 6, 7, 8, 9, 3, 4])
    for day in range(36):
        suit, num, planet = next(suit_iter),  next(num_iter), next(planet_iter)
        meaning = MEANINGS[suit][num - 2]
        yield {"suit": suit, "n": "%02d" % num, "m": meaning, "p":planet}

CARDS = list(_small_cards())


def _ruler_cards():
    meaning = {12: "Prince", 13: "Queen", 14: "Knight"}
    suit_iter = cycle("wwdddssscccw")
    num_iter = cycle([13, 13, 12, 12, 12, 14, 14, 14, 13])
    for day in range(36):
        card_num = next(num_iter)
        yield {"card": "%s%s" % (next(suit_iter), card_num), "m": meaning[card_num]}
RULER = list(_ruler_cards())


def get_card(long):
    idx = (long / 360.0) * 36
    return CARDS[int(idx)],  RULER[int(idx)]


def _get_cusp(kind, planet, longitude, dat, delta):
    """
    When does planet exit its current sign?
    """
    n_dat = dat
    card = get_card(longitude)
    zodiac_number = int(longitude / 30)

    for inc in range(1, 100000):
        n_dat = n_dat + timedelta(hours=delta * 12)
        planet.compute(n_dat, n_dat)
        longitude = math.degrees(ephem.Ecliptic(planet).lon.norm)
        if kind == "sign":
            n_zodiac_number = int(longitude / 30)
            if n_zodiac_number != zodiac_number:
                return n_dat
        elif kind == "card":
            n_card = get_card(longitude)
            if n_card != card:
                return n_dat
        else:
            raise Exception("Bad kind %s" % kind)

def get_exit_date(kind, planet, longitude, dat):
    return _get_cusp(kind, planet, longitude, dat, delta=1)

def get_enter_date(kind, planet, longitude, dat):
    return _get_cusp(kind, planet, longitude, dat, delta=-1)

def get_day_part(enter_date, exit_date):
    dat = UTCNOW()
    in_days = (dat - enter_date).days
    tot_days = (exit_date - enter_date).days
    return {
        "in_days": in_days, "tot_days": tot_days
    }

def get_wheel_deg(dat=None):
    if dat is None:
        dat = UTCNOW()
        info = get_planet_info(pos_time=dat)
        sun_info = info[6]["body"]
        sun_info.compute(dat, dat)
        longitude = math.degrees(ephem.Ecliptic(sun_info).lon.norm)
        return 90-longitude
    

def zodiac_body(body, dat=None):
    if dat is None:
        dat = UTCNOW()

    info = get_planet_info(pos_time=dat)
    planet = info[body]["body"]
    planet.compute(dat, dat)
    longitude = math.degrees(ephem.Ecliptic(planet).lon.norm)
    (small, ruler) = get_card(longitude)
    zodiac_number = int(longitude / 30)
    _enter = lambda _kind: get_enter_date(_kind, planet, longitude, dat)
    _exit = lambda _kind: get_exit_date(_kind, planet, longitude, dat)
    (body_zodiac, zodiac_symbol) = ZODIAC[zodiac_number], ZU[zodiac_number]
    suit_meaning = {"w": "Fire", "s": "Air", "c": "Water", "d": "Earth"}
    return {
        "sign_day_part": get_day_part(_enter("sign"), _exit("sign")),
        "card_day_part": get_day_part(_enter("card"), _exit("card")),
        "body_symbol": info[body]["glyph"],
        "zodiac_symbol": zodiac_symbol,
        "body_zodiac": body_zodiac,
        "zodiac_number": zodiac_number,
        "zodiac_font_letter": "abcdefghijkl"[zodiac_number],
        "zodiac_atu": "%02d" % ZODIAC_ATU[zodiac_number],
        "planet_atu": "%02d" % info[body]["atu"],
        "degrees": int(longitude % 30),
        "minutes": int(round((longitude % 1) * 60)),
        "small": small,
        "ruler": ruler,
        "planet_num": small["p"],
        "ace": {"card": "%s01" % small["suit"], "m": suit_meaning[small["suit"]]},
        "decan": "%s%s" % (small["suit"], small["n"]),
        "longitude": longitude,
        "planet_img": "%02d" % info[body]["atu"],
        "zodiac_img": "%02d" % ZODIAC_ATU[zodiac_number],
    }

def zodiacal_longitude(body, dat=None):
    "Format longitude in zodiacal form (like '00AR00') and return as a string."
    if dat is None:
        dat = datetime.datetime.now()

    info = get_planet_info(pos_time=dat)
    planet = info[body]["body"]
    planet.compute(dat, dat)
    longitude = math.degrees(ephem.Ecliptic(planet).lon.norm)
    degrees = int(longitude % 30)
    sign = int(longitude / 30)
    (name, symbol) = ZODIAC[sign], ZU[sign]
    body_symbol = info[body]["glyph"]
    minutes = int(round((longitude % 1) * 60))
    return u"{0} {1:02}\u00B0 {2:02}' {3}".format(body_symbol, degrees, minutes, symbol )


def colour_wheel_HSV(num_colours):
    step = [(_i * 1.0 / num_colours) for _i in xrange(num_colours)]
    HSV = [(_i % 1.0, 0.9, 0.9) for _i in step]
    print (HSV)
    RGB = map(lambda hsv: colorsys.hsv_to_rgb(*hsv), HSV)
    RGB_set = [map(lambda col: int(255*col), rgb) for rgb in RGB]
    return ["#%02x%02x%02x" % tuple(rgb) for rgb in RGB_set]


def g_p(phase):
    sweep = []; mag = 0; ang=0

    if (phase <= 0.25):
        sweep = [ 1, 0 ]
        mag = 20 - 20 * phase * 4

    elif (phase <= 0.50):
        sweep = [ 0, 0 ]
        mag = 20 * (phase - 0.25) * 4

    elif (phase <= 0.75):
        sweep = [ 1, 1 ]
        mag = 20 - 20 * (phase - 0.50) * 4
    elif (phase <= 1):
        sweep = [ 0, 1 ]
        mag = 20 * (phase - 0.75) * 4

    return {
        "mag": mag,
        "sweep": sweep,
        "ang": 2.5 * math.pi - (2 * math.pi * phase)
    }


def crescent_calc():
    mk_ts = lambda _x: calendar.timegm(_x.datetime().timetuple())

    now = UTCNOW()
    scd = {
        "new": {
            "date_ts": mk_ts(ephem.next_new_moon(now)),
            "date": ephem.next_new_moon(now).datetime(),
        },
        "full": {
            "date_ts": mk_ts(ephem.next_full_moon(now)),
            "date": ephem.next_full_moon(now).datetime(),
        },
        "sun": {
            "crescent": g_p(zodiac_body(6)["degrees"]/30.0),
            "degrees": zodiac_body(6)["degrees"],
        },
    }
    for phase in ("new", "full"):
        _dur = (scd[phase]["date"] - now)
        scd[phase]["days"] = _dur.days
        scd[phase]["fmt"] = "%s days" % _dur.days if _dur.days > 1 else "%s day" % _dur.days
        scd[phase]["day_count"] = _dur.days + (_dur.seconds / 3600) / 24.0
        scd[phase]["day_age"] =  29.53059 - scd[phase]["day_count"]
        scd[phase]["phase"] = scd[phase]["day_age"] / 29.53059
        scd[phase]["crescent"] =  g_p(scd[phase]["phase"])
        if scd[phase]["days"] < 1:
            scd[phase]["hours"] = _dur.seconds / 3600
            scd[phase]["fmt"] = "%s hours" % scd[phase]["hours"] if scd[phase]["hours"] > 1 else "%s hour" % scd[phase]["hours"]
            if scd[phase]["hours"] < 1:
                scd[phase]["mins"] = (_dur.seconds / 60) - scd[phase]["hours"] * 60
                scd[phase]["fmt"] = "%s minutes" % scd[phase]["mins"] if scd[phase]["mins"] > 1 else "%s minutes" % scd[phase]["mins"]

    return scd


if __name__ == "__main__":
    #print colour_wheel_HSV(num_colours=12)
    print(zodiacal_longitude(body=6))
    print (RULER)
    print(zodiac_body(body=6))
