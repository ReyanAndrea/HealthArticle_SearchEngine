"""
Sample corpus data untuk testing
Dalam implementasi nyata, data ini akan didapat dari web crawling
"""

SAMPLE_CORPUS = [
    {
        "id": 1,
        "title": "Cara Mencegah Diabetes Mellitus",
        "content": "Diabetes mellitus adalah penyakit kronis yang ditandai dengan kadar gula darah tinggi. Pencegahan diabetes dapat dilakukan dengan menjaga pola makan sehat, olahraga teratur minimal 30 menit sehari, dan menghindari stres. Konsumsi makanan tinggi serat seperti sayuran hijau, buah-buahan, dan biji-bijian sangat dianjurkan. Hindari makanan tinggi gula dan karbohidrat sederhana. Pemeriksaan gula darah rutin juga penting untuk deteksi dini.",
        "url": "https://health.example.com/diabetes-prevention",
        "date": "2024-10-15"
    },
    {
        "id": 2,
        "title": "Gejala dan Pengobatan Hipertensi",
        "content": "Hipertensi atau tekanan darah tinggi merupakan kondisi medis serius yang dapat menyebabkan komplikasi jantung dan stroke. Gejala hipertensi meliputi sakit kepala, pusing, sesak napas, dan penglihatan kabur. Pengobatan melibatkan perubahan gaya hidup seperti mengurangi konsumsi garam, olahraga teratur, dan obat-obatan antihipertensi. Pemantauan tekanan darah secara rutin sangat penting.",
        "url": "https://health.example.com/hypertension",
        "date": "2024-11-01"
    },
    {
        "id": 3,
        "title": "Manfaat Olahraga untuk Kesehatan Jantung",
        "content": "Olahraga teratur sangat penting untuk kesehatan jantung dan pembuluh darah. Aktivitas fisik membantu menurunkan tekanan darah, meningkatkan sirkulasi darah, dan mengurangi risiko penyakit jantung koroner. Jenis olahraga yang direkomendasikan termasuk jalan cepat, jogging, berenang, dan bersepeda. Lakukan olahraga minimal 150 menit per minggu dengan intensitas sedang.",
        "url": "https://health.example.com/exercise-heart",
        "date": "2024-10-20"
    },
    {
        "id": 4,
        "title": "Pola Makan Sehat untuk Penderita Diabetes",
        "content": "Penderita diabetes perlu mengatur pola makan dengan ketat untuk mengontrol kadar gula darah. Makanan yang direkomendasikan meliputi sayuran non-starch, protein tanpa lemak, lemak sehat, dan karbohidrat kompleks dalam porsi terbatas. Hindari makanan tinggi gula, karbohidrat olahan, dan lemak jenuh. Makan dengan porsi kecil tapi sering dapat membantu menstabilkan gula darah. Konsultasi dengan ahli gizi sangat dianjurkan.",
        "url": "https://health.example.com/diabetes-diet",
        "date": "2024-11-05"
    },
    {
        "id": 5,
        "title": "Mengenal Gejala Stroke dan Pertolongan Pertama",
        "content": "Stroke adalah kondisi darurat medis yang terjadi ketika aliran darah ke otak terganggu. Gejala stroke dapat dikenali dengan metode FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency. Gejala lain termasuk mati rasa mendadak, kebingungan, kesulitan melihat, dan sakit kepala hebat. Penanganan cepat dalam golden period 3-4.5 jam sangat krusial untuk mencegah kerusakan otak permanen.",
        "url": "https://health.example.com/stroke-symptoms",
        "date": "2024-10-28"
    },
    {
        "id": 6,
        "title": "Kolesterol Tinggi: Penyebab dan Cara Menurunkan",
        "content": "Kolesterol tinggi meningkatkan risiko penyakit jantung dan stroke. Kolesterol LDL yang tinggi dapat menyebabkan penumpukan plak di pembuluh darah. Cara menurunkan kolesterol termasuk mengonsumsi makanan tinggi serat, mengurangi lemak jenuh, olahraga teratur, dan menjaga berat badan ideal. Makanan seperti oatmeal, kacang-kacangan, ikan berlemak, dan minyak zaitun dapat membantu menurunkan kolesterol.",
        "url": "https://health.example.com/cholesterol",
        "date": "2024-11-10"
    },
    {
        "id": 7,
        "title": "Pentingnya Pemeriksaan Kesehatan Rutin",
        "content": "Pemeriksaan kesehatan rutin atau medical check-up penting untuk deteksi dini penyakit. Pemeriksaan dasar meliputi tekanan darah, gula darah, kolesterol, fungsi hati dan ginjal. Untuk usia di atas 40 tahun, disarankan melakukan pemeriksaan jantung seperti EKG dan treadmill test. Pemeriksaan kanker seperti mammografi dan kolonoskopi juga penting sesuai usia dan faktor risiko. Deteksi dini meningkatkan kesempatan pengobatan berhasil.",
        "url": "https://health.example.com/health-checkup",
        "date": "2024-10-25"
    },
    {
        "id": 8,
        "title": "Mengatasi Insomnia dan Gangguan Tidur",
        "content": "Insomnia atau kesulitan tidur dapat mempengaruhi kesehatan fisik dan mental. Penyebab insomnia termasuk stres, kebiasaan tidur buruk, dan kondisi medis tertentu. Cara mengatasi insomnia meliputi menjaga jadwal tidur teratur, menghindari kafein dan gadget sebelum tidur, menciptakan lingkungan tidur nyaman, dan teknik relaksasi. Jika berlanjut, konsultasi dengan dokter diperlukan untuk penanganan lebih lanjut.",
        "url": "https://health.example.com/insomnia",
        "date": "2024-11-08"
    },
    {
        "id": 9,
        "title": "Vitamin dan Mineral Penting untuk Tubuh",
        "content": "Vitamin dan mineral merupakan mikronutrien penting untuk fungsi tubuh optimal. Vitamin A penting untuk penglihatan, vitamin C untuk sistem imun, vitamin D untuk tulang, dan vitamin E sebagai antioksidan. Mineral seperti kalsium, zat besi, zinc, dan magnesium juga esensial. Kebutuhan mikronutrien dapat dipenuhi melalui pola makan seimbang dengan beragam sayuran, buah, protein, dan biji-bijian. Suplemen mungkin diperlukan untuk kondisi tertentu.",
        "url": "https://health.example.com/vitamins-minerals",
        "date": "2024-10-18"
    },
    {
        "id": 10,
        "title": "Cara Meningkatkan Sistem Imun Tubuh",
        "content": "Sistem imun yang kuat penting untuk melawan infeksi dan penyakit. Cara meningkatkan imun termasuk konsumsi makanan bergizi tinggi antioksidan, tidur cukup 7-8 jam, olahraga teratur, kelola stres, dan menjaga kebersihan. Makanan yang baik untuk imun termasuk jeruk, brokoli, bayam, yogurt, kacang almond, dan jahe. Hindari rokok dan alkohol berlebihan. Vaksinasi juga penting untuk perlindungan terhadap penyakit tertentu.",
        "url": "https://health.example.com/immune-system",
        "date": "2024-11-12"
    }
]

# Test queries dengan ground truth untuk evaluasi
TEST_QUERIES = [
    {
        "id": "q1",
        "query": "cara mencegah diabetes",
        "relevant_docs": [1, 4]
    },
    {
        "id": "q2",
        "query": "gejala dan pengobatan hipertensi tekanan darah tinggi",
        "relevant_docs": [2]
    },
    {
        "id": "q3",
        "query": "olahraga untuk kesehatan jantung",
        "relevant_docs": [3, 6]
    },
    {
        "id": "q4",
        "query": "makanan untuk penderita diabetes",
        "relevant_docs": [1, 4]
    },
    {
        "id": "q5",
        "query": "gejala stroke pertolongan pertama",
        "relevant_docs": [5]
    },
    {
        "id": "q6",
        "query": "menurunkan kolesterol",
        "relevant_docs": [6]
    },
    {
        "id": "q7",
        "query": "pemeriksaan kesehatan rutin",
        "relevant_docs": [7]
    },
    {
        "id": "q8",
        "query": "mengatasi susah tidur insomnia",
        "relevant_docs": [8]
    },
    {
        "id": "q9",
        "query": "vitamin mineral penting",
        "relevant_docs": [9]
    },
    {
        "id": "q10",
        "query": "meningkatkan sistem imun tubuh",
        "relevant_docs": [10]
    }
]