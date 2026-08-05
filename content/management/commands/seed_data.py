import random

from django.core.management.base import BaseCommand

from content.models import Answer, Category, Language, Lesson, LessonExample, Question, Quiz, Vocabulary
from learning.models import Badge


CATEGORIES = [
    ("greetings", "Salutations", "👋"),
    ("family", "Famille", "👪"),
    ("food", "Nourriture", "🍎"),
    ("colors", "Couleurs", "🎨"),
    ("animals", "Animaux", "🐾"),
    ("school", "École", "🏫"),
    ("work", "Travail", "💼"),
    ("travel", "Voyage", "✈️"),
    ("health", "Santé", "🩺"),
    ("hobbies", "Loisirs", "🎮"),
    ("sports", "Sports", "⚽"),
    ("house", "Maison", "🏠"),
]

LANGUAGES = [
    ("en", "Anglais", "🇬🇧"),
    ("es", "Espagnol", "🇪🇸"),
    ("fr", "Français", "🇫🇷"),
]

VOCAB_EN = [
    ("greetings", "Hello", "Bonjour", "heh-LOH", "Hello, how are you?"),
    ("greetings", "Goodbye", "Au revoir", "good-BYE", "Goodbye, see you tomorrow!"),
    ("greetings", "Thank you", "Merci", "THANK-you", "Thank you for your help."),
    ("greetings", "Please", "S'il vous plaît", "pleez", "Please, sit down."),
    ("greetings", "Sorry", "Pardon", "SOR-ree", "Sorry, I'm late."),
    ("greetings", "Yes", "Oui", "yes", "Yes, I agree."),
    ("greetings", "No", "Non", "noh", "No, thank you."),
    ("greetings", "Welcome", "Bienvenue", "WEL-kum", "Welcome to our home."),
    ("family", "Mother", "Mère", "MUH-ther", "My mother is a teacher."),
    ("family", "Father", "Père", "FAH-ther", "My father works in Cotonou."),
    ("family", "Sister", "Sœur", "SIS-ter", "I have one sister."),
    ("family", "Brother", "Frère", "BRUH-ther", "My brother lives in Paris."),
    ("family", "Grandmother", "Grand-mère", "GRAND-muh-ther", "My grandmother tells great stories."),
    ("family", "Grandfather", "Grand-père", "GRAND-fah-ther", "My grandfather is retired."),
    ("family", "Son", "Fils", "sun", "Their son is five years old."),
    ("family", "Daughter", "Fille", "DAW-ter", "Her daughter goes to university."),
    ("food", "Rice", "Riz", "rice", "I eat rice every day."),
    ("food", "Water", "Eau", "WAW-ter", "Can I have some water?"),
    ("food", "Fish", "Poisson", "fish", "We had grilled fish for dinner."),
    ("food", "Bread", "Pain", "bred", "She bought fresh bread."),
    ("food", "Meat", "Viande", "meet", "He doesn't eat meat."),
    ("food", "Egg", "Œuf", "eg", "I'll have two eggs, please."),
    ("food", "Milk", "Lait", "milk", "The children drink milk every morning."),
    ("food", "Fruit", "Fruit", "froot", "Fresh fruit is good for your health."),
    ("colors", "Red", "Rouge", "red", "The car is red."),
    ("colors", "Blue", "Bleu", "bloo", "The sky is blue."),
    ("colors", "Green", "Vert", "green", "The grass is green."),
    ("colors", "Yellow", "Jaune", "YEL-oh", "The sun looks yellow."),
    ("colors", "Black", "Noir", "blak", "She wore a black dress."),
    ("colors", "White", "Blanc", "wyte", "The walls are white."),
    ("colors", "Orange", "Orange", "OR-anj", "I like the orange sunset."),
    ("colors", "Purple", "Violet", "PUR-pul", "Purple is her favorite color."),
    ("animals", "Dog", "Chien", "dawg", "The dog is barking."),
    ("animals", "Cat", "Chat", "kat", "The cat is sleeping."),
    ("animals", "Bird", "Oiseau", "burd", "A bird is singing outside."),
    ("animals", "Horse", "Cheval", "hors", "The horse is running fast."),
    ("animals", "Cow", "Vache", "kow", "The cow gives milk."),
    ("animals", "Goat", "Chèvre", "goht", "The goat is eating grass."),
    ("animals", "Chicken", "Poule", "CHIK-en", "The chicken laid an egg."),
    ("animals", "Sheep", "Mouton", "sheep", "The sheep are in the field."),
    ("school", "Teacher", "Enseignant", "TEE-cher", "The teacher explains the lesson."),
    ("school", "Book", "Livre", "book", "I am reading a book."),
    ("school", "Pen", "Stylo", "pen", "Can I borrow your pen?"),
    ("school", "Pencil", "Crayon", "PEN-sul", "She writes with a pencil."),
    ("school", "Classroom", "Salle de classe", "KLASS-room", "The classroom is very quiet."),
    ("school", "Student", "Élève", "STOO-dent", "The student asked a question."),
    ("school", "Exam", "Examen", "ig-ZAM", "The exam is next week."),
    ("school", "Notebook", "Cahier", "NOHT-book", "Write it down in your notebook."),
    ("work", "Job", "Emploi", "job", "She found a new job."),
    ("work", "Office", "Bureau", "OF-iss", "He works at the office."),
    ("work", "Colleague", "Collègue", "KOL-eeg", "My colleague helped me finish the report."),
    ("work", "Salary", "Salaire", "SAL-uh-ree", "The salary is paid monthly."),
    ("work", "Meeting", "Réunion", "MEE-ting", "We have a meeting at 10 a.m."),
    ("work", "Manager", "Directeur", "MAN-uh-jer", "The manager approved the project."),
    ("work", "Computer", "Ordinateur", "kom-PYOO-ter", "My computer is very fast."),
    ("work", "Contract", "Contrat", "KON-trakt", "Please sign the contract."),
    ("travel", "Airport", "Aéroport", "AIR-port", "The airport is far from here."),
    ("travel", "Ticket", "Billet", "TIK-et", "I bought a plane ticket."),
    ("travel", "Passport", "Passeport", "PASS-port", "Don't forget your passport."),
    ("travel", "Hotel", "Hôtel", "hoh-TEL", "We stayed at a nice hotel."),
    ("travel", "Suitcase", "Valise", "SOOT-kayss", "My suitcase is too heavy."),
    ("travel", "Train", "Train", "trayn", "The train leaves at noon."),
    ("travel", "Flight", "Vol", "flyte", "Our flight was delayed."),
    ("travel", "Map", "Carte", "map", "Use the map to find your way."),
    ("health", "Doctor", "Médecin", "DOK-ter", "I need to see a doctor."),
    ("health", "Hospital", "Hôpital", "HOSS-pih-tul", "She works at the hospital."),
    ("health", "Medicine", "Médicament", "MED-ih-sin", "Take this medicine twice a day."),
    ("health", "Nurse", "Infirmière", "nurs", "The nurse checked his temperature."),
    ("health", "Pain", "Douleur", "payn", "I have a pain in my back."),
    ("health", "Pharmacy", "Pharmacie", "FAR-muh-see", "The pharmacy is open until 8 p.m."),
    ("health", "Fever", "Fièvre", "FEE-ver", "The child has a fever."),
    ("health", "Injury", "Blessure", "IN-juh-ree", "He recovered quickly from his injury."),
    ("hobbies", "Reading", "Lecture", "REE-ding", "Reading is my favorite hobby."),
    ("hobbies", "Music", "Musique", "MYOO-zik", "She listens to music every evening."),
    ("hobbies", "Dancing", "Danse", "DAN-sing", "They enjoy dancing on weekends."),
    ("hobbies", "Painting", "Peinture", "PAYN-ting", "Painting helps him relax."),
    ("hobbies", "Photography", "Photographie", "fuh-TOG-ruh-fee", "Photography is a creative hobby."),
    ("hobbies", "Cooking", "Cuisine", "KOOK-ing", "Cooking together is fun."),
    ("hobbies", "Gardening", "Jardinage", "GAR-den-ing", "Gardening keeps her busy on Sundays."),
    ("hobbies", "Gaming", "Jeux vidéo", "GAY-ming", "He spends hours gaming."),
    ("sports", "Football", "Football", "FOOT-bawl", "We play football every weekend."),
    ("sports", "Basketball", "Basketball", "BAS-ket-bawl", "She plays basketball on Fridays."),
    ("sports", "Swimming", "Natation", "SWIM-ing", "Swimming is great exercise."),
    ("sports", "Running", "Course à pied", "RUN-ing", "Running every morning keeps him fit."),
    ("sports", "Tennis", "Tennis", "TEN-iss", "They watched a tennis match."),
    ("sports", "Cycling", "Cyclisme", "SY-kling", "Cycling is popular in the city."),
    ("sports", "Boxing", "Boxe", "BOK-sing", "Boxing requires discipline."),
    ("sports", "Volleyball", "Volleyball", "VOL-ee-bawl", "We played volleyball on the beach."),
    ("house", "Kitchen", "Cuisine", "KIH-chen", "The kitchen is very clean."),
    ("house", "Bedroom", "Chambre", "BED-room", "My bedroom is upstairs."),
    ("house", "Bathroom", "Salle de bain", "BATH-room", "The bathroom needs cleaning."),
    ("house", "Garden", "Jardin", "GAR-den", "We grow vegetables in the garden."),
    ("house", "Roof", "Toit", "roof", "The roof was damaged by the storm."),
    ("house", "Door", "Porte", "dor", "Please close the door."),
    ("house", "Window", "Fenêtre", "WIN-doh", "Open the window, it's hot."),
    ("house", "Living room", "Salon", "LIV-ing room", "We watch TV in the living room."),
]

VOCAB_ES = [
    ("greetings", "Hola", "Bonjour", "OH-la", "¡Hola! ¿Cómo estás?"),
    ("greetings", "Gracias", "Merci", "GRA-see-as", "Gracias por tu ayuda."),
    ("greetings", "Adiós", "Au revoir", "ah-dee-OSS", "Adiós, hasta mañana."),
    ("greetings", "Por favor", "S'il vous plaît", "por fa-VOR", "Ayúdame, por favor."),
    ("greetings", "Buenos días", "Bonjour (le matin)", "BWAY-nos DEE-as", "Buenos días, ¿qué tal?"),
    ("family", "Madre", "Mère", "MA-dreh", "Mi madre es profesora."),
    ("family", "Padre", "Père", "PA-dreh", "Mi padre trabaja mucho."),
    ("family", "Hermana", "Sœur", "er-MA-na", "Tengo una hermana."),
    ("family", "Hermano", "Frère", "er-MA-no", "Mi hermano vive en Madrid."),
    ("family", "Abuela", "Grand-mère", "ah-BWAY-la", "Mi abuela cocina muy bien."),
    ("food", "Agua", "Eau", "AH-gwa", "Quiero un vaso de agua."),
    ("food", "Arroz", "Riz", "ar-ROSS", "Como arroz todos los días."),
    ("food", "Pan", "Pain", "pan", "Compré pan fresco."),
    ("food", "Carne", "Viande", "KAR-neh", "No como carne."),
    ("food", "Leche", "Lait", "LEH-cheh", "Los niños beben leche."),
    ("colors", "Rojo", "Rouge", "RO-kho", "El coche es rojo."),
    ("colors", "Azul", "Bleu", "ah-SOOL", "El cielo es azul."),
    ("colors", "Verde", "Vert", "VER-deh", "La hierba es verde."),
    ("colors", "Amarillo", "Jaune", "ah-ma-REE-yo", "El sol parece amarillo."),
    ("colors", "Negro", "Noir", "NEH-gro", "Ella llevaba un vestido negro."),
    ("animals", "Perro", "Chien", "PEH-rro", "El perro está ladrando."),
    ("animals", "Gato", "Chat", "GA-to", "El gato está durmiendo."),
    ("animals", "Caballo", "Cheval", "ka-BA-yo", "El caballo corre rápido."),
    ("animals", "Pájaro", "Oiseau", "PA-kha-ro", "Un pájaro canta afuera."),
    ("animals", "Vaca", "Vache", "VA-ka", "La vaca da leche."),
    ("school", "Profesor", "Enseignant", "pro-feh-SOR", "El profesor explica la lección."),
    ("school", "Libro", "Livre", "LEE-bro", "Estoy leyendo un libro."),
    ("school", "Lápiz", "Crayon", "LA-pees", "Escribe con un lápiz."),
    ("school", "Escuela", "École", "es-KWEH-la", "La escuela está cerca de casa."),
    ("school", "Estudiante", "Élève", "es-too-DYAN-teh", "El estudiante hizo una pregunta."),
    ("work", "Trabajo", "Emploi", "tra-BA-kho", "Ella encontró un nuevo trabajo."),
    ("work", "Oficina", "Bureau", "oh-fee-SEE-na", "Él trabaja en la oficina."),
    ("work", "Reunión", "Réunion", "reh-oo-NYON", "Tenemos una reunión a las diez."),
    ("work", "Salario", "Salaire", "sa-LA-ryo", "El salario se paga cada mes."),
    ("work", "Compañero", "Collègue", "kom-pa-NYEH-ro", "Mi compañero me ayudó mucho."),
    ("travel", "Aeropuerto", "Aéroport", "ah-eh-ro-PWER-to", "El aeropuerto está lejos de aquí."),
    ("travel", "Billete", "Billet", "bee-YEH-teh", "Compré un billete de avión."),
    ("travel", "Hotel", "Hôtel", "oh-TEL", "Nos quedamos en un buen hotel."),
    ("travel", "Maleta", "Valise", "ma-LEH-ta", "Mi maleta pesa mucho."),
    ("travel", "Pasaporte", "Passeport", "pa-sa-POR-teh", "No olvides tu pasaporte."),
    ("health", "Médico", "Médecin", "MEH-dee-ko", "Necesito ver a un médico."),
    ("health", "Hospital", "Hôpital", "os-pee-TAL", "Ella trabaja en el hospital."),
    ("health", "Medicina", "Médicament", "meh-dee-SEE-na", "Toma esta medicina dos veces al día."),
    ("health", "Enfermera", "Infirmière", "en-fer-MEH-ra", "La enfermera revisó su temperatura."),
    ("health", "Farmacia", "Pharmacie", "far-MA-sya", "La farmacia está abierta hasta las ocho."),
    ("hobbies", "Lectura", "Lecture", "lek-TOO-ra", "La lectura es mi afición favorita."),
    ("hobbies", "Música", "Musique", "MOO-see-ka", "Ella escucha música todas las noches."),
    ("hobbies", "Baile", "Danse", "BAI-leh", "Les encanta el baile los fines de semana."),
    ("hobbies", "Cocina", "Cuisine", "ko-SEE-na", "Cocinar juntos es divertido."),
    ("hobbies", "Pintura", "Peinture", "peen-TOO-ra", "La pintura le ayuda a relajarse."),
    ("sports", "Fútbol", "Football", "FOOT-bol", "Jugamos al fútbol cada fin de semana."),
    ("sports", "Natación", "Natation", "na-ta-SYON", "La natación es un buen ejercicio."),
    ("sports", "Baloncesto", "Basketball", "ba-lon-SES-to", "Ella juega baloncesto los viernes."),
    ("sports", "Tenis", "Tennis", "TEH-nees", "Vieron un partido de tenis."),
    ("sports", "Ciclismo", "Cyclisme", "see-KLEES-mo", "El ciclismo es popular en la ciudad."),
    ("house", "Cocina", "Cuisine", "ko-SEE-na", "La cocina está muy limpia."),
    ("house", "Dormitorio", "Chambre", "dor-mee-TOR-yo", "Mi dormitorio está arriba."),
    ("house", "Jardín", "Jardin", "khar-DEEN", "Cultivamos verduras en el jardín."),
    ("house", "Puerta", "Porte", "PWER-ta", "Cierra la puerta, por favor."),
    ("house", "Ventana", "Fenêtre", "ben-TA-na", "Abre la ventana, hace calor."),
]

VOCAB_FR = [
    ("greetings", "Bonjour", "Hello", "bɔ̃.ʒuʁ", "Bonjour, comment ça va ?"),
    ("greetings", "Merci", "Thank you", "mɛʁ.si", "Merci beaucoup !"),
    ("greetings", "Au revoir", "Goodbye", "o.ʁə.vwaʁ", "Au revoir, à demain !"),
    ("family", "Mère", "Mother", "mɛʁ", "Ma mère est enseignante."),
    ("family", "Père", "Father", "pɛʁ", "Mon père travaille beaucoup."),
    ("family", "Frère", "Brother", "fʁɛʁ", "Mon frère habite à Paris."),
    ("food", "Eau", "Water", "o", "Je voudrais de l'eau, s'il vous plaît."),
    ("food", "Pain", "Bread", "pɛ̃", "Elle a acheté du pain frais."),
    ("food", "Riz", "Rice", "ʁi", "Je mange du riz tous les jours."),
    ("colors", "Rouge", "Red", "ʁuʒ", "La voiture est rouge."),
    ("colors", "Bleu", "Blue", "blø", "Le ciel est bleu."),
    ("colors", "Vert", "Green", "vɛʁ", "L'herbe est verte."),
    ("animals", "Chien", "Dog", "ʃjɛ̃", "Le chien aboie."),
    ("animals", "Chat", "Cat", "ʃa", "Le chat dort."),
    ("animals", "Cheval", "Horse", "ʃə.val", "Le cheval court vite."),
    ("school", "Livre", "Book", "livʁ", "Je lis un livre."),
    ("school", "École", "School", "e.kɔl", "L'école est proche de la maison."),
    ("school", "Élève", "Student", "e.lɛv", "L'élève a posé une question."),
    ("work", "Emploi", "Job", "ɑ̃.plwa", "Elle a trouvé un nouvel emploi."),
    ("work", "Bureau", "Office", "by.ʁo", "Il travaille au bureau."),
    ("work", "Réunion", "Meeting", "ʁe.y.njɔ̃", "Nous avons une réunion à dix heures."),
    ("travel", "Aéroport", "Airport", "a.e.ʁɔ.pɔʁ", "L'aéroport est loin d'ici."),
    ("travel", "Hôtel", "Hotel", "o.tɛl", "Nous avons logé dans un bel hôtel."),
    ("travel", "Valise", "Suitcase", "va.liz", "Ma valise est trop lourde."),
    ("health", "Médecin", "Doctor", "med.sɛ̃", "Je dois voir un médecin."),
    ("health", "Hôpital", "Hospital", "ɔ.pi.tal", "Elle travaille à l'hôpital."),
    ("health", "Pharmacie", "Pharmacy", "faʁ.ma.si", "La pharmacie est ouverte jusqu'à 20h."),
    ("hobbies", "Lecture", "Reading", "lɛk.tyʁ", "La lecture est mon passe-temps préféré."),
    ("hobbies", "Musique", "Music", "my.zik", "Elle écoute de la musique tous les soirs."),
    ("hobbies", "Cuisine", "Cooking", "kɥi.zin", "Cuisiner ensemble, c'est amusant."),
    ("sports", "Football", "Football", "fut.bol", "Nous jouons au football chaque week-end."),
    ("sports", "Natation", "Swimming", "na.ta.sjɔ̃", "La natation est un bon exercice."),
    ("sports", "Tennis", "Tennis", "te.nis", "Ils ont regardé un match de tennis."),
    ("house", "Cuisine", "Kitchen", "kɥi.zin", "La cuisine est très propre."),
    ("house", "Jardin", "Garden", "ʒaʁ.dɛ̃", "Nous cultivons des légumes dans le jardin."),
    ("house", "Porte", "Door", "pɔʁt", "Ferme la porte, s'il te plaît."),
]

LESSONS = [
    ("en", "Le présent simple", "debutant", 1,
     "Le présent simple sert à exprimer une habitude, une vérité générale ou un fait régulier. "
     "On ajoute un « s » à la troisième personne du singulier.",
     ["I play football.", "She plays football.", "They play football."]),
    ("en", "Les articles A / AN / THE", "debutant", 2,
     "« A » et « AN » sont des articles indéfinis (un/une), « AN » s'utilise devant un son voyelle. "
     "« THE » est l'article défini (le/la/les).",
     ["A book", "An apple", "The teacher"]),
    ("en", "Le prétérit (passé simple)", "intermediaire", 3,
     "Le prétérit exprime une action terminée dans le passé. La plupart des verbes réguliers prennent « -ed ».",
     ["I played football yesterday.", "She visited Paris last year."]),
    ("en", "Le pluriel des noms", "debutant", 4,
     "La plupart des noms prennent un « s » au pluriel. Certains noms ont un pluriel irrégulier "
     "(child → children, man → men, foot → feet).",
     ["One book, two books.", "One child, two children."]),
    ("en", "Les verbes modaux CAN / MUST", "intermediaire", 5,
     "« CAN » exprime une capacité ou une permission. « MUST » exprime une obligation forte. "
     "Ils sont suivis d'un verbe à l'infinitif sans « to ».",
     ["I can swim.", "You must finish your homework."]),
    ("en", "Le futur avec WILL", "intermediaire", 6,
     "« WILL » sert à exprimer une décision spontanée, une prédiction ou une promesse pour le futur.",
     ["I will call you tomorrow.", "It will rain tonight."]),
    ("en", "Les comparatifs et superlatifs", "avance", 7,
     "Pour comparer, on ajoute « -er » (ou « more » pour les mots longs). Pour le superlatif, "
     "on utilise « the -est » (ou « the most »).",
     ["She is taller than me.", "This is the most beautiful city."]),
    ("es", "Le verbe SER et ESTAR", "debutant", 1,
     "« Ser » exprime une caractéristique permanente, « Estar » exprime un état temporaire ou une localisation.",
     ["Yo soy estudiante.", "Estoy en casa."]),
    ("es", "Les articles définis et indéfinis", "debutant", 2,
     "El/la (le/la) sont des articles définis, un/una (un/une) sont des articles indéfinis, accordés en genre.",
     ["El libro", "Una casa"]),
    ("es", "Le futur proche (IR A + infinitif)", "intermediaire", 3,
     "Pour exprimer une action proche dans le futur, on utilise le verbe « ir » conjugué + « a » + l'infinitif.",
     ["Voy a estudiar.", "Vamos a viajar mañana."]),
    ("es", "Les verbes réfléchis", "intermediaire", 4,
     "Les verbes réfléchis (comme levantarse, lavarse) s'utilisent avec un pronom réfléchi "
     "(me, te, se, nos, os, se).",
     ["Me levanto a las siete.", "Ella se lava las manos."]),
    ("es", "Le pluriel des noms", "debutant", 5,
     "On ajoute « -s » si le mot se termine par une voyelle, « -es » s'il se termine par une consonne.",
     ["Un libro, dos libros.", "Una ciudad, dos ciudades."]),
    ("es", "Les comparatifs", "avance", 6,
     "« Más... que » exprime la supériorité, « menos... que » l'infériorité, « tan... como » l'égalité.",
     ["Ella es más alta que yo.", "Es tan importante como el trabajo."]),
    ("fr", "Le présent de l'indicatif (1er groupe)", "debutant", 1,
     "Les verbes du premier groupe se terminent en « -er » à l'infinitif. Au présent, on retire « -er » "
     "et on ajoute les terminaisons : -e, -es, -e, -ons, -ez, -ent.",
     ["Je parle.", "Nous parlons.", "Ils parlent."]),
    ("fr", "Les articles définis et indéfinis", "debutant", 2,
     "Les articles définis (le, la, les) désignent quelque chose de précis. Les articles indéfinis "
     "(un, une, des) désignent quelque chose de non précis.",
     ["Le chat", "Une maison", "Des livres"]),
    ("fr", "Les adjectifs possessifs", "debutant", 3,
     "Les adjectifs possessifs (mon, ma, mes, ton, ta, tes...) s'accordent en genre et en nombre "
     "avec le nom qu'ils accompagnent.",
     ["Mon frère", "Ma sœur", "Mes parents"]),
    ("fr", "Le passé composé", "intermediaire", 4,
     "Le passé composé se forme avec l'auxiliaire « avoir » ou « être » au présent, suivi du participe passé.",
     ["J'ai mangé.", "Elle est partie."]),
    ("en", "Le present perfect", "intermediaire", 8,
     "Le present perfect (HAVE/HAS + participe passé) relie une action passée à une conséquence présente. "
     "On l'utilise souvent avec « just », « already », « never », « ever ».",
     ["I have finished my homework.", "She has never been to Spain."]),
    ("en", "Le conditionnel avec WOULD", "avance", 9,
     "« WOULD » exprime une action hypothétique, une demande polie, ou la conséquence d'une condition "
     "irréelle (structure « If + prétérit, would + base verbale »).",
     ["If I had time, I would travel more.", "Would you like some tea?"]),
    ("es", "El pretérito indefinido", "intermediaire", 7,
     "Le passé simple espagnol (pretérito indefinido) exprime une action terminée et ponctuelle "
     "dans le passé, contrairement à l'imparfait qui décrit un état.",
     ["Ayer comí pizza.", "Ella viajó a México el año pasado."]),
    ("es", "El subjuntivo (introducción)", "avance", 8,
     "Le subjonctif exprime le doute, le souhait ou l'émotion. Il se forme différemment de l'indicatif "
     "et s'utilise souvent après « que ».",
     ["Espero que tengas un buen día.", "Quiero que vengas conmigo."]),
    ("fr", "Le futur simple", "intermediaire", 5,
     "Le futur simple exprime une action à venir. Pour les verbes réguliers, on ajoute les terminaisons "
     "-ai, -as, -a, -ons, -ez, -ont à l'infinitif.",
     ["Je parlerai demain.", "Nous finirons bientôt."]),
    ("fr", "Le subjonctif présent (introduction)", "avance", 6,
     "Le subjonctif s'utilise après certaines expressions de sentiment, de doute ou de volonté "
     "(« il faut que », « je veux que », « bien que »...).",
     ["Il faut que tu partes.", "Je veux qu'elle vienne."]),
]

BADGES = [
    ("first_lesson", "Premier pas", "Terminer sa première leçon", "🥇", "lessons", 1),
    ("lessons_5", "Assidu", "Terminer 5 leçons", "📖", "lessons", 5),
    ("lessons_10", "Expert en herbe", "Terminer 10 leçons", "🎓", "lessons", 10),
    ("streak_3", "Bon départ", "3 jours de suite", "⭐", "streak", 3),
    ("streak_7", "Régularité", "7 jours de suite", "🔥", "streak", 7),
    ("streak_30", "Un mois complet", "30 jours de suite", "💎", "streak", 30),
    ("words_10", "Premiers mots", "10 mots appris", "🌱", "words", 10),
    ("words_25", "Curieux", "25 mots appris", "🔎", "words", 25),
    ("words_50", "Polyglotte en herbe", "50 mots appris", "🌍", "words", 50),
    ("words_100", "Maître du vocabulaire", "100 mots appris", "🏆", "words", 100),
    ("words_200", "Légende linguistique", "200 mots appris", "👑", "words", 200),
]

QUESTIONS_PER_QUIZ = 5
DISTRACTORS_PER_QUESTION = 3


class Command(BaseCommand):
    help = (
        "Peuple la base de données avec un large jeu de vocabulaire, des leçons de grammaire, "
        "des quiz (générés automatiquement à partir du vocabulaire) et des badges de démonstration."
    )

    def handle(self, *args, **options):
        languages = self._seed_languages()
        categories = self._seed_categories()
        self._seed_vocabulary(languages, categories)
        self._seed_lessons(languages)
        self._seed_quizzes(languages, categories)
        self._seed_badges()
        self.stdout.write(self.style.SUCCESS("Données de démonstration prêtes ! 🎉"))

    def _seed_languages(self):
        languages = {}
        for code, name, flag in LANGUAGES:
            lang, _ = Language.objects.get_or_create(code=code, defaults={"name": name, "flag_emoji": flag})
            languages[code] = lang
        self.stdout.write(self.style.SUCCESS(f"{len(languages)} langues prêtes."))
        return languages

    def _seed_categories(self):
        categories = {}
        for slug, name, icon in CATEGORIES:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "icon": icon})
            categories[slug] = cat
        self.stdout.write(self.style.SUCCESS(f"{len(categories)} catégories prêtes."))
        return categories

    def _seed_vocabulary(self, languages, categories):
        count = 0
        for lang_code, entries in (("en", VOCAB_EN), ("es", VOCAB_ES), ("fr", VOCAB_FR)):
            for cat_slug, word, translation, pron, example in entries:
                _, created = Vocabulary.objects.get_or_create(
                    language=languages[lang_code],
                    category=categories[cat_slug],
                    word=word,
                    defaults={"translation": translation, "pronunciation": pron, "example": example},
                )
                if created:
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"{count} mots de vocabulaire ajoutés."))

    def _seed_lessons(self, languages):
        lesson_count = 0
        for lang_code, title, level, order, explanation, examples in LESSONS:
            lesson, created = Lesson.objects.get_or_create(
                language=languages[lang_code],
                title=title,
                defaults={"level": level, "order": order, "explanation": explanation},
            )
            if created:
                lesson_count += 1
                for ex in examples:
                    LessonExample.objects.create(lesson=lesson, text=ex)
        self.stdout.write(self.style.SUCCESS(f"{lesson_count} leçons de grammaire ajoutées."))

    def _seed_quizzes(self, languages, categories):
        """Génère automatiquement, pour chaque catégorie et chaque langue, un ou
        plusieurs quiz classés par niveau :
        - Débutant (dès 3 mots) : reconnaître la traduction d'un mot.
        - Intermédiaire (dès 5 mots) : retrouver le mot à partir de sa traduction
          (sens de production, plus difficile).
        - Avancé (dès 7 mots) : questions mélangées avec des distracteurs plus
          proches (même catégorie), pour plus de discrimination.
        """
        quiz_count = 0
        question_count = 0

        for lang_code, language in languages.items():
            all_words_this_lang = list(Vocabulary.objects.filter(language=language))
            all_translations = [w.translation for w in all_words_this_lang]

            for cat_slug, category in categories.items():
                words = [w for w in all_words_this_lang if w.category_id == category.id]
                cat_translations = [w.translation for w in words]

                tiers = []
                if len(words) >= 3:
                    tiers.append(("debutant", "Découverte", "word_to_translation", all_translations))
                if len(words) >= 5:
                    tiers.append(("intermediaire", "Entraînement", "translation_to_word", [w.word for w in words]))
                if len(words) >= 7:
                    tiers.append(("avance", "Défi", "mixed", cat_translations))

                for level, tier_label, mode, distractor_source in tiers:
                    title = f"{category.name} — {tier_label} ({language.name})"
                    quiz, created = Quiz.objects.get_or_create(
                        language=language,
                        title=title,
                        defaults={"category": category, "level": level},
                    )
                    if not created:
                        continue
                    quiz_count += 1

                    sample_size = min(QUESTIONS_PER_QUIZ, len(words))
                    quiz_words = random.sample(words, sample_size)

                    for i, word in enumerate(quiz_words):
                        word_mode = mode
                        if mode == "mixed":
                            word_mode = "word_to_translation" if i % 2 == 0 else "translation_to_word"

                        if word_mode == "translation_to_word":
                            question_text = f"Comment dit-on « {word.translation} » ?"
                            correct_answer = word.word
                            pool = [w.word for w in words if w.word != word.word] or [
                                w.word for w in all_words_this_lang if w.word != word.word
                            ]
                        else:
                            question_text = f"Que signifie « {word.word} » ?"
                            correct_answer = word.translation
                            pool = (
                                [t for t in cat_translations if t != word.translation]
                                if level == "avance"
                                else [t for t in all_translations if t != word.translation]
                            )
                            if len(pool) < DISTRACTORS_PER_QUESTION:
                                pool = [t for t in all_translations if t != word.translation]

                        question = Question.objects.create(quiz=quiz, text=question_text)
                        question_count += 1

                        pool = list(dict.fromkeys(pool))
                        random.shuffle(pool)
                        distractors = pool[:DISTRACTORS_PER_QUESTION]

                        Answer.objects.create(question=question, text=correct_answer, is_correct=True)
                        for distractor in distractors:
                            Answer.objects.create(question=question, text=distractor, is_correct=False)

        self.stdout.write(
            self.style.SUCCESS(f"{quiz_count} quiz générés automatiquement ({question_count} questions).")
        )

    def _seed_badges(self):
        badge_count = 0
        for slug, title, description, icon, metric, required in BADGES:
            _, created = Badge.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": description,
                    "icon": icon,
                    "metric": metric,
                    "required_value": required,
                },
            )
            if created:
                badge_count += 1
        self.stdout.write(self.style.SUCCESS(f"{badge_count} badges ajoutés."))
