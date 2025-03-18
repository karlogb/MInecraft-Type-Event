import time, os, keyboard, random, winsound, datetime, re, win32gui, win32con, itertools, webbrowser
from pynput.mouse import Button, Controller
from ctypes import *

def follow(thefile):

	opakuj = True
	hlasuj = False

	thefile.seek(0,2)

	while True:

		if keyboard.is_pressed('F7'):

			if opakuj:
				print("STATUS: OFF")
				winsound.Beep(500, 200)
				opakuj = False
			else:
				print("STATUS: ON")
				thefile.seek(0,2)
				winsound.Beep(1000, 200)
				opakuj = True

			time.sleep(0.5)

		if opakuj:
			line = thefile.readline()
			if not line:
				time.sleep(0.1)
				continue
			yield line

def napisSlovo(odpoved, anagram):

	#delay necessary for execution around 0.55 (minimum)
	#reaction time 0.25s
	#75 wpm = 0.8s per word typing time
	#1.6s initial delay
	#additionalDelay = based on word length

	global AFK
	global BACKGROUND_MODE

	if AFK:
		print("Si AFK, neodpovedám!")
		return

	reakcnaDoba = random.uniform(0.2, 0.25)
	napisanieSlova = random.uniform(0.8, 0.9)
	dodatocneOneskorenie = 0

	if anagram:
		if len(odpoved) == 10:
			dodatocneOneskorenie += random.uniform(0.5, 1)
		elif len(odpoved) > 8:
			dodatocneOneskorenie += random.uniform(0.75, 1)
		elif len(odpoved) > 6:
			dodatocneOneskorenie += random.uniform(0.5, 0.75)
		else:
			dodatocneOneskorenie += random.uniform(0, 0.5)
	else:
		dodatocneOneskorenie = random.uniform((len(odpoved) / 2) / 15, (len(odpoved) / 2 + 1) / 15)

	prev = datetime.datetime.now()

	blokujVstup = windll.user32.BlockInput(True) #enable block

	keyboard.release('w')
	keyboard.release('s')
	keyboard.release('a')
	keyboard.release('d')
	keyboard.release('shift')
	keyboard.release('space')
	keyboard.release('ctrl')
	keyboard.release('esc')
	keyboard.release('tab')

	mouse.release(Button.left)
	mouse.release(Button.right)

	currentOknoID = win32gui.GetForegroundWindow()
	currentOkno = win32gui.GetWindowText(currentOknoID)

	if currentOkno == "Minecraft 1.12.2":
		BACKGROUND_MODE = False
	else:
		BACKGROUND_MODE = True

	if BACKGROUND_MODE:
		minecraftOkno = win32gui.FindWindow(0, "Minecraft 1.12.2")
		win32gui.SetForegroundWindow(minecraftOkno)
		keyboard.press_and_release('F11')

		time.sleep(0.25)

		hwnd = win32gui.GetForegroundWindow()
		win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
	else:
		time.sleep(0.25)

	time.sleep(0.1)
	keyboard.press_and_release('esc')

	if BACKGROUND_MODE:
		time.sleep(0.1)
		mouse.position = (960, 320)
	
	if not BACKGROUND_MODE:
		time.sleep(0.1)
		mouse.position = (960, 340)

	time.sleep(0.05)
	mouse.press(Button.left)
	time.sleep(0.05)
	mouse.release(Button.left)

	time.sleep(reakcnaDoba)
	keyboard.press_and_release('enter')
	time.sleep(napisanieSlova)
	keyboard.write(odpoved)
	time.sleep(dodatocneOneskorenie)
	keyboard.press_and_release('enter')

	if BACKGROUND_MODE:
		keyboard.press_and_release('F11')

	blokujVstup = windll.user32.BlockInput(False) #disable block 

	cas = (datetime.datetime.now() - prev).total_seconds()

	if(anagram):
		print("Rozlúštené: " + odpoved + " za %.2f sekund" % round(cas, 2))
	else:
		print("Napísané: " + odpoved + " za %.2f sekund" % round(cas, 2))

	print("Reakčná doba: %.2f sekund" % round(reakcnaDoba, 2))
	print("Napísanie slova: %.2f sekund" % round(napisanieSlova, 2))
	print("Dodatočné oneskorenie: %.2f sekund" % round(dodatocneOneskorenie, 2))

clear = lambda: os.system('cls')
mouse = Controller()

BACKGROUND_MODE = False
AFK = False

DATABAZA_ANAGRAMOV = {}

suborAnagramov = open("", "r")

for anagramText in suborAnagramov:
	if anagramText != "":
		data = anagramText.split(';')
		DATABAZA_ANAGRAMOV[data[0]] = data[1].rstrip()

suborAnagramov.close()

clear()

print("F7: ON/OFF")
print("")

winsound.Beep(2500, 200)

logfile = open("", "r")
loglines = follow(logfile)

for line in loglines:

	if "" in line:
		AFK = True

	if "" in line:
		AFK = False

	if " [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] " in line:
		templine = line
		chat = templine.split(' [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] ')
		print(chat[0] + " " + chat[1][:-1])

	if "[CHAT] Event >> Napis jako prvni do chatu slovo" in line:

		data = line.split()
		odpoved = data[len(data) - 3]

		if(len(odpoved)) > 16:
			print("Slovo je príliš dlhé, preskakujem")
			continue

		napisSlovo(odpoved, 0)

	if "[CHAT] Event >> Rozlusti slovo" in line:

		data = line.split()
		odpoved = data[len(data) - 5]

		if len(odpoved) > 10:
			print("Aangram je príliš dlhý, preskakujem")
			continue

		vsetkyAnagramy = ["".join(perm) for perm in itertools.permutations(odpoved)]
		odpovedAnagram = ""

		for anagram in vsetkyAnagramy:
			if anagram in DATABAZA_ANAGRAMOV:
				odpovedAnagram = DATABAZA_ANAGRAMOV[anagram]

		if odpovedAnagram == "":
			print("Anagramv databázy nenájdený.")
		else:
			napisSlovo(odpovedAnagram, 1)