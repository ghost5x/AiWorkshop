from db import get_conn
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

NEET_BIO = {
  "subject": "Biology",
  "sections": [
    {
      "section": "Unit 1: Diversity in Living World",
      "topics": [
        "What is living?; Biodiversity; Need for classification; Taxonomy & Systematics; Concept of species and taxonomical hierarchy; Binomial nomenclature",
        "Five kingdom classification; salient features and classification of Monera; Protista and Fungi into major groups; Lichens; Viruses and Viroids",
        "Salient features and classification of plants into major groups - Algae, Bryophytes, Pteridophytes, Gymnosperms (three to five salient and distinguishing features and at least two examples of each category)",
        "Salient features and classification of animals - nonchordate up to phyla level and chordate up to classes level (three to five salient features and at least two examples)"
      ]
    },
    {
      "section": "Unit 2: Structural Organisation in Animals and Plants",
      "topics": [
        "Morphology and modifications; Tissues; Anatomy and functions of different parts of flowering plants: Root, stem, leaf, inflorescence - cymose and recemose, flower, fruit and seed; Family (malvaceae, Cruciferae, leguminoceae, compositae, graminae)",
        "Animal tissues; Morphology, anatomy and functions of different systems (digestive, circulatory, respiratory, nervous and reproductive) of an insect (Frog)"
      ]
    },
    {
      "section": "Unit 3: Cell Structure and Function",
      "topics": [
        "Cell theory and cell as the basic unit of life; Structure of prokaryotic and eukaryotic cell; Plant cell and animal cell; Cell envelope, cell membrane, cell wall",
        "Cell organelles - structure and function; Endomembrane system - endoplasmic reticulum, Golgi bodies, lysosomes, vacuoles; mitochondria, ribosomes, plastids, micro bodies; Cytoskeleton, cilia, flagella, centrioles; Nucleus - nuclear membrane, chromatin, nucleolus",
        "Chemical constituents of living cells: Biomolecules - structure and function of proteins, carbohydrates, lipids, nucleic acids; Enzymes - types, properties, enzyme action, classification and nomenclature",
        "Cell division: Cell cycle, mitosis, meiosis and their significance"
      ]
    },
    {
      "section": "Unit 4: Plant Physiology",
      "topics": [
        "Photosynthesis: Autotrophic nutrition; Site of photosynthesis; pigments involved; Photochemical and biosynthetic phases; Cyclic and non-cyclic photophosphorylation; Chemiosmotic hypothesis; Photorespiration C3 and C4 pathways; Factors affecting photosynthesis",
        "Respiration: Exchange of gases; Cellular respiration - glycolysis, fermentation (anaerobic), TCA cycle and electron transport system (aerobic); Energy relations; Amphibolic pathways; Respiratory quotient",
        "Plant growth and development: Seed germination; Phases of plant growth and growth rate; Conditions of growth; Differentiation, dedifferentiation and redifferentiation; Growth regulators - auxin, gibberellin, cytokinin, ethylene, ABA"
      ]
    },
    {
      "section": "Unit 5: Human Physiology",
      "topics": [
        "Breathing and Respiration: Respiratory organs in animals; Respiratory system in humans; Mechanism of breathing and its regulation; Exchange and transport of gases; Disorders - Asthma, Emphysema, Occupational respiratory disorders",
        "Body fluids and circulation: Composition of blood, blood groups, coagulation; Composition of lymph; Human circulatory system; Cardiac cycle, cardiac output, ECG, Double circulation; Disorders - Hypertension, Coronary artery disease, Angina pectoris, Heart failure",
        "Excretory products and their elimination: Modes of excretion; Human excretory system; Urine formation, Osmoregulation; Regulation of kidney function - Renin-angiotensin, ADH; Disorders - Uraemia, Renal failure, Renal calculi, Nephritis; Dialysis and artificial kidney",
        "Locomotion and Movement: Types of movement; Skeletal muscle and muscle contraction; Skeletal system and its functions; Joints; Disorders - Myasthenia gravis, Tetany, Muscular dystrophy, Arthritis, Osteoporosis, Gout",
        "Neural control and coordination: Neuron and nerves; Central, peripheral and visceral nervous system; Generation and conduction of nerve impulse",
        "Chemical coordination and regulation: Endocrine glands and hormones; Human endocrine system - Hypothalamus, Pituitary, Pineal, Thyroid, Parathyroid, Adrenal, Pancreas, Gonads; Mechanism of hormone action; Disorders - Dwarfism, Acromegaly, Cretinism, goiter, diabetes, Addison's disease"
      ]
    },
    {
      "section": "Unit 6: Reproduction",
      "topics": [
        "Sexual reproduction in flowering plants: Flower structure; Development of male and female gametophytes; Pollination - types, agencies and examples; Outbreeding devices; Pollen-Pistil interaction; Double fertilization; Post fertilization events; Special modes - apomixis, parthenocarpy, polyembryony",
        "Human Reproduction: Male and female reproductive systems; Microscopic anatomy of testis and ovary; Gametogenesis - spermatogenesis and oogenesis; Menstrual cycle; Fertilisation, embryo development upto blastocyst formation, implantation; Pregnancy and placenta formation; Parturition; Lactation",
        "Reproductive health: Prevention of STDs; Birth control - Need and Methods, Contraception and MTP; Amniocentesis; Infertility and assisted reproductive technologies - IVF, ZIFT, GIFT"
      ]
    },
    {
      "section": "Unit 7: Genetics and Evolution",
      "topics": [
        "Heredity and variation: Mendelian Inheritance; Deviations from Mendelism - Incomplete dominance, Co-dominance, Multiple alleles; Pleiotropy; Polygenic inheritance; Chromosome theory; Sex determination; Linkage and crossing over; Sex linked inheritance - Haemophilia, Colour blindness; Mendelian disorders - Thalassemia; Chromosomal disorders - Down's syndrome, Turner's and Klinefelter's syndromes",
        "Molecular basis of Inheritance: DNA as genetic material; Structure of DNA and RNA; DNA packaging; DNA replication; Central dogma; Transcription, genetic code, translation; Gene expression and regulation - Lac Operon; Human genome project; DNA fingerprinting; Protein biosynthesis",
        "Evolution: Origin of life; Biological evolution and evidences from Paleontology, comparative anatomy, embryology and molecular evidence; Darwin's contribution; Modern Synthetic theory; Mechanism of evolution - Variation, Natural Selection; Gene flow and genetic drift; Hardy-Weinberg's principle; Adaptive Radiation; Human evolution"
      ]
    },
    {
      "section": "Unit 8: Biology and Human Welfare",
      "topics": [
        "Health and Disease; Pathogens; parasites causing human diseases - Malaria, Filariasis, Ascariasis, Typhoid, Pneumonia, common cold, amoebiasis, ring worm, dengue, chikungunya; Basic concepts of immunology; Cancer, HIV and AIDS; Adolescence, drug and alcohol abuse; Tobacco abuse",
        "Microbes in human welfare: household food processing, industrial production, sewage treatment, energy generation, biocontrol agents and biofertilizers"
      ]
    },
    {
      "section": "Unit 9: Biotechnology and Its Applications",
      "topics": [
        "Principles and process of Biotechnology: Genetic engineering (Recombinant DNA technology)",
        "Application of Biotechnology in health and agriculture: Human insulin and vaccine production; Gene therapy; Genetically modified organisms - Bt crops; Transgenic Animals; Biosafety issues - Biopiracy and patents"
      ]
    },
    {
      "section": "Unit 10: Ecology and Environment",
      "topics": [
        "Organisms and environment: Population interactions - mutualism, competition, predation, parasitism; Population attributes - growth, birth rate, death rate, age distribution",
        "Ecosystem: Patterns, components; Productivity and decomposition; Energy flow; Pyramids of number, biomass, energy",
        "Biodiversity and its conservation: Concept, Patterns, Importance and Loss of Biodiversity; Biodiversity conservation; Hotspots, endangered organisms, extinction, Red Data Book, biosphere reserves, National parks and sanctuaries, Sacred Groves"
      ]
    }
  ]
}

# Map level + subject to the correct data dict
SUBJECT_DATA_MAP = {
    ("NEET", "Biology"): NEET_BIO,
    # ("NEET", "Physics"): NEET_PHY,   # add when ready
    # ("NEET", "Chemistry"): NEET_CHE,
    # ("JEE",  "Physics"): JEE_PHY,
}

@app.route("/insert", methods=["POST"])
def insertData():
    conn   = get_conn()
    cursor = conn.cursor()
    data    = request.get_json()
    org_id  = data.get("org_id")
    level   = data.get("level")
    subject = data.get("subject")
    created_by = data.get("created_by", "SYSTEM")

    # Validate input
    if not org_id or not level or not subject:
        return jsonify({"status": "error", "message": "org_id, level and subject are required"}), 400

    # Pick the right data dict
    subject_data = SUBJECT_DATA_MAP.get((level, subject))
    if not subject_data:
        return jsonify({"status": "error", "message": f"No data found for {level} - {subject}"}), 404

    try:
        # Step 1: Get or insert Level
        cursor.execute(
            "SELECT id FROM aca_levels WHERE org_id = %s AND level = %s",
            (org_id, level)
        )
        row = cursor.fetchone()
        if row:
            level_id = row[0]
        else:
            cursor.execute(
                "INSERT INTO aca_levels (org_id, level, created_by) VALUES (%s, %s, %s)",
                (org_id, level, created_by)
            )
            level_id = cursor.lastrowid

        # Step 2: Insert Subject
        cursor.execute(
            "INSERT INTO aca_subjects (org_id, level_id, subject, created_by) VALUES (%s, %s, %s, %s)",
            (org_id, level_id, subject_data["subject"], created_by)
        )
        subject_id = cursor.lastrowid

        # Step 3: Loop sections
        for section_obj in subject_data["sections"]:
            cursor.execute(
                "INSERT INTO aca_sections (subject_id, section, created_by) VALUES (%s, %s, %s)",
                (subject_id, section_obj["section"], created_by)
            )
            section_id = cursor.lastrowid

            # Step 4: Batch insert topics
            topic_rows = [
                (section_id, topic, created_by)
                for topic in section_obj["topics"]
            ]
            cursor.executemany(
                "INSERT INTO aca_topics (section_id, topic, created_by) VALUES (%s, %s, %s)",
                topic_rows
            )

        conn.commit()
        return jsonify({
            "status": "success",
            "message": f"{level} - {subject} inserted successfully for org {org_id}"
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)