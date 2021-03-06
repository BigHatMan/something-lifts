from pymongo import MongoClient

db = MongoClient('mongodb://localhost:27017/').dataclient
lifts = db.lifts
food = db.food

# Edit the password requirements to suit needs.
PASSWORD_REQUIREMENTS = {
	'chars': 6,
	'uppers': 1,
	'numbers': 1
}

def valid_password(password):
	chars_hit = len(password) >= PASSWORD_REQUIREMENTS['chars']

	num_uppers = sum([char.isupper() for char in password])
	uppers_hit = num_uppers >= PASSWORD_REQUIREMENTS['uppers']

	num_nums = sum([char.isdigit() for char in password])
	nums_hit = num_nums >= PASSWORD_REQUIREMENTS['numbers']

	print chars_hit, uppers_hit, nums_hit
	return chars_hit and uppers_hit and nums_hit

def enterInfo(user, inputLifts):
        lifts.insert({"user": user,
                      "lifts": inputLifts})

def getLifts(user, workoutNumber):
        ans = lifts.find({"user":user})[int(workoutNumber)]
        return ans['lifts']

def getAllLifts(user):
        liftsDict = {}
        for day in lifts.find({"user":user}):
                for lift in day['lifts']:
                        if lift not in liftsDict:
                                liftsDict[lift] = [day['lifts'][lift]]
                        else:
                                liftsDict[lift].append(day['lifts'][lift])
        print "liftsDict: " + str(liftsDict)
        return liftsDict
 
def enterFood(user, day, calories, fat, carbs, protein):
        food.insert({ "user": user,
                      "date": day,
                      "calories": calories,
                      "fat": fat,
                      "carbs": carbs,
                      "protein": protein})

def getFood(user, day):
        calories = 0.0
        fat = 0.0
        carbs = 0.0
        protein = 0.0
        for f in food.find({"user":user, "date":day}):
                calories += float(f['calories'])
                fat += float(f['fat'])
                carbs += float(f['carbs'])
                protein += float(f['protein'])
        return { "calories": calories,
                 "fat": fat,
                 "carbs": carbs,
                 "protein": protein }

def getAllFood(user):
        dates = []
        for f in food.find({"user": user}):
                date = f['date']
                if date not in dates:
                        dates.append(date)
        foodsDict = {}
        numDates = 0
        for date in dates:
                calories = 0
                fat = 0
                carbs = 0
                protein = 0
                numDates += 1
                for f in food.find({"user": user, "date": date}):
                        calories += float(f['calories'])
                        fat += float(f['fat'])
                        carbs += float(f['carbs'])
                        protein += float(f['protein'])
                foodsDict[date] = {"calories": calories,
                                    "fat": fat,
                                    "carbs": carbs,
                                    "protein": protein,
                                    "numDates": numDates}
        return foodsDict

def getAvgROC(val):
		avg = ((val[-1]-val[0])/len(val))
		return avg
		