import schedule
import time

def job(t):
    print "I'm working...", t
    return

schedule.every().day.at("01:00").do(job,'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

#run on terminal with this following command
nohup python2.7 MyScheduledProgram.py &
nohup python3 MyScheduledProgram.py &
