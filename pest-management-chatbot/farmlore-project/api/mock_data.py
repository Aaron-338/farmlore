"""Mock data for API endpoints when database is not available"""

# Mock pests data
PESTS_DATA = [
    {
        "Pest ID": "P001",
        "Local Name": "Rice Stem Borer",
        "Scientific Name": "Scirpophaga incertulas",
        "Host Crops": "Rice",
        "Symptoms (Early)": "Yellow leaves",
        "Symptoms (Advanced)": "Dead leaves",
        "Pest Type": "Insect"
    },
    {
        "Pest ID": "P002",
        "Local Name": "Corn Earworm",
        "Scientific Name": "Helicoverpa zea",
        "Host Crops": "Corn",
        "Symptoms (Early)": "Holes in leaves",
        "Symptoms (Advanced)": "Damaged ears",
        "Pest Type": "Insect"
    },
    {
        "Pest ID": "P003",
        "Local Name": "Tomato Hornworm",
        "Scientific Name": "Manduca quinquemaculata",
        "Host Crops": "Tomato",
        "Symptoms (Early)": "Defoliation",
        "Symptoms (Advanced)": "Severe defoliation",
        "Pest Type": "Insect"
    },
    {
        "Pest ID": "P004",
        "Local Name": "Cabbage Aphid",
        "Scientific Name": "Brevicoryne brassicae",
        "Host Crops": "Cabbage",
        "Symptoms (Early)": "Curled leaves",
        "Symptoms (Advanced)": "Stunted growth",
        "Pest Type": "Insect"
    },
    {
        "Pest ID": "P005",
        "Local Name": "Potato Blight",
        "Scientific Name": "Phytophthora infestans",
        "Host Crops": "Potato",
        "Symptoms (Early)": "Dark spots",
        "Symptoms (Advanced)": "Rotting tubers",
        "Pest Type": "Fungus"
    }
]

# Mock methods data
METHODS_DATA = [
    {
        "Method ID": "M001",
        "Method Name": "Organic Pesticide",
        "Target Pests (Pest ID)": "P001, P002",
        "Effectiveness": "High",
        "Method Type": "Chemical",
        "Description": "Natural pesticide made from neem oil"
    },
    {
        "Method ID": "M002",
        "Method Name": "Biological Control",
        "Target Pests (Pest ID)": "P003, P004",
        "Effectiveness": "Medium",
        "Method Type": "Biological",
        "Description": "Using natural predators to control pests"
    },
    {
        "Method ID": "M003",
        "Method Name": "Cultural Control",
        "Target Pests (Pest ID)": "P005",
        "Effectiveness": "Medium",
        "Method Type": "Cultural",
        "Description": "Crop rotation and sanitation practices"
    },
    {
        "Method ID": "M004",
        "Method Name": "Mechanical Control",
        "Target Pests (Pest ID)": "P001, P003",
        "Effectiveness": "Low",
        "Method Type": "Mechanical",
        "Description": "Handpicking pests or using traps"
    },
    {
        "Method ID": "M005",
        "Method Name": "Resistant Varieties",
        "Target Pests (Pest ID)": "P002, P005",
        "Effectiveness": "High",
        "Method Type": "Genetic",
        "Description": "Using pest-resistant crop varieties"
    }
]

# Mock soil data
SOIL_DATA = [
    {
        "Treatment Name": "Compost Application",
        "Soil Type": "Clay",
        "Target Crop": "Rice",
        "Materials": "Compost, organic matter",
        "Application Method": "Mix into soil before planting",
        "Description": "Improves soil structure and adds nutrients"
    },
    {
        "Treatment Name": "Green Manure",
        "Soil Type": "Sandy",
        "Target Crop": "Corn",
        "Materials": "Cover crops",
        "Application Method": "Grow cover crops and till into soil",
        "Description": "Adds organic matter and improves soil fertility"
    },
    {
        "Treatment Name": "Mulching",
        "Soil Type": "Loam",
        "Target Crop": "Tomato",
        "Materials": "Straw, leaves, grass clippings",
        "Application Method": "Apply around plants",
        "Description": "Conserves moisture and suppresses weeds"
    },
    {
        "Treatment Name": "Crop Rotation",
        "Soil Type": "All",
        "Target Crop": "All",
        "Materials": "Different crop families",
        "Application Method": "Rotate crops each season",
        "Description": "Prevents pest buildup and balances nutrients"
    },
    {
        "Treatment Name": "Vermicompost",
        "Soil Type": "All",
        "Target Crop": "Vegetables",
        "Materials": "Worm castings",
        "Application Method": "Mix into soil or use as top dressing",
        "Description": "Rich in nutrients and beneficial microorganisms"
    }
]

def filter_pests(query):
    """Filter pests by query"""
    if not query:
        return PESTS_DATA
    
    query = query.lower()
    return [
        pest for pest in PESTS_DATA if
        query in pest["Local Name"].lower() or
        query in pest["Scientific Name"].lower() or
        query in pest["Host Crops"].lower() or
        query in pest["Symptoms (Early)"].lower() or
        query in pest["Symptoms (Advanced)"].lower()
    ]

def filter_methods(pest_id):
    """Filter methods by pest ID"""
    if not pest_id:
        return METHODS_DATA
    
    return [
        method for method in METHODS_DATA if
        pest_id in method["Target Pests (Pest ID)"]
    ]

def filter_soil(soil_type=None, crop=None):
    """Filter soil treatments by soil type and/or crop"""
    result = SOIL_DATA
    
    if soil_type:
        soil_type = soil_type.lower()
        result = [
            treatment for treatment in result if
            soil_type in treatment["Soil Type"].lower() or
            treatment["Soil Type"] == "All"
        ]
    
    if crop:
        crop = crop.lower()
        result = [
            treatment for treatment in result if
            crop in treatment["Target Crop"].lower() or
            treatment["Target Crop"] == "All"
        ]
    
    return result