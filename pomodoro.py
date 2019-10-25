import time
import math

"""
Status of pomodoro clock:
0: No pomodoro event
1: Pomodoro clock is running
2: A Pomodoro clock has been finished
3: Pomodoro clock is paused
"""


class Pomodoro:
    def __init__(self, str_len, t_dur):
        self.str_len = str_len
        self.t_dur = t_dur

        self.status = 0
        self.count_down = 0
        self.start_t = 0
        self.cur_t = 0
        self.end_t = 0
        self.remain_t = 60*self.t_dur

    def progressbar(self, slen, ret, dur):
        if (slen < 3):
            return('-'*slen)
        bar = '-'*(slen - 1) + '>'

        tick_index = math.floor((slen-1)*(dur*60.0 - ret)/(dur*60.0))
        if tick_index >= slen - 1:
            tick_index = slen - 2
        if tick_index < 0:
            tick_index = 0
        bar = bar[:tick_index] + '|' + bar[tick_index + 1:]
        bar = bar + ' Remining: ' + "{0:0>2}".format(int(self.remain_t // 60.0)) + ":" + "{0:0>2}".format(int(self.remain_t % 60.0))
        return(bar)

    def process_start(self):
        self.start_t = time.time()
        self.end_t = time.time() + 60*self.t_dur
        self.status = 1
        return("Pomodoro Clock of " + str(self.t_dur) + " mins started... Ending in " + str(self.end_t))

    def process_pause(self):
        self.status = 3
        return("Pomodoro Clock paused...")

    def process_resume(self):
        self.status = 1
        return("Pomodoro Clock resumed...")

    def process_stop(self):
        self.status = 0
        return("stop")

    def process_print(self):
        if self.status == 0:
            return("No Pomodoro clock running...")
        if self.status == 1:
            return(self.progressbar(30, self.remain_t, self.t_dur))
        if self.status == 2:
            return("Pomodoro clock finished! " + time.strftime('%H:%M', time.localtime(self.end_t)))
        if self.status == 3:
            return("Pomodoro clock is paused..., " + "{0:.2f}".format(self.remain_t / 60.0) + " minutes remaining")
        return("Pomodoro server running...")

    def process_inquiry(self):
        return(str(self.status))

    def update(self):
        if self.status == 0 or self.status == 2:
            return
        self.cur_t = time.time()
        if self.status == 3:
            self.end_t = self.cur_t + self.remain_t
        self.remain_t = self.end_t - self.cur_t
        if self.cur_t > self.end_t:
            print("One Pomodoro done!")
            self.status = 2
