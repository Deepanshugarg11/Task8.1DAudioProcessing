import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Setup GPIO for the LED
GPIO.setmode(GPIO.BCM)
LED_PIN = 17  # Replace with your GPIO pin number
GPIO.setup(LED_PIN, GPIO.OUT)

def led_on():
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED ON")
    time.sleep(0.5)  # Debounce time

def led_off():
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED OFF")
    time.sleep(0.5)  # Debounce time

def listen_for_command():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Adjusting for background noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command...")
            audio = recognizer.listen(source)

            # Recognize speech using Google Speech Recognition
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from the speech recognition service.")
    
    return ""

def process_command(command):
    print(f"Processing command: {command}")
    if "led on" in command:
        print("Recognized command: LED ON")
        led_on()
    elif "led off" in command:
        print("Recognized command: LED OFF")
        led_off()
    else:
        print("Command not recognized. Please say 'led on' or 'led off'.")

if __name__ == "__main__":
    try:
        while True:
            command = listen_for_command()
            if command:
                process_command(command)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        GPIO.cleanup()
