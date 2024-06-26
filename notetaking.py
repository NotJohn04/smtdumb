import speech_recognition as sr
import keyboard
import time

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Adjusting for ambient noise. Please wait.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)
    print("Ready to record. Start speaking...")

    final_transcript = []

    def callback(recognizer, audio):
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            final_transcript.append(text)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    stop_listening = recognizer.listen_in_background(microphone, callback)

    try:
        while True:
            if keyboard.is_pressed('esc'):
                print("Stopping...")
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_listening(wait_for_stop=False)
        with open("notes.txt", "w") as file:
            file.write("\n".join(final_transcript))
        print("Text saved to notes.txt")

if __name__ == "__main__":
    main()
