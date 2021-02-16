from flask_restful import Resource, reqparse
from flask_restful import abort
from src.system.utils.shell import execute_command_with_exception

_tz_list = [
    {
        "zone": "Africa/Abidjan"
    },
    {
        "zone": "Africa/Accra"
    },
    {
        "zone": "Africa/Addis_Ababa"
    },
    {
        "zone": "Africa/Algiers"
    },
    {
        "zone": "Africa/Asmara"
    },
    {
        "zone": "Africa/Bamako"
    },
    {
        "zone": "Africa/Bangui"
    },
    {
        "zone": "Africa/Banjul"
    },
    {
        "zone": "Africa/Bissau"
    },
    {
        "zone": "Africa/Blantyre"
    },
    {
        "zone": "Africa/Brazzaville"
    },
    {
        "zone": "Africa/Bujumbura"
    },
    {
        "zone": "Africa/Cairo"
    },
    {
        "zone": "Africa/Casablanca"
    },
    {
        "zone": "Africa/Ceuta"
    },
    {
        "zone": "Africa/Conakry"
    },
    {
        "zone": "Africa/Dakar"
    },
    {
        "zone": "Africa/Dar_es_Salaam"
    },
    {
        "zone": "Africa/Djibouti"
    },
    {
        "zone": "Africa/Douala"
    },
    {
        "zone": "Africa/El_Aaiun"
    },
    {
        "zone": "Africa/Freetown"
    },
    {
        "zone": "Africa/Gaborone"
    },
    {
        "zone": "Africa/Harare"
    },
    {
        "zone": "Africa/Johannesburg"
    },
    {
        "zone": "Africa/Juba"
    },
    {
        "zone": "Africa/Kampala"
    },
    {
        "zone": "Africa/Khartoum"
    },
    {
        "zone": "Africa/Kigali"
    },
    {
        "zone": "Africa/Kinshasa"
    },
    {
        "zone": "Africa/Lagos"
    },
    {
        "zone": "Africa/Libreville"
    },
    {
        "zone": "Africa/Lome"
    },
    {
        "zone": "Africa/Luanda"
    },
    {
        "zone": "Africa/Lubumbashi"
    },
    {
        "zone": "Africa/Lusaka"
    },
    {
        "zone": "Africa/Malabo"
    },
    {
        "zone": "Africa/Maputo"
    },
    {
        "zone": "Africa/Maseru"
    },
    {
        "zone": "Africa/Mbabane"
    },
    {
        "zone": "Africa/Mogadishu"
    },
    {
        "zone": "Africa/Monrovia"
    },
    {
        "zone": "Africa/Nairobi"
    },
    {
        "zone": "Africa/Ndjamena"
    },
    {
        "zone": "Africa/Niamey"
    },
    {
        "zone": "Africa/Nouakchott"
    },
    {
        "zone": "Africa/Ouagadougou"
    },
    {
        "zone": "Africa/Porto-Novo"
    },
    {
        "zone": "Africa/Sao_Tome"
    },
    {
        "zone": "Africa/Tripoli"
    },
    {
        "zone": "Africa/Tunis"
    },
    {
        "zone": "Africa/Windhoek"
    },
    {
        "zone": "America/Adak"
    },
    {
        "zone": "America/Anchorage"
    },
    {
        "zone": "America/Anguilla"
    },
    {
        "zone": "America/Antigua"
    },
    {
        "zone": "America/Araguaina"
    },
    {
        "zone": "America/Argentina/Buenos_Aires"
    },
    {
        "zone": "America/Argentina/Catamarca"
    },
    {
        "zone": "America/Argentina/Cordoba"
    },
    {
        "zone": "America/Argentina/Jujuy"
    },
    {
        "zone": "America/Argentina/La_Rioja"
    },
    {
        "zone": "America/Argentina/Mendoza"
    },
    {
        "zone": "America/Argentina/Rio_Gallegos"
    },
    {
        "zone": "America/Argentina/Salta"
    },
    {
        "zone": "America/Argentina/San_Juan"
    },
    {
        "zone": "America/Argentina/San_Luis"
    },
    {
        "zone": "America/Argentina/Tucuman"
    },
    {
        "zone": "America/Argentina/Ushuaia"
    },
    {
        "zone": "America/Aruba"
    },
    {
        "zone": "America/Asuncion"
    },
    {
        "zone": "America/Atikokan"
    },
    {
        "zone": "America/Bahia"
    },
    {
        "zone": "America/Bahia_Banderas"
    },
    {
        "zone": "America/Barbados"
    },
    {
        "zone": "America/Belem"
    },
    {
        "zone": "America/Belize"
    },
    {
        "zone": "America/Blanc-Sablon"
    },
    {
        "zone": "America/Boa_Vista"
    },
    {
        "zone": "America/Bogota"
    },
    {
        "zone": "America/Boise"
    },
    {
        "zone": "America/Cambridge_Bay"
    },
    {
        "zone": "America/Campo_Grande"
    },
    {
        "zone": "America/Cancun"
    },
    {
        "zone": "America/Caracas"
    },
    {
        "zone": "America/Cayenne"
    },
    {
        "zone": "America/Cayman"
    },
    {
        "zone": "America/Chicago"
    },
    {
        "zone": "America/Chihuahua"
    },
    {
        "zone": "America/Costa_Rica"
    },
    {
        "zone": "America/Creston"
    },
    {
        "zone": "America/Cuiaba"
    },
    {
        "zone": "America/Curacao"
    },
    {
        "zone": "America/Danmarkshavn"
    },
    {
        "zone": "America/Dawson"
    },
    {
        "zone": "America/Dawson_Creek"
    },
    {
        "zone": "America/Denver"
    },
    {
        "zone": "America/Detroit"
    },
    {
        "zone": "America/Dominica"
    },
    {
        "zone": "America/Edmonton"
    },
    {
        "zone": "America/Eirunepe"
    },
    {
        "zone": "America/El_Salvador"
    },
    {
        "zone": "America/Fort_Nelson"
    },
    {
        "zone": "America/Fortaleza"
    },
    {
        "zone": "America/Glace_Bay"
    },
    {
        "zone": "America/Goose_Bay"
    },
    {
        "zone": "America/Grand_Turk"
    },
    {
        "zone": "America/Grenada"
    },
    {
        "zone": "America/Guadeloupe"
    },
    {
        "zone": "America/Guatemala"
    },
    {
        "zone": "America/Guayaquil"
    },
    {
        "zone": "America/Guyana"
    },
    {
        "zone": "America/Halifax"
    },
    {
        "zone": "America/Havana"
    },
    {
        "zone": "America/Hermosillo"
    },
    {
        "zone": "America/Indiana/Indianapolis"
    },
    {
        "zone": "America/Indiana/Knox"
    },
    {
        "zone": "America/Indiana/Marengo"
    },
    {
        "zone": "America/Indiana/Petersburg"
    },
    {
        "zone": "America/Indiana/Tell_City"
    },
    {
        "zone": "America/Indiana/Vevay"
    },
    {
        "zone": "America/Indiana/Vincennes"
    },
    {
        "zone": "America/Indiana/Winamac"
    },
    {
        "zone": "America/Inuvik"
    },
    {
        "zone": "America/Iqaluit"
    },
    {
        "zone": "America/Jamaica"
    },
    {
        "zone": "America/Juneau"
    },
    {
        "zone": "America/Kentucky/Louisville"
    },
    {
        "zone": "America/Kentucky/Monticello"
    },
    {
        "zone": "America/Kralendijk"
    },
    {
        "zone": "America/La_Paz"
    },
    {
        "zone": "America/Lima"
    },
    {
        "zone": "America/Los_Angeles"
    },
    {
        "zone": "America/Lower_Princes"
    },
    {
        "zone": "America/Maceio"
    },
    {
        "zone": "America/Managua"
    },
    {
        "zone": "America/Manaus"
    },
    {
        "zone": "America/Marigot"
    },
    {
        "zone": "America/Martinique"
    },
    {
        "zone": "America/Matamoros"
    },
    {
        "zone": "America/Mazatlan"
    },
    {
        "zone": "America/Menominee"
    },
    {
        "zone": "America/Merida"
    },
    {
        "zone": "America/Metlakatla"
    },
    {
        "zone": "America/Mexico_City"
    },
    {
        "zone": "America/Miquelon"
    },
    {
        "zone": "America/Moncton"
    },
    {
        "zone": "America/Monterrey"
    },
    {
        "zone": "America/Montevideo"
    },
    {
        "zone": "America/Montserrat"
    },
    {
        "zone": "America/Nassau"
    },
    {
        "zone": "America/New_York"
    },
    {
        "zone": "America/Nipigon"
    },
    {
        "zone": "America/Nome"
    },
    {
        "zone": "America/Noronha"
    },
    {
        "zone": "America/North_Dakota/Beulah"
    },
    {
        "zone": "America/North_Dakota/Center"
    },
    {
        "zone": "America/North_Dakota/New_Salem"
    },
    {
        "zone": "America/Nuuk"
    },
    {
        "zone": "America/Ojinaga"
    },
    {
        "zone": "America/Panama"
    },
    {
        "zone": "America/Pangnirtung"
    },
    {
        "zone": "America/Paramaribo"
    },
    {
        "zone": "America/Phoenix"
    },
    {
        "zone": "America/Port-au-Prince"
    },
    {
        "zone": "America/Port_of_Spain"
    },
    {
        "zone": "America/Porto_Velho"
    },
    {
        "zone": "America/Puerto_Rico"
    },
    {
        "zone": "America/Punta_Arenas"
    },
    {
        "zone": "America/Rainy_River"
    },
    {
        "zone": "America/Rankin_Inlet"
    },
    {
        "zone": "America/Recife"
    },
    {
        "zone": "America/Regina"
    },
    {
        "zone": "America/Resolute"
    },
    {
        "zone": "America/Rio_Branco"
    },
    {
        "zone": "America/Santarem"
    },
    {
        "zone": "America/Santiago"
    },
    {
        "zone": "America/Santo_Domingo"
    },
    {
        "zone": "America/Sao_Paulo"
    },
    {
        "zone": "America/Scoresbysund"
    },
    {
        "zone": "America/Sitka"
    },
    {
        "zone": "America/St_Barthelemy"
    },
    {
        "zone": "America/St_Johns"
    },
    {
        "zone": "America/St_Kitts"
    },
    {
        "zone": "America/St_Lucia"
    },
    {
        "zone": "America/St_Thomas"
    },
    {
        "zone": "America/St_Vincent"
    },
    {
        "zone": "America/Swift_Current"
    },
    {
        "zone": "America/Tegucigalpa"
    },
    {
        "zone": "America/Thule"
    },
    {
        "zone": "America/Thunder_Bay"
    },
    {
        "zone": "America/Tijuana"
    },
    {
        "zone": "America/Toronto"
    },
    {
        "zone": "America/Tortola"
    },
    {
        "zone": "America/Vancouver"
    },
    {
        "zone": "America/Whitehorse"
    },
    {
        "zone": "America/Winnipeg"
    },
    {
        "zone": "America/Yakutat"
    },
    {
        "zone": "America/Yellowknife"
    },
    {
        "zone": "Antarctica/Casey"
    },
    {
        "zone": "Antarctica/Davis"
    },
    {
        "zone": "Antarctica/DumontDUrville"
    },
    {
        "zone": "Antarctica/Macquarie"
    },
    {
        "zone": "Antarctica/Mawson"
    },
    {
        "zone": "Antarctica/McMurdo"
    },
    {
        "zone": "Antarctica/Palmer"
    },
    {
        "zone": "Antarctica/Rothera"
    },
    {
        "zone": "Antarctica/Syowa"
    },
    {
        "zone": "Antarctica/Troll"
    },
    {
        "zone": "Antarctica/Vostok"
    },
    {
        "zone": "Arctic/Longyearbyen"
    },
    {
        "zone": "Asia/Aden"
    },
    {
        "zone": "Asia/Almaty"
    },
    {
        "zone": "Asia/Amman"
    },
    {
        "zone": "Asia/Anadyr"
    },
    {
        "zone": "Asia/Aqtau"
    },
    {
        "zone": "Asia/Aqtobe"
    },
    {
        "zone": "Asia/Ashgabat"
    },
    {
        "zone": "Asia/Atyrau"
    },
    {
        "zone": "Asia/Baghdad"
    },
    {
        "zone": "Asia/Bahrain"
    },
    {
        "zone": "Asia/Baku"
    },
    {
        "zone": "Asia/Bangkok"
    },
    {
        "zone": "Asia/Barnaul"
    },
    {
        "zone": "Asia/Beirut"
    },
    {
        "zone": "Asia/Bishkek"
    },
    {
        "zone": "Asia/Brunei"
    },
    {
        "zone": "Asia/Chita"
    },
    {
        "zone": "Asia/Choibalsan"
    },
    {
        "zone": "Asia/Colombo"
    },
    {
        "zone": "Asia/Damascus"
    },
    {
        "zone": "Asia/Dhaka"
    },
    {
        "zone": "Asia/Dili"
    },
    {
        "zone": "Asia/Dubai"
    },
    {
        "zone": "Asia/Dushanbe"
    },
    {
        "zone": "Asia/Famagusta"
    },
    {
        "zone": "Asia/Gaza"
    },
    {
        "zone": "Asia/Hebron"
    },
    {
        "zone": "Asia/Ho_Chi_Minh"
    },
    {
        "zone": "Asia/Hong_Kong"
    },
    {
        "zone": "Asia/Hovd"
    },
    {
        "zone": "Asia/Irkutsk"
    },
    {
        "zone": "Asia/Jakarta"
    },
    {
        "zone": "Asia/Jayapura"
    },
    {
        "zone": "Asia/Jerusalem"
    },
    {
        "zone": "Asia/Kabul"
    },
    {
        "zone": "Asia/Kamchatka"
    },
    {
        "zone": "Asia/Karachi"
    },
    {
        "zone": "Asia/Kathmandu"
    },
    {
        "zone": "Asia/Khandyga"
    },
    {
        "zone": "Asia/Kolkata"
    },
    {
        "zone": "Asia/Krasnoyarsk"
    },
    {
        "zone": "Asia/Kuala_Lumpur"
    },
    {
        "zone": "Asia/Kuching"
    },
    {
        "zone": "Asia/Kuwait"
    },
    {
        "zone": "Asia/Macau"
    },
    {
        "zone": "Asia/Magadan"
    },
    {
        "zone": "Asia/Makassar"
    },
    {
        "zone": "Asia/Manila"
    },
    {
        "zone": "Asia/Muscat"
    },
    {
        "zone": "Asia/Nicosia"
    },
    {
        "zone": "Asia/Novokuznetsk"
    },
    {
        "zone": "Asia/Novosibirsk"
    },
    {
        "zone": "Asia/Omsk"
    },
    {
        "zone": "Asia/Oral"
    },
    {
        "zone": "Asia/Phnom_Penh"
    },
    {
        "zone": "Asia/Pontianak"
    },
    {
        "zone": "Asia/Pyongyang"
    },
    {
        "zone": "Asia/Qatar"
    },
    {
        "zone": "Asia/Qostanay"
    },
    {
        "zone": "Asia/Qyzylorda"
    },
    {
        "zone": "Asia/Riyadh"
    },
    {
        "zone": "Asia/Sakhalin"
    },
    {
        "zone": "Asia/Samarkand"
    },
    {
        "zone": "Asia/Seoul"
    },
    {
        "zone": "Asia/Shanghai"
    },
    {
        "zone": "Asia/Singapore"
    },
    {
        "zone": "Asia/Srednekolymsk"
    },
    {
        "zone": "Asia/Taipei"
    },
    {
        "zone": "Asia/Tashkent"
    },
    {
        "zone": "Asia/Tbilisi"
    },
    {
        "zone": "Asia/Tehran"
    },
    {
        "zone": "Asia/Thimphu"
    },
    {
        "zone": "Asia/Tokyo"
    },
    {
        "zone": "Asia/Tomsk"
    },
    {
        "zone": "Asia/Ulaanbaatar"
    },
    {
        "zone": "Asia/Urumqi"
    },
    {
        "zone": "Asia/Ust-Nera"
    },
    {
        "zone": "Asia/Vientiane"
    },
    {
        "zone": "Asia/Vladivostok"
    },
    {
        "zone": "Asia/Yakutsk"
    },
    {
        "zone": "Asia/Yangon"
    },
    {
        "zone": "Asia/Yekaterinburg"
    },
    {
        "zone": "Asia/Yerevan"
    },
    {
        "zone": "Atlantic/Azores"
    },
    {
        "zone": "Atlantic/Bermuda"
    },
    {
        "zone": "Atlantic/Canary"
    },
    {
        "zone": "Atlantic/Cape_Verde"
    },
    {
        "zone": "Atlantic/Faroe"
    },
    {
        "zone": "Atlantic/Madeira"
    },
    {
        "zone": "Atlantic/Reykjavik"
    },
    {
        "zone": "Atlantic/South_Georgia"
    },
    {
        "zone": "Atlantic/St_Helena"
    },
    {
        "zone": "Atlantic/Stanley"
    },
    {
        "zone": "Australia/Adelaide"
    },
    {
        "zone": "Australia/Brisbane"
    },
    {
        "zone": "Australia/Broken_Hill"
    },
    {
        "zone": "Australia/Currie"
    },
    {
        "zone": "Australia/Darwin"
    },
    {
        "zone": "Australia/Eucla"
    },
    {
        "zone": "Australia/Hobart"
    },
    {
        "zone": "Australia/Lindeman"
    },
    {
        "zone": "Australia/Lord_Howe"
    },
    {
        "zone": "Australia/Melbourne"
    },
    {
        "zone": "Australia/Perth"
    },
    {
        "zone": "Australia/Sydney"
    },
    {
        "zone": "Europe/Amsterdam"
    },
    {
        "zone": "Europe/Andorra"
    },
    {
        "zone": "Europe/Astrakhan"
    },
    {
        "zone": "Europe/Athens"
    },
    {
        "zone": "Europe/Belgrade"
    },
    {
        "zone": "Europe/Berlin"
    },
    {
        "zone": "Europe/Bratislava"
    },
    {
        "zone": "Europe/Brussels"
    },
    {
        "zone": "Europe/Bucharest"
    },
    {
        "zone": "Europe/Budapest"
    },
    {
        "zone": "Europe/Busingen"
    },
    {
        "zone": "Europe/Chisinau"
    },
    {
        "zone": "Europe/Copenhagen"
    },
    {
        "zone": "Europe/Dublin"
    },
    {
        "zone": "Europe/Gibraltar"
    },
    {
        "zone": "Europe/Guernsey"
    },
    {
        "zone": "Europe/Helsinki"
    },
    {
        "zone": "Europe/Isle_of_Man"
    },
    {
        "zone": "Europe/Istanbul"
    },
    {
        "zone": "Europe/Jersey"
    },
    {
        "zone": "Europe/Kaliningrad"
    },
    {
        "zone": "Europe/Kiev"
    },
    {
        "zone": "Europe/Kirov"
    },
    {
        "zone": "Europe/Lisbon"
    },
    {
        "zone": "Europe/Ljubljana"
    },
    {
        "zone": "Europe/London"
    },
    {
        "zone": "Europe/Luxembourg"
    },
    {
        "zone": "Europe/Madrid"
    },
    {
        "zone": "Europe/Malta"
    },
    {
        "zone": "Europe/Mariehamn"
    },
    {
        "zone": "Europe/Minsk"
    },
    {
        "zone": "Europe/Monaco"
    },
    {
        "zone": "Europe/Moscow"
    },
    {
        "zone": "Europe/Oslo"
    },
    {
        "zone": "Europe/Paris"
    },
    {
        "zone": "Europe/Podgorica"
    },
    {
        "zone": "Europe/Prague"
    },
    {
        "zone": "Europe/Riga"
    },
    {
        "zone": "Europe/Rome"
    },
    {
        "zone": "Europe/Samara"
    },
    {
        "zone": "Europe/San_Marino"
    },
    {
        "zone": "Europe/Sarajevo"
    },
    {
        "zone": "Europe/Saratov"
    },
    {
        "zone": "Europe/Simferopol"
    },
    {
        "zone": "Europe/Skopje"
    },
    {
        "zone": "Europe/Sofia"
    },
    {
        "zone": "Europe/Stockholm"
    },
    {
        "zone": "Europe/Tallinn"
    },
    {
        "zone": "Europe/Tirane"
    },
    {
        "zone": "Europe/Ulyanovsk"
    },
    {
        "zone": "Europe/Uzhgorod"
    },
    {
        "zone": "Europe/Vaduz"
    },
    {
        "zone": "Europe/Vatican"
    },
    {
        "zone": "Europe/Vienna"
    },
    {
        "zone": "Europe/Vilnius"
    },
    {
        "zone": "Europe/Volgograd"
    },
    {
        "zone": "Europe/Warsaw"
    },
    {
        "zone": "Europe/Zagreb"
    },
    {
        "zone": "Europe/Zaporozhye"
    },
    {
        "zone": "Europe/Zurich"
    },
    {
        "zone": "Indian/Antananarivo"
    },
    {
        "zone": "Indian/Chagos"
    },
    {
        "zone": "Indian/Christmas"
    },
    {
        "zone": "Indian/Cocos"
    },
    {
        "zone": "Indian/Comoro"
    },
    {
        "zone": "Indian/Kerguelen"
    },
    {
        "zone": "Indian/Mahe"
    },
    {
        "zone": "Indian/Maldives"
    },
    {
        "zone": "Indian/Mauritius"
    },
    {
        "zone": "Indian/Mayotte"
    },
    {
        "zone": "Indian/Reunion"
    },
    {
        "zone": "Pacific/Apia"
    },
    {
        "zone": "Pacific/Auckland"
    },
    {
        "zone": "Pacific/Bougainville"
    },
    {
        "zone": "Pacific/Chatham"
    },
    {
        "zone": "Pacific/Chuuk"
    },
    {
        "zone": "Pacific/Easter"
    },
    {
        "zone": "Pacific/Efate"
    },
    {
        "zone": "Pacific/Enderbury"
    },
    {
        "zone": "Pacific/Fakaofo"
    },
    {
        "zone": "Pacific/Fiji"
    },
    {
        "zone": "Pacific/Funafuti"
    },
    {
        "zone": "Pacific/Galapagos"
    },
    {
        "zone": "Pacific/Gambier"
    },
    {
        "zone": "Pacific/Guadalcanal"
    },
    {
        "zone": "Pacific/Guam"
    },
    {
        "zone": "Pacific/Honolulu"
    },
    {
        "zone": "Pacific/Kiritimati"
    },
    {
        "zone": "Pacific/Kosrae"
    },
    {
        "zone": "Pacific/Kwajalein"
    },
    {
        "zone": "Pacific/Majuro"
    },
    {
        "zone": "Pacific/Marquesas"
    },
    {
        "zone": "Pacific/Midway"
    },
    {
        "zone": "Pacific/Nauru"
    },
    {
        "zone": "Pacific/Niue"
    },
    {
        "zone": "Pacific/Norfolk"
    },
    {
        "zone": "Pacific/Noumea"
    },
    {
        "zone": "Pacific/Pago_Pago"
    },
    {
        "zone": "Pacific/Palau"
    },
    {
        "zone": "Pacific/Pitcairn"
    },
    {
        "zone": "Pacific/Pohnpei"
    },
    {
        "zone": "Pacific/Port_Moresby"
    },
    {
        "zone": "Pacific/Rarotonga"
    },
    {
        "zone": "Pacific/Saipan"
    },
    {
        "zone": "Pacific/Tahiti"
    },
    {
        "zone": "Pacific/Tarawa"
    },
    {
        "zone": "Pacific/Tongatapu"
    },
    {
        "zone": "Pacific/Wake"
    },
    {
        "zone": "Pacific/Wallis"
    },
    {
        "zone": "UTC"
    }
]


def validate_host_set_timezone(timezone) -> str:
    if tz_list_match(timezone):
        return "sudo timetable set-timezone {}".format(timezone)
    abort(400, message="incorrect timezone sent try:`{}`".format(timezone))


def tz_list_match(timezone):
    """
    Returns a list of valid timezones for linux Example: Australia/Sydney.
    """
    tz_valid = False
    for d in _tz_list:
        if d['zone'] == timezone:
            tz_valid = True
    return tz_valid


class SetSystemTimeZone(Resource):
    def get(self):
        return _tz_list

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('timezone',
                            type=str,
                            help='timezone should be `Australia/Sydney`',
                            required=True)
        args = parser.parse_args()
        timezone = args['timezone']
        service = validate_host_set_timezone(timezone)
        try:
            execute_command_with_exception(service)
            return service
        except Exception as e:
            abort(501, message=str(e))
