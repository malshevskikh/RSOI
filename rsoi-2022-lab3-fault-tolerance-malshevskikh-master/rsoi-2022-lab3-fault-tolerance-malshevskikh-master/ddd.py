
import schedule

k = 0
def run_request():
    global k
    print("ssssafdf")
    if k >= 10:
        schedule.cancel_job(j)
    else:
        k = k + 1
    print(k)
    print(j)


#j = schedule.every(3).seconds.do(run_request)
j = schedule.every(3).seconds.do(run_request)

def run_task():
    while True:
        schedule.run_pending()

run_task()