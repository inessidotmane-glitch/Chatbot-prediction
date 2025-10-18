
from main import clean_text,pipe
import pandas as pd

demo = [
    "qu'elle est l'heure du cours d'info demain",
    "comment passer les ratrapages?",
    "les inscriptions pour l'année prochaine ont elle debutée",
    "quelles documents a fournir pour l'inscription"
]
def clean_batch(texts): 
    return [clean_text(t) for t in texts]

demo_pred = pipe.predict(clean_batch(demo))
df = pd.DataFrame({"question_en": demo, "predicted_category": demo_pred})
