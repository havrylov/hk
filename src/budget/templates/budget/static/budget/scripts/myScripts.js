tday = new Array("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat ");
tmonth = new Array("January", "February", "March", "April", "May", "June",
		"July", "August", " September", "October", "November", "December");
     

function GetClock() {
	d = new Date();
	nday = d.getDay();
	nmonth = d.getMonth();
	ndate = d.getDate();
	nyeara = d.getFullYear();
	nhour = d.getHours();
	nmin = d.getMinutes();
	nsec = d.getSeconds();
//	if (nyeara < 1000) {
//		nyeara = ("" + (nyeara + 11900)).substring(1, 5);
//	} else {
//		nyeara = ("" + (nyeara + 10000)).substring(1, 5);
//	}
	// if(nhour == 0) {ap = " AM";nhour = 12;}
	// else if(nhour <= 11) {ap = " AM";}
	// else if(nhour == 12) {ap = " PM";}
	// else if(nhour >= 13) {ap = " PM";nhour -= 12;}
	if (nhour <= 9) {
		nhour = "0" + nhour;
	}
	if (nmin <= 9) {
		nmin = "0" + nmin;
	}
	if (nsec <= 9) {
		nsec = "0" + nsec;
	}
	document.getElementById('date').innerHTML = "" + tday[nday] + ", "
			+ tmonth[nmonth] + " " + ndate + ", " + nyeara;
	document.getElementById('time').innerHTML = "" + nhour + ":" + nmin + ":"
			+ nsec;
	setTimeout("GetClock()", 1000);
}

function resizeIframe(obj) {
	obj.style.height = Math
			.round(1.03 * obj.contentWindow.document.body.scrollHeight)
			+ 'px';
	obj.style.width = obj.contentWindow.document.body.scrollWidth + 'px';
}

function setCorrectPeriod(select){
	options = select.options;
	selectedPeriod = select.selectedIndex;
	period = options[selectedPeriod].value;
	switch(period){
            case "none":
		setPeriodEnd("");
                setPeriodBegin("");
		break;
            case "curweek":
		setPeriodCurrentWeek();
		break;
            case "curmonth":
		setPeriodCurrentMonth();
		break;
            case "curyear":
		setPeriodCurrentYear();
		break;
            case "prevweek":
		setPeriodPreviousWeek();
		break;
            case "prevmonth":
		setPeriodPreviousMonth();
		break;
            case "prevyear":
		setPeriodPreviousYear();
		break;
            default:
		setPeriodCurrentMonth();	
	}
}

function setPeriodCurrentWeek(){
	setPeriodEnd(convertToString(getCurrentDate()));
	setPeriodBegin(convertToString(getCurrentWeekBegin()));
}

function setPeriodCurrentMonth() {
	setPeriodEnd(convertToString(getCurrentDate()));
	setPeriodBegin(convertToString(getCurrentMonthBegin()));
}

function setPeriodCurrentYear(){
	setPeriodEnd(convertToString(getCurrentDate()));
	setPeriodBegin(convertToString(getCurrentYearBegin()));
}

function setPeriodPreviousWeek(){
	setPeriodEnd(convertToString(getPreviousWeekEnd()));
	setPeriodBegin(convertToString(getPreviousWeekBegin()));
}

function setPeriodPreviousMonth() {
	setPeriodEnd(convertToString(getPreviousMonthEnd()));
	setPeriodBegin(convertToString(getPreviousMonthBegin()));
}

function setPeriodPreviousYear(){
	setPeriodEnd(convertToString(getPreviousYearEnd()));
	setPeriodBegin(convertToString(getPreviousYearBegin()));
}

function getCurrentDate() {
	var today = new Date();
	today.setHours(23);
	today.setMinutes(59);
	return today;	
}

function getCurrentMonthBegin() {
	var monthBegin = new Date();
	monthBegin.setHours(0);
	monthBegin.setMinutes(0);
	monthBegin.setDate(1);
	return monthBegin;
}

function getCurrentWeekEnd(){
	var weekEnd = new Date();
	if (weekEnd.getDay()!=0 ){
		weekEnd.setDate(weekEnd.getDate() + (7-weekEnd.getDay()));	
	}	
	weekEnd.setHours(23);
	weekEnd.setMinutes(59);	
	return weekEnd;
}

function getCurrentWeekBegin(){
	var weekBegin = new Date();
	if (weekBegin.getDay()!=0 ){
		weekBegin.setDate(weekBegin.getDate() - (weekBegin.getDay()-1));	
	}
	else{
		weekBegin.setDate(weekBegin.getDate() - 6);
	}
	weekBegin.setHours(0);
	weekBegin.setMinutes(0);
	return weekBegin;
}

function getPreviousWeekEnd(){
	var weekEnd = new Date();
	if (weekEnd.getDay()!=0 ){
		weekEnd.setDate(weekEnd.getDate()+7-weekEnd.getDay()-7);	
	}	
	else {
		weekEnd.setDate(weekEnd.getDate()-7);
	}
	weekEnd.setHours(23);
	weekEnd.setMinutes(59);	
	return weekEnd;
}

function getPreviousWeekBegin(){
	var weekBegin = new Date();
	if (weekBegin.getDay()!=0 ){
		weekBegin.setDate(weekBegin.getDate() - (weekBegin.getDay()-1) -7);	
	}
	else{
		weekBegin.setDate(weekBegin.getDate() - 6 -7);
	}
	weekBegin.setHours(0);
	weekBegin.setMinutes(0);
	return weekBegin;
}

function getCurrentMonthBegin(){
	var monthBegin = new Date();
	monthBegin.setDate(1);
	monthBegin.setHours(0);
	monthBegin.setMinutes(0);
	return monthBegin;
}

function getCurrentMonthEnd(){
	var monthEnd = new Date();
	monthEnd.setDate(getDaysInMonth(monthEnd));
	monthEnd.setHours(23);
	monthEnd.setMinutes(59);
	return monthEnd;
}

function getPreviousMonthBegin(){
	var monthBegin = new Date();
	monthBegin = setPreviousMonth(monthBegin);
	monthBegin.setDate(1);
	monthBegin.setHours(0);
	monthBegin.setMinutes(0);
	return monthBegin;
}

function getPreviousMonthEnd(){
	var monthEnd = new Date();
	monthEnd = setPreviousMonth(monthEnd);
	monthEnd.setDate(getDaysInMonth(monthEnd));
	monthEnd.setHours(23);
	monthEnd.setMinutes(59);
	return monthEnd;
}

function getCurrentYearBegin(){
	var yearBegin = new Date();
	yearBegin.setMonth(0);
	yearBegin.setDate(1);
	yearBegin.setHours(0);
	yearBegin.setMinutes(0);
	return yearBegin;
}

function getCurrentYearEnd(){
	var yearEnd = new Date();
	yearEnd.setMonth(11);
	yearEnd.setDate(31);
	yearEnd.setHours(23);
	yearEnd.setMinutes(59);
	return yearEnd;
}

function getPreviousYearBegin(){
	var yearBegin = new Date();
	yearBegin.setFullYear(yearBegin.getFullYear()-1);
	yearBegin.setMonth(0);
	yearBegin.setDate(1);
	yearBegin.setHours(0);
	yearBegin.setMinutes(0);
	return yearBegin;
}

function getPreviousYearEnd(){
	var yearEnd = new Date();
	yearEnd.setFullYear(yearEnd.getFullYear()-1);
	yearEnd.setMonth(11);
	yearEnd.setDate(31);
	yearEnd.setHours(23);
	yearEnd.setMinutes(59);
	return yearEnd;
}

function convertToString(dateForCoversion) {
	day = convertToReadableValue(dateForCoversion.getDate());
	month = convertToReadableValue(dateForCoversion.getMonth() + 1);
	year = convertToReadableValue(dateForCoversion.getFullYear());
	hour = convertToReadableValue(dateForCoversion.getHours());
	minute = convertToReadableValue(dateForCoversion.getMinutes());
	dateStr = day + "." + month + "." + year + " " + hour + ":" + minute;
	return dateStr;
}

function convertToReadableValue(oldValue) {
	if (oldValue <= 9) {
		oldValue = "0" + oldValue;
	}
	return oldValue;
}

function setPeriodEnd(periodEnd) {
	document.getElementById('end').value = periodEnd;
}

function setPeriodBegin(periodBegin) {
	document.getElementById('begin').value = periodBegin;
}

function isLeapYear(inputYear){
	if(inputYear%400==0||(inputYear%4==0&&inputYear%100!=0)) return true;
	return false;
}

function getDaysInMonth(date){
	var daysInMonths = [31,28,31,30,31,30,31,31,30,31,30,31];
	if (date.getMonth()==1&&isLeapYear(date.getFullYear())){
		return 29;
	}
	else {
		return daysInMonths[date.getMonth()];
	}
}

function setPreviousMonth(date){
	if (date.getMonth()==0){
		date.setFullYear(date.getFullYear()-1);
		date.setMonth(11);		
	}
	else{
		date.setMonth(date.getMonth()-1);
	}
	return date;
}