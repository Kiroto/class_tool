from datetime import date, datetime, timedelta
from io import StringIO
from typing import Callable
import csv

takenDates = []

takenDates.append(datetime(2024, 5, 17))

# Yo hago lo que me manden
# Prefiero backend a frontend 100 veces
DAY_INDEX_MAPPING = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

SPARE_DAY = "Spare"
HOLIDAY = "Holiday"


def daysFilter(availableWeekdays: list[int] = [0, 1, 2, 3, 4, 5, 6]):
    def returnedFilter(date: datetime):
        if date.weekday() not in availableWeekdays or date in takenDates:
            return False
        return True

    return returnedFilter


def createDaysList(
    startDate: datetime,
    endDate: datetime,
    filter: Callable[[datetime], bool],
) -> list[datetime]:
    # do you hear me?
    dates = []
    currentDate = datetime(startDate.year, startDate.month, startDate.day)
    while currentDate < endDate:
        if filter(currentDate):
            dates.append(currentDate)
        currentDate += timedelta(days=1)
    return dates


def dateFromAmericanString(amstr: str) -> datetime:
    splitstr = [int(x) for x in amstr.split("/")]
    return datetime(splitstr[2], splitstr[0], splitstr[1])


def getDateInput() -> list[datetime]:

    # Get information from filled template
    program_configuration = {"holidays": [], "class_names": [], "available_days": []}
    with open("ClassesConfiguration.csv", "r") as configurationFile:
        configuration_string = configurationFile.read()
        configuration_string_io = StringIO(configuration_string)
        configuration_reader = csv.reader(configuration_string_io)
        for index, configuration_row in enumerate(configuration_reader):
            if index in [0, 2]:
                continue

            if index == 1:
                program_configuration["start_date"] = dateFromAmericanString(
                    configuration_row[0]
                )
                program_configuration["end_date"] = dateFromAmericanString(
                    configuration_row[1]
                )
                continue

            if index in [3, 4, 5, 6, 7, 8, 9]:
                if len(configuration_row) > 3 and configuration_row[3]:
                    program_configuration["available_days"].append(index - 3)

            if len(configuration_row[0]) > 0:
                program_configuration["holidays"].append(
                    dateFromAmericanString(configuration_row[0])
                )

            if len(configuration_row[1]) > 0:
                program_configuration["class_names"].append(
                    configuration_row[1]
                )

    ## Set variables with the configured information
    startDate = program_configuration["start_date"]
    endDate = program_configuration["end_date"]

    # Ready up the class names 
    class_names = program_configuration["class_names"]

    # Ready up the holidays
    holidays = program_configuration["holidays"]

    # Generate the days filter (filters out all un-selected days)
    filterToUse = daysFilter(program_configuration["available_days"])

    dates = createDaysList(startDate, endDate, filterToUse)

    output_text = ""
    day_index = 0

    for date in dates:
        is_holiday = date in holidays
        class_to_show = (
            HOLIDAY
            if is_holiday
            else (class_names[day_index] if len(class_names) > day_index else SPARE_DAY)
        )
        output_text += f"{date.month}/{date.day}/{date.year},{DAY_INDEX_MAPPING[date.weekday()]},{class_to_show}\n"
        if not is_holiday:
            day_index += 1

    with open("output.csv", "w") as f:
        f.write(output_text)


# today = datetime.today()
# inOneMonth = today + timedelta(days=30 * 4)

# newDates = createDaysList(today, inOneMonth, daysFilter())

# for dt in newDates:
#     print(str(dt))


# Si yo soy un duro esto funciona a la primera
getDateInput()
