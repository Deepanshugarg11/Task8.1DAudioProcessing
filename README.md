import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
light_pin = 18  # Use any available GPIO pin
GPIO.setup(light_pin, GPIO.OUT)

# Function to turn light ON or OFF
def control_light(command):
    if 'turn on' in command:
        GPIO.output(light_pin, GPIO.HIGH)
        print("Light is turned ON.")
    elif 'turn off' in command:
        GPIO.output(light_pin, GPIO.LOW)
        print("Light is turned OFF.")
    else:
        print("Command not recognized.")

# Function to recognize voice commands
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    

    with mic as source:
    
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said: " + command)
        return command.lower()  # Convert command to lowercase
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print("Request error from Google Speech Recognition service; {0}".format(e))

    return None

# Main loop
try:
    while True:
        command = recognize_speech()
        if command:
            control_light(command)
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated.")
finally:
    GPIO.cleanup()  # Cleanup GPIO on exit
