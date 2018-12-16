#coding=utf-8

import requests
import pandas as pd
import MySQLdb
import time
import sms_send
import lxml

if __name__=="__main__":
    #爬虫初始网络参数，不要修改
    postdata={
            'username':"username",
            'password':"password",
            'session_locale':'zh_CN',
         #   'rememberme':'true',
         #   'redirect_to':'http://www.santostang.com/wp-admin/profile.php',
         #   'wp-submit':'登陆',
                }   
    post_url='http://us.nwpu.edu.cn/eams/login.action'
    get_grade_url='http://us.nwpu.edu.cn/eams/teach/grade/course/person!search.action?semesterId=18&projectType='
    headers={
           'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Host':'www.santostang.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
            }
    #
    #修改登录翱翔门户帐号的函数定义，不用修改
    def change_login_information(username,password):
        global postdata
        postdata={
            'username':username,
            'password':password,
            'session_locale':'zh_CN',
         #   'rememberme':'true',
         #   'redirect_to':'http://www.santostang.com/wp-admin/profile.php',
         #   'wp-submit':'登陆',
                }   
    #
    #循环通知参数，times用来统计循环次数，i用来确定程序运行成功。
    times=1
    i=1
    #
    while True:

    #session.cookies.load(ignore_discard=True)
    #login_cookies=session.get('http://www.santostang.com/wp-admin/profile.php',headers=headers)
    #print(login_cookies.text)
    #print(logincode.status_code)


    #soup=BeautifulSoup('grade_page.text','html.parser')
    #grade_table=soup.table.tr
    #print(grade_table)
    #grade=re.findall(u'<tr(.*)([\u4e00-\u9fa5])(.*)+/tr>',grade_page.text)
    #print(grade)
    #   tb=pd.read_html(grade_page.text)[0]
    #   shuju1=pd.read_csv(r'F:\stock.csv')
    #   tb.to_csv(r'F:\stock.csv', mode='w', encoding='utf_8_sig', header=1, index=0)
    #   print(tb)
    #   print("\n")
    #   shuju2=pd.read_csv(r'F:\stock.csv')
    #   if shuju1.shape[0]==shuju2.shape[0]:
    #       print("success")


    #
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd="123456",db='work',charset='utf8')
        cur=conn.cursor()
        cur.execute("select * from inform_list")
        data=cur.fetchall()
    #连接数据库获得数据,元组形式

        time_seach=1
        for datastream in data:

            change_login_information(datastream[2],datastream[3])
            #print(postdata)
            session=requests.session()
            login_page =session.post(post_url, data=postdata,headers=headers)
            grade_page=session.get(get_grade_url,headers=headers)
            tb=pd.read_html(grade_page.text)[0]
            col_online_str=tb.shape[0]
            col_online=int(col_online_str)#得到目前网上成绩的行数并转换为int
            col_base=datastream[5]#得到目前数据库里成绩的行数
            if col_base!=col_online:
                now_data=tb.values#获取每一行的数据，形成多维矩阵
                col_number=0
                km=now_data[col_number][3]
                xf=now_data[col_number][5]
                pscj=now_data[col_number][6]
                kscj=now_data[col_number][7]
                zzcj=now_data[col_number][9]
                xfj=now_data[col_number][10]
                number=datastream[6]
                params=[datastream[1],km,xf,pscj,kscj,zzcj,xfj]
                try:
                    sms_send.sender(number,params)
                except:
                    print('error')
                cur.execute("update inform_list set line=%d where name='%s'"%(col_online,params[0]))
            print("完成第%d次搜索"%(time_seach))
                #print("update inform_list set line=%d where name='%s'"%(col_online,params[0]))
            time_seach+=1
        cur.close()
        conn.commit()
        conn.close()
        if i==1:
            print("程序启动成功")
        i+=1    
        print("程序正常运行%d回"%times)
        print(time.asctime( time.localtime(time.time()) ))

        times+=1    
            #    sms_send.sender()
      #  print (data)
        
        time.sleep(500)
    #    with open(r'F:\stock.csv','r',encoding='utf-8') as csvfile:
    #        csv_reader=csv.reader(csvfile)
    #        score=[]
    #        i=0;
    #        for row in csv_reader:
    #            if(i!=0):
    #                score=[row[-8],row[-6],row[-5],row[-4],row[-2],row[-1]]
    #            i+=1
    #        print(score)
    # #   def check_change(csv_reader):
    #        k=0
    #        for row in csv_reader:
    #            k+=1
    #        conn=MySQLdb.connect(host='localhost',user='root',password='233wsgtc',db='test',charset='utf8')
    #        cur=conn.cursor()
    #        cur.execute("SELECT line FROM viptables WHERE name='刘政东'")
    #        lines=cur.fetchone()
    #        print (lines[0])
    #        time.sleep(5)
    #    g+=1
    #    if g==5:
    #        break    
    #
    #    row_str='|'.join(row)
    #    print(row_str)
    #    print(row[-4])

    '''数据库操作
    conn=MySQLdb.connect(host='localhost',user='root',password='233wsgtc',db='test')
    cur=conn.cursor()
    cur.execute("INSERT INTO viptables (name, score) VALUES ('刘政东', )")
    cur.close()
    conn.commit()
    conn.close()
    '''
    #session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
    #print(grade_page.text)
    #print(login_page.text)
    #print(login_page.text)
    #session.cookies.save(ignore_discard=True, ignore_expires=True )
    #try:
     #   session.cookies.load(ignore_discard=True)
       # print("Cookie正常加载")

    #    print('logincode.status_code')
     #   r=requests.get('http://www.santostang.com/wp-admin/profile.php',headers=headers)
     #   print(r.text)
    #except:
      #  print("Cookie未能加载")

    '''
    session.cookies =cookielib.LWPCookieJar(filename='cookies')
    try:
        session.cookies.load(ignore_discard=true)
    except:
         print('error')
    print(login_page.status_code)
    '''

    '''
    r=requests.get(link, headers=headers)
    soup=BeautifulSoup(r.text,"html.parser")
    pipei=re.findall(r'<span class="title">(.*)</span>',r.text)
    print(pipei)
    '''

