from flask import Flask,render_template,request,send_file
import random,json,os
from time import sleep
from threading import Thread
def get_randnum():
    nums={}
    try:
        with open("numbers.txt",'r') as file:
            nums = json.loads(file.read())
    except:
        num = random.randint(1111,9999)
        nums[str(num)]="none"
        with open("numbers.txt",'w') as file:
                file.write(str(nums).replace("'",'"'))
        return num
    while(1):
        num = random.randint(1111,9999)
        if num not in nums:
            nums[str(num)]="none"
            with open("numbers.txt",'w') as file:
                file.write(str(nums).replace("'",'"'))
            return num
        

def savedata(randnum,filename):
    data={}
    try:
        with open('data.txt','r') as file:
            data=json.loads(file.read())
    except:
        pass
    data[str(randnum)]=filename
    with open('data.txt','w') as file:
        file.write(str(data).replace("'",'"'))


def rmdata(randnum,filename):
    sleep(7200)
    data={}
    with open('numbers.txt','r') as file:
        data=json.loads(file.read())
    data.pop(str(randnum))
    with open("numbers.txt","w") as file:
        file.write(str(data).replace("'",'"'))
    with open('data.txt','r') as file:
        data=json.loads(file.read())
    data.pop(str(randnum))
    with open("data.txt","w") as file:
        file.write(str(data).replace("'",'"'))
    os.remove('static/files/'+str(randnum)+'/'+filename)
    os.rmdir('static/files/'+str(randnum))



app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def main():
    if request.method=='GET':
        return render_template('index.html')
    else:
        file = request.files["file"]
        randnum = get_randnum()
        savedata(randnum,file.filename)
        os.mkdir("static/files/"+str(randnum))
        file.save("static/files/"+str(randnum)+"/"+file.filename)
        Thread(target=rmdata,args=(randnum,file.filename,)).start()
        return str(randnum)
    
    
@app.route('/download',methods=['POST'])
def down():
    num = request.form['n1'] + request.form['n2'] + request.form['n3'] + request.form['n4']
    data={}
    with open('data.txt','r') as file:
        data=json.loads(file.read())
    if num not in data:
        return "Error:404--NOT-Found"
    else:
        return {"code":num,"name":data[num]}    
    


app.run(host='0.0.0.0',debug=True)