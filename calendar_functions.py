_MONTH_NAME = ['january', 'february','march','april',
	'may','june','july','august','september','october',
	'november','december']
	
_DAYS_IN_MONTH = [31,28,31,30,31,30,31,31,30,31,30,31]

def month_name(month):
	return _MONTH_NAME[month-1]
	
def days_in_month(month, year):
	if month == 2:
		if year % 4 == 0:
			leap = 1
		else:
			leap = 0
		return _DAYS_IN_MONTH[month-1] + leap
	return _DAYS_IN_MONTH[month-1]