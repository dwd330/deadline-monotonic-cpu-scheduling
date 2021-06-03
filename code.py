import pygame,sys
class task():

	def __init__(self, name, releasetime, period, excutiontime, deadline):
		self.releasetime = releasetime
		self.period = period
		self.excutiontime = excutiontime
		self.deadline = deadline
		self.next_avliable = releasetime
		self.name = name
		self.excuted = False
		self.addedtime = 0  # what arealy exucted from current period


class timeline():

	def __init__(self, inittask):
		self.currenttime = 0
		self.totaltime = 121
		self.currenttask = inittask
		self.tasks = []

	def addtask(self, task):
		fromtime = self.currenttime
		endtime = fromtime+1
		self.tasks.append([task.name, fromtime, endtime])
		self.currenttime = endtime
		self.currenttask = task


def avliabale_task(tasks):
	available_tasks = []
	for task in tasks:
		if timeline.currenttime >= task.next_avliable:
			available_tasks.append(task)

	if len(available_tasks) == 0:
		return False
	else:
		return available_tasks


def order_by_next_avliable(tasks):
	# sort list with key
	tasks.sort(key=lambda x: x.next_avliable)
	return tasks


def order_by_deadline(tasks):
	tasks.sort(key=lambda x: x.deadline)
	return tasks


# if any task of higher priority comes then, running task is preempted
def preempted(tasks):
	available = avliabale_task(tasks)
	if available:
		# if a task with higher perirty is avaiible
		orderd_with_priority = order_by_deadline(available)
		return orderd_with_priority[0]
	else:
		return False


def schedule(orderd_tasked):
	while(timeline.currenttime < timeline.totaltime):
		# No available tasks
		if (preempted(orderd_tasked) == False):
			timeline.currenttime += 1
			continue

		task = preempted(orderd_tasked)
		if task.addedtime < task.excutiontime:
			# then add higher task to time line
			timeline.addtask(task)
			task.addedtime += 1  # keep adding till it equal task.excutiontime
		elif task.addedtime == task.excutiontime:  # task compled
			task.addedtime = 0
			task.excuted = True
			# update next avliable
			task.next_avliable += task.period  # note


# Formating output
def formating_output():
	tasks=timeline.tasks
	name =""
	start = 0
	end = 0
	ftasks = []
	checked = False
	for i in range(len(tasks)-1):
		if tasks[i][0] == tasks[i+1][0]:
			if checked == False:
				checked = True
				name = tasks[i][0]
				start = tasks[i][1]
		elif tasks[i][0] != tasks[i+1][0]:
			checked = False
			end=tasks[i][2]
			ftasks.append([name, start, end])
	return ftasks
		
		

###*********main*******###
t1 = task("task1", 0, 60, 25, 50)
t2 = task("task2", 15, 60, 10, 40)
t3 = task("task3", 20, 60, 15, 60)
tasks = [t1, t2, t3]
orderd_tasked = order_by_next_avliable(tasks)
timeline = timeline(orderd_tasked[0])  # init task

schedule(orderd_tasked)
# print(timeline.tasks)
print(formating_output())
#draw:
while(True):
	data=formating_output()
	SIZE = 500, 200
	screencolor = (0, 0, 0)
	pygame.init()
	pygame.display.set_caption('output timeline')

	screen = pygame.display.set_mode(SIZE)
	screen.fill(screencolor)
	font = pygame.font.SysFont("monospace", 10, bold=False)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	for i in range(len(data)):
		if data[i][0]=="task1":
			color=(215, 0, 0)
		elif data[i][0]=="task2":
			color=(0, 240, 0)
		elif data[i][0]=="task3":
			color=(0, 0, 255)
		
		posX=2*data[i][1]
		posY=30
		width=2*data[i][2]-data[i][1]
		height=50
		#add text:
		label = font.render(str(data[i][1]), 0, color)
		screen.blit(label,(posX,83))
		pygame.draw.rect( screen, color,( posX, posY, width, height))
	#finashing drawing
	lbl= font.render(str(data[-1][2]), 0, (0,255,0))
	screen.blit(lbl,(2*data[-1][2],83))
	pygame.draw.rect( screen, (0,0,0),( 2*data[-1][2], 30, 170, 50)) 
	pygame.display.update()


