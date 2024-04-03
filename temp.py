from deepface import DeepFace
import os

cwd = os.getcwd()
print(DeepFace.analyze(cwd+"Yatharth.jpg"))

print("Current Working Directory:", cwd)


