import os
import re
import certifi
import airportsdata
import requests
import pycountry
from dotenv import load_dotenv

load_dotenv()

# get in the path correctly
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

API_KEY  = os.getenv("AVIATIONSTACK_API_KEY")
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "SLK")

BASE_URL = "http://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load('IATA')

COUNTRY_ALIASES = {
    "usa": "US",
    "u.s.a": "US",
    "u.s.": "US",
    "america": "US",
    "united states": "US",
    "uk": "GB",
    "u.k.": "GB",
    "britain": "GB",
    "england": "GB",
    "uae": "AE",
    "dubai": "AE",
    "south korea": "KR",
    "korea": "KR",
    "russia": "RU",
    "vietnam": "VN",
    "bangladesh": "BD",
    "india": "IN",
    "japan": "JP",
    "china": "CN",
    "singapore": "SG",
    "malaysia": "MY",
    "thailand": "TH",
    "indonesia": "ID",
    "nepal": "NP",
    "qatar": "QA",
    "saudi arabia": "SA",
    "turkey": "TR",
    "canada": "CA",
    "australia": "AU",
    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",
}

COUNTRY_MAIN_AIRPORT = {
    "LK": "CMB",  # Sri Lanka
    "BD": "DAC",  # Bangladesh
    "IN": "DEL",  # India
    "PK": "ISB",  # Pakistan
    "NP": "KTM",  # Nepal
    "BT": "PBH",  # Bhutan
    "MV": "MLE",  # Maldives

    "JP": "NRT",  # Japan
    "KR": "ICN",  # South Korea
    "CN": "PEK",  # China
    "HK": "HKG",  # Hong Kong
    "TW": "TPE",  # Taiwan
    "SG": "SIN",  # Singapore
    "MY": "KUL",  # Malaysia
    "TH": "BKK",  # Thailand
    "ID": "CGK",  # Indonesia
    "PH": "MNL",  # Philippines
    "VN": "SGN",  # Vietnam
    "KH": "PNH",  # Cambodia
    "LA": "VTE",  # Laos
    "MM": "RGN",  # Myanmar
    "BN": "BWN",  # Brunei
    "MN": "UBN",  # Mongolia

    "AE": "DXB",  # United Arab Emirates
    "SA": "JED",  # Saudi Arabia
    "QA": "DOH",  # Qatar
    "KW": "KWI",  # Kuwait
    "BH": "BAH",  # Bahrain
    "OM": "MCT",  # Oman
    "TR": "IST",  # Turkey
    "IL": "TLV",  # Israel
    "JO": "AMM",  # Jordan
    "EG": "CAI",  # Egypt

    "GB": "LHR",  # United Kingdom
    "IE": "DUB",  # Ireland
    "FR": "CDG",  # France
    "DE": "FRA",  # Germany
    "IT": "FCO",  # Italy
    "ES": "MAD",  # Spain
    "PT": "LIS",  # Portugal
    "NL": "AMS",  # Netherlands
    "BE": "BRU",  # Belgium
    "CH": "ZRH",  # Switzerland
    "AT": "VIE",  # Austria
    "SE": "ARN",  # Sweden
    "NO": "OSL",  # Norway
    "DK": "CPH",  # Denmark
    "FI": "HEL",  # Finland
    "PL": "WAW",  # Poland
    "CZ": "PRG",  # Czech Republic
    "HU": "BUD",  # Hungary
    "GR": "ATH",  # Greece
    "RO": "OTP",  # Romania
    "BG": "SOF",  # Bulgaria
    "HR": "ZAG",  # Croatia
    "RS": "BEG",  # Serbia
    "UA": "KBP",  # Ukraine

    "US": "JFK",  # United States
    "CA": "YYZ",  # Canada
    "MX": "MEX",  # Mexico
    "BR": "GRU",  # Brazil
    "AR": "EZE",  # Argentina
    "CL": "SCL",  # Chile
    "CO": "BOG",  # Colombia
    "PE": "LIM",  # Peru

    "AU": "SYD",  # Australia
    "NZ": "AKL",  # New Zealand
    "FJ": "NAN",  # Fiji

    "ZA": "JNB",  # South Africa
    "NG": "LOS",  # Nigeria
    "KE": "NBO",  # Kenya
    "ET": "ADD",  # Ethiopia
    "TZ": "DAR",  # Tanzania
    "UG": "EBB",  # Uganda
    "GH": "ACC",  # Ghana
    "MA": "CMN",  # Morocco
    "TN": "TUN",  # Tunisia
    "DZ": "ALG",  # Algeria
}

CITY_MAIN_AIRPORT = {
    # Sri Lanka
    "colombo": "CMB",
    "negombo": "CMB",
    "kandy": "CMB",
    "galle": "CMB",
    "jaffna": "JAF",
    "trincomalee": "TRR",
    "batticaloa": "BTC",

    # Bangladesh
    "dhaka": "DAC",
    "chittagong": "CGP",
    "chattogram": "CGP",
    "sylhet": "ZYL",

    # India
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "bombay": "BOM",
    "kolkata": "CCU",
    "calcutta": "CCU",
    "chennai": "MAA",
    "madras": "MAA",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "hyderabad": "HYD",
    "ahmedabad": "AMD",
    "pune": "PNQ",
    "goa": "GOI",
    "kochi": "COK",
    "cochin": "COK",
    "jaipur": "JAI",
    "lucknow": "LKO",
    "patna": "PAT",
    "varanasi": "VNS",
    "surat": "STV",
    "amritsar": "ATQ",
    "bhubaneswar": "BBI",

    # Pakistan
    "islamabad": "ISB",
    "karachi": "KHI",
    "lahore": "LHE",
    "peshawar": "PEW",
    "multan": "MUX",

    # Nepal
    "kathmandu": "KTM",
    "pokhara": "PKR",

    # Maldives
    "male": "MLE",
    "malé": "MLE",

    # Japan
    "tokyo": "NRT",
    "osaka": "KIX",
    "kyoto": "KIX",
    "nagoya": "NGO",
    "fukuoka": "FUK",
    "sapporo": "CTS",
    "okinawa": "OKA",
    "naha": "OKA",

    # South Korea
    "seoul": "ICN",
    "busan": "PUS",
    "incheon": "ICN",
    "jeju": "CJU",

    # China
    "beijing": "PEK",
    "shanghai": "PVG",
    "guangzhou": "CAN",
    "shenzhen": "SZX",
    "chengdu": "CTU",
    "chongqing": "CKG",
    "hangzhou": "HGH",
    "nanjing": "NKG",
    "xian": "XIY",
    "xi'an": "XIY",
    "wuhan": "WUH",

    # Hong Kong / Taiwan
    "hong kong": "HKG",
    "taipei": "TPE",
    "kaohsiung": "KHH",

    # Southeast Asia
    "singapore": "SIN",
    "kuala lumpur": "KUL",
    "jakarta": "CGK",
    "bali": "DPS",
    "denpasar": "DPS",
    "bangkok": "BKK",
    "phuket": "HKT",
    "chiang mai": "CNX",
    "manila": "MNL",
    "cebu": "CEB",
    "ho chi minh city": "SGN",
    "saigon": "SGN",
    "hanoi": "HAN",
    "phnom penh": "PNH",
    "siem reap": "SAI",
    "vientiane": "VTE",
    "yangon": "RGN",
    "brunei": "BWN",
    "bandar seri begawan": "BWN",

    # Middle East
    "dubai": "DXB",
    "abu dhabi": "AUH",
    "doha": "DOH",
    "riyadh": "RUH",
    "jeddah": "JED",
    "medina": "MED",
    "kuwait city": "KWI",
    "manama": "BAH",
    "muscat": "MCT",
    "istanbul": "IST",
    "ankara": "ESB",
    "tel aviv": "TLV",
    "amman": "AMM",
    "cairo": "CAI",

    # United Kingdom & Ireland
    "london": "LHR",
    "manchester": "MAN",
    "birmingham": "BHX",
    "edinburgh": "EDI",
    "glasgow": "GLA",
    "liverpool": "LPL",
    "dublin": "DUB",
    "belfast": "BFS",

    # France
    "paris": "CDG",
    "nice": "NCE",
    "lyon": "LYS",
    "marseille": "MRS",
    "toulouse": "TLS",

    # Germany
    "frankfurt": "FRA",
    "berlin": "BER",
    "munich": "MUC",
    "hamburg": "HAM",
    "dusseldorf": "DUS",
    "düsseldorf": "DUS",
    "cologne": "CGN",

    # Italy
    "rome": "FCO",
    "milan": "MXP",
    "venice": "VCE",
    "florence": "FLR",
    "naples": "NAP",

    # Spain & Portugal
    "madrid": "MAD",
    "barcelona": "BCN",
    "seville": "SVQ",
    "valencia": "VLC",
    "lisbon": "LIS",
    "porto": "OPO",

    # Netherlands / Belgium / Switzerland
    "amsterdam": "AMS",
    "rotterdam": "RTM",
    "brussels": "BRU",
    "zurich": "ZRH",
    "geneva": "GVA",

    # Nordic countries
    "stockholm": "ARN",
    "oslo": "OSL",
    "copenhagen": "CPH",
    "helsinki": "HEL",
    "reykjavik": "KEF",

    # Central / Eastern Europe
    "vienna": "VIE",
    "prague": "PRG",
    "warsaw": "WAW",
    "budapest": "BUD",
    "bucharest": "OTP",
    "athens": "ATH",
    "sofia": "SOF",
    "zagreb": "ZAG",
    "belgrade": "BEG",
    "istanbul": "IST",
    "kyiv": "KBP",
    "moscow": "SVO",
    "st petersburg": "LED",
    "saint petersburg": "LED",

    # United States
    "new york": "JFK",
    "new york city": "JFK",
    "los angeles": "LAX",
    "san francisco": "SFO",
    "chicago": "ORD",
    "houston": "IAH",
    "dallas": "DFW",
    "miami": "MIA",
    "washington": "IAD",
    "washington dc": "IAD",
    "boston": "BOS",
    "seattle": "SEA",
    "las vegas": "LAS",
    "atlanta": "ATL",
    "denver": "DEN",
    "orlando": "MCO",
    "phoenix": "PHX",

    # Canada
    "toronto": "YYZ",
    "vancouver": "YVR",
    "montreal": "YUL",
    "calgary": "YYC",
    "ottawa": "YOW",
    "edmonton": "YEG",

    # Australia
    "sydney": "SYD",
    "melbourne": "MEL",
    "brisbane": "BNE",
    "perth": "PER",
    "adelaide": "ADL",
    "canberra": "CBR",
    "gold coast": "OOL",

    # New Zealand
    "auckland": "AKL",
    "wellington": "WLG",
    "christchurch": "CHC",
    "queenstown": "ZQN",

    # South America
    "sao paulo": "GRU",
    "rio de janeiro": "GIG",
    "buenos aires": "EZE",
    "santiago": "SCL",
    "lima": "LIM",
    "bogota": "BOG",
    "medellin": "MDE",
    "quito": "UIO",
    "caracas": "CCS",

    # Africa
    "johannesburg": "JNB",
    "cape town": "CPT",
    "durban": "DUR",
    "lagos": "LOS",
    "abuja": "ABV",
    "nairobi": "NBO",
    "addis ababa": "ADD",
    "dar es salaam": "DAR",
    "kampala": "EBB",
    "accra": "ACC",
    "casablanca": "CMN",
    "marrakech": "RAK",
    "tunis": "TUN",
    "algiers": "ALG",
}

def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    stop_words = [
        "flight", "flights", "ticket", "tickets", "trip", "travel",
        "plan", "complete", "days", "day", "including", "hotel",
        "hotels", "sightseeing", "under", "budget", "info", "information"
    ]
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words).strip()

def country_name_to_code(text: str):
    text = clean_text(text)

    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]

    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass

    # Detect country name inside longer text
    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2

    for alias, code in COUNTRY_ALIASES.items():
        if alias in text:
            return code

    return None

def airport_country_matches(airport: dict, country_code: str) -> bool:
    airport_country = str(airport.get("country", "")).upper().strip()

    if airport_country == country_code:
        return True

    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country and airport_country.lower() == country.name.lower():
            return True
    except Exception:
        pass

    return False




def get_best_airport_for_country(country_code: str):
    preferred = COUNTRY_MAIN_AIRPORT.get(country_code)

    if preferred and preferred in AIRPORTS:
        return preferred

    candidates = []

    for iata, airport in AIRPORTS.items():
        if not iata:
            continue

        if airport_country_matches(airport, country_code):
            name = str(airport.get("name", "")).lower()
            city = str(airport.get("city", "")).lower()

            score = 0

            if "international" in name:
                score += 50
            if "intl" in name:
                score += 40
            if "capital" in name:
                score += 20
            if city:
                score += 5

            candidates.append((score, iata))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]




def resolve_location_to_iata(location: str):
    """
    Converts country/city/airport/IATA into IATA code.

    Examples:
    Bangladesh -> DAC
    Japan -> NRT
    Dhaka -> DAC
    Tokyo -> NRT
    DAC -> DAC
    """

    if not location:
        return None

    raw_location = location.strip()

    # Direct IATA code
    if re.fullmatch(r"[A-Za-z]{3}", raw_location):
        code = raw_location.upper()
        if code in AIRPORTS:
            return code

    location_clean = clean_text(raw_location)

    if not location_clean:
        return None

    # City preferred airport
    if location_clean in CITY_MAIN_AIRPORT:
        return CITY_MAIN_AIRPORT[location_clean]

    # Country preferred airport
    country_code = country_name_to_code(location_clean)
    if country_code:
        airport = get_best_airport_for_country(country_code)
        if airport:
            return airport

    # Exact city match from airport database
    city_matches = []

    for iata, airport in AIRPORTS.items():
        city = str(airport.get("city", "")).lower().strip()
        name = str(airport.get("name", "")).lower().strip()

        score = 0

        if city == location_clean:
            score += 100
        elif location_clean in city:
            score += 70

        if location_clean in name:
            score += 50

        if "international" in name:
            score += 10

        if score > 0:
            city_matches.append((score, iata))

    if city_matches:
        city_matches.sort(reverse=True)
        return city_matches[0][1]

    return None




def find_location_mentions(query: str):
    """
    Finds country or city names inside a natural language query.
    """

    q = query.lower()
    mentions = []

    # Country aliases
    for alias in COUNTRY_ALIASES:
        if re.search(rf"\b{re.escape(alias)}\b", q):
            mentions.append(alias)

    # Country names from pycountry
    for country in pycountry.countries:
        name = country.name.lower()
        if len(name) >= 4 and re.search(rf"\b{re.escape(name)}\b", q):
            mentions.append(name)

    # City names from our preferred city map
    for city in CITY_MAIN_AIRPORT:
        if re.search(rf"\b{re.escape(city)}\b", q):
            mentions.append(city)

    # Remove duplicate while keeping order
    unique_mentions = []
    for item in mentions:
        if item not in unique_mentions:
            unique_mentions.append(item)

    return unique_mentions


def parse_route(query: str):
    """
    Returns:
    dep_iata, arr_iata

    Can return:
    None, None  -> global live flights
    DAC, NRT    -> filtered route
    DAC, None   -> all flights from DAC
    None, NRT   -> all flights to NRT
    """

    q = query.strip()
    q_lower = q.lower()

    # Global / all-country query
    global_keywords = [
        "all country",
        "all countries",
        "global flight",
        "global flights",
        "all flight",
        "all flights",
        "worldwide flight",
        "worldwide flights",
    ]

    if any(keyword in q_lower for keyword in global_keywords):
        return None, None

    # Direct IATA code route: DAC to NRT
    codes = re.findall(r"\b[A-Z]{3}\b", q)

    if len(codes) >= 2:
        dep = codes[0].upper()
        arr = codes[1].upper()
        return dep, arr

    # Pattern: from X to Y
    match = re.search(
        r"\bfrom\s+(.+?)\s+\bto\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:
        origin_text = match.group(1)
        dest_text = match.group(2)

        dep_iata = resolve_location_to_iata(origin_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # Pattern: to Y from X
    match = re.search(
        r"\bto\s+(.+?)\s+\bfrom\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:
        dest_text = match.group(1)
        origin_text = match.group(2)

        dep_iata = resolve_location_to_iata(origin_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # Pattern: flights from X
    match = re.search(r"\bfrom\s+(.+?)(?:[.!?]|$)", q_lower)

    if match:
        origin_text = match.group(1)
        dep_iata = resolve_location_to_iata(origin_text)
        return dep_iata, None

    # Pattern: flights to X
    match = re.search(r"\bto\s+(.+?)(?:[.!?]|$)", q_lower)

    if match:
        dest_text = match.group(1)
        arr_iata = resolve_location_to_iata(dest_text)
        return None, arr_iata

    # Fallback: find country/city mentions
    mentions = find_location_mentions(q)

    if len(mentions) >= 2:
        dep_iata = resolve_location_to_iata(mentions[0])
        arr_iata = resolve_location_to_iata(mentions[1])
        return dep_iata, arr_iata

    if len(mentions) == 1:
        arr_iata = resolve_location_to_iata(mentions[0])
        return DEFAULT_ORIGIN_IATA, arr_iata

    return None, None


def format_flight(flight: dict):
    airline = flight.get("airline", {}).get("name") or "Unknown airline"
    flight_number = flight.get("flight", {}).get("iata") or "Unknown flight number"
    status = flight.get("flight_status") or "Unknown"

    dep = flight.get("departure", {}) or {}
    arr = flight.get("arrival", {}) or {}

    dep_airport = dep.get("airport") or "Unknown departure airport"
    dep_iata = dep.get("iata") or "Unknown"
    dep_terminal = dep.get("terminal") or "N/A"
    dep_gate = dep.get("gate") or "N/A"
    dep_scheduled = dep.get("scheduled") or "Unknown"
    dep_delay = dep.get("delay")
    dep_delay_text = f"{dep_delay} minutes" if dep_delay is not None else "N/A"

    arr_airport = arr.get("airport") or "Unknown arrival airport"
    arr_iata = arr.get("iata") or "Unknown"
    arr_terminal = arr.get("terminal") or "N/A"
    arr_gate = arr.get("gate") or "N/A"
    arr_scheduled = arr.get("scheduled") or "Unknown"
    arr_delay = arr.get("delay")
    arr_delay_text = f"{arr_delay} minutes" if arr_delay is not None else "N/A"

    return f"""
Airline: {airline}
Flight: {flight_number}
Status: {status}

Departure:
- Airport: {dep_airport}
- IATA: {dep_iata}
- Terminal: {dep_terminal}
- Gate: {dep_gate}
- Scheduled: {dep_scheduled}
- Delay: {dep_delay_text}

Arrival:
- Airport: {arr_airport}
- IATA: {arr_iata}
- Terminal: {arr_terminal}
- Gate: {arr_gate}
- Scheduled: {arr_scheduled}
- Delay: {arr_delay_text}
""".strip()


def search_flights(query: str, limit: int = 15):
    if not API_KEY:
        return (
            "Flight API error: AVIATIONSTACK_API_KEY is missing.\n"
            "Please add this in your .env file:\n"
            "AVIATIONSTACK_API_KEY=your_api_key_here"
        )

    dep_iata, arr_iata = parse_route(query)

    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }

    if dep_iata:
        params["dep_iata"] = dep_iata

    if arr_iata:
        params["arr_iata"] = arr_iata

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Flight API request failed: {e}"
    except ValueError:
        return "Flight API returned invalid JSON."

    if "error" in data:
        error = data["error"]
        return (
            "Flight API error:\n"
            f"Code: {error.get('code', 'Unknown')}\n"
            f"Message: {error.get('message', 'Unknown error')}"
        )

    flight_data = data.get("data", [])

    if not flight_data:
        route_text = ""

        if dep_iata and arr_iata:
            route_text = f" for route {dep_iata} to {arr_iata}"
        elif dep_iata:
            route_text = f" from {dep_iata}"
        elif arr_iata:
            route_text = f" to {arr_iata}"

        return (
            f"No live flight data found{route_text}.\n\n"
            "Note: AviationStack provides live/status flight data, not ticket prices. "
            "For actual fare prices, use a flight-pricing API such as Amadeus."
        )

    route_info = "Global live flights"

    if dep_iata and arr_iata:
        route_info = f"Live flights from {dep_iata} to {arr_iata}"
    elif dep_iata:
        route_info = f"Live flights from {dep_iata}"
    elif arr_iata:
        route_info = f"Live flights to {arr_iata}"

    formatted_flights = [format_flight(flight) for flight in flight_data[:limit]]

    return f"{route_info}\n\n" + "\n\n---\n\n".join(formatted_flights)


if __name__ == "__main__":
    print(search_flights("Plan a 7 days Japan trip from sri lanka including flights and hotels"))
    print("\n" + "=" * 80 + "\n")
    print(search_flights("all country flight info"))

