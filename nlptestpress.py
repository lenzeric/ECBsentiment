# Import block
import csv
import re
from datetime import datetime
import urllib.request
import ssl
from bs4 import BeautifulSoup

# Global constants
#url_list = ['https://www.ecb.europa.eu/press/pr/date/1999/html/pr990304.en.html']

url_list = ['https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1998/html/is980609.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1998/html/is980708.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1998/html/is980911.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1998/html/is981013.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1998/html/is981103.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1998/html/is981201.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1998/html/is981222.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990107.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990204.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990304.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990408.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990506.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990602.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990715.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is990909.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is991007.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is991104.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/1999/html/is991202.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000105.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000203.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000302.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000330.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000413.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000511.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000608.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000706.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is000914.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is001005.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is001019.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is001102.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2000/html/is001214.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010201.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010301.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010411.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010510.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010607.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010621.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010705.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is010830.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is011011.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is011108.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is011206.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2001/html/is011213.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020103_2.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020103.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020207.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020307.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020404.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020502.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020606.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020704.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is020912.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is021010.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is021107.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2002/html/is021205.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030109.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030206.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030306.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030403.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030508.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030508_1.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030605.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030710.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030904.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is030917.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is031002.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is031013.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is031106.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2003/html/is031204.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040108.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040205.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040304.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040401.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040506.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040603.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040701.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is040902.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is041007.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is041104.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2004/html/is041202.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050113.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050120_1.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050120.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050121.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050203.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050303.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050407.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050504.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050602.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050707.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is050901.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is051006.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is051103.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2005/html/is051201.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060112.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060202.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060302.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060406.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060504.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060608.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060706.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060803.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is060831.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is061005.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is061102.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2006/html/is061207.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070111.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070208.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070308.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070412.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070510.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070606.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070705.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070802.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is070906.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is071004.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is071108.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2007/html/is071206.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080110.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080207.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080306.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080410.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080508.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080605.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080703.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080807.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is080904.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is081002.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is081106.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2008/html/is081204.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090115.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090205.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090305.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090402.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090507.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090604.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090702.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090806.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is090903.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is091008.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is091105.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2009/html/is091203.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100114.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100204.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100304.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100408.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100506.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100610.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100708.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100805.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is100902.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is101007.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is101104.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2010/html/is101202.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110113.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110203.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110303.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110407.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110505.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110609.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110707.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110804.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is110908.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is111006.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is111103.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2011/html/is111208.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120112.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120209.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120308.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120404.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120503.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120606.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120705.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120802.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is120906.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is121004.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is121108.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2012/html/is121206.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130110.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130207.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130307.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130404.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130502.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130606.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130704.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130801.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is130905.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is131002.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is131107.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2013/html/is131205.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140109.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140206.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140306.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140403.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140508.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140605.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140703.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140807.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is140904.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is141002.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is141026.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is141106.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2014/html/is141204.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is150122.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is150305.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is150415.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is150603.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is150716.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is150903.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is151022.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2015/html/is151203.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is160121.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is160310.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is160421.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is160602.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is160721.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is160908.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is161020.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2016/html/is161208.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/is170119.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/is170309.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/ecb.is170427.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/ecb.is170608.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/ecb.is170720.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/ecb.is170907.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/ecb.is171026.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2017/html/ecb.is171214.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is180125.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is180308.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is180426.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is180614.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is180726.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is180913.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is181025.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2018/html/ecb.is181213.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is190124~cd3821f8f5.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is190307~de1fdbd0b0.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is190410~c27197866f.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is190606~32b6221806.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is190725~547f29c369.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is190912~658eb51d68.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is191024~78a5550bc1.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2019/html/ecb.is191212~c9e1a6ab3e.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is200123~0bc778277b.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is200312~f857a21b6c.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is200430~ab3058e07f.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is200604~b479b8cfff.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is200716~3865f74bf8.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is200910~5c43e3a591.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is201029~80b00b5789.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2020/html/ecb.is201210~9b8e5f3cdd.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is210121~e601112a72.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is210311~d368d7151a.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is210422~b0ad2d3414.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is210610~115f4c0246.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.sp210708~ab68c3bd9d.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is210722~13e7f5e795.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is210909~b2d882f724.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is211028~939f22970b.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2021/html/ecb.is211216~9abaace28e.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is220203~ca7001dec0.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is220310~1bc8c1b1ca.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is220414~fa5c8fe142.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is220609~abe7c95b19.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is220721~51ef267c68.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is220908~cd8363c58e.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is221027~358a06a35f.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2022/html/ecb.is221215~197ac630ae.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is230202~4313651089.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is230316~6c10b087b5.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is230504~f242392c72.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is230615~3de9d68335.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is230727~e0a11feb2e.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is230914~686786984a.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is231026~c23b4eb5f0.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2023/html/ecb.is231214~df8627de60.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is240125~db0f145c32.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is240307~314650bd5c.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is240411~9974984b58.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is240606~d32cd6cc8a.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is240718~6600b4add6.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is240912~4f7b17040c.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is241017~59ad385bab.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2024/html/ecb.is241212~ce143b3bc8.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2025/html/ecb.is250130~1f418aa0f4.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2025/html/ecb.is250306~4307bd0941.en.html',
'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2025/html/ecb.is250417~091c625eb6.en.html'
]

# Main execution block
# Create unverified SSL context (⚠️ not recommended for production use)
ssl_context = ssl._create_unverified_context()
results = []
date_pattern = re.compile(r'(?:pr|ecb\.mp|ecb\.is|is)(\d{6})')

for url in url_list:
    try:
        # Extract date from URL
        match = date_pattern.search(url)
        if match:
            raw_date = match.group(1)
            date_obj = datetime.strptime(raw_date, "%y%m%d")
            formatted_date = date_obj.strftime("%d-%m-%y")
        else:
            formatted_date = ""

        html = urllib.request.urlopen(url, context=ssl_context).read()
        soup = BeautifulSoup(html, 'html.parser')

        section_texts = []

        # Get all <div class="section"> blocks
        section_divs = soup.find_all("div", class_="section")

        for div in section_divs:
            # Add all <p> tags inside this section
            for p in div.find_all("p"):
                section_texts.append(p.get_text(" ", strip=True))

            # Look at siblings after the section div in case Q&A follows
            for sibling in div.find_next_siblings():
                if sibling.name == "p":
                    section_texts.append(sibling.get_text(" ", strip=True))
                # Stop if we hit another section or different structure
                elif sibling.name == "div" and "section" in sibling.get("class", []):
                    break

        # Fallback if no text found
        if not section_texts:
            section_texts = [p.get_text(" ", strip=True) for p in soup.find_all("p")]

        section_text = " ".join(section_texts)

        # Also try to include any <div class="orderedlist">
        list_div = soup.find("div", class_="orderedlist")
        list_text = list_div.get_text(" ", strip=True) if list_div else ""

        full_text = section_text + " " + list_text
        results.append((formatted_date, url, full_text))

    except Exception as e:
        print(f"Error on {url}: {e}")
        results.append(("", url, ""))



# Save to CSV with date, url, and text
with open("scraped_texts_with_dates_2.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "url", "text"])
    writer.writerows(results)
