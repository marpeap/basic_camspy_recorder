import cv2
import time
import os
from datetime import datetime
import threading
import tkinter as tk

# Fonction pour générer le chemin du répertoire en fonction de la date actuelle
def generate_directory_path():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m_%B")
    day = now.strftime("%d_%A")
    directory_path = os.path.join(year, month, day)
    return directory_path

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# Classe pour gérer l'enregistrement vidéo avec l'interface Tkinter
class VideoRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Enregistreur Vidéo")
        
        # Boutons de contrôle
        self.start_button = tk.Button(root, text="Démarrer Enregistrement", command=self.start_recording)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Arrêter Enregistrement", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.is_recording = False
        self.recording_thread = None

        # Initialisation de la caméra
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erreur : Impossible d'ouvrir la caméra.")
            exit()
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.fps = 20
        self.record_time = 10 * 60  # 10 minutes

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.recording_thread = threading.Thread(target=self.record_video)
            self.recording_thread.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            if self.recording_thread is not None:
                self.recording_thread.join()

    def record_video(self):
        while self.is_recording:
            start_time = time.time()
            directory_path = generate_directory_path()
            create_directory(directory_path)
            
            timestamp = datetime.now().strftime("%Hh%M_%S")
            filename = os.path.join(directory_path, f"{timestamp}.avi")
            
            # Créer l'objet VideoWriter pour un nouveau fichier vidéo
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filename, fourcc, self.fps, (self.frame_width, self.frame_height))
            
            print(f"Enregistrement démarré : {filename}. Appuyez sur 'Arrêter Enregistrement' pour terminer.")
            
            while self.is_recording and (time.time() - start_time) <= self.record_time:
                ret, frame = self.cap.read()
                if ret:
                    out.write(frame)
                else:
                    print("Erreur : Impossible de lire l'image.")
                    break
            
            out.release()

        print("Enregistrement arrêté.")

    def on_closing(self):
        self.stop_recording()
        self.cap.release()
        self.root.destroy()

# Création de l'interface Tkinter
root = tk.Tk()
video_recorder = VideoRecorder(root)
root.protocol("WM_DELETE_WINDOW", video_recorder.on_closing)
root.mainloop()

