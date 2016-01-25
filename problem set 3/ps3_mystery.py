# for exercise1
#def mystery_test(i, complement): 
#	if complement.find('bo') > -1: return "FAIL"

# for exercise2
def mystery_test(i, complement): 
	if i == 0 and complement.find('style="margin:0px;"') > -1: return "FAIL"
	if i == 1 and complement.find('<body onload="') > -1: return "FAIL"
	if i == 2 and complement.find('<div style="display:none;">') > -1: return "FAIL"
	if i == 3 and complement.find('action="process_bug.cgi"') > -1: return "FAIL"
	if i == 4 and complement.find('<div class="indent-box"> <div>') > -1: return "FAIL"
	return "PASS"
	
