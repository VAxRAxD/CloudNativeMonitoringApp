log='04/07/2023 09:31:01     CPU UTILIZATION : 78.2%    MEMORY UTILIZATION : 49.0%     DISK UTILIZATION : 23.2%     NETWORK SPEED : - MBITS/S'
s=log[:len(log)-1]
s=s.split('  ')
print(s)
s=[data.strip() for data in s if data!=""]
data=dict()
data['time']=s[0]
for i in range(1,len(s)-1):
    k,v=s[i].split(':')
    data[k.split(' ')[0].lower()]=float(v[:len(v)-1].strip())
k,v=s[len(s)-1].split(':')
if v.split(' ')[1]!="-":
    data[k.split(' ')[0].lower()]=float(v.split(' ')[1])
else:
    data[k.split(' ')[0].lower()]="-"
print(data)